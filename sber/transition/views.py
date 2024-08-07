from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse_lazy, reverse                                                               
from django.views.generic import CreateView
from .forms import RegisterForm, TransitionForm
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from .models import UserProfile, TransferModel
from django import forms
from django.contrib.auth.decorators import login_required

# Create your views here.
def format_number(num):
    return f"{num:,}".replace(",", ".")

def index(request):
    users = User.objects.all()
    return render(request, 'index.html', {'all_users': users})

def logout_profile(request):
    logout(request)
    return redirect("/")

class RegistrationView(CreateView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('main')

class Login(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse('login_succes')

def add_userprofile(request):
    try:
        user_info = request.user.userprofile
    except User.userprofile.RelatedObjectDoesNotExist:
        user_model_profile = UserProfile(profile=request.user)
        user_model_profile.save()
    return HttpResponseRedirect(reverse('main'))

def profile_user(request, pk, other_pk):
    user_recipient = get_object_or_404(User, pk=pk)
    user_sender = get_object_or_404(User, pk=other_pk)
    money = None
    error = []
    try:
        user_recipient_info = user_recipient.userprofile
    except User.userprofile.RelatedObjectDoesNotExist:
        user_model_profile = UserProfile(profile=user_recipient)
        user_model_profile.save()
    form = TransitionForm(request.POST or None)
    if form.is_valid():
        money = form.cleaned_data.get('money')
        comm = form.cleaned_data.get('commentary')
        if (user_sender.userprofile.money-money) < 0:
            error = ["Недостаточно средств для перевода", f"Максимально сумма для перевода: {user_sender.userprofile.money}"]
        else:
            transfer_obj = TransferModel(user=user_sender, other_user=user_recipient, commentary=comm, translation_money=money)
            transfer_obj.save() 
            user_sender.userprofile.transition.add(transfer_obj)
            user_recipient_info.transition.add(transfer_obj)
            user_recipient.save()
            user_sender.save()
            user_sender.userprofile.money = user_sender.userprofile.money - money
            user_sender.userprofile.profile = user_sender
            user_sender.userprofile.save()
            user_recipient.userprofile.money = user_recipient.userprofile.money + money
            user_recipient.userprofile.profile = user_recipient
            user_recipient.userprofile.save()
    money_all = format_number(user_recipient.userprofile.money)

    money = format_number(money) if money else money

    return render(request, 'user_profile.html', {'money': money_all, 'user_info': user_recipient.userprofile, 'form': form, 'MoneyError': error, 'transaction_money': money})   

def transactions(request):
    user = request.user
    new_transitions = []
    for i in user.userprofile.transition.all():
        if user == i.user:
            if i.read_status_sender == False:
                new_transitions.append(i)
                i.read_status_sender = True
                i.save()
        elif user == i.other_user:
            if i.read_status_recipient == False:
                new_transitions.append(i)
                i.read_status_recipient = True
                i.save()
    return render(request, 'user_transactions.html', {'user_transition': user.userprofile.transition, 'user_transition_new': new_transitions}) 

