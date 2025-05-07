from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Sim, LoadTest
from .serializers import SimSerializer, LoadTestSerializer
from .services import execute_scenario_for_users, run_burst_load


class SimListCreateView(generics.ListCreateAPIView):
    queryset = Sim.objects.all()
    serializer_class = SimSerializer
    permission_classes = [IsAuthenticated]


class SimRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sim.objects.all()
    serializer_class = SimSerializer
    permission_classes = [IsAuthenticated]


class ScenarioExecutionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, scenario_id):
        user_count = request.data.get('user_count', 10)
        task_info = execute_scenario_for_users(scenario_id=scenario_id, user_count=user_count)
        return Response(task_info, status=status.HTTP_202_ACCEPTED)


class LoadTestCreateView(generics.CreateAPIView):
    queryset = LoadTest.objects.all()
    serializer_class = LoadTestSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class LoadTestUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = LoadTest.objects.all()
    serializer_class = LoadTestSerializer
    permission_classes = [IsAuthenticated]


class LoadTestExecutionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, loadtest_id):
        count = request.data.get('count', 50)
        task_info = run_burst_load(load_test_id=loadtest_id, created_by=request.user, count=count)
        return Response(task_info, status=status.HTTP_202_ACCEPTED)
