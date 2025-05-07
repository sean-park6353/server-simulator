from datetime import datetime
from .models import LoadTest, Sim
import uuid


def execute_scenario_for_users(scenario_id: int, user_count: int):
    """
    주어진 시나리오 ID를 user_count명의 가상 유저가 동시에 실행하도록 처리.
    현재는 더미 처리지만, 실제로는 celery나 async job으로 분산 처리되어야 함.
    """
    # 실제론 시나리오와 그 스텝을 불러와야 함
    task_id = str(uuid.uuid4())  # 실행 ID 생성

    # (예시) 결과 반환
    return {
        'status': 'started',
        'scenario_id': scenario_id,
        'user_count': user_count,
        'task_id': task_id,
        'started_at': datetime.utcnow().isoformat() + 'Z'
    }


def run_burst_load(load_test_id: int, created_by, count: int):
    """
    주어진 LoadTest ID를 기준으로 count만큼 가상 요청을 수행 (동시성 처리 가정)
    """
    try:
        load_test = LoadTest.objects.get(id=load_test_id)
    except LoadTest.DoesNotExist:
        return {'error': f'LoadTest {load_test_id} not found'}

    task_id = str(uuid.uuid4())

    # 실제로는 여기서 요청을 병렬로 실행하거나, celery에 task로 넘겨야 함
    # 예: send_request(load_test.endpoint, load_test.method, ...)

    return {
        'status': 'started',
        'load_test_id': load_test.id,
        'task_id': task_id,
        'request_count': count,
        'concurrent_users': load_test.concurrent_users,
        'started_at': datetime.utcnow().isoformat() + 'Z'
    }
