from django.shortcuts import render,redirect
import requests
import hmac
from hashlib import md5
import base64
import ast,json
from .models import Symptoms,Issue
from Med.forms import InputForm
from django.contrib.auth.decorators import login_required


def getAuthToken():
	# Authentication PART: To obtain Access Token

	END_POINT = 'https://sandbox-authservice.priaid.ch/login'
	API_KEY = 'tmsreekanth98@gmail.com'
	SECRET_KEY = 'q7T8Qzn3BSk6j2YWt'
	
	#Authorization header as per API documentation
	AUTH_HEADER = 'Bearer tmsreekanth98@gmail.com:2XmUO5zQED3gMqFxfLXMdQ=='

	headers = {
		'Authorization':AUTH_HEADER,
	}

	#Sending the post request and parsing token from response
	r = requests.post(url=END_POINT,data={},headers=headers)
	ACCESS_TOKEN = r.json().get("Token")

	return ACCESS_TOKEN





@login_required
def home(request):

	#Sending POST request to obtain list of medical symptoms when the homepage loads up

	#Obtaining Access token

	ACCESS_TOKEN = getAuthToken()

	SYMPTOMS_END_POINT = 'https://sandbox-healthservice.priaid.ch/symptoms?token='+ACCESS_TOKEN+'&language=en-gb'
	r = requests.get(url=SYMPTOMS_END_POINT,params={})

	symptom_list = r.json()

	# s_dict will store the symptoms as a dictionary of elements with ID and Name of the symptom.
	s_dict={}

	#clear the table
	Symptoms.objects.all().delete()

	for x in symptom_list:
		s_dict[x['ID']]=x['Name']
		sy = Symptoms()
		sy.symptom_id=x['ID']
		sy.symptom_desc=x['Name']
		sy.save()

	return render(request,'Med/index.html',{'symptom_list':s_dict})




@login_required
def symptom_page(request,symptom_id):

	#Form data handling for year of birth and gender
	if request.method=='POST':
		form = InputForm(request.POST)
		if form.is_valid():
			YOB=form.cleaned_data['Year_of_Birth']
			gender=form.cleaned_data['gender']
			return redirect('diagnosis/'+str(YOB)+'/'+gender+'/')
	else:
		form = InputForm()

	try:
		symptom_desc=Symptoms.objects.get(symptom_id=symptom_id)
	except:
		symptom_desc="Symptom does not exist!"
	return render(request,'Med/details.html',{'symptom_id':symptom_id,'symptom_desc':symptom_desc,'form':form})





@login_required
def symptom_diagnosis(request,symptom_id,yob,gender):

	#Calling diagnosis API to retrieve the possible diagnosis

	ACCESS_TOKEN = getAuthToken()
	
	gc=''

	if int(gender) == 1:
		gc='Male'
	if int(gender) == 2:
		gc='Female'


	DIAGNOSIS_END_POINT = 'https://sandbox-healthservice.priaid.ch/diagnosis?token='+ACCESS_TOKEN+'&language=en-gb&symptoms=['+symptom_id+']&gender='+gc+'&year_of_birth='+yob

	r = requests.get(url=DIAGNOSIS_END_POINT,params={})
	diagnosis_list=r.json()

	#Calling issue info API for Treatment Options

	ct=0
	treatment_desc=[]

	for x in diagnosis_list:
		issue_id = x["Issue"]["ID"]
		ct=ct+1;

		try:
			#If issue is found in database we can directly fetch it from the table to display treatment options.
			issue_object = Issue.objects.get(issue_id=issue_id)
			x["Issue"]["TreatmentDescription"]=issue_object.treatment_details

		except:
			#If issue is not in the database we need to request it from the API
			ISSUE_INFO_ENDPOINT = 'https://sandbox-healthservice.priaid.ch/issues/'+ str(issue_id) +'/info?token='+ACCESS_TOKEN+'&language=en-gb'
			r2 = requests.get(url=ISSUE_INFO_ENDPOINT,params={})
			issue_info_list = r2.json()
			td = issue_info_list["TreatmentDescription"]
			x["Issue"]["TreatmentDescription"]=td

			#storing the obtained information into Issue table
			iss = Issue()
			iss.issue_id = issue_id
			iss.issue_name = x["Issue"]["Name"]
			iss.issue_profName = x["Issue"]["ProfName"]

			ct2=1
			for y in x["Specialisation"]:
				if ct2==1:
					iss.specialist_one = y["Name"]
				if ct2==2:
					iss.specialist_two = y["Name"]
				if ct2==3:
					iss.specialist_three = y["Name"]
				ct2=ct2+1;

			iss.treatment_details = td 
			iss.save()
		


	return render(request,'Med/diagnosis.html',{'diagnosis_list':diagnosis_list})




@login_required
def treatment(request,issue_id,lat,lon):
	#Obtaining the issue object corresponding to the issue id of the URL
	issue_object = Issue.objects.get(issue_id=issue_id)

	#Alternate Google places API key: AIzaSyAfUA3v46Q3PfeMAnzc4rPYw2Zk0VImGE8

	DOCTOR_ENDPOINT = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location='+ lat +','+ lon +'&radius=5000&type=doctor&keyword='+ issue_object.specialist_two +'&key=AIzaSyBKFKov5f5YoSDRnWrT3y7MFf9DfsdRgCg'

	r=requests.get(url=DOCTOR_ENDPOINT,params={})
	doctor_list = r.json()

	#To store the required details for a doctor fetched from Google API
	req_doc_details={}
	req_doc_details_total=[]

	ct=1;
	for x in doctor_list["results"]:
		#We will only pass first 3 doctor results to the template
		if ct==4:
			break;
		req_doc_details["name"]=x["name"]
		req_doc_details["vicinity"]=x["vicinity"]
		req_doc_details["rating"]=x["rating"]
		req_doc_details_total.append(req_doc_details)
		req_doc_details={}
		ct=ct+1;


	return render(request,'Med/treatment.html',{'issue_object':issue_object,'req_doc_details_total':req_doc_details_total})