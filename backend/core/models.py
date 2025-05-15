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
