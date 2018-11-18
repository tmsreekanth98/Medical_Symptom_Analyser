from django import forms

#Form to take year of birth and gender to display medical conditions
class InputForm(forms.Form):
	Year_of_Birth = forms.IntegerField()
	gender = forms.ChoiceField(choices=[(1,'Male'),(2,'Female')])