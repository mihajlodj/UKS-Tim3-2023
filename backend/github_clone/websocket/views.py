from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from main.models import Notification


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notifications(request):
    notifications = Notification.objects.filter(sent_to=request.user.username).order_by('-timestamp')
    result = [
        {
            'message': notif.message,
            'timestamp': notif.timestamp,
            'is_read': notif.is_read,
            'id': notif.id
        }
        for notif in notifications
    ]
    return Response(result, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def mark_as_read(request, notification_id):
    if not Notification.objects.filter(id=notification_id).exists():
        return Response(status=status.HTTP_404_NOT_FOUND)
    notification = Notification.objects.get(id=notification_id)
    notification.is_read = True
    notification.save()
    return Response(status=status.HTTP_200_OK)
