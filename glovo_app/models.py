from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField


class UserProfile(AbstractUser):
    phone_number = PhoneNumberField(region='KG', null=True, blank=True)
    ROLE_CHOICES = (
        ('клиент', 'клиент'),
        ('курьер', 'курьер'),
        ('владелец', 'владелец'),
    )
    user_role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='клиент')

    def __str__(self):
        return f'{self.first_name}, {self.last_name}'


class Category(models.Model):
    category_name = models.CharField(max_length=16, unique=True)

    def __str__(self):
        return f'{self.category_name}'


class Store(models.Model):
    store_name = models.CharField(max_length=64)
    store_image = models.ImageField(upload_to='store_images/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=64)
    owner = models.ForeignKey(UserProfile, related_name="stores", on_delete=models.CASCADE)
    avg_rating = models.FloatField(default=0)
    total_people = models.CharField(max_length=10, default='0+')
    check_good = models.CharField(max_length=10, default='0%')

    def __str__(self):
        return self.store_name

    def get_avg_ratings(self):
        ratings = self.store_reviews.all()
        if ratings.exists():
            return round(sum(i.rating for i in ratings) / ratings.count(), 1)
        return 0
    # рточо маанисин табат

    def get_total_people(self):
        ratings = self.store_reviews.all()
        if ratings.exists():
            if ratings.count() > 3:
                return f'3+'
            return ratings.count()
        return 0
# если рейтингдер бар болсо жана алардын саны 3тон коп болсо 3 + деп чыгарат
# если рейтингдер 3 же андан аз болсо так сандарды чыгарат
# если рейтинг жок болсо анда 0ду чыгарып берет

    def get_check_good(self):
        ratings = self.store_reviews.all()
        if ratings.exists():
            num = 0
            for i in ratings:
                if i.rating > 3:
                    num += 1
            return f'{round((num * 100) / ratings.count())}%'
        return f'0%'

# Эгерде рейтингдер бар болсо, ал 3төн жогору рейтингдердин санын эсептеп, андан кийин ошол санды жалпы рейтингдердин санына бөлүп, пайызын чыгарат.
# Эгерде рейтингдер жок болсо, анда 0% кайтарат.


class ContactInfo(models.Model):
    contact_info = PhoneNumberField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='contacts')

    def __str__(self):
        return f'{self.store}, {self.contact_info}'


class Product(models.Model):
    store = models.ForeignKey(Store, related_name="products", on_delete=models.CASCADE)
    product_name = models.CharField(max_length=64)
    product_image = models.ImageField(upload_to='store_images/', blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.product_name}'


class ProductCombo(models.Model):
    combo_name = models.CharField(max_length=32, unique=True)
    combo_image = models.ImageField(upload_to='combo_images')
    price = models.PositiveSmallIntegerField()
    description = models.TextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='combos')

    def __str__(self):
        return f'{self.combo_name}, {self.store}'


class Cart (models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name='cart')

    def __str__(self):
        return f'{self.user}'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,  related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self):
        return f'{self.product}, {self.quantity}'


class Order (models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ('Ожидает обработки', 'Ожидает обработки'),
        ('В процессе доставки', 'В процессе доставки'),
        ('Доставлено', 'Доставлено'),
        ('Отменено', 'Отменено'),
    )
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default='Ожидает обработки')
    delivery_address = models.CharField(max_length=64)
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_orders')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.status}, {self.courier}'


class Courier(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier')
    current_orders = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orders')
    TYPE_STATUS_CHOICES = (
        ('занят', 'занят'),
        ('доступен', 'доступен')
    )
    status = models.CharField(max_length=16, choices=TYPE_STATUS_CHOICES)

    def __str__(self):
        return f'{self.user}, {self.status}'


class StoreReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='store_reviews')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    comment = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.client}, {self.store}, {self.rating}'


class CourierReview(models.Model):
    client = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='client_review')
    courier = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='courier_review')
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.courier}, {self.rating}'


class Chat(models.Model):
    person = models.ManyToManyField(UserProfile)
    created_date = models.DateTimeField(auto_now_add=True)


class Massage(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    video = models.ImageField(upload_to='videos', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
