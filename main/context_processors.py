from main.forms import UserForm, AccountForm


def add_user_form(request):
    return {
        'user_form': UserForm()
    }


def add_account_form(request):
    return {
        'account_form': AccountForm()
    }
