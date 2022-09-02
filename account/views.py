from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from account.forms import SignUpForm
from account.models import Profile


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')

            user = authenticate(request, username=username, password=password)
            login(request, user)
            Profile.objects.create(user=user)

            return HttpResponse('yes')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'account/sign_up.html', context)


def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is None:
            context['error'] = 'username or password is wrong'
            return render(request, 'account/login.html', context)
        else:
            login(request, user)
            return HttpResponse('yes')
    else:
        return render(request, 'account/login.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))


def table_view(request):
    record1 = Profile.objects.all().order_by('-best_record')[:10]
    record2 = Profile.objects.all().order_by('-best_record2')[:10]
    return render(request, 'account/table.html', {'record1': record1, 'record2': record2})
