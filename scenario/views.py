from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError
from .serializers import ScenarioStepBulkSerializer


from .models import Scenario, ScenarioStep
from simulator.models import Sim
from .serializers import ScenarioSerializer
from common.mixins import AutoUserAssignmentMixin

import random

class ScenarioView(generics.ListCreateAPIView):
    queryset = Scenario.objects.all()
    serializer_class = ScenarioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Scenario.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        sims = Sim.objects.filter(user=self.request.user)
        if not sims.exists():
            raise ValidationError("해당 유저의 Sim이 없습니다.")

        sim = random.choice(sims)

        serializer.save(user=self.request.user, sim=sim)

    # def create(self, request, *args, **kwargs):
    #     scenario_name = request.data.get('name')
    #     scenario_description = request.data.get('description')

    #     sims = Sim.objects.filter(user=request.user)
    #     if not sims.exists():
    #         return Response({"error": "해당 유저의 Sim이 없습니다."}, status=400)

    #     sim = random.choice(sims)

    #     scenario = Scenario.objects.create(
    #         name=scenario_name,
    #         description=scenario_description,
    #         user=request.user,
    #         sim=sim
    #     )

    #     step_name = request.data.get('stepname')
    #     method = request.data.get('method')
    #     endpoint = request.data.get('endpoint')
    #     step_description = request.data.get('stepdescription')

    #     ScenarioStep.objects.create(
    #         scenario=scenario,
    #         stepname=step_name,
    #         method=method,
    #         endpoint=endpoint,
    #         stepdescription=step_description,
    #         user=request.user
    #     )

    #     return Response(
    #         {"message": "시나리오가 생성되었습니다."},
    #         status=status.HTTP_201_CREATED
    #     )
class ScenarioStepBulkCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        step_data_list = request.data

        if not isinstance(step_data_list, list):
            return Response({"error": "리스트 형태의 데이터가 필요합니다."}, status=400)

        # 각 항목에 user를 붙여서 일괄 생성
        for step in step_data_list:
            step["user"] = request.user.id

        serializer = ScenarioStepBulkSerializer(data=step_data_list, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "시나리오 스텝이 모두 저장되었습니다."}, status=201)
        return Response(serializer.errors, status=400)


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