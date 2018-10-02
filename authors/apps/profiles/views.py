from rest_framework import status
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer
from .models import Profile

# Create your views here.

class ProfileAPIView(APIView):
    #Allow any user to hit this endpoint
    permission_classes = (AllowAny,)
    renderer_classes = (ProfileJSONRenderer,)

    def get(self, request, username, format=None):
        try:
            profile =  Profile.objects.get(user__username=username)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                {
                    'message': 'Profile not found'
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request, username, format=None):
        try:
            profile = Profile.objects.get(user__username=username)
            serializer_data = request.data.get('user', {})
            serializer = ProfileSerializer(profile, data=serializer_data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Profile.DoesNotExist:
            return Response(
                    {
                        'message': 'Profile not found'
                    }, 
                    status=status.HTTP_404_NOT_FOUND
                )