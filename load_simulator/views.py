from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Sim, Scenario, ScenarioStep, ScenarioStepOrder, LoadTest, NotificationTemplate
from .serializers import (
    SimSerializer,
    ScenarioSerializer,
    ScenarioStepSerializer,
    LoadTestSerializer,
    NotificationTemplateSerializer,
)
from .services import execute_scenario_for_users, run_burst_load

# -------- Sim --------
class SimListCreateView(generics.ListCreateAPIView):
    queryset = Sim.objects.all()
    serializer_class = SimSerializer
    permission_classes = [IsAuthenticated]

class SimRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Sim.objects.all()
    serializer_class = SimSerializer
    permission_classes = [IsAuthenticated]

# -------- Scenario --------
class ScenarioCreateView(generics.CreateAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ScenarioUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]

class ScenarioExecutionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, scenario_id):
        user_count = request.data.get('user_count', 10)
        task_info = execute_scenario_for_users(scenario_id=scenario_id, user_count=user_count)
        return Response(task_info, status=status.HTTP_202_ACCEPTED)

# -------- Scenario with Steps --------
class ScenarioWithStepsCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        scenario_data = request.data.get('scenario')
        steps_data = request.data.get('steps', [])

        scenario_serializer = ScenarioSerializer(data=scenario_data)
        scenario_serializer.is_valid(raise_exception=True)
        scenario = scenario_serializer.save(user=request.user)

        for step in steps_data:
            ScenarioStepOrder.objects.create(
                scenario=scenario,
                step_id=step['step_id'],
                order=step['order'],
                is_optional=step.get('is_optional', False),
                weight=step.get('weight', 1.0),
                group=step.get('group'),
                depends_on_id=step.get('depends_on')
            )

        return Response({'scenario_id': scenario.id}, status=status.HTTP_201_CREATED)

# -------- ScenarioStep --------
class ScenarioStepCreateView(generics.CreateAPIView):
    queryset = ScenarioStep.objects.all()
    serializer_class = ScenarioStepSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ScenarioStepUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = ScenarioStep.objects.all()
    serializer_class = ScenarioStepSerializer
    permission_classes = [IsAuthenticated]

# -------- ScenarioStepOrder --------
class ScenarioStepOrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        scenario_id = request.data.get('scenario_id')
        step_id = request.data.get('step_id')
        order = request.data.get('order')
        is_optional = request.data.get('is_optional', False)
        weight = request.data.get('weight', 1.0)
        group = request.data.get('group')
        depends_on = request.data.get('depends_on')

        step_order = ScenarioStepOrder.objects.create(
            scenario_id=scenario_id,
            step_id=step_id,
            order=order,
            is_optional=is_optional,
            weight=weight,
            group=group,
            depends_on_id=depends_on
        )

        return Response({'id': step_order.id}, status=status.HTTP_201_CREATED)

# -------- LoadTest --------
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

# -------- NotificationTemplate --------
class NotificationTemplateCreateView(generics.CreateAPIView):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]

class NotificationTemplateUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = NotificationTemplate.objects.all()
    serializer_class = NotificationTemplateSerializer
    permission_classes = [IsAuthenticated]

# -------- Notification Sending --------
class NotificationSendView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        template_id = request.data.get('template_id')
        receiver_ids = request.data.get('receiver_ids', [])
        # 실제 발송 로직 호출 예정
        return Response({'message': 'Notification sent', 'template_id': template_id}, status=status.HTTP_200_OK)