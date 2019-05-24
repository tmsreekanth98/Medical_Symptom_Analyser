from django.db import models

# Create your models here.

#Symptoms table to store symptom description and ID
class Symptoms(models.Model):
	symptom_id=models.IntegerField()
	symptom_desc=models.CharField(max_length=150)

	def __str__(self):
		return self.symptom_desc



#Issue table to store details related to a particular issue
class Issue(models.Model):
	issue_id=models.IntegerField()
	issue_name=models.CharField(max_length=100)
	issue_profName=models.CharField(max_length=200)
	specialist_one=models.CharField(max_length=100)
	specialist_two=models.CharField(max_length=100)
	specialist_three=models.CharField(max_length=100)
	treatment_details=models.CharField(max_length=2000)

	#User pinned issue notes
	notes=models.CharField(max_length=200,default="")
	
	def __str__(self):
		return str(self.issue_id)