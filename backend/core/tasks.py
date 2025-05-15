from celery import shared_task
from core import models


@shared_task
def hello_task(name):
    print(f'*** Hello, {name}! This task is running. ***')


@shared_task
def handle_ai_request(request_id):
    """
    Handle the AI request
    """
    request = models.AiRequest.objects.get(id=request_id)
    request.handle()
