from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from account.models import Province, Ward
from account.serializers.province import ProvinceSerializer
from account.serializers.ward import WardSerializer


@extend_schema(tags=['Location'])
class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Province.objects.all()
    serializer_class = ProvinceSerializer

    search_fields = ('full_name', 'full_name_en')

    ordering_fields = ('id', 'name',)
    ordering = ('id',)


@extend_schema(tags=['Location'])
class WardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ward.objects.all()
    serializer_class = WardSerializer

    search_fields = ('full_name', 'full_name_en')

    filterset_fields = ('province',)

    ordering_fields = ('id', 'name',)
    ordering = ('id',)
