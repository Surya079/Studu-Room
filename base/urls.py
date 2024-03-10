from django.urls import path
from . import views

urlpatterns = [
    path('',views.home, name="Home"),
    
    path('login/',views.loginPage,name="login"),
    path('register/',views.registerPage,name='register'),
    path('logout/',views.logoutUser,name="logout"),
    
    path('room/<str:pk>/',views.room, name="room"),
    path('profile/<str:pk>/',views.UserProfile, name="profile"),

    path('Room_create/',views.Room_create, name="Room_create"),
    path('Update_room/<str:pk>/', views.Update_room, name="Update_room"),
    path('Delete_room/<str:pk>/', views.DeleteRoom, name="Delete_room"),
    path('Delete_message/<str:pk>/', views.Deletemessage, name="Delete_message"),

    path('Update_user/',views.UpdateUser,name='Update_user'),

    path('Topic/',views.TopicPage,name='Topics'),
    path('Activity/',views.ActivityPage,name='Activity'),
]