
import json
from rest_framework.views import APIView
from rest_framework.response import Response

api_key = 'bd03e598-252e-11e9-9ee8-0200cd936042'

class SendOtp(APIView,api_key):

	def __init__(self,phone_number):
		self.phone_number	=phone_number

	def get(self, request, format=None):
		url = 'https://2factor.in/API/V1/'+{api_key}+'/SMS/'+{self.phone_number}+'/AUTOGEN'
		req = request.get(url)
		



