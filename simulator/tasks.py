from celery import shared_task
import random
import time
from .models import Scenario, LoadTest
from .models import NotificationHistory

@shared_task
def execute_scenario_task(scenario_id, user_count):
    scenario = Scenario.objects.get(id=scenario_id)
    step_orders = scenario.step_orders.select_related('step', 'depends_on')
    results = []
    for user_id in range(1, user_count + 1):
        executed = []
        executed_ids = set()
        for so in step_orders:
            if so.depends_on and so.depends_on.id not in executed_ids:
                continue
            if so.is_optional and random.random() > so.weight:
                continue
            executed.append(so.step.name)
            executed_ids.add(so.id)
        results.append({'user': user_id, 'actions': executed})
    return results

@shared_task
def run_load_test_task(load_test_id, user_id, count):
    load_test = LoadTest.objects.get(id=load_test_id)
    # 실제 요청 로직은 생략, 예시로 sleep
    data = []
    for i in range(count):
        start = time.time()
        # 여기에 requests 호출 etc.
        time.sleep(random.random() * 0.1)
        duration = time.time() - start
        data.append({'virtual_user': user_id, 'latency': duration * 1000})
    return data