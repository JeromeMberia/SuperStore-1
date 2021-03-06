from django.urls import path
from . import views
from store.views import *
from django.conf.urls import include

urlpatterns = [
    path('register-merchant/', views.MerchantRegistration.as_view()),
    path('register-manager/', views.ManagerRegistration.as_view()),
    # path('activate/<uidb64>/<token>', views.ActivateAccountView.as_view(),name='activate'),
    path('register-clerk/', views.ClerkRegistration.as_view()),
    path('login/', views.UserLogin.as_view(), name='login'),
    path('api/merchant/', views.MerchantList.as_view(), name='merchant'),
    path('api/merchant/merchant-id/<pk>/', views.SoloMerchant.as_view()),
    path('api/manager/', views.ManagerList.as_view(), name='manger'),
    path('api/manager/manager-id/<int:pk>/', views.SoloManager.as_view()),
    path('api/manager/manager-id/activate/<int:pk>/', views.SoloActivateManager.as_view()),
    path('api/clerk/', views.ClerkList.as_view()),
    path('api/clerk/clerk-id/activate/<int:pk>/', views.SoloActivateClerk.as_view()),
    path('api/clerk/clerk-id/<int:pk>/', views.SoloClerk.as_view()),
    path('api/product-batch/', views.ProductBatchList.as_view()),
    path('api/product-batch/<int:pk>/', ProductBatchDetail.as_view(), name='shops'),
    path('api/shop/', ShopsList.as_view(), name='shops'),
    path('api/clerk/clerk-id/<pk>/', views.SoloClerk.as_view()),
    path('api/items/', views.ItemList.as_view()),
    path('api/purchases/', views.PurchaseList.as_view()),
    path('api/sales/', views.SalesList.as_view()),
    path('api/product-batch/paid/<int:pk>/', views.PaymentStatus.as_view()),
    path('api/items/item-id/<int:pk>/', views.SoloItemDamage.as_view(), )
]