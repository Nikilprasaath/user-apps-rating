from django.shortcuts import render
from rest_framework.decorators import APIView
from knox.views import LoginView
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from .serializer import RegisterSerializer, appserializer, user_profile_serializer, admintaskserializer, taskserializer, AdminRegisterSerializer, nameserializer
from rest_framework import status, mixins, generics
from rest_framework.permissions import BasePermission, IsAuthenticated, DjangoModelPermissions
from django.contrib.auth.models import User
from .models import app, user_profile, tasks
from knox.auth import TokenAuthentication
from drf_yasg.utils import swagger_auto_schema

'''
This permission class checks whether the user is present in the admin group
'''
class adminpermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(id=1):
            return True
        return False

'''
This permission class checks whether the user is present in the user group
'''
class userpermission(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(id=2):
            return True
        return False

#user views
'''
It is a login view for normal users, they login using user_name, password and get a token after authentication
'''
class login(LoginView):
    authentication_classes = [BasicAuthentication,]
    permission_classes = [IsAuthenticated,userpermission]

'''
It is a sign up view for normal users and when a user signs in they get addes to rhe user group
'''
class signup(APIView):
    def post(self, request):
        serial = RegisterSerializer(data= request.data)
        if serial.is_valid():
            serial.save()
            return Response("user created", status= status.HTTP_201_CREATED)
        return Response(serial.errors, status= status.HTTP_400_BAD_REQUEST)


'''
It is the homeview, it returns all the available apps and user id and name to the user, using user authentication details
'''
class homeview(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = app.objects.all()
    
    
    def get(self, request):
        
        id = request.user.id
        try:
            obj=app.objects.all()
            obj2=User.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serial = appserializer(obj,many=True)
        serial1= nameserializer(obj2)
        return Response([serial1.data]+serial.data,status=status.HTTP_200_OK)


'''
In this view the user gets all info about the apps that he downloaded and got verifed by the admin
'''
class userprofile(generics.GenericAPIView):
    queryset = user_profile.objects.all()
    serializer_class = user_profile_serializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]

    def get(self, request):
        id = request.user.id
        try:
            obj = user_profile.objects.get(user= id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serial = self.get_serializer(obj)
        return Response(serial.data,status=status.HTTP_200_OK)


'''
This view gives info about his tasks, and says whether it is approved or rejected or still in pending based on the screenshot he uploaded.
And can add new tasks by uploading a scrn shot of the app by selecting the app
'''      
class usertasks(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = tasks.objects.all() 
    serializer_class = taskserializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = None or 'id'

    def get(self, request):
        id= request.user.id
        try:
            set = tasks.objects.filter(user= id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serial = self.get_serializer(set,many= True)
        return Response(serial.data,status=status.HTTP_200_OK)
        

    def post(self, request):
        
        request.data['user']= request.user.id
        
        # print(request.FILES)
        return self.create(request)


#admin views
'''
It is admin sign up view where only admin user can add an admin user
'''
class adminsignup(APIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated,adminpermission]
    def post(self, request):
        serial = AdminRegisterSerializer(data= request.data)
        if serial.is_valid():
            serial.save()
            return Response('admin created', status= status.HTTP_201_CREATED)
        return Response(serial.errors, status= status.HTTP_400_BAD_REQUEST)


'''
It is admin login view where only users in admin group will be authenticated
'''
class adminlogin(LoginView):
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated, adminpermission]


'''
In this view an admin can get, create and edit the apps
'''
class editapps(mixins.ListModelMixin,mixins.RetrieveModelMixin,mixins.CreateModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = app.objects.all()
    serializer_class = appserializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions, adminpermission]
    lookup_field = None or 'id'

    
    def get(self, request, id = None):
        if id:
            return self.retrieve(request)
        return self.list(request)

    def post(self, request, ):
        return self.create(request)

    
    def put(self, request, id):
        return self.update(request)

    
    def delete(self, request, id):
        return self.destroy(request)
    

'''
In this an admin can get, create and edit all the userprofiles
'''
class edituserprofile(mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = user_profile.objects.all()
    serializer_class = user_profile_serializer
    authentication_classes= [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    lookup_field = None or 'id'

    @swagger_auto_schema(operation_description="if needed single userprofile object send its id in request.data or to get all userprofile make it empty")
    def get(self, request):
        if request.data:
            id = request.data['id']
            try:
                obj = user_profile.objects.get(id=id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serial = self.get_serializer(obj)
            return Response(serial.data,status=status.HTTP_200_OK)
        set = user_profile.objects.all()
        serial = self.get_serializer(set,many=True)
        
        return Response(serial.data,status=status.HTTP_200_OK)

    def post(self, request):
        return self.create(request)

    def put(self, request):
        try:
            id = request.data['id']
            obj = user_profile.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serial = self.get_serializer(obj,data=request.data)
        serial.is_valid(raise_exception=True)
        serial.save()
        return Response(serial.data,status=status.HTTP_202_ACCEPTED)

    def delete(self, request):
        try:
            id = request.data['id']
            obj = user_profile.objects.get(id=id)
        except:
            return Response("data not found",status=status.HTTP_400_BAD_REQUEST)
        obj.delete()
        return Response("Deleted successfully",status=status.HTTP_200_OK )


'''
Here an admin gets the tasks of the users and he checks the screen shot and changes status of the task. If the task and screen shot is approved 
the app gets added to the user profile and the user points gets auto updated
'''
class admin_user_tasks(generics.GenericAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, DjangoModelPermissions, adminpermission]
    queryset = tasks.objects.all()
    serializer_class = admintaskserializer
    lookup_field = None or 'id'


    @swagger_auto_schema(operation_description="if needed single task object send its id in request.data or to get all tasks make it empty")
    def get(self, request):
        
        if request.data:
            id = request.data['id']
            try:
                obj = tasks.objects.get(id=id)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serial = self.get_serializer(obj)
            return Response(serial.data,status=status.HTTP_200_OK)
        set = tasks.objects.all()
        serial = self.get_serializer(set,many=True)
        
        return Response(serial.data,status=status.HTTP_200_OK)

        ''' 
        set = tasks.objects.filter(status='pending')
        serial = self.get_serializer(set, many=True)
        return Response(serial.data)
        '''

    @swagger_auto_schema(operation_description="It handles the request based on the id present in request.data")
    def put(self, request, **kwargs):
        
        try:
            id = request.data['id']
            obj = tasks.objects.get(id=id)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serial = self.get_serializer(obj,data=request.data)
        serial.is_valid(raise_exception=True)
        serial.save()
        
        if serial.data['status'] == 'approved':
            user_id = serial.data['user']
            
            app = serial.data['app']
            
            # print(user_profile.objects.get(user=user_id))
            user_profile.objects.get(user=user_id).apps.add(app)
        apps=user_profile.objects.get(user=user_id).apps.all().values()
        points = 0
        for i in apps:
            points += i['points']
            

        obj2 = user_profile.objects.get(user=user_id)
        obj2.points = points
        obj2.save()
        
        return Response(serial.data,status=status.HTTP_202_ACCEPTED)
        
        
    @swagger_auto_schema(operation_description="It handles the request based on the id present in request.data")
    def delete(self, request):
        if request.data:
            id = request.data['id']
            obj = tasks.objects.get(id=id)
            obj.delete()
            return Response("Deleted successfully",status=status.HTTP_200_OK)
        else:
            message = 'data not found'
            return Response(message,status=status.HTTP_400_BAD_REQUEST)

