from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError


from .models import Sim, LoadTest
from .serializers import SimSerializer, LoadTestSerializer
from .services import execute_scenario_for_users, run_burst_load
from common.mixins import AutoUserAssignmentMixin


# -------- Sim (가상 유저) --------
class SimListCreateView(generics.ListCreateAPIView):
    queryset = Sim.objects.all()
    serializer_class = SimSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        try:
            count = int(request.data.get("count"))
            if count <= 0:
                raise ValueError
        except (TypeError, ValueError):
            raise ValidationError({"count": "1 이상의 숫자를 입력하세요."})

        created_sims = []
        for _ in range(count):
            sim = Sim.objects.create(user=request.user)
            created_sims.append(sim)

        serializer = self.get_serializer(created_sims, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class SimRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sim.objects.all()
    serializer_class = SimSerializer
    permission_classes = [IsAuthenticated]


class ScenarioExecutionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, scenario_id):
        try:                                                                                                
            user_count = int(request.data.get('user_count', 10))
        except (ValueError, TypeError):
            return Response({'error': 'Invalid user_count'}, status=status.HTTP_400_BAD_REQUEST)

        task_info = execute_scenario_for_users(scenario_id=scenario_id, user_count=user_count)
        return Response(task_info, status=status.HTTP_202_ACCEPTED)


class LoadTestCreateView(AutoUserAssignmentMixin, generics.CreateAPIView):
    queryset = LoadTest.objects.all()
    serializer_class = LoadTestSerializer
    permission_classes = [IsAuthenticated]


class LoadTestUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = LoadTest.objects.all()
    serializer_class = LoadTestSerializer
    permission_classes = [IsAuthenticated]


class LoadTestExecutionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loadtest_id):
        try:
            count = int(request.data.get('count', 50))
        except (ValueError, TypeError):
            return Response({'error': 'Invalid count'}, status=status.HTTP_400_BAD_REQUEST)

        task_info = run_burst_load(load_test_id=loadtest_id, created_by=request.user, count=count)
        return Response(task_info, status=status.HTTP_202_ACCEPTED)
