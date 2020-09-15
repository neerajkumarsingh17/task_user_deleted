from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt


from django.contrib.auth import authenticate, login, logout

from django.contrib import messages

from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm

# Create your views here.

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		form = CreateUserForm()
		if request.method == 'POST':
			form = CreateUserForm(request.POST)
			if form.is_valid():
				form.save()
				return redirect('login')
			
		context = {'form':form}
		return render(request, 'accounts/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password =request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		context = {}
		return render(request, 'accounts/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def home(request):
    user_list = User.objects.values('username')
    context = {'user_list':user_list}
    return render(request, 'accounts/dashboard.html', context)


@csrf_exempt
def delete_user(request):
    try:
        import pdb; pdb.set_trace()
        # if request.is_ajax():
        #     # extract your params (also, remember to validate them)
        # 	param = request.POST.get('param', None)
		# find_user = User.objects.get(username=param)
		# find_user.delete()
		# messages.success(request, "The user is deleted")
    except User.DoesNotExist:
        messages.error(request, "User Doesnot exist")
        return redirect('home')
    except Exception as e:
        messages.error(request, e.message)
    return redirect('home')
