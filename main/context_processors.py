from main.forms import UserForm, AccountForm
from main.models import Account


def add_user_form(request):
    return {
        'user_form': UserForm()
    }


def add_account_form(request):
    return {
        'account_form': AccountForm()
    }


def add_balance(request):
    if request.user.is_authenticated:
        return {
            'balance': Account.objects.get(user=request.user).balance
        }
    else:
        return {
            'balance': 0
        }