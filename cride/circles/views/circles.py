""" Circles Views. """

# Django REST Framework
from rest_framework import mixins, viewsets

# Models
from cride.circles.models import Circle, Membership

# Serializer
from cride.circles.serializers import CircleModelSerializer

# Permissions
from cride.circles.permissions.circles import IsCircleAdmin
from rest_framework.permissions import IsAuthenticated

# filter
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend


class CircleViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    """ Circle viewset. """

    serializer_class = CircleModelSerializer
    lookup_field = 'slug_name'

    # Filters
    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('slug_name', 'name')
    ordering_fields = ('rides_offered', 'rides_taken', 'name', 'created', 'member_limit')
    ordering = ('-members__count', '-rides_offered', '-rides_taken')
    filter_fields = ('verified', 'is_limited')

    def get_queryset(self):
        """ Restric to public-only. """
        queryset = Circle.objects.all()
        if self.action == 'list':
            return queryset.filter(is_public=True)
        return queryset
    
    def get_permissions(self):
        """ Assign permisions based on action. """
        permissions = [IsAuthenticated]
        if self.action in ['update', 'partial_update']:
            permissions.append(IsCircleAdmin)
        return [permission() for permission in permissions]
    
    def perform_create(self, serializer):
        """ Assign circle admin """
        circle = serializer.save()
        user = self.request.user
        profile = user.profile
        Membership.objects.create(
            user=user,
            profile=profile,
            circle=circle,
            is_admin=True,
            remaining_invitations=10
        )

