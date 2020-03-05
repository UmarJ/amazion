from django.shortcuts import render
from main.forms import ProductForm, UserForm, AccountForm, ImageForm, ReviewForm
from main.models import User, Product, ProductImage, Account, Review, Cart, Transaction
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.generic.detail import DetailView


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


@login_required
def add_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        image_form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.sellerID = Account.objects.get(
                user=request.user)
            product.save()
            image = image_form.save(commit=False)
            image.productID = product
            image.save()
            return HttpResponseRedirect(reverse('product-detail', kwargs={'pk': product.id}))

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
    return HttpResponseRedirect(reverse('index'))


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
    return HttpResponse("Invalid Credentials")


class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)

        context['image'] = ProductImage.objects.get(
            productID=context.get('object').id)
        return context


def account_info(request):
    return render(request, 'account.html')


def review(request, product_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.reviewer = Account.objects.get(user=request.user)
            review.wasBought = True
            review.product_id = product_id
            review.save()
        else:
            print(form.errors)
        return HttpResponseRedirect(reverse('review', kwargs={'product_id': product_id}))

    else:
        context_dict = {
            'product': Product.objects.get(id=product_id),
            'reviews': Review.objects.filter(product_id=product_id),
            'range': {0, 1, 2, 3, 4}
        }
        return render(request, 'review.html', context=context_dict)


def add_to_cart(request, product_id):
    if request.method == 'POST':
        cartItem = Cart(customer=Account.objects.get(
            user=request.user), product=Product.objects.get(id=product_id))
        cartItem.save()
        return HttpResponseRedirect(reverse('show-cart'))


def remove_from_cart(request, product_id):
    if request.method == 'POST':
        Cart.objects.filter(customer=Account.objects.get(
            user=request.user), product=Product.objects.get(id=product_id)).delete()
        return HttpResponseRedirect(reverse('show-cart'))


def show_cart(request):
    cart = Cart.objects.filter(
        customer_id=Account.objects.get(user=request.user))
    products = []
    price = 0
    for item in cart:
        product = Product.objects.get(id=item.product_id)
        products.append(Product.objects.get(id=item.product_id))
        price += product.price

    context_dict = {
        'items': products,
        'total': price
    }
    return render(request, 'cart.html', context=context_dict)


def checkout(request):
    if request.method == 'POST':
        cart = Cart.objects.filter(
            customer_id=Account.objects.get(user=request.user))
        price = 0
        for item in cart:
            product = Product.objects.get(id=item.product_id)
            product.quantity -= 1
            product.save()
            price += product.price
            print(price)
            transaction = Transaction(
                accountID=product.sellerID, changeAmount=(product.price))
            transaction.save()
        transaction.save()
        currentAccount = Account.objects.get(user=request.user)
        currentAccount.balance -= price
        currentAccount.save()
        cart.delete()
        transaction = Transaction(accountID=Account.objects.get(
            user=request.user), changeAmount=(-price))
        transaction.save()
        return HttpResponse("Items Purchased")


def transactions(request):
    transactions = Transaction.objects.filter(
        accountID=Account.objects.get(user=request.user))
    context_dict = {
        'transactions': transactions,
    }
    return render(request, 'transactions.html', context=context_dict)


def search(request, search_query):
    products = Product.objects.filter(
        name__icontains=search_query)
    context_dict = {
        'items': products,
        'query': search_query
    }
    return render(request, 'results.html', context=context_dict)
