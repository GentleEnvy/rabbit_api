from django.urls import path

from rabbit_api.urls import DOCS
from api.views import *

urlpatterns = [
    path('', DOCS),
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
                ),
                # partners
                *[
                    path(
                        'rabbit/mother/<int:id>/partners/',
                        MotherRabbitPartnersView.as_view()
                    ),
                    path(
                        'rabbit/father/<int:id>/partners/',
                        FatherRabbitPartnersView.as_view()
                    )
                ],
                # recast
                *[
                    path(
                        'rabbit/fattening/<int:id>/recast/',
                        FatteningRabbitRecastView.as_view()
                    ),
                    path(
                        'rabbit/mother/<int:id>/recast/',
                        MotherRabbitRecastView.as_view()
                    ),
                    path(
                        'rabbit/father/<int:id>/recast/',
                        FatherRabbitRecastView.as_view()
                    )
                ],
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
        # period
        *[
            path('statistic/slaughters/', SlaughtersStatisticView.as_view()),
            path('statistic/deaths/', DeathsStatisticView.as_view()),
            path('statistic/bunny_jigs/', BunnyJigsStatisticView.as_view()),
            path('statistic/matings/', MatingsStatisticView.as_view())
        ],
        # time
        *[
            path('statistic/rabbits/', RabbitsStatisticView.as_view()),
            path('statistic/fattenings/', FatteningsStatisticView.as_view()),
            path('statistic/mothers/', MothersStatisticView.as_view()),
            path('statistic/fathers/', FathersStatisticView.as_view()),
            path('statistic/bunnies/', BunniesStatisticView.as_view()),
        ]
    ],
    # operation
    path('operation/', OperationGeneralView.as_view()),
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
    *[
        # general
        path('user/', UserGeneralView.as_view()),
        # docx
        path('user/<int:id>/docx/', UserDocxView.as_view())
    ],
    # task
    *[
        # detail
        path('task/mating/<int:id>/', MatingTaskDetailView.as_view()),
        # anonymous
        *[
            # general
            path('task/anonymous/', AnonymousTaskGeneralView.as_view()),
            # detail
            path('task/anonymous/<int:id>/', AnonymousTaskDetailView.as_view()),
        ],
        # in_progress
        *[
            # generals
            *[
                # general
                path('task/in_progress/', InProgressTaskGeneralView.as_view()),
                # update
                path(
                    'task/in_progress/complete/update/',
                    CompleteUpdateTaskGeneralView.as_view()
                )
            ],
            # details
            *[
                # complete
                *[
                    path(
                        'task/in_progress/complete/<int:id>/',
                        CompleteTaskDetailView.as_view()
                    ),
                    path(
                        'task/in_progress/complete/bunny_jigging/<int:id>/',
                        CompleteBunnyJiggingTaskDetailView.as_view()
                    ),
                    path(
                        'task/in_progress/complete/slaughter_inspection/<int:id>/',
                        CompleteSlaughterInspectionTaskDetailView.as_view()
                    )
                ],
                # confirm
                path(
                    'task/in_progress/confirm/<int:id>/',
                    ConfirmTaskDetailView.as_view()
                )
            ]
        ]
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
    ],
    # feeds
    path('feeds/', FatteningFeedsView.as_view()),
]
