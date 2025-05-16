import ast
import os

import google.generativeai as genai
from core.tasks import handle_ai_request
from django.db import models


class Recipe(models.Model):
    """
    Recipe model
    """
    name = models.CharField(max_length=255)
    steps = models.TextField()
    favorite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class AiChatSession(models.Model):
    """
    AI Chat Session model
    """
    # id added by default
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_last_request(self):
        """
        Get the last request
        """
        return self.requests.all().order_by('-created_at').first()  # using related_name

    def _create_message(self, message, role='user'):
        """
        Create a message
        """
        return {"role": role, "parts": [message]}

    def create_first_message(self, message):
        """
        Create the first message
        """
        return [self._create_message('You are snarky but helpful assistant', role='system'),
                self._create_message(message, role='user')]

    def messages(self):
        """
        Get all messages in the conversation
        """
        messages = []
        request = self.get_last_request()

        if request:
            messages.extend(ast.literal_eval(request.messages))
            try:
                messages.append(request.response['candidates'][0]['content'])
            except (KeyError, TypeError, IndexError):
                # response can take some time, so we skip cases, when response is not ready yet
                pass

        return messages

    def send(self, message):
        """
        Send a message
        """
        last_request = self.get_last_request()

        if not last_request:
            AiRequest.objects.create(session=self, messages=self.create_first_message(message))
        elif last_request.status in [AiRequest.COMPLETED, AiRequest.FAILED]:
            AiRequest.objects.create(session=self, messages=self.messages() + [self._create_message(message)])
        else:
            return


class AiRequest(models.Model):
    """
    AI Request model
    """
    PENDING = 'pending'
    RUNNING = 'running'
    COMPLETED = 'completed'
    FAILED = 'failed'
    STATUS_OPTIONS = (
        (PENDING, 'Pending'),
        (RUNNING, 'Running'),
        (COMPLETED, 'Completed'),
        (FAILED, 'Failed'),
    )

    status = models.CharField(choices=STATUS_OPTIONS, default=PENDING)
    session = models.ForeignKey(AiChatSession, on_delete=models.CASCADE,
                                null=True, blank=True, related_name='requests')
    messages = models.CharField()
    response = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def _queue_job(self):
        """
        Queue the job
        """
        handle_ai_request.delay(self.id)

    def handle(self):
        """
        Handle the request
        """
        self.status = self.RUNNING
        self.save()

        # call Google Gemini API client
        genai.configure(api_key=os.environ["GEMINI_API_KEY"])
        client = genai.GenerativeModel(model_name="models/gemini-2.0-flash")
        try:
            response = client.generate_content(self.messages)
            self.response = response.to_dict() # {"text": response.text}
            self.status = self.COMPLETED
        except Exception:
            self.status = self.FAILED

        self.save()

    def save(self, *args, **kwargs):
        """
        Save the request
        """
        is_new = self._state.adding
        super().save(*args, **kwargs)

        if is_new:
            self._queue_job()
