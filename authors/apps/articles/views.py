from rest_framework.generics import (ListCreateAPIView, 
        RetrieveUpdateDestroyAPIView, GenericAPIView)
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound, ValidationError

from .permissions import IsOwnerOrReadonly
from .models import ArticlesModel, Comment, Rating
from .serializers import ArticlesSerializers, CommentsSerializers, RatingSerializer
from .renderers import ArticlesRenderer, RatingJSONRenderer


def get_article(slug):
        """
        This method returns article for further reference made to article slug
        """
        article = ArticlesModel.objects.filter(slug=slug).first()
        if not article:
            message = {'message': 'Article slug is not valid.'}
            return message
        # queryset always has 1 thing as long as it is unique
        return article
    
class ArticlesList(ListCreateAPIView):
    queryset = ArticlesModel.objects.all()
    serializer_class = ArticlesSerializers
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticlesRenderer,)

    def post(self, request):
        article = request.data.get('article', {})
        serializer = self.serializer_class(
            data=article, 
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(author=request.user)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

class ArticlesDetails(RetrieveUpdateDestroyAPIView, ):
    queryset = ArticlesModel.objects.all()
    serializer_class = ArticlesSerializers
    renderer_classes = (ArticlesRenderer,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)
    lookup_field = 'slug'

    def put(self, request, slug):
        """This method overwrites the """
        article = ArticlesModel.objects.get(slug=slug)
        data = request.data.get('article', {})
        serializer = self.serializer_class(
            article, 
            data=data, 
            partial=True, 
            context={'request': request}
        )
        if serializer.is_valid():
            self.check_object_permissions(request, article)
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, slug):
        """This method overwrites the default django for an error message"""
        super().delete(self, request, slug)
        return Response({"message": "Article Deleted Successfully"})


class RatingDetails(GenericAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)
    renderer_classes = (RatingJSONRenderer,)

    def get_rating(self, user, article):
        """
        Returns a rating given the user id and the article id
        """
        try:
            return Rating.objects.get(user=user, article=article)
        except Rating.DoesNotExist:
            raise NotFound(detail={'rating': 'Rating not found'})

    def get(self, request, slug):
        """
        Returns the authenticated user's rating on an article given
        its slug.
        """
        article = get_article(slug) 
        if isinstance(article, dict):
            raise ValidationError(detail={'artcle': 'No article found for the slug given'})

        # If the user is authenticated, return their rating as well, if not or
        # the user has not rated the article return the rating average...
        rating = None
        if request.user.is_authenticated:
            try:
                rating = Rating.objects.get(user=request.user, article=article)
            except Rating.DoesNotExist:
                pass
        if not rating:
            rating = Rating.objects.first()

        serializer = self.serializer_class(rating)
        return Response(serializer.data)

    def post(self, request, slug):
        """
        This will create a rating by user on an article. We also check 
        if the user has rated this article before and if that is the case,
        we just update the existing rating.
        """
        article = get_article(slug) 
        if isinstance(article, dict):
            raise ValidationError(detail={'artcle': 'No article found for the slug given'})
        rating = request.data.get('rating', {})
        rating.update({
            'user': request.user.pk,
            'article': article.pk
        })
        # ensure a user cannot rate their own articles
        if article.author == request.user:
            raise ValidationError(detail={'author': 'You cannot rate your own article'})
        # users current rating exists?
        try:
            # if the rating exists, we update it
            current_rating = Rating.objects.get(
                user=request.user.id, 
                article=article.id
            )
            serializer = self.serializer_class(current_rating, data=rating)
        except Rating.DoesNotExist:
            # if it doesn't, create a new one
            serializer = self.serializer_class(data=rating)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, article=article)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, slug):
        """
        Gets an existing rating and updates it
        """
        rating = request.data.get('rating', {})
        article = get_article(slug) 
        if isinstance(article, dict):
            raise ValidationError(detail={'artcle': 'No article found for the slug given'})
        current_rating = self.get_rating(user=request.user.id, article=article.id)
        serializer = self.serializer_class(current_rating, data=rating, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, article=article)

        return Response(serializer.data)
      
    def delete(self, request, slug):
        """
        Deletes a rating
        """
        article = get_article(slug) 
        if isinstance(article, dict):
            raise ValidationError(detail={'artcle': 'No article found for the slug given'})

        rating = self.get_rating(user=request.user, article=article)
        rating.delete()

        return Response(
            {'message': 'Successfully deleted rating'}, 
            status=status.HTTP_200_OK
        )


def get_article(slug):
        """
        This method returns article for further reference made to article slug
        """
        article = ArticlesModel.objects.filter(slug=slug).first()
        if not article:
            message = {'message': 'Article slug is not valid.'}
            return message
        # queryset always has 1 thing as long as it is unique
        return article
    
    
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
        article = get_article(slug=slug)
        if isinstance(article, dict):
            return Response(article, status=status.HTTP_404_NOT_FOUND)

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
        article = get_article(slug=slug)
        if isinstance(article, dict):
            return Response(article, status=status.HTTP_404_NOT_FOUND)
        comments = article.comments.filter(parent=None)
        serializer = self.serializer_class(comments.all(), many=True)
        data = {
            'count': comments.count(),
            'comments': serializer.data
        }
        return Response(data, status=status.HTTP_200_OK)


class CommentsRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView, ListCreateAPIView):
    """
    Class for retrieving, updating and deleting a comment
    """
    queryset = Comment.objects.all()
    lookup_url_kwarg = 'id'
    serializer_class = CommentsSerializers
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)

    def create(self, request, slug, id):
        """Create a child comment on a parent comment."""
        context = super(CommentsRetrieveUpdateDestroy,
                        self).get_serializer_context()
        
        article = get_article(slug)
        if isinstance(article, dict):
            return Response(article, status=status.HTTP_404_NOT_FOUND)
        parent = article.comments.filter(id=id).first().pk
        if not parent:
            message = {'detail': 'Comment not found.'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        body = request.data.get('comment', {}).get('body', {})
        
        data = {
            'body': body,
            'parent': parent,
            'article': article.pk,
            'author': request.user.id
        }
        
        serializer = self.serializer_class(
            data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def destroy(self, request, slug, id):
        """
        Method for deleting a comment
        """
        article = get_article(slug)
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
        article = get_article(slug)
        if isinstance(article, dict):
            return Response(article, status=status.HTTP_404_NOT_FOUND)

        comment = article.comments.filter(id=id).first()
        if not comment:
            message = {'detail': 'Comment not found.'}
            return Response(message, status=status.HTTP_404_NOT_FOUND)
        
        new_comment = request.data.get('comment',{}).get('body', None)
        data = {
            'body': new_comment,
            'article': article.pk,
            'author': request.user.id
        }
        serializer = self.serializer_class(comment, data=data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    

class RatingDetails(GenericAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsOwnerOrReadonly)
    renderer_classes = (RatingJSONRenderer,)

    def get_rating(self, user, article):
        """
        Returns a rating given the user id and the article id
        """
        try:
            return Rating.objects.get(user=user, article=article)
        except Rating.DoesNotExist:
            raise NotFound(detail={'rating': 'Rating not found'})

    def get_article(self, slug):
        """
        Returns an article given its slug
        """
        try:
            return ArticlesModel.objects.get(slug=slug)
        except ArticlesModel.DoesNotExist:
            raise ValidationError(detail={'artcle': 'No article found for the slug given'})

    def get(self, request, slug):
        """
        Returns the authenticated user's rating on an article given
        its slug.
        """
        article = self.get_article(slug) 
        rating = self.get_rating(article=article.id, user=request.user.id)
        serializer = self.serializer_class(rating)

        return Response(serializer.data)

    def post(self, request, slug):
        """
        This will create a rating by user on an article. We also check 
        if the user has rated this article before and if that is the case,
        we just update the existing rating.
        """
        article = self.get_article(slug) 
        rating = request.data.get('rating', {})
        rating.update({
            'user': request.user.pk,
            'article': article.pk
        })
        # ensure a user cannot rate their own articles
        if article.author == request.user:
            raise ValidationError(detail={'author': 'You cannot rate your own article'})
        # users current rating exists?
        try:
            # if the rating exists, we update it
            current_rating = Rating.objects.get(
                user=request.user.id, 
                article=article.id
            )
            serializer = self.serializer_class(current_rating, data=rating)
        except Rating.DoesNotExist:
            # if it doesn't, create a new one
            serializer = self.serializer_class(data=rating)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, article=article)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, slug):
        """
        Gets an existing rating and updates it
        """
        rating = request.data.get('rating', {})
        article = self.get_article(slug) 
        current_rating = self.get_rating(user=request.user.id, article=article.id)
        serializer = self.serializer_class(current_rating, data=rating, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, article=article)

        return Response(serializer.data)
