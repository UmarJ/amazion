from django import forms
from main.models import Product, Account, Category, ProductImage, Review
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100)
    description = forms.CharField(
        max_length=1000)
    quantity = forms.IntegerField(initial=0)
    categoryID = forms.CharField(max_length=20)
    price = forms.DecimalField()

    class Meta:
        model = Product
        fields = ('name', 'description', 'quantity', 'categoryID', 'price')

    def clean(self):
        cleaned_data = super(ProductForm, self).clean()
        cleaned_data['categoryID'] = Category.objects.get(
            name=cleaned_data['categoryID'])


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('gender',)


class ImageForm(forms.ModelForm):
    picture = forms.ImageField()

    class Meta:
        model = ProductImage
        fields = ('picture',)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('stars', 'text')
