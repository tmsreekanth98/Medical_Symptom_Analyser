from django import forms

#Form to take year of birth and gender to display medical conditions
# class InputForm(forms.Form):
# 	Year_of_Birth = forms.IntegerField()
# 	gender = forms.ChoiceField(choices=[(1,'Male'),(2,'Female')])


class LoginForm(forms.Form):
	username=forms.CharField(max_length=20)
	password=forms.CharField(max_length=50,widget=forms.PasswordInput)




class RegisterForm(forms.Form):
	username=forms.CharField(max_length=20)
	password=forms.CharField(max_length=50,widget=forms.PasswordInput)
	password_repeat=forms.CharField(max_length=50,widget=forms.PasswordInput)