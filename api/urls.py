from django.urls import path

from api import views

urlpatterns = [
    path('rabbit/<int:id>/', views.RabbitView.as_view(), name='rabbit_url'),
    path('rabbit/', views.RabbitView.as_view(), name='rabbits_url'),
    path('rabbit/bunny/<int:id>/', views.MotherRabbitView.as_view(), name='bunny_url'),
    path('rabbit/bunny/<int:id>/', views.MotherRabbitView.as_view(), name='bunny_url'),
    path('rabbit/mother/<int:id>/', views.MotherRabbitView.as_view(), name='mother_url'),
    path('rabbit/bunny/<int:id>/', views.MotherRabbitView.as_view(), name='bunny_url')
]
