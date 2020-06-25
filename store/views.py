from django.shortcuts import render,redirect
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.permissions import AllowAny
from django.http import HttpResponse, Http404,HttpResponseRedirect
from django.views.generic import View
from django.template.loader import render_to_string
from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model 
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError
from .serializer import *
from .renderers import UserJSONRenderer
from .utils import generate_token

class MerchantRegistration(APIView):
    permission_classes =  [ permissions.AllowAny ]
    renderer_classes = (UserJSONRenderer,)
    serializer_class = MerchantSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ManagerRegistration(APIView):
    permission_classes =  [ permissions.AllowAny ]
    renderer_classes = (UserJSONRenderer,)
    serializer_class = ManagerSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()  

        return Response(serializer.data, status=status.HTTP_201_CREATED)
         
       

class ClerkRegistration(APIView):
    permission_classes =  [ permissions.AllowAny]
    renderer_classes = (UserJSONRenderer,)
    serializer_class = ClerkSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class UserLogin(APIView):
    permission_classes = [ permissions.AllowAny]
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserLoginSearilizer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

USER = get_user_model()

class MerchantList(APIView):
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = MerchantSerializer
    def get(self, request, format=None ):
        all_users =  Merchant.objects.all()
        serializers = MerchantSerializer(all_users, many=True)
        return Response(serializers.data)

class ManagerList(APIView):
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = ManagerSerializer
    def get(self, request, format=None):
        all_users =  Manager.objects.all()
        serializers = ManagerSerializer(all_users, many=True)
        return Response(serializers.data)

class ClerkList(APIView):
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = ClerkSerializer
    def get(self, request, format=None):
        all_users =  Clerk.objects.all()
        serializers = ClerkSerializer(all_users, many=True)
        return Response(serializers.data)



class SoloMerchant(APIView):
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = MerchantSerializer
    
    def get_Merch(self, pk):
        try:
            return Merchant.objects.get(pk=pk)
        except Merchant.DoesNotExist:
            return Http404

    
    def get(self, request, pk, format=None):
        Merch = self.get_Merch(pk)
        serializers = MerchantSerializer(Merch)
        return Response(serializers.data)


    def put(self, request, pk, format=None):
        Merch = self.get_Merch(pk)
        serializers = MerchantSerializer(Merch, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, is_superuser, is_staff, pk, format=None):
        if is_superuser==True and is_staff==True:
            Merch = self.get_Merch(pk)
            Merch.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

class SoloManager(APIView):
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = ManagerSerializer
    def get_Manager(self, pk):
        try:
            return Manager.objects.get(pk=pk)
        except Manager.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        Manager = self.get_Manager(pk)
        serializers = ManagerSerializer(Manager)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        Manager = self.get_Manager(pk)
        serializers = ManagerSerializer(Manager, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk, format=None):
        Manager = self.get_Manager(pk)
        Manager.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class SoloClerk(APIView):
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = ClerkSerializer
    def get_Clerk(self, pk):
        try:
            return Clerk.objects.get(pk=pk)
        except Clerk.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        Clerk = self.get_Clerk(pk)
        serializers = ClerkSerializer(Clerk)
        return Response(serializers.data)

    
    def put(self, request, pk, format=None):
        Clerk = self.get_Clerk(pk)
        serializers = ClerkSerializer(Clerk, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    
    def delete(self, request, pk, format=None):
        Clerk = self.get_Clerk(pk)
        Clerk.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ShopsList(APIView):
    serializer_class = ShopSerializer
    def get(self, request, format=None):
        shops = Shop.objects.all()
        serializer = ShopSerializer(shops, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ShopSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductBatchList(APIView):

    serializer_class = ProductBatchSerializer

    def get(self, request, format=None):
        products = ProductBatch.objects.all()
        serializer = ProductBatchSerializer(products, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = ProductBatchSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class ProductBatchDetail(APIView):
    serializer_class = ProductBatchSerializer
    def get_object(self, pk):
        try:
            return ProductBatch.objects.get(pk=pk)
        except ProductBatch.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProductBatchSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = ProductBatchSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SoloActivateManager(APIView):
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = ManagerActivateSerializer
    def get_Manager(self, pk):
        try:
            return get_user_model().objects.get(pk=pk)
        except get_user_model().DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        Manager = self.get_Manager(pk)
        serializers = ManagerActivateSerializer(Manager)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        Manager = self.get_Manager(pk)
        serializers = ManagerActivateSerializer(Manager, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class SoloActivateClerk(APIView):
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = ClerkActivateSerializer
    def get_Clerk(self, pk):
        try:
            return Clerk.objects.get(pk=pk)
        except Clerk.DoesNotExist:
            return Http404

    def get(self, request, pk, format=None):
        Clerk = self.get_Clerk(pk)
        serializers = ClerkActivateSerializer(Clerk)
        return Response(serializers.data)

    def put(self, request, pk, format=None):
        Clerk = self.get_Clerk(pk)
        serializers = ClerkActivateSerializer(Clerk, request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data)
        else:
            return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
class ItemList(APIView):
    permission_classes = [permissions.AllowAny ]
    serializer_class = ItemSerializer
    def get(self, request, format=None):
        all_items =  Item.objects.all()
        serializers = ItemSerializer(all_items, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ItemSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class PurchaseList(APIView):
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = ProductBatchSerializer
    def get(self, request, format=None):
        all_items =  ProductBatch.objects.all()
        serializers = ProductBatchSerializer(all_items, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProductBatchSerializer(data=request.data)
        order = request.data
        item = Item.objects.get(shop=order["shop"],item_name=order["item"])
        item.quantity = item.quantity+int(order["quantity_bought"])
        
        item.save()
        print(item.quantity)
        print(order["quantity_bought"])

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class SalesList(APIView):
    permission_classes = [
        permissions.AllowAny 
    ]
    serializer_class = ProductSalesSerializer
    def get(self, request, format=None):
        all_items =  ProductSales.objects.all()
        serializers = ProductSalesSerializer(all_items, many=True)
        return Response(serializers.data)

    def post(self, request, format=None):
        serializers = ProductSalesSerializer(data=request.data)
        sale = request.data
        item = Item.objects.get(shop=sale["shop"],item_name=sale["item"])
        item.quantity = item.quantity-int(sale["quantity"])
        item.save()
        print(item.quantity)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)