from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from main.models import Project, Milestone
from milestone.serializers import MilestoneSerializer


class CreateMilestoneView(generics.CreateAPIView):
    queryset = Milestone.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MilestoneSerializer

class UpdateMilestoneView(generics.UpdateAPIView):
    queryset = Milestone.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = MilestoneSerializer
    lookup_field = 'title'

