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
                    'rabbit/mother/<int:id>/partners/', MotherRabbitPartnersView.as_view()
                ),
                path(
                    'rabbit/father/<int:id>/', FatherRabbitDetailView.as_view(),
                    name='father_rabbit__detail__url'
                ),
                path(
                    'rabbit/father/<int:id>/partners/', FatherRabbitPartnersView.as_view()
                )
            ],
            # death
            path('rabbit/death/', RabbitDeathView.as_view())
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
    *[
        path('auth/token/', AuthTokenView.as_view()),
        path('auth/session/', AuthSessionView.as_view())
    ],
    # user
    path('user/', UserListView.as_view()),
    # task
    *[
        # anonymous
        *[
            path('task/anonymous/', AnonymousTaskGeneralView.as_view()),
            path('task/anonymous/<int:id>/', AnonymousTaskDetailView.as_view()),
        ],
        # in_progress
        *[
            path('task/in_progress/', InProgressTaskGeneralView.as_view()),
            path('task/in_progress/<int:id>/', InProgressTaskDetailView.as_view()),
            path(
                'task/in_progress/bunny_jigging/<int:id>/',
                InProgressBunnyJiggingTaskDetailView.as_view()
            ),
            path(
                'task/in_progress/slaughter_inspection/<int:id>/',
                InProgressSlaughterInspectionTaskDetailView.as_view()
            ),
        ],
        # waiting_confirmation
        *[
            path(
                'task/waiting_confirmation/', WaitingConfirmationTaskGeneralView.as_view()
            ),
            path(
                'task/waiting_confirmation/<int:id>/',
                WaitingConfirmationTaskDetailView.as_view()
            ),
        ],
    ],
    # birth
    *[
        # general
        *[
            path('birth/confirmed/', BirthConfirmedGeneralView.as_view()),
            path('birth/unconfirmed/', BirthUnconfirmedGeneralView.as_view())
        ],
        # detail
        *[
            path('birth/confirmed/<int:id>/', BirthConfirmedDetailView.as_view()),
            path('birth/unconfirmed/<int:id>/', BirthUnconfirmedDetailView.as_view())
        ]
    ]
]
