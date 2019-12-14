from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=20, unique=True)
    parentCategory = models.ForeignKey(
        'self', blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Account(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Genders(models.TextChoices):
        MALE = 'M', _('Male')
        FEMALE = 'F', _('Female')

    gender = models.CharField(
        max_length=1,
        choices=Genders.choices
    )
    creationDate = models.DateTimeField(auto_now_add=True)
    phone = models.IntegerField(blank=True)
    balance = models.FloatField(default=1000)

    def __str__(self):
        return self.user.username


class TransactionHistory(models.Model):
    accountID = models.ForeignKey(Account, on_delete=models.CASCADE)
    changeAmount = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)


class Seller(Account):
    rating = models.IntegerField(default=5)


class Customer(Account):
    pass


class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    categoryID = models.ForeignKey(
        Category, on_delete=models.CASCADE)
    price = models.FloatField()
    quantity = models.IntegerField(blank=True, default=0)
    sellerID = models.ForeignKey(Seller, on_delete=models.CASCADE)
    dateAdded = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    productID = models.ForeignKey(Product, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='product_images/')


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    dateAdded = models.DateTimeField(auto_now_add=True)


class Deal(models.Model):
    percentage = models.IntegerField()
    description = models.TextField(max_length=250)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stars = models.IntegerField
    text = models.TextField(max_length=250)
    reviewer = models.ForeignKey(Account, on_delete=models.CASCADE)
    wasBought = models.BooleanField()


class ReviewImages(models.Model):
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    image = models.TextField(max_length=20, default='')


class ReviewRating(models.Model):
    helpful = models.BooleanField()
    by = models.ForeignKey(Account, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)


class Address(models.Model):
    house = models.TextField(max_length=30)
    street = models.TextField(max_length=30)
    city = models.TextField(max_length=30)
    country = models.TextField(max_length=30)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)


class Question(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    by = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    by = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField(max_length=250)


class AnswerRating(models.Model):
    helpful = models.BooleanField()
    by = models.ForeignKey(Account, on_delete=models.CASCADE)
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
