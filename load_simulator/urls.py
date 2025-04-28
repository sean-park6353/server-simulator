from django.urls import path
from . import views

urlpatterns = [
    # Sim CUD
    path('sims/', views.SimListCreateView.as_view(), name='sim_list_create'),
    path('sims/<int:pk>/', views.SimRetrieveUpdateDestroyView.as_view(), name='sim_detail'),

    # Scenario CUD
    path('scenarios/', views.ScenarioCreateView.as_view(), name='scenario_create'),
    path('scenarios/<int:pk>/', views.ScenarioUpdateDestroyView.as_view(), name='scenario_update_destroy'),

    # Scenario + StepOrder 복합 저장
    path('scenarios/with-steps/', views.ScenarioWithStepsCreateView.as_view(), name='scenario_with_steps_create'),

    # Scenario Execution
    path('scenarios/<int:scenario_id>/executions/', views.ScenarioExecutionView.as_view(), name='scenario_execution'),

    # ScenarioStep CUD
    path('scenario-steps/', views.ScenarioStepCreateView.as_view(), name='scenariostep_create'),
    path('scenario-steps/<int:pk>/', views.ScenarioStepUpdateDestroyView.as_view(), name='scenariostep_update_destroy'),

    # ScenarioStepOrder CUD
    path('scenario-step-orders/', views.ScenarioStepOrderCreateView.as_view(), name='scenariosteporder_create'),

    # LoadTest CUD
    path('load-tests/', views.LoadTestCreateView.as_view(), name='loadtest_create'),
    path('load-tests/<int:pk>/', views.LoadTestUpdateDestroyView.as_view(), name='loadtest_update_destroy'),

    # LoadTest Execution
    path('load-tests/<int:loadtest_id>/executions/', views.LoadTestExecutionView.as_view(), name='loadtest_execution'),

    # NotificationTemplate CUD
    path('notification-templates/', views.NotificationTemplateCreateView.as_view(), name='notificationtemplate_create'),
    path('notification-templates/<int:pk>/', views.NotificationTemplateUpdateDestroyView.as_view(), name='notificationtemplate_update_destroy'),

    # Notification Sending
    path('notifications/send/', views.NotificationSendView.as_view(), name='notification_send'),
]