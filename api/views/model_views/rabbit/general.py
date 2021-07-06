from django.db.models import Q
from django.forms import model_to_dict
from rest_framework.fields import HiddenField

from api.models import *
from api.serializers.base import BaseModelSerializer
from api.views.model_views.base import BaseGeneralView
from api.views.model_views.rabbit._default_serializers import *

__all__ = [
    'RabbitGeneralView', 'RabbitLiveGeneralView', 'DeadRabbitGeneralView',
    'FatteningRabbitGeneralView', 'BunnyGeneralView', 'MotherRabbitGeneralView',
    'FatherRabbitGeneralView'
]


class RabbitGeneralView(BaseGeneralView):
    class __ListSerializer(BaseModelSerializer):
        class Meta:
            model = Rabbit
            fields = '__all__'

    model = Rabbit
    list_serializer = __ListSerializer
    queryset = model.objects.all()

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        params = self.request.query_params
        farm_number = params.get('farm_number')
        gender = params.get('gender')
        rabbit_type = params.get('type')
        # breed = params.get('breed')
        status = params.get('status')
        age_from = params.get('age_from', 0)
        age_to = params.get('age_to', float('inf'))
        weight_from = params.get('weight_from', 0)
        weight_to = params.get('weight_to', float('inf'))

        limit_from = params.get('__limit_from__')
        limit_to = params.get('__limit_to__')
        order_by = params.get('__order_by__')

        if order_by is None:
            ordered_queryset = queryset
        else:
            ordered_queryset = queryset.order_by(order_by)

        filtered_queryset = ordered_queryset.filter(
            is_male=True if gender == 'male' else False,
            current_type=rabbit_type[:1].upper(),
        ).filter(
            pk__in=[
                rabbit.id for rabbit in ordered_queryset
                if any(s in rabbit.cast.manager.status for s in status) and rabbit.cast.cage.farm_number in farm_number
            ]
        ).filter(
            pk__in=[
                rabbit.id for rabbit in ordered_queryset
                if age_from < rabbit.cast.manager.age < age_to and weight_from < rabbit.weight < weight_to
            ]
        )

        if limit_from is not None:
            if limit_to is not None:
                return filtered_queryset[int(limit_from):int(limit_to)]
            return filtered_queryset[int(limit_from):]
        if limit_to is not None:
            return filtered_queryset[:int(limit_to)]
        return filtered_queryset


class RabbitLiveGeneralView(BaseGeneralView):
    model = Rabbit
    list_serializer = create_default_retrieve_serializer(model)
    queryset = model.objects.exclude(current_type=DeadRabbit.CHAR_TYPE).all()

    def list(self, request, *args, **kwargs):
        super_list = super().list(request, *args, **kwargs)
        ids = [rabbit_info['id'] for rabbit_info in super_list.data]
        mother_cages = MotherCage.objects.filter(
            Q(fatherrabbit__id__in=ids) | Q(motherrabbit__id__in=ids) |
            Q(bunny__id__in=ids)
        )
        fattening_cages = FatteningCage.objects.filter(
            Q(fatherrabbit__id__in=ids) | Q(fatteningrabbit__id__in=ids)
        )
        cages = {c.id: c for c in mother_cages} | {c.id: c for c in fattening_cages}
        for rabbit_info in super_list.data:
            if cage := cages.get(rabbit_info['id']):
                cage_info = model_to_dict(cage)
                cage_info.pop('cage_ptr')
                rabbit_info['cage'] = cage_info
        return super_list


class DeadRabbitGeneralView(BaseGeneralView):
    model = DeadRabbit
    list_serializer = create_default_retrieve_serializer(model)
    queryset = model.objects.all()


class FatteningRabbitGeneralView(BaseGeneralView):
    model = FatteningRabbit
    create_serializer = create_default_create_serializer(model)
    list_serializer = create_default_retrieve_serializer(model, 1)
    queryset = model.objects.all()


class BunnyGeneralView(BaseGeneralView):
    model = Bunny
    create_serializer = create_default_create_serializer(model)
    list_serializer = create_default_retrieve_serializer(model, 1)
    queryset = model.objects.all()


class MotherRabbitGeneralView(BaseGeneralView):
    model = MotherRabbit
    create_serializer = create_default_create_serializer(
        model, is_male_field=HiddenField(default=False)
    )
    list_serializer = create_default_retrieve_serializer(model, 1)
    queryset = model.objects.all()


class FatherRabbitGeneralView(BaseGeneralView):
    model = FatherRabbit
    create_serializer = create_default_create_serializer(
        model, is_male_field=HiddenField(default=True)
    )
    list_serializer = create_default_retrieve_serializer(model, 1)
    queryset = model.objects.all()
