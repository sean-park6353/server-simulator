from django.urls import path
from . import views

urlpatterns = [
    path('sims/', views.SimListCreateView.as_view(), name='sim_list_create'),
    path('sims/<int:pk>/', views.SimRetrieveUpdateDestroyView.as_view(), name='sim_detail'),

    path('load-tests/', views.LoadTestCreateView.as_view(), name='loadtest_create'),
    path('load-tests/<int:pk>/', views.LoadTestUpdateDestroyView.as_view(), name='loadtest_update_destroy'),
    path('load-tests/<int:loadtest_id>/executions/', views.LoadTestExecutionView.as_view(), name='loadtest_execution'),

    path('scenarios/<int:scenario_id>/executions/', views.ScenarioExecutionView.as_view(), name='scenario_execution'),
]
