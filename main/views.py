from django.shortcuts import render
from main.forms import ProductForm, UserForm, AccountForm, ImageForm
from main.models import Seller, User, Product
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, 'index.html')


def productDetails(request, product_id_slug):
    product = Product.objects.get(id=product_id_slug)
    context_dict = {'name': product.name,
                    'description': product.description,
                    'price': product.price,
                    'seller_name': product.sellerID
                    }
    return render(request, 'product.html', context=context_dict)


def add_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        image_form = ImageForm(request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.sellerID = Seller.objects.get(
                user=User.objects.get(username='project'))
            product.save()
            print('lmao')

            if image_form.is_valid():
                print('ayyy')
                image = form.save(commit=False)
                image = image.productID = product
                image.save()
            return HttpResponseRedirect(reverse('index'))

        else:
            print(form.errors)
    return render(request, 'add_product.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        account_form = AccountForm(data=request.POST)

        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            account = account_form.save(commit=False)
            account.user = user
            account.save()

        else:
            print(user_form.errors, account_form.errors)
    else:
        user_form = UserForm()
        account_form = AccountForm()
    return render(request, 'index.html')


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    return HttpResponse("Invalid Credentials")
