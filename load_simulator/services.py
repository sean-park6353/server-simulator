from .models import Scenario, ScenarioStepOrder, LoadTest
from .tasks import execute_scenario_task, run_load_test_task


def execute_scenario_for_users(scenario_id, user_count=10):
    # Celery task 호출
    task = execute_scenario_task.delay(scenario_id=scenario_id, user_count=user_count)
    return {'task_id': task.id}


def run_burst_load(step_order_id, created_by, count=50):
    # Celery task 호출
    task = run_load_test_task.delay(load_test_id=step_order_id, user_id=created_by.id, count=count)
    return {'task_id': task.id}