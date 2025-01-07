from django_filters import FilterSet
from .models import Product, Store, ProductCombo


class StoreFilter(FilterSet):
    class Meta:
        model = Store
        fields = {
            'category': ['exact'],
        }


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            'price': ['gt', 'lt'],
        }


class ProductComboFilter(FilterSet):
    class Meta:
        model = ProductCombo
        fields = {
            'price': ['gt', 'lt'],
        }
