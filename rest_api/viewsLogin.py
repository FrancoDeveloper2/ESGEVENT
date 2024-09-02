from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password
from Store.models import Usuario 
from rest_framework.authtoken.models import Token

@csrf_exempt
@api_view(['POST'])
def login_api(request):
    data = JSONParser().parse(request)
    username = data['username']
    password = data['password']
    
    try:
        user = Usuario.objects.get(username=username)
    except Usuario.DoesNotExist:
        return Response("Usuario invalido", status=status.HTTP_404_NOT_FOUND)
    
    pass_valido = check_password(password, user.password)
    
    if not pass_valido:
        return Response("Password incorrecta", status=status.HTTP_401_UNAUTHORIZED)
    
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key})