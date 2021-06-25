from django.urls import path

from api import views

urlpatterns = [
    path(
        'rabbit/<int:id>/', views.RabbitView.as_view(),
        name='rabbit_url'
    ),
    path(
        'rabbit/dead/<int:id>/', views.DeadRabbitView.as_view(),
        name='dead_rabbit_url'
    ),

    path(
        'rabbit/bunny/<int:id>/', views.BunnyView.as_view(),
        name='bunny_url'
    ),
    path(
        'rabbit/bunny/create/', views.BunnyCreateView.as_view(),
        name='bunny_create_url'
    ),

    path(
        'rabbit/fattening/<int:id>/', views.FatteningRabbitView.as_view(),
        name='fattening_rabbit_url'
    ),
    path(
        'rabbit/fattening/create/', views.FatteningRabbitCreateView.as_view(),
        name='fattening_create_url'
    ),

    path(
        'rabbit/mother/<int:id>/', views.MotherRabbitView.as_view(),
        name='mother_rabbit_url'
    ),
    path(
        'rabbit/mother/create/', views.MotherRabbitCreateView.as_view(),
        name='mother_create_url'
    ),

    path(
        'rabbit/father/<int:id>/', views.FatherRabbitView.as_view(),
        name='father_rabbit_url'
    ),
    path(
        'rabbit/father/create/', views.FatherRabbitCreateView.as_view(),
        name='father_create_url'
    )
]
