from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Scenario, ScenarioStep
from .serializers import ScenarioSerializer, ScenarioStepSerializer
from common.mixins import AutoUserAssignmentMixin


class ScenarioCreateView(AutoUserAssignmentMixin, generics.CreateAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]


class ScenarioUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]


class ScenarioWithStepsCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        scenario_data = request.data.get('scenario')
        steps_data = request.data.get('steps', [])

        scenario_serializer = ScenarioSerializer(data=scenario_data)
        scenario_serializer.is_valid(raise_exception=True)
        scenario = scenario_serializer.save(user=request.user)

        for step in steps_data:
            ScenarioStep.objects.create(
                scenario=scenario,
                name=step['name'],
                method=step['method'],
                endpoint=step['endpoint'],
                headers=step.get('headers'),
                body=step.get('body'),
                user=request.user,
                description=step.get('description', '')
            )

        return Response({'scenario_id': scenario.id}, status=201)


class ScenarioStepCreateView(AutoUserAssignmentMixin, generics.CreateAPIView):
    queryset = ScenarioStep.objects.all()
    serializer_class = ScenarioStepSerializer
    permission_classes = [IsAuthenticated]


class ScenarioStepUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = ScenarioStep.objects.all()
    serializer_class = ScenarioStepSerializer
    permission_classes = [IsAuthenticated]
