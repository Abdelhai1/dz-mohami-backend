from django.urls import path
from . import views

urlpatterns = [
    path('', views.apiOverview ,name='apiOverview' ),
    path('users-list/', views.showAllUsers ,name='users-list' ),
    path('user-details/<int:pk>/', views.showUser ,name='user-details' ),
    path('user-info/', views.getUser ,name='user-info' ),
    path('user-create/', views.createUser ,name='user-create' ),
    path('user-update/<int:pk>/', views.updateUser ,name='user-update' ),
    path('user-delete/<int:pk>/', views.deleteUser ,name='user-delete' ),
    
    
    #avocat
    path('search/<int:n>/<str:name>/<str:rating>/<str:wilaya>/', views.searchLawyer, name='lawyer-search'),
    path('lawyer-details/<str:pk>', views.showLawyer ,name='lawyer-details' ),
    path('lawyer-detail/<str:pk>', views.showLawyerWithId,name='lawyer-detail' ),
    path('lawyers-list/', views.showAllLawyers ,name='lawyers-list' ),
    path('lawyers-listed/<int:n>/', views.showAllLawyersPaginated ,name='lawyers-listed' ),
    path('lawyer-create/', views.createLawyer.as_view() ,name='lawyer-create' ),
    path('lawyer-delete/<int:pk>/', views.deleteLawyer ,name='lawyer-delete' ),
    path('lawyer-update/<int:lawyer_id>/', views.updateLawyer ,name='lawyer-update' ),
    
    #main screen details
    path('main-details/<str:pk>', views.mainScreenDetails ,name='main-details' ),
    
    #cities
    path('cities/', views.get_all_lawyer_cities, name='all_lawyer_cities'),
    
    #appointment
    path('appointment-create/', views.createAppointment, name='appointment-create'),
    
    #get lawyer appointments
    path('get-lawyer-appointments/<int:lawyer_id>/', views.getLawyerAppointments, name='get-lawyer-appointments'),
    
    #reservation
    path('reservation-create/', views.createReservation, name='reservation-create'),
    path('reservation-accept/', views.acceptReservation, name='reservation-accept'),
    path('reservation-delete/<int:reservation_id>/', views.deleteReservation, name='reservation-delete'),
    
    #login
    path('login/', views.LoginWithEmailAndPassword.as_view(), name='LoginWithEmailAndPassword'),
    
    #comment
    path('comment-create/', views.createComment, name='comment-create'),
]