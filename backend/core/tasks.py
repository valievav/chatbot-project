from celery import shared_task


@shared_task
def hello_task(name):
    print(f'*** Hello, {name}! This task is running. ***')
