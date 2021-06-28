from django.urls import path

from api.views import *

urlpatterns = [
    # model_views
    *[
        # rabbit
        *[
            # general
            *[
                path(
                    'rabbit/', RabbitGeneralView.as_view(),
                    name='rabbit__general__url'
                ),
                path(
                    'rabbit/live/', RabbitLiveGeneralView.as_view(),
                    name='rabbit_live__general__url'
                ),
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
            # detail
            *[
                path(
                    'rabbit/<int:id>/', RabbitDetailView.as_view(),
                    name='rabbit__detail__url'
                ),
                path(
                    'rabbit/dead/<int:id>/', DeadRabbitDetailView.as_view(),
                    name='dead_rabbit__detail__url'
                ),
                path(
                    'rabbit/fattening/<int:id>/', FatteningRabbitDetailView.as_view(),
                    name='fattening_rabbit__detail__url'
                ),
                path(
                    'rabbit/bunny/<int:id>/', BunnyDetailView.as_view(),
                    name='bunny__detail__url'
                ),
                path(
                    'rabbit/mother/<int:id>/', MotherRabbitDetailView.as_view(),
                    name='mother_rabbit__detail__url'
                ),
                path(
                    'rabbit/father/<int:id>/', FatherRabbitDetailView.as_view(),
                    name='father_rabbit__detail__url'
                ),
            ]
        ],
        # cage
        *[
            # general
            *[
                path(
                    'cage/', CageGeneralView.as_view(),
                    name='cage__general__url'
                ),
                path(
                    'cage/mother/', MotherCageGeneralView.as_view(),
                    name='mother_cage__general__url'
                ),
                path(
                    'cage/fattening/', FatteningCageGeneralView.as_view(),
                    name='fattening_cage__general__url'
                ),
            ],
            # detail
            *[
                path(
                    'cage/<int:id>/', CageDetailView.as_view(),
                    name='cage__detail__url'
                ),
                path(
                    'cage/mother/<int:id>/', MotherCageDetailView.as_view(),
                    name='mother_cage__detail__url'
                ),
                path(
                    'cage/fattening/<int:id>/', FatteningCageDetailView.as_view(),
                    name='fattening_cage__detail__url'
                ),
            ]
        ]
    ]

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
