from celery import shared_task

@shared_task
def test_queue_work(x, y):
    print(f"CELERY 실행: {x} + {y} = {x + y}")
    return x + y
