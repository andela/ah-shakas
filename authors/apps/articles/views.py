from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status

from .permissions import IsOwnerOrReadonly
from .models import ArticlesModel, Comment
from .serializers import ArticlesSerializers, CommentsSerializers


class ArticlesList(ListCreateAPIView):
    queryset = ArticlesModel.objects.all()
    serializer_class = ArticlesSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticlesRenderer,)

    def post(self, request):
        article = request.data.get('article', {})
        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ArticlesDetails(RetrieveUpdateDestroyAPIView):
    queryset = ArticlesModel.objects.all()
    serializer_class = ArticlesSerializers
    renderer_classes = (ArticlesRenderer,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)
    lookup_field = 'slug'

    def put(self, request, slug):
        """This method overwrites the """
        article = ArticlesModel.objects.get(slug=slug)
        data = request.data.get('article', {})
        serializer = self.serializer_class(article, data=data, partial=True)
        if serializer.is_valid():
            self.check_object_permissions(request, article)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        """This method overwrites the default django for an error message"""
        super().delete(self, request, slug)
        return Response({"message": "Article Deleted Successfully"})

class CommentsListCreateView(ListCreateAPIView):
    """
    Class for creating and listing all comments
    """
    queryset = Comment.objects.all()
    serializer_class = CommentsSerializers
    permission_classes= (IsAuthenticatedOrReadOnly,)


    def post(self, request, slug):
        """
        Method for creating article
        """
        article = ArticlesModel.objects.get(slug=slug)
        comment = request.data.get('comment',{})
        comment['author'] = request.user.id
        comment['article'] = article.pk
        serializer = self.serializer_class(data=comment)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, slug): 
        """
        Method for getting all comments
        """
        article = ArticlesModel.objects.get(slug=slug)
        comments = Comment.objects.filter(article=article)
        serializer = self.serializer_class(comments.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CommentsRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    """
    Class for retrieving, updating and deleting a comment
    """
    queryset = Comment.objects.all()
    lookup_field = 'id'
    lookup_url_kwarg = 'id'
    serializer_class = CommentsSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)

    def get_article(self, slug):
        """
        This method returns article for further reference made to article slug
        """
        article = ArticlesModel.objects.filter(slug=slug)
        if not article:
            message = {'message': 'Article slug is not valid.'}
            return message
        # queryset always has 1 thing as long as it is unique
        return article[0]
    
    def destroy(self, request, slug, id):
        """
        Method for deleting a comment
        """
        article = self.get_article(slug)
        if isinstance(article, dict):
            return Response(article, status=status.HTTP_404_NOT_FOUND)

        comment = article.comments.filter(id=id) 
        if not comment:
            message = {'detail': 'Comment not found.'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        comment[0].delete()
        message = {'detail': 'You have deleted the comment'}
        return Response(message, status=status.HTTP_200_OK)

    def update(self, request, slug, id):
        """
        Method for editing a comment
        """
        article = self.get_article(slug)
        if isinstance(article, dict):
            return Response(article, status=status.HTTP_404_NOT_FOUND)

        comment = article.comments.get(id=id)
        if not comment:
            message = {'detail': 'Comment not found.'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        
        new_comment = request.data.get('comment',{})
        serializer = self.serializer_class(comment, data=new_comment, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(article=article, author=request.user)
        return Response(serializer.data)
    
