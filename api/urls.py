from django.urls import path

from api.views import *

urlpatterns = [
    # model_views
    *[
        # rabbit
        *[
            # general
            *[
                path('rabbit/', RabbitGeneralView.as_view()),
                path('rabbit/reproduction/', ReproductionRabbitGeneralView.as_view())
            ],
            # detail
            *[
                path('rabbit/<int:id>/', RabbitDetailView.as_view()),
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
                )
            ]
        ],
        # cage
        *[
            # general
            path('cage/', CageGeneralView.as_view()),
            # detail
            path('cage/<int:id>/', CageDetailView.as_view())
        ]
    ],
    # statistic
    *[
        path('statistic/', StatisticView.as_view()),
        # INPROGRESS: branch: feature-static-(envy):
        #   path('statistic/.../', )
    ],
    # operation
    path('operation/', OperationGeneralView.as_view()),
    # recast
    *[
        path('rabbit/<int:id>/recast_to_dead/', DeadRabbitRecastView.as_view()),
        path('rabbit/<int:id>/recast_to_fattening/', FatteningRabbitRecastView.as_view()),
        path(
            'rabbit/<int:id>/recast_to_reproduction/',
            ReproductionRabbitRecastView.as_view()
        )
    ],
    # breed
    path('breed/', BreedGeneralView.as_view()),
    # plan
    *[
        path('plan/', PlanGeneralView.as_view()),
        path('plan/<int:id>/', PlanDetailView.as_view()),
        path('plan/<int:id>/rabbits/', PlanRabbitsView.as_view())
    ],
    path('breed/', BreedGeneralView.as_view()),
    # echo
    path('echo/', EchoView.as_view()),
    # auth
    path('auth/token/', AuthTokenView.as_view()),
    path('auth/session/', AuthSessionView.as_view()),
    # task
    *[
        # anonymous
        *[
            path('task/anonymous/', AnonymousTaskGeneralView.as_view()),  # FIXME
            # path('task/anonymous/<int:id>', None),  # FIXME
        ],
        # in_progress
        *[
            # path('task/in_progress/', None),  # FIXME
            # path('task/in_progress/<int:id>', None),  # FIXME
        ],
        # waiting_confirmation
        *[
            # path('task/waiting_confirmation/', None),  # FIXME
            # path('task/waiting_confirmation/<int:id>', None),  # FIXME
        ],
    ]
]
