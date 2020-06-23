from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
import jwt
from datetime import datetime, timedelta



class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, email, password):
        if not username:
            raise TypeError('Users must have a username.')

        if not email :
            raise TypeError('User must have email.')
        email = self.normalize_email(email)

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save()

        return user

   

    def create_superuser(self, username, email, password):
    
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user

    
    def get_by_natural_key(self, email):
        return self.get(email=email)

       


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=100, unique=True,)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    shop = models.CharField(max_length=100,null=True,blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [ 'username']
    objects = CustomUserManager()
    def __str__(self):
        return self.email
        
    @property
    def token(self):
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        return self.first_name

    def natural_key(self):
        return self.first_name, self.last_name


class MerchantManager(BaseUserManager):
    def create_merchant(self, username, email,first_name,last_name, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        email = self.normalize_email(email)
        merchant = Merchant(username=username, email=email, first_name=first_name, last_name=last_name)
        merchant.is_staff = True
        merchant.is_superuser = True
        merchant.set_password(password)
        merchant.save()
        return merchant

class ManagerManager(BaseUserManager):
    def create_manager(self, username, email, shop, first_name, last_name, password=None, is_active=True):
        if email is None:
            raise TypeError('Users must have an email address.')
        email = self.normalize_email(email)
        manager = Manager(username=username, email=email ,shop=shop, first_name=first_name, last_name=last_name, is_active=is_active)
        manager.is_staff = True
        manager.set_password(password)
        manager.save()
        return manager

class ClerkManager(BaseUserManager):
    def create_clerk(self, username, email, shop,first_name,last_name, password=None):
        if email is None:
            raise TypeError('Users must have an email address.')
        email = self.normalize_email(email)
        clerk = Clerk(username=username, shop=shop, email=email, first_name=first_name, last_name=last_name)
        clerk.set_password(password)
        clerk.save()
        return clerk


class Merchant(User, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['email', 'username']
  

    objects = MerchantManager()

    def __str__(self):
        return self.username


class Manager(User, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['email', 'username']

   

    objects = ManagerManager()

    def __str__(self):
        return self.username



class Clerk(User, PermissionsMixin):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELD = ['email', 'username']
    

    objects = ClerkManager()


    def __str__(self):
        return self.username




class Shop(models.Model):
    shop_name = models.CharField(max_length=50, null=True)
 
    def __str__(self):
        return self.shop_name


    
class Product(models.Model):
    product_name = models.CharField(max_length=50, null=True)

    manager = models.OneToOneField(Manager, on_delete=models.CASCADE)

    def __str__(self):
        return self.shop_name

class Supplier(models.Model):
    supplier_name = models.CharField(max_length=20, null=True)
    supplier_contant = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.supplier_name

class Item(models.Model):
    item_name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.item_name

class ProductBatch(models.Model):

    item = models.ForeignKey(Item, null=True, on_delete=models.SET_NULL)

    buying_price = models.IntegerField(null=True)

    date_received = models.DateField(auto_now_add=True)

    damaged_items = models.IntegerField(null=True)

    supplier = models.ForeignKey(Supplier, null=True, on_delete=models.SET_NULL)

    clerk = models.ForeignKey(Clerk, null=True, on_delete=models.SET_NULL)

    payment_status = models.BooleanField(default=False)

    def __str__(self):
        return self.item.item_name



class ProductSales(models.Model):
    product = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(null=True)
    selling_price = models.DateField(auto_now_add=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    def __str__(self):
        return self.product.item_name


