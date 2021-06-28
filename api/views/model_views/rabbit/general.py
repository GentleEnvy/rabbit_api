from django.db.models import Q
from django.forms import model_to_dict
from rest_framework.fields import HiddenField

from api.models import *
from api.serializers.base import BaseModelSerializer
from api.views.model_views.base import BaseGeneralView
from api.views.model_views.rabbit._default_serializers import \
    create_default_retrieve_serializer

__all__ = [
    'RabbitGeneralView', 'RabbitLiveGeneralView', 'DeadRabbitGeneralView',
    'FatteningRabbitGeneralView', 'BunnyGeneralView', 'MotherRabbitGeneralView',
    'FatherRabbitGeneralView'
]


def _create_default_create_serializer(serializer_model, is_male_field=None):
    if is_male_field is None:
        class DefaultCreateSerializer(BaseModelSerializer):
            class Meta:
                model = serializer_model
                fields = '__all__'

            current_type = HiddenField(default=serializer_model.CHAR_TYPE)
    else:
        class DefaultCreateSerializer(BaseModelSerializer):
            class Meta:
                model = serializer_model
                fields = '__all__'

            current_type = HiddenField(default=serializer_model.CHAR_TYPE)
            is_male = is_male_field

    return DefaultCreateSerializer


class RabbitGeneralView(BaseGeneralView):
    class __ListSerializer(BaseModelSerializer):
        class Meta:
            model = Rabbit
            fields = '__all__'

    model = Rabbit
    list_serializer = __ListSerializer
    queryset = model.objects.all()


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
    create_serializer = _create_default_create_serializer(model)
    list_serializer = create_default_retrieve_serializer(model, 1)
    queryset = model.objects.all()


class BunnyGeneralView(BaseGeneralView):
    model = Bunny
    create_serializer = _create_default_create_serializer(model)
    list_serializer = create_default_retrieve_serializer(model, 1)
    queryset = model.objects.all()


class MotherRabbitGeneralView(BaseGeneralView):
    model = MotherRabbit
    create_serializer = _create_default_create_serializer(
        model, is_male_field=HiddenField(default=False)
    )
    list_serializer = create_default_retrieve_serializer(model, 1)
    queryset = model.objects.all()


class FatherRabbitGeneralView(BaseGeneralView):
    model = FatherRabbit
    create_serializer = _create_default_create_serializer(
        model, is_male_field=HiddenField(default=True)
    )
    list_serializer = create_default_retrieve_serializer(model, 1)
    queryset = model.objects.all()
