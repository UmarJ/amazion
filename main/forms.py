from django import forms
from main.models import Product, Account, Category, ProductImage
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100, help_text="Enter Product name: ")
    description = forms.CharField(
        max_length=1000, help_text="Enter Description: ")
    quantity = forms.IntegerField(initial=0, help_text="Enter Quantity: ")
    categoryID = forms.CharField(max_length=20, help_text="Enter Category: ")
    price = forms.DecimalField(help_text="Enter Price: ")

    class Meta:
        model = Product
        fields = ('name', 'description', 'quantity', 'categoryID')

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
