from django.urls import path
from scenario import views

urlpatterns = [
    path('scenarios/', views.ScenarioCreateView.as_view(), name='scenario_create'),
    path('scenarios/<int:pk>/', views.ScenarioUpdateDestroyView.as_view(), name='scenario_update_destroy'),
    path('scenarios/with-steps/', views.ScenarioWithStepsCreateView.as_view(), name='scenario_with_steps_create'),

    path('scenario-steps/', views.ScenarioStepCreateView.as_view(), name='scenariostep_create'),
    path('scenario-steps/<int:pk>/', views.ScenarioStepUpdateDestroyView.as_view(), name='scenariostep_update_destroy'),
]
