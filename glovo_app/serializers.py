from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('username', 'email', 'password', 'first_name', 'last_name',
                  'phone_number')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError('Неверные учетные данные')

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class UserProfileSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username']


class UserProfileReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_name']


class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['contact_info']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_image', 'price', 'description']


class ProductCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['product_name', 'description', 'price', 'store', 'product_image', ]


class ProductDetailUpdateDeleteAPIView(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_name', 'product_image', 'price', 'description', 'store']


class ProductComboSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCombo
        fields = ['combo_name', 'combo_image', 'price', 'description']


class ProductCreateComboSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductCombo
        fields = ['combo_name', 'description',
                  'price', 'combo_image']


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class CourierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Courier
        fields = '__all__'


class StoreReviewSerializer(serializers.ModelSerializer):
    created_date = serializers.DateTimeField(format('%d-%m-%Y %H:%M'))
    client = UserProfileReviewSerializer()

    class Meta:
        model = StoreReview
        fields = ['client', 'rating', 'comment', 'created_date']


class CourierReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourierReview
        fields = '__all__'


class StoreListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    avg_rating = serializers.SerializerMethodField()
    total_people = serializers.SerializerMethodField()
    check_good = serializers.SerializerMethodField()

    class Meta:
        model = Store
        fields = ['id', 'store_name', 'store_image', 'category', 'avg_rating', 'total_people', 'check_good']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_total_people(self, obj):
        return obj.get_total_people()

    def get_check_good(self, obj):
        return obj.get_check_good()


class StoreDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    owner = UserProfileSimpleSerializer()
    contacts = ContactInfoSerializer(many=True, read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    combos = ProductComboSerializer(many=True, read_only=True)
    store_reviews = StoreReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Store
        fields = ['id', 'store_name', 'store_image', 'category', 'description', 'address', 'owner', 'contacts',
                  'products', 'combos', 'store_reviews', ]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_name', 'store_image', 'category', 'description', 'address', 'owner']


class StoreDetailUpdateDeleteAPIView(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['store_name', 'store_image', 'category', 'description', 'address', 'owner']
