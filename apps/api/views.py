from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import service


@api_view(['GET'])
def test(request):
    response = service.test(request.GET)
    return Response(data=response)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def create_fake_info(request):
    if request.user.is_staff:
        service.create_fake_information()
