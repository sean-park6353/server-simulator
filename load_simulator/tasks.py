# import time
# import requests
#
# from celery import shared_task
# from load_simulator.models import LoadTest
#
#
# @shared_task
# def run_load_test(load_test_id):
#     try:
#         load_test = LoadTest.objects.get(id=load_test_id)
#     except LoadTest.DoesNotExist:
#         return f"LoadTest with id {load_test_id} not found"
#
#     total_requests = load_test.rps * load_test.duration
#     delay = 1.0 / load_test.rps if load_test.rps else 0.1  # 요청 간 시간 간격
#
#     success = 0
#     failed = 0
#
#     for i in range(total_requests):
#         try:
#             if load_test.method == 'GET':
#                 response = requests.get(
#                     load_test.target_url,
#                     headers=load_test.headers or {}
#                 )
#             elif load_test.method == 'POST':
#                 response = requests.post(
#                     load_test.target_url,
#                     headers=load_test.headers or {},
#                     json=load_test.payload or {}
#                 )
#             else:
#                 failed += 1
#                 continue
#
#             if response.status_code >= 200 and response.status_code < 300:
#                 success += 1
#             else:
#                 failed += 1
#
#         except Exception as e:
#             failed += 1
#
#         time.sleep(delay)
#
#     return {
#         "total": total_requests,
#         "success": success,
#         "failed": failed,
#     }


from celery import shared_task

@shared_task
def test_queue_work(x, y):
    print("이게 다 뭐냐")
    return "🥕"


@shared_task
def test_queue_work2(x):
    print("이게 다 뭐냐2")
    return "🥕🥕fsdfsdf"