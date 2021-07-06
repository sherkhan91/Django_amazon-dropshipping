from typing import Optional
from pydantic import BaseModel, EmailStr
import requests
import urllib.request as req
import urllib as urllib22
from urllib3 import ProxyManager, PoolManager
import json
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import time
import xmltodict 
import datetime
import logging
import os
import sys
import pathlib
import traceback
parentsDirectory = pathlib.Path(__file__).parent.parent.parent.absolute()
sys.path.append(str(parentsDirectory))
from database import DatabaseQueries
from utils import MarketPlaceUtils
from inspect import currentframe
from datetime import datetime, timedelta
from constant import Constants
from inspect import currentframe



class WortenOrder():
	
	def __init__(self, logger):
		os.system('clear')
		os.system('clear')
		self.logger = logger
		self.Queries = DatabaseQueries(logger=self.logger)
		self.Utils = MarketPlaceUtils()
		self.filename = self.get_filename()

	def logError(self, line, errorStr):
		''' Format for logging the error '''
		self.logger.logevent("File: "+str(self.filename)+ "  Line: "+str(line)+ "  Description: "+str(errorStr))


	def get_filename(self):
		''' for getting the file name for logger '''
		return sys.argv[0]

	#TODO: remove this function!
	def doaprintfaltu(self):
		print("just adding these lines to see change on git")

	#TODO: remove this function!
	def tryexceptfaltu(self):
		print("this is a blah blah print function")

	def get_line(self):
		''' for getting the line number for later logging  '''
		cf = currentframe()
		return str(cf.f_back.f_lineno)

	def formatDate(self,date_string):
		'''format date for worten '''
		return date_string[:10]

	#TODO: remove this function!
	def functionfaltu(self):
		faltu_string = "Display the given set of images, optionally with titles.images: list or array of image tensors in HWC format.."
	

	def worten_mock_data(self):
		mock_data = """{
				"orders": [{
					"acceptance_decision_date": "2019-04-02T14:56:01Z",
					"can_cancel": false,
					"can_shop_ship": false,
					"channel": {
						"code": "US",
						"label": "Website US"
					},
					"commercial_id": "Order_00010",
					"created_date": "2019-04-02T14:18:43Z",
					"currency_iso_code": "USD",
					"customer": {
						"billing_address": {
							"city": "New York",
							"civility": "M",
							"company": "simple customer",
							"country": "USA",
							"country_iso_code": "USA",
							"firstname": "smith",
							"lastname": "Taylor",
							"state": "manhattan",
							"street_1": "113 MacDougal Street",
							"street_2": "1st floor",
							"zip_code": "NY 10012"
						},
						"civility": "Mr",
						"customer_id": "Customer_id_001",
						"firstname": "Smith",
						"lastname": "Taylor",
						"locale": "fr_FR",
						"shipping_address": {
							"additional_info": "One article per box",
							"city": "New York",
							"civility": "M",
							"company": "simple customer",
							"country": "USA",
							"country_iso_code": "USA",
							"firstname": "Smith",
							"lastname": "Taylor",
							"state": "Manhattan",
							"street_1": "113 MacDougal Street",
							"street_2": "1st floor",
							"zip_code": "NY 10012"
						}
					},
					"customer_debited_date": "2019-04-02T14:58:22.460Z",
					"customer_notification_email": "notification+ec1riop21ju4rfynl0helvzou.e0z0r7cj2@notification.mirakl.net",
					"delivery_date": {
						"earliest": "2019-09-02T08:07:22.326Z",
						"latest": "2019-09-03T08:07:22.326Z"
					},
					"has_customer_message": false,
					"has_incident": false,
					"has_invoice": false,
					"last_updated_date": "2019-04-02T14:59:58Z",
					"leadtime_to_ship": 5,
					"order_additional_fields": [

					],
					"order_id": "Order_00010-A",
					"order_lines": [
                {
                    "can_refund": false,
                    "cancelations": [],
                    "category_code": "MG02011",
                    "category_label": "Figuras",
                    "commission_fee": 2.25,
                    "commission_rate_vat": 23.0000,
                    "commission_taxes": [
                        {
                            "amount": 0.52,
                            "code": "TAXDEFAULT",
                            "rate": 23.0000
                        }
                    ],
                    "commission_vat": 0.52,
                    "created_date": "2020-12-04T16:45:39Z",
                    "debited_date": null,
                    "description": null,
                    "last_updated_date": "2020-12-07T19:00:18Z",
                    "offer_id": 24999,
                    "offer_sku": "SKU0889698339797",
                    "offer_state_code": "11",
                    "order_line_additional_fields": [],
                    "order_line_id": "30638830-A-1",
                    "order_line_index": 1,
                    "order_line_state": "REFUSED",
                    "order_line_state_reason_code": "ACCEPTANCE_TIMEOUT",
                    "order_line_state_reason_label": "Automatically rejected",
                    "price": 15.02,
                    "price_additional_info": null,
                    "price_unit": 15.02,
                    "product_medias": [],
                    "product_sku": "fae80d05-57aa-40c5-93f0-5a15dbecf1b1",
                    "product_title": "Figura FUNKO Pop! Bobble: Marvel Man: Into the Spider-Verse: Green Goblin",
                    "promotions": [],
                    "quantity": 1,
                    "received_date": null,
                    "refunds": [],
                    "shipped_date": null,
                    "shipping_price": 0.00,
                    "shipping_price_additional_unit": null,
                    "shipping_price_unit": null,
                    "shipping_taxes": [],
                    "taxes": [],
                    "total_commission": 2.77,
                    "total_price": 15.02
                },
                {
                    "can_refund": false,
                    "cancelations": [],
                    "category_code": "MG0201",
                    "category_label": "Figuras",
                    "commission_fee": 2.25,
                    "commission_rate_vat": 23.0000,
                    "commission_taxes": [
                        {
                            "amount": 0.52,
                            "code": "TAXDEFAULT",
                            "rate": 23.0000
                        }
                    ],
                    "commission_vat": 0.52,
                    "created_date": "2020-12-04T16:45:39Z",
                    "debited_date": null,
                    "description": null,
                    "last_updated_date": "2020-12-07T19:00:18Z",
                    "offer_id": 24999,
                    "offer_sku": "SKU0889698339797",
                    "offer_state_code": "11",
                    "order_line_additional_fields": [],
                    "order_line_id": "30638830-A-2",
                    "order_line_index": 2,
                    "order_line_state": "REFUSED",
                    "order_line_state_reason_code": "ACCEPTANCE_TIMEOUT",
                    "order_line_state_reason_label": "Automatically rejected",
                    "price": 15.02,
                    "price_additional_info": null,
                    "price_unit": 15.02,
                    "product_medias": [],
                    "product_sku": "fae80d05-57aa-40c5-93f0-5a15dbecf1b1",
                    "product_title": "Figura FUNKO Pop! Bobble: Marvel Man: Into the Spider-Verse: Green Goblin",
                    "promotions": [],
                    "quantity": 1,
                    "received_date": null,
                    "refunds": [],
                    "shipped_date": null,
                    "shipping_price": 0.00,
                    "shipping_price_additional_unit": null,
                    "shipping_price_unit": null,
                    "shipping_taxes": [],
                    "taxes": [],
                    "total_commission": 2.77,
                    "total_price": 15.02
                }
            ],
					"order_state": "RECEIVED",
					"order_state_reason_code": null,
					"order_state_reason_label": null,
					"payment_type": "Visa",
					"payment_workflow": "PAY_ON_ACCEPTANCE",
					"price": 165,
					"promotions": {
						"applied_promotions": [

						],
						"total_deduced_amount": 0
					},
					"quote_id": null,
					"shipping_carrier_code": "UPS",
					"shipping_company": "UPS",
					"shipping_deadline": "2019-09-01T08:07:22.326Z",
					"shipping_price": 8,
					"shipping_pudo_id": "C1039",
					"shipping_tracking": "2344",
					"shipping_tracking_url": "https://wwwapps.ups.com/WebTracking/track?track=yes&trackNums=2344",
					"shipping_type_code": "STD",
					"shipping_type_label": "Standard",
					"shipping_zone_code": "INT1",
					"shipping_zone_label": "International 1",
					"total_commission": 21.3,
					"total_price": 173,
					"transaction_date": "2019-06-25T07:42:21.215Z",
					"transaction_number": "TR_MIR-PHHV83UB",
					"fulfillment": {
						"center": {
							"code": "FULFILLMENT_CENTER_CODE"
						}
					}
				}],
				"total_count": 1
			}"""

		return mock_data

	def parseWortenResponse(self,resp_json, catalog):
		''' api response json string will be parsed here '''
		order_status = 0
		product_price_array = []

		print("length of orders:",len(resp_json['orders']))

		for i in range(len(resp_json['orders'])):
			orderfirst = resp_json['orders'][i]
			for orderItem in orderfirst['order_lines']:
				marketplace_order_number =  orderfirst['order_id']
				ean = orderItem['offer_sku'][3:]
				asin = self.Queries.extractAsin(ean, catalog)
				amazon_price = None
				keepa_price = self.Queries.getKeepaPrice(ean, catalog)
				date_created =  self.formatDate(orderItem['created_date'])
				date_updated = self.formatDate(orderItem['last_updated_date'])
				productId = orderItem['order_line_id']
				try:
					self.Queries.saveProductImage(orderItem['product_medias'][0].media_url)
				except:
					print("no image found for product in worten medias")
				quantity = orderItem['quantity']
				commission_fee = orderItem['commission_fee']
				marketplace_order_state = orderItem['order_line_state']
				price =  orderItem['total_price']
				net_profit = self.Utils.calculateProductProfit(keepa_price,price,commission_fee)
				amazon_vat_rate = None # will be updated by autobuy job
				gmail_status = None
				tracking_carrier = None # unknown later will be changed e.g  bluecare 
				tracking_number = None # as initially we don't know
				tracking_url = None # may be we just put bluecare url
				amazon_vat_number = None

				self.Queries.saveProducts(marketplace_order_number,ean,asin,amazon_price,keepa_price,
				date_created,date_updated,productId,quantity,commission_fee,marketplace_order_state,
				net_profit,price,amazon_vat_rate,gmail_status,tracking_carrier,tracking_number,tracking_url,amazon_vat_number)

			autobuy_id  = None # Todo: will set it to a default autoincrement number
			marketplace_order_number =  orderfirst['order_id']
			amazon_order_number = None # as this can be filled after placing order
			marketplace  = "WORTEN"
			number_messages = self.Queries.getMessageCount(marketplace_order_number) 
			ordered_date = self.formatDate(orderfirst['created_date'])
			marketplace_fees = orderfirst['total_commission']
			autobuy_action = None # it will be reviewed, accepted, refused
			autobuy_status = None # accepted, shipped etc
			date_created = self.formatDate(orderfirst['created_date'])
			date_updated = self.formatDate(orderfirst['last_updated_date'])
			price = orderfirst['total_price']
			net_profit = self.Queries.calculateOrderProfit(marketplace_order_number,price,marketplace_fees)
			email = orderfirst['customer_notification_email']
			order_status = orderfirst['order_state']
			# print("order state from market place", order_status)
			if order_status == 'RECEIVED':
				order_status = 'ACTIVE'
			else:
				order_status = 'HISTORY'
			# print("order state saved into db", order_status)
			amazon_price = None
			keepa_price = self.Utils.CalculateKeepaPrice(product_price_array)
			refunded_price = None

			self.Queries.saveOrders(autobuy_id,marketplace_order_number,amazon_order_number,
			marketplace,number_messages,ordered_date,marketplace_fees,autobuy_action,autobuy_status,
			date_created,date_updated,net_profit,price,email,order_status,amazon_price,keepa_price,refunded_price,catalog)
		

			marketplace_order_number = orderfirst['order_id']
			try:
				shipping_marketplace_info =  orderfirst['customer']['shipping_address']['additional_info']
				address1 = orderfirst['customer']['shipping_address']['street_1']
				address2 = orderfirst['customer']['shipping_address']['street_2']
				city = orderfirst['customer']['shipping_address']['city']
				civility = orderfirst['customer']['shipping_address']['civility']
				companyName = orderfirst['customer']['shipping_address']['company']
				country = orderfirst['customer']['shipping_address']['country']
				firstname = orderfirst['customer']['shipping_address']['firstname']
				lastname = orderfirst['customer']['shipping_address']['lastname']
				instructions = orderfirst['customer']['shipping_address']['additional_info']
				placename = orderfirst['customer']['shipping_address']['state']
				street = orderfirst['customer']['shipping_address']['street_1']
				zipcode = orderfirst['customer']['shipping_address']['zip_code']
				shippingFirstName = orderfirst['customer']['firstname']
				shippingLastName = orderfirst['customer']['lastname']
			except:
				shipping_marketplace_info = None
				address1 = None
				address2 = None
				city = None
				civility = None
				companyName = None
				country = None
				firstname = None
				lastname = None
				instructions = None
				placename = None
				street = None
				zipcode = None
				shippingFirstName = None
				shippingLastName = None
			apartmentNumber = None 
			building = None

			mobilephone = '0000000000'
			phone =  '0000000000'

			date_created =  self.formatDate(orderfirst['created_date'])
			date_updated = self.formatDate(orderfirst['last_updated_date'])
			self.Queries.saveOrderShipping(marketplace_order_number,shipping_marketplace_info,address1,address2,apartmentNumber,building,city,civility,companyName,country,firstname,lastname,instructions,placename,street,zipcode,mobilephone,phone,shippingFirstName,shippingLastName,date_created,date_updated)
 
	def WortenCall(self, shopkey, catalog, proxy):
		

		response = ''
		payload = {}
		headers = {
			'Authorization': shopkey,
			'Accept': 'application/json'
		}
	
		try:
			if proxy is not None:
				response = requests.request("GET", Constants.worten_order_url_lasthour+str(self.Utils.getLastHourWorten()), headers=headers, data=payload, proxies=proxy)
			else:
				response = requests.request("GET", Constants.worten_order_url_lasthour+str(self.Utils.getLastHourWorten()), headers=headers, data=payload)
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())

		#TODO: when actual response comes then remove mock data option
		# resp_json = json.loads(response.text)
		# try:
		# 	print("orders: ", resp_json['orders'])
		# except:
		# 	self.logError(self.get_line(), sys.exc_info()[1])
		print("Worten Orders")
		resp_json = json.loads(self.worten_mock_data())

		print("sending mock response")
		self.parseWortenResponse(resp_json, catalog)
	
		# return True  # return if does not conflict with threading
		
	def wortenResetCall(self, shopkey, catalog, proxy):
		
		def wortenResetCall(number):
			finished = False
			response = ''
			url = Constants.worten_reset_order+str(number)

			payload={}
			headers = {
			'Authorization': shopkey,
			'Accept': 'application/json'
			}
			try:
				if proxy is None:
					response = requests.request("GET", url, headers=headers, data=payload)
				else:
					response = requests.request("GET", url, headers=headers, data=payload)
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
			resp_json = json.loads(response.text)
			total_count = resp_json['total_count']
			self.parseWortenResponse(resp_json, catalog) # Currently it will throw an error due to no billing and shipping address
			if number+100 >= total_count:
				finished = True
				print("finished parsing all the orders for worten")
				print("Total_count: ", str(total_count), "number is: ", str(number))
				quit()
				
			
			return finished

		def wortenPagination():
			count = 0
			while True:
				if wortenResetCall(count):
					quit()
				count = count + 100

		#---------------- call pagination functions here---------
		wortenPagination()   #billing and shipping addresses are empty so it cause problem but otherwise its fixed



'''uncomment the following for testing individually '''
# if __name__ == '__main__':
# 	mOrder =  WortenOrder()
# 	mOrder.WortenCall()
# 	mOrder.wortenResetCall()  #billing and shipping addresses are empty so it cause problem but otherwise its fixed
	

