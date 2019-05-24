from django.shortcuts import render
from django.contrib.auth import login,authenticate
from Registration.forms import LoginForm,RegisterForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect



def check_password(password,password_repeat):
	if password == password_repeat:
		return True
	else:
		return False


def register(req):
	error=""

	if req.user.is_authenticated:
		return HttpResponseRedirect('../../symptom/')

	if req.method == 'POST':
		form = RegisterForm(req.POST)

		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			password_repeat = form.cleaned_data['password_repeat']

			if check_password(password,password_repeat):
				new_user = User.objects.create_user(username=username,password=password)
				new_user.save()
				new_user = authenticate(req,username=username,password=password)

				if new_user is not None:
					login(req, new_user)

				return HttpResponseRedirect('../../symptom/')
			else:
				error = "Passwords entered do not match!"

	else:
		form = RegisterForm()



	return render(req,'registration/register.html',{'form':form,'error':error})