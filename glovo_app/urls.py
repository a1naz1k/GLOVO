from django.urls import path, include
from .views import *
from rest_framework import routers


router = routers.SimpleRouter()
router.register(r'user', UserProfileViewSet, basename='users')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'combos', ProductComboViewSet, basename='combos')
router.register(r'cart', CartViewSet, basename='cart_list')
router.register(r'cart_item', CartItemViewSet, basename='cart_items')
router.register(r'store_review', StoreReviewViewSet, basename='store_review')
router.register(r'courier_review', CourierReviewViewSet, basename='courier_review')
router.register(r'order', OrderViewSet, basename='order')
router.register(r'courier', CourierViewSet, basename='courier')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('', include(router.urls)),
    path('store/', StoreListAPIView.as_view(), name='store_list'),
    path('store/<int:pk>/', StoreDetailAPIView.as_view(), name='store_detail'),
    path('create/', StoreCreateAPIView.as_view(), name='store_create'),
    path('product/', ProductListAPIView.as_view(), name='product_list'),
    path('create_product/', ProductCreateAPIView.as_view(), name='product_create'),
    path('create_product/<int:pk>', ProductDetailUpdateDeleteAPIView.as_view(), name='product_create'),
    path('add_product_combo', ProductComboCreateAPIView.as_view(), name='product_combo_create'),
    path('add_product_combo/<int:pk>', ProductComboDetailUpdateDeleteAPIView.as_view(), name='product_combo_edit')

]
