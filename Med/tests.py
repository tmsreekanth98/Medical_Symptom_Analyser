from django.test import TestCase
from Med.models import Symptoms,Issue
from django.urls import reverse
from Med.forms import InputForm


#Unit tests


class MedTest(TestCase):

	####################### TESTS FOR MODELS ############################

	def create_symptom(self,symptom_id=100,symptom_desc='Test Symptom Description'):
		return Symptoms.objects.create(symptom_id=symptom_id,symptom_desc=symptom_desc)

	#Testing of new entry creation in Symptom table
	def test_create_symptom(self):
		a = self.create_symptom()
		self.assertTrue(isinstance(a,Symptoms))
		self.assertEqual(a.__str__(),a.symptom_desc)

	def create_issue(self,issue_id=10,issue_name='Test Issue',issue_profName='Test Prof Name',specialist_one='Test Specialist',treatment_details='Test Treatment Details'):
		return Issue.objects.create(issue_id=issue_id,issue_name=issue_name,issue_profName=issue_profName,specialist_one=specialist_one,treatment_details=treatment_details)

	#Testing of new entry creation in Issue table
	def test_create_issue(self):
		a = self.create_issue()
		self.assertTrue(isinstance(a,Issue))
		self.assertEqual(a.__str__(),str(a.issue_id))


	####################### TESTS FOR VIEWS ############################

	def test_home_view(self):
		url = reverse('home')
		resp = self.client.get(url)
		#Checking whether the TestCase Client gets a 200 OK status while visiting the reversed URL
		self.assertEqual(resp.status_code,200)


	def test_symptom_page_view(self):
		a = self.create_symptom()
		url = reverse('symptom_page',args=[a.symptom_id])
		resp = self.client.get(url)
		#Checking the reversed URL with actual URL
		self.assertEqual(url,'/symptom/'+str(a.symptom_id)+'/')
		#Checking whether the TestCase Client gets a 200 OK status while visiting the reversed URL
		self.assertEqual(resp.status_code,200)
		#Checking whether the loaded content has symptom_desc in it
		self.assertIn(a.symptom_desc.encode(),resp.content)


	def test_symptom_diagnosis_view(self):
		a = self.create_symptom()
		url = reverse('symptom_diagnosis',args=[a.symptom_id,1998,1])
		resp = self.client.get(url)
		#Checking the reversed URL with actual URL
		self.assertEqual(url,'/symptom/'+str(a.symptom_id)+'/diagnosis/'+'1998'+'/1/')
		#Checking whether the TestCase Client gets a 200 OK status while visiting the reversed URL
		self.assertEqual(resp.status_code,200)


	def test_treatment_view(self):
		a = self.create_issue()
		url = reverse('treatment',args=[a.issue_id,10,10])
		resp = self.client.get(url)
		#Checking the reversed URL with actual URL
		self.assertEqual(url,'/treatment/'+str(a.issue_id)+'/10/10/')
		#Checking whether the TestCase Client gets a 200 OK status while visiting the reversed URL
		self.assertEqual(resp.status_code,200)
		#Checking whether the loaded content has symptom_desc in it
		self.assertIn(a.issue_name.encode(),resp.content)



	####################### TESTS FOR FORM ############################

	def test_InputForm_valid(self):
		data={'Year_of_Birth':'1998','gender':'1'}
		form = InputForm(data=data)
		self.assertTrue(form.is_valid())

	def test_InputForm_invalid(self):
		data={'Year_of_Birth':'','gender':'1'}
		form = InputForm(data=data)
		self.assertFalse(form.is_valid())