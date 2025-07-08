from django.urls import path
from scenario.views import ScenarioView, ScenarioDeleteView, ScenarioStepBulkCreateView
# ScenarioStepListCreateView


urlpatterns = [
    path('scenarios/', ScenarioView.as_view(), name='scenario-create'),
    path('scenario-steps/', ScenarioStepBulkCreateView.as_view(), name='scenario-step-create'),
    path('scenarios/<int:pk>/', ScenarioDeleteView.as_view(), name='scenario-delete'),



    # path('scenario-steps/', views.ScenarioStepCreateView.as_view(), name='scenariostep_create'),
    # path('scenario-steps/<int:pk>/', views.ScenarioStepUpdateDestroyView.as_view(), name='scenariostep_update_destroy'),
]
    # path('scenarios/with-steps/', views.ScenarioWithStepsCreateView.as_view(), name='scenario_with_steps_create'),
