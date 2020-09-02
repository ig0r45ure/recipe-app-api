from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import OrgUnit

from eramis import serializers


class OrgUnitViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage org units in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = OrgUnit.objects.all()
    serializer_class = serializers.OrgUnitSerializer

    def get_queryset(self):
        """Return objects"""
        return self.queryset.order_by('-is_HQUnit', 'acronym', )
