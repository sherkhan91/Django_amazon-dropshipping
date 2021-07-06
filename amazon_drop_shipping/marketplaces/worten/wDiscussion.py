import requests
from bs4 import BeautifulSoup
from urllib3 import ProxyManager, PoolManager
import time
import json
import xmltodict
import os
import pathlib
import sys
parentsDirectory = pathlib.Path(__file__).parent.parent.parent.absolute()
# print("parent: ",parentsDirectory)
sys.path.append(str(parentsDirectory))
from database import DatabaseQueries
from utils import MarketPlaceUtils
from constant import Constants


class WortenDiscussions():

	def __init__(self, logger):
		# os.system("clear")
		# os.system("clear")
		self.logger = logger
		self.Queries = DatabaseQueries(logger=self.logger)
		self.proxysetting = {'http': 'http://user:password@45.33.152.117:21242',
						'https': 'https://user:password@45.33.152.117:21242',
						'ftp': 'ftp://user:password@45.33.152.117:21242'}

	def worten_mock_discussions(self):
		data = 	'''
		{
		  "data" : [ {
		    "authorized_participants" : [ {
		      "display_name" : "Shop display name",
		      "id" : "Shop id",
		      "type" : "SHOP"
		    }, {
		      "display_name" : "Customer display name",
		      "id" : "Customer id",
		      "type" : "CUSTOMER"
		    } ],
		    "current_participants" : [ {
		      "display_name" : "Shop display name",
		      "id" : "Shop id",
		      "type" : "SHOP"
		    }, {
		      "display_name" : "Customer display name",
		      "id" : "Customer id",
		      "type" : "CUSTOMER"
		    } ],
		    "date_created" : "2016-09-03T13:37:00Z",
		    "date_updated" : "2018-09-03T13:37:00Z",
		    "entities" : [ {
		      "id" : "Order_00010-A",
		      "label" : "Entity label",
		      "type" : "MMP_ORDER"
		    } ],
		    "id" : "random id",
		    "metadata" : {
		      "last_message_date" : "2018-09-03T13:37:00Z",
		      "total_count" : 2
		    },
		    "topic" : {
		      "type" : "FREE_TEXT",
		      "value" : "Topic value"
		    }
		  } ],
		  "next_page_token" : "bGltaXQ9NTAmYWZ0ZXI9MjA3NjYwNTAtZDc5Yy00YzUyLWEwODctZWI5YjY1MjFkNzA5JnNvcnQ9ZGF0ZSxERVND"
		}
		'''
		return data
	
	#TODO: remove this function!
	def doaprintfaltu(self):
		print("just adding these lines to see change on git")

	#TODO: remove this function!
	def tryexceptfaltu(self):
		print("this is a blah blah print function")

	def retrieveThreadWorten(self, threadID):

		data = '''{
					"authorized_participants" : [],
					"current_participants" : [ {
						"display_name" : "Shop display name",
						"id" : "Shop id",
						"type" : "SHOP"
					}, {
						"display_name" : "Customer display name",
						"id" : "Customer id",
						"type" : "CUSTOMER"
					} ],
					"date_created" : "2018-10-02T08:36:36.479Z",
					"date_updated" : "2018-10-03T09:40:17.241Z",
					"entities" : [ {
						"id" : "Entity id",
						"label" : "Entity label",
						"type" : "Entity type"
					} ],
					"id" : "702c3e56-dcca-41e2-b6bd-72ba3fa809be",
					"messages" : [ {
						"body" : "Hello, I have recently order a service and I have a few questions ...",
						"date_created" : "2018-10-02T08:36:36.479Z",
						"from" : {
						"display_name" : "Customer display name",
						"type" : "CUSTOMER_USER"
						},
						"id" : "df4a3163-a44b-4c5f-8380-faebfa43ca68",
						"to" : [ {
						"display_name" : "Shop display name",
						"id" : "Shop id",
						"type" : "SHOP"
						} ]
					}, {
						"attachments" : [ {
						"id" : "fce1742e-8160-45ed-b88a-100023d9d97b",
						"name" : "Brochure du service",
						"size" : 200
						}, {
						"id" : "983fd83f-0b39-4bdf-9932-bd774ab66ce4",
						"name" : "Tarif",
						"size" : 10
						} ],
						"body" : "Dear customer, ...",
						"date_created" : "2018-10-03T09:40:17.241Z",
						"from" : {
						"display_name" : "Shop user display name",
						"organization_details" : {
							"display_name" : "Shop display name",
							"id" : "Shop id",
							"type" : "SHOP"
						},
						"type" : "SHOP_USER"
						},
						"id" : "d752f26f-03eb-499c-8f4d-828fa9640055",
						"to" : [ {
						"display_name" : "Customer display name",
						"id" : "Customer id",
						"type" : "CUSTOMER"
						} ]
					} ],
					"metadata" : {
						"last_message_date" : "2018-10-03T09:40:17.241Z",
						"total_count" : 2
					},
					"topic" : {
						"type" : "FREE_TEXT",
						"value" : "Questions about my order"
					}
					}'''
		return data

	def mDiscussions(self, shopkey,proxy):

		response = ''
		

		payload={}
		headers = {
		  'Authorization': shopkey,
		  'Accept': 'application/json'
		}

		if proxy is not None:
			response =  requests.request("GET",Constants.worten_discussions, headers=headers, data=payload, proxies=proxy) 
		else:
			response = requests.request("GET", Constants.worten_discussions, headers=headers, data=payload)

		# print("here is response: ", response.text)

		print("Worten Discussions")
		mock_response =  self.worten_mock_discussions()
		# resp_json = json.loads(response.text)  # uncomment this line when real data comes
		resp_json = json.loads(mock_response)

		for discussion_sequence in range(len(resp_json['data'])):
			subject =  resp_json['data'][discussion_sequence]['topic']['type'] 
			disccussion_id = resp_json['data'][discussion_sequence]['id'] 
			status = 'N/A'
			marketplace_order_number = resp_json['data'][discussion_sequence]['entities'][0]['id']
			marketplace = 'WORTEN'
			date_created =  resp_json['data'][discussion_sequence]['date_created']
			date_created =  date_created[0:4]+"-"+date_created[5:7]+"-"+date_created[8:10]
			date_updated = resp_json['data'][discussion_sequence]['date_updated']
			date_updated = date_updated[0:4]+"-"+date_updated[5:7]+"-"+date_updated[8:10]
			self.Queries.saveDiscussions(subject,disccussion_id,status,marketplace_order_number,marketplace,date_created,date_updated)
				
			# TODO: Need to change and test on actual response 
			thread_response = self.retrieveThreadWorten(marketplace_order_number) 
			message_json = json.loads(str(thread_response))

			for message in message_json['messages']:
				disccussion_id = resp_json['data'][discussion_sequence]['id']  #(reference to DISCUSSIONS TABLE)
				content = message['body'] 
				sender =  message['from']['type']
				if sender == 'CUSTOMER_USER':
					sender = 'BUYER'
				else:
					sender = 'SELLER'
				mtimestamp = message['date_created'][0:10]  
				message_id = message['date_created'] 
				self.Queries.saveMessage(disccussion_id,content,sender,mtimestamp,message_id)
			
'''uncomment the following for testing individually '''

# if __name__ == '__main__':
# 	myDiscussions = WortenDiscussions()
# 	myDiscussions.mDiscussions()
