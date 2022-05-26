from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from . import service


@api_view(['POST'])
def verification_sms(request):
    phone = request.POST.get('phone')

    if phone is None:
        return Response(data={'error': 'phone is not specified'}, status=400)
    
    body, status = service.start_new_verification(phone)

    return Response(data=body, status=status)

@api_view(['PUT'])
def verificate_phone(request):
    phone = request.POST.get('phone')
    code = request.POST.get('code')

    if phone is None or code is None:
        return Response(data={'error': 'phone and verification code are required'}, status=400)
    
    body, status = service.verification(phone, code)

    return Response(data=body, status=status)
