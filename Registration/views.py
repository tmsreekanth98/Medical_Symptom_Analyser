from django.shortcuts import render
from django.contrib.auth import login,authenticate
from Registration.forms import LoginForm
from django.contrib.auth.models import User

def homepage(req):

	context={'login_status':0,'form':LoginForm()}

	if req.method == 'POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			print("---")
			username=form.cleaned_data['username']
			password=form.cleaned_data['password']
			u=User.objects.create_user(username=username,password=password)
			u.save()
			user=authenticate(req,username=username,password=password)
			print("---------"+str(user.username))
			if user is not None:
				login(req,user)
				context['login_status']=1
				return redirect('symptom/')


	else:
		form=LoginForm()


	return render(req,'Registration/index.html',context)