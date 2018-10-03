from .models import ArticlesModel
from .serializers import ArticlesSerializers
from rest_framework import mixins, viewsets, generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status


class ArticlesViews(generics.ListCreateAPIView):
    queryset = ArticlesModel.objects.all()
    serializer_class = ArticlesSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)

