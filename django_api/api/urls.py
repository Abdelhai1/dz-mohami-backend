from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview ,name='apiOverview' ),
    path('users-list/', views.showAllUsers ,name='users-list' ),
    path('user-details/<int:pk>/', views.showUser ,name='user-details' ),
    path('user-create/', views.createUser ,name='user-create' ),
    path('user-update/<int:pk>/', views.updateUser ,name='user-update' ),
    path('user-delete/<int:pk>/', views.deleteUser ,name='user-delete' ),
    
    
    #avocat
    path('lawyers-list/', views.showAllLawyers ,name='lawyers-list' ),
    path('lawyer-create/', views.createLawyer ,name='lawyer-create' ),
    path('lawyer-delete/<int:pk>/', views.deleteLawyer ,name='lawyer-delete' ),
    path('lawyer-update/<int:lawyer_id>/', views.updateLawyer ,name='lawyer-update' ),
    
    
    #appointment
    path('appointment-create/', views.createAppointment, name='appointment-create'),
    
    #get lawyer appointments
    path('get-lawyer-appointments/<int:lawyer_id>/', views.getLawyerAppointments, name='get-lawyer-appointments'),
    
    #reservation
    path('reservation-create/', views.createReservation, name='reservation-create'),
    path('reservation-accept/<int:reservation_id>/', views.acceptReservation, name='reservation-accept'),
    path('reservation-delete/<int:reservation_id>/', views.deleteReservation, name='reservation-delete'),
    
    #login
    path('login/', views.LoginView.as_view(), name='login'),
    
]