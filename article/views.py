from django.shortcuts import render , get_object_or_404
from django.contrib.auth import authenticate , login
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated 
from .permissions import ISAuthorOrReadOnly , IsAdmin
from .models import ArticleModel
from.serializers import ArticleSerializer
from core.models import User
from core.serializers import UserRegSerializer , UserLoginSerializer

# Create your views here.

        
class UserRegisterView(APIView):
    serializer_class = UserRegSerializer

    def post(self, request):
        serializer = UserRegSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            response = {
                'user': serializer.data,
                'token': token.key
            }

            return Response(response) 
        return Response(serializer.errors)


class UserLoginView(APIView):

    def post(self, request, *args, **kargs):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        if User.objects.filter(username=request.data['username'] , password = request.data['password']).exists():

            user = User.objects.get(username=request.data['username'])
            token, created = Token.objects.get_or_create(user=user)
            response = {
                'username':user.username,
                'email':user.email,
                'token': token.key
            }
            return Response(response)
        else:
            return Response("incorrect username or password")



class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        user = get_object_or_404(User, id= request.user.id  )
        serializer = UserRegSerializer(user)

        return Response(serializer.data)
    
    def post(self,request):
        user= User.objects.get(id= request.user.id)

        #  we can use both permisons of if else condition for handle this part but permisons works better for modelviewset
        if user.role == 3 :
            serializer = UserRegSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            return Response(serializer.data )
        
        else:
            return Response('you dont have permision')
        
    def put(self,request ):
        user = User.objects.get(id= request.user.id)
        serializer = UserRegSerializer(user, data=request.data , partial = True)

        serializer.is_valid(raise_exception=True )
        if 'role' in request.data:
            return Response('role can not be update ')
        serializer.save()

        return Response(serializer.data)


class ArticleView(APIView):
    permission_classes =[IsAuthenticated]
    serializer_class = ArticleSerializer
    
    def get(self,request , pk=None):
        user=request.user
        if pk is None:

            # this part is for showing just the author articles and all artile to admin but i comment that because i think it is better to show all article to everyone:
            
            # ---------------------------------
            # if user.role <3:
            #     queryset = ArticleModel.objects.filter(author = user)

            # else:
            #     queryset = ArticleModel.objects.all()

            # serializer = ArticleSerializer(queryset , many=True)
            
            # ---------------------------------

            queryset = ArticleModel.objects.all()
            serializer = ArticleSerializer(queryset , many=True)
            
            return Response(serializer.data)
        else:
            try:
                queryset = ArticleModel.objects.get(id = pk)
                serializer = ArticleSerializer(queryset)

                return Response(serializer.data)
            except:
                return Response("The article you are lookking for doesnt exist")
    
    def post(self,request ):
        user = User.objects.get(id= request.user.id)

        #  we can use both permisons of if else condition for handle this part but permisons works better for modelviewset
        if user.role ==1:
            return Response('you dont have permission')
        
        serializer = ArticleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(author = user)

        return Response(serializer.data)

    def delete(self, request, pk):
        user = User.objects.get(id=request.user.id)
        
        if user.role != 3:
            return Response('You do not have permission to delete articles')
        
        try:
            article = ArticleModel.objects.get(id=pk)

        except ArticleModel.DoesNotExist:
            return Response('Article not found',)
        
        article.delete()
        return Response('Article deleted successfully')



