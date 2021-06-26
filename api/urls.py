from django.urls import path

from api import views
from api.views import *

urlpatterns = [
    # model_views
    *[
        # rabbit
        *[
            # general
            *[
                path(
                    'rabbit/dead/', DeadRabbitGeneralView.as_view(),
                    name='dead_rabbit__general__url'
                ),
                path(
                    'rabbit/fattening/', FatteningRabbitGeneralView.as_view(),
                    name='fattening_rabbit__general__url'
                ),
                path(
                    'rabbit/bunny/', BunnyGeneralView.as_view(),
                    name='bunny__general__url'
                ),
                path(
                    'rabbit/mother/', MotherRabbitGeneralView.as_view(),
                    name='mother_rabbit__general__url'
                ),
                path(
                    'rabbit/father/', FatherRabbitGeneralView.as_view(),
                    name='father_rabbit__general__url'
                ),
            ],
        ]
    ],

    # view
    path(
        'rabbit/<int:id>/', views.RabbitView.as_view(),
        name='rabbit_url'
    )

    # TODO: cast_to
    # path(
    #     'rabbit/<int:id>/cast_to_dead', views.DeadRabbitView.as_view(),
    #     name='dead_cast_url'
    # ),
    # path(
    #     'rabbit/<int:id>/cast_to_fattening', views.DeadRabbitView.as_view(),
    #     name='fattening_cast_url'
    # ),
    # path(
    #     'rabbit/<int:id>/cast_to_mother', views.DeadRabbitView.as_view(),
    #     name='mother_cast_url'
    # ),
    # path(
    #     'rabbit/<int:id>/cast_to_father', views.DeadRabbitView.as_view(),
    #     name='father_cast_url'
    # )
]
