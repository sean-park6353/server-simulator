from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


from .models import Scenario, ScenarioStep
from simulator.models import Sim
from .serializers import ScenarioSerializer, ScenarioStepSerializer
from common.mixins import AutoUserAssignmentMixin

import random

class ScenarioView(generics.ListCreateAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Scenario.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        scenario_name = request.data.get('name')
        scenario_description = request.data.get('description')

        sims = Sim.objects.filter(user=request.user)
        if not sims.exists():
            return Response({"error": "해당 유저의 Sim이 없습니다."}, status=400)

        sim = random.choice(sims)

        scenario = Scenario.objects.create(
            name=scenario_name,
            description=scenario_description,
            user=request.user,
            sim=sim
        )

        step_name = request.data.get('stepname')
        method = request.data.get('method')
        endpoint = request.data.get('endpoint')
        step_description = request.data.get('stepdescription')

        ScenarioStep.objects.create(
            scenario=scenario,
            stepname=step_name,
            method=method,
            endpoint=endpoint,
            stepdescription=step_description,
            user=request.user
        )

        return Response(
            {"message": "시나리오가 생성되었습니다."},
            status=status.HTTP_201_CREATED
        )
class ScenarioDeleteView(APIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        try:
            scenario = Scenario.objects.get(pk=pk)
        except Scenario.DoesNotExist:
            return Response({"message": "시나리오가 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        ScenarioStep.objects.filter(scenario=scenario).delete()
        scenario.delete()

        return Response({"message": "시나리오와 관련 스텝이 삭제되었습니다."}, status=status.HTTP_200_OK)

# class ScenarioStepUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
#     queryset = ScenarioStep.objects.all()
#     serializer_class = ScenarioStepSerializer
#     permission_classes = [IsAuthenticated]

# class ScenarioUpdateDestroyView(generics.UpdateAPIView, generics.DestroyAPIView):
#     queryset = Scenario.objects.all()
#     serializer_class = ScenarioSerializer
#     permission_classes = [IsAuthenticated]