from typing import Optional
# from fastapi import FastAPI
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
import sys
import datetime
import logging
import os
import sys
sys.path.append(".")
from datetime import datetime, timedelta
from constant import Constants
import sys
import pathlib
import traceback
parentsDirectory = pathlib.Path(__file__).parent.parent.parent.absolute()
sys.path.append(str(parentsDirectory))
from database import DatabaseQueries
from utils import MarketPlaceUtils
from . import rDiscussion
from Logging_Program import myLogger

class RakutenOrder():
	
	def __init__(self, logger):
		self.logger = logger
		self.Queries = DatabaseQueries(logger=self.logger)
		self.Utils = MarketPlaceUtils()
		self.filename = self.get_filename()
		self.logger = myLogger()

		self.rakutenDiscussion = rDiscussion.RakutenDiscussions(self.logger)
		
		# self.rakutenDiscussion = rDiscussion.Rakuten


	def logError(self, line, errorStr):
		''' Format for logging the error '''
		self.logger.logevent("File: "+str(self.filename)+ "  Line: "+str(line)+ "  Description: "+str(errorStr))

	def get_filename(self):
		''' will be used to get file name for logger '''
		return sys.argv[0]
	
	def get_line(self):
		''' will be used for getting line number of error '''
		cf = currentframe()
		return str(cf.f_back.f_lineno)
	
	def rakutenMultiSale(self, resp_dict,saletype,catalog,username,password,proxy):
		''' multi sale parsing if there are more than one orders then it will be parsed in this function '''
		mobilephone = '0000000000' 
		phone =  '0000000000' 
		asin = 'FAKEASIN123'
		product_price_array = []
		order_count = 0
		for sale in resp_dict[saletype]['response']['sales']['sale']:
			item_count = 0
			try:
				''' if there are multiple items in a single order then it will be in try else except '''
				for item in sale['items']['item']:
					marketplace_order_number = sale['purchaseid']
					ean = sale['items']['item'][item_count]['ean']  
					try:
						asin = self.Queries.extractAsin(ean, catalog) # get asin from database
					except:
						self.logError(self.get_line(), sys.exc_info()[1])
						print(traceback.print_exc())
					amazon_price = None #as this can be filled after placing order
					keepa_price = self.Queries.getKeepaPrice(ean,catalog)
					temp_date = sale['purchasedate']
					date_created = temp_date[6:10]+"-"+temp_date[3:5]+"-"+temp_date[0:2]
					date_updated =  None # there is no field like  that in api response for product
					productId = sale['items']['item'][item_count]['itemid']
					''' Modification for discussion of each item '''
					if proxy is not None:
						self.rakutenDiscussion.mDiscussions(username,password,productId,proxy)
					else:
						self.rakutenDiscussion.mDiscussions(username,password,productId)
					quantity = 1 # which is default
					commission_fee = 0 # as there is no such field in rakuten api response
					marketplace_order_state =  sale['items']['item'][item_count]['itemstatus']
					net_profit = None	
					price =  sale['items']['item'][item_count]['price']['amount']
					amazon_vat_rate= None
					gmail_status = None
					tracking_number = None # as initially we don't know
					tracking_carrier = None # unknown later will be changed e.g  bluecare 
					tracking_url = None # may be we just put bluecare url
					amazon_vat_number = None
					item_count =  item_count+1
					''' saving individual product details in product table for a given order '''
					self.Queries.saveProducts(marketplace_order_number,ean,asin,amazon_price,keepa_price,
					date_created,date_updated,productId,quantity,commission_fee,marketplace_order_state,
					net_profit,price,amazon_vat_rate,gmail_status,tracking_carrier,tracking_number,tracking_url,amazon_vat_number)


			except:
				''' if it is a single order then it will parsed here '''
				marketplace_order_number = sale['purchaseid']
				ean = sale['items']['item']['ean'] 
				try:
					asin = self.Queries.extractAsin(ean, catalog)
				except:
					self.logError(self.get_line(), sys.exc_info()[1])
					print(traceback.print_exc())
				amazon_price = None #as this can be filled after placing order
				keepa_price = self.Queries.getKeepaPrice(ean,catalog)
				temp_date = sale['purchasedate']
				date_created = temp_date[6:10]+"-"+temp_date[3:5]+"-"+temp_date[0:2]
				date_updated =  None # there is no field like  that in api response for product
				productId = sale['items']['item']['itemid']

				''' Modification for discussion of each item '''
				if proxy is not None:
					self.rakutenDiscussion.mDiscussions(username,password,productId,proxy)
				else:
					self.rakutenDiscussion.mDiscussions(username,password,productId)

				quantity = 1 # which is default
				commission_fee = 0 # as there is no such field in rakuten api response
				marketplace_order_state =  sale['items']['item']['itemstatus']
				net_profit = None
				amazon_vat_rate = None
				price =  sale['items']['item']['price']['amount']
				gmail_status = None
				tracking_number = None # as initially we don't know
				tracking_carrier = None # unknown later will be changed e.g  bluecare 
				tracking_url = None # may be we just put bluecare url
				amazon_vat_number = None
				item_count =  item_count+1
				''' except case if there is a single product in an order '''
				''' saving individual product details in product table for a given order '''
				self.Queries.saveProducts(marketplace_order_number,ean,asin,amazon_price,keepa_price,
				date_created,date_updated,productId,quantity,commission_fee,marketplace_order_state,
				net_profit,price,amazon_vat_rate,gmail_status,tracking_carrier,tracking_number,tracking_url,amazon_vat_number)

			autobuy_id  = None 
			marketplace_order_number =  sale['purchaseid']
			amazon_order_number = None # as this can be filled after placing order
			marketplace  = "RAKUTEN"
			number_messages = self.Queries.getMessageCount(marketplace_order_number)
			ordered_date = sale['purchasedate']
			ordered_date = ordered_date[6:10]+'-'+ordered_date[3:5]+'-'+ordered_date[0:2]
			marketplace_fees = None # couldn't find this in rakauten, its not there in response neither in doc
			autobuy_action = None 
			autobuy_status = None
			date_created = sale['purchasedate']
			date_created = date_created[6:10]+'-'+date_created[3:5]+'-'+date_created[0:2]
			date_updated = None # there was no field like this neither in response nor in doc
			price = None # no price for whole order
			''' for getting emails as currently there is no email '''
			try:
				email = sale['deliveryinformation']['Purchasebuyeremail']
			except:
				email = None # not available right now but doc shows it should be here
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
			if saletype == 'getnewsalesresult':
				order_status = 'ACTIVE' # not available for whole order in rakuten, ask ben to suggest, may be we put status of last itme in order
			else:
				order_status = 'HISTORY'
			amazon_price = None  # autobuy job will fill it
			keepa_price = self.Utils.CalculateKeepaPrice(product_price_array)
			refunded_price = None
			net_profit = self.Queries.calculateOrderProfit(marketplace_order_number,price,marketplace_fees)

			''' saving the order detail for an order '''
			self.Queries.saveOrders(autobuy_id,marketplace_order_number,amazon_order_number,
			marketplace,number_messages,ordered_date,marketplace_fees,autobuy_action,autobuy_status,
			date_created,date_updated,net_profit,price,email,order_status,amazon_price,keepa_price,refunded_price,catalog)
		
			marketplace_order_number = sale['purchaseid']
			shipping_marketplace_info =  None # couldn't find similar field in cdiscount + ben told its optional
			address1 = sale['deliveryinformation']['deliveryaddress']['address1']
			address2 = sale['deliveryinformation']['deliveryaddress']['address2']
			apartmentNumber = None
			building = None
			city =  sale['deliveryinformation']['deliveryaddress']['city']
			civility =sale['deliveryinformation']['deliveryaddress']['civility']
			companyName = None # this is not provided by rakauten
			country = sale['deliveryinformation']['deliveryaddress']['country']
			firstname = sale['deliveryinformation']['deliveryaddress']['firstname']
			lastname = sale['deliveryinformation']['deliveryaddress']['lastname']
			instructions = None #couldn't find this in respons neither in doc
			placename = None
			street = sale['deliveryinformation']['deliveryaddress']['address1']
			zipcode = sale['deliveryinformation']['deliveryaddress']['zipcode']
			''' try except to see if there is any mobile number else it will be default numbers '''
			try:
				mobilephone = sale['deliveryinformation']['deliveryaddress']['phonenumber1'] 
				phone = sale['deliveryinformation']['deliveryaddress']['phonenumber2']
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
				# as it will pick default values given above
			shippingFirstName =  sale['deliveryinformation']['deliveryaddress']['firstname']
			shippingLastName = sale['deliveryinformation']['deliveryaddress']['lastname']
			date_created =   sale['purchasedate']
			date_created = date_created[6:10]+'-'+date_created[3:5]+'-'+date_created[0:2]
			date_updated = None # there was no field like this neither in response nor in doc
			''' saving shipping details for an order '''
			self.Queries.saveOrderShipping(marketplace_order_number,shipping_marketplace_info,address1,address2,apartmentNumber,building,city,civility,companyName,country,firstname,lastname,instructions,placename,street,zipcode,mobilephone,phone,shippingFirstName,shippingLastName,date_created,date_updated)

			order_count = order_count+1 # get next sale data 

	def rakutenSingleSale(self, resp_dict,saletype,catalog,username,password,proxy):
		''' single sale parsing if there is one order then it will be parsed in this function '''
		# variable initialization for  phone number and array
		mobilephone = '0000000000' 
		phone =  '0000000000' 
		asin = 'FAKEASIN123'
		product_price_array = []

		order_count = 0
		for i in range(1):
			item_count = 0
			sale= resp_dict[saletype]['response']['sales']['sale']
			try:
				''' if there are multiple items in a single order then it will be in try else except '''
				for item in sale['items']['item']:
					marketplace_order_number = sale['purchaseid']
					ean = sale['items']['item'][item_count]['ean']  
					try:
						asin = self.Queries.extractAsin(ean)
					except:
						self.logError(self.get_line(), sys.exc_info()[1])
						print(traceback.print_exc())
					amazon_price = None #as this can be filled after placing order
					keepa_price = self.Queries.getKeepaPrice(ean,catalog)
					temp_date = sale['purchasedate']
					date_created = temp_date[6:10]+"-"+temp_date[3:5]+"-"+temp_date[0:2]
					date_updated =  None # there is no field like  that in api response for product
					productId = sale['items']['item'][item_count]['itemid']
					''' Modification for discussion of each item '''
					if proxy is not None:
						self.rakutenDiscussion.mDiscussions(username,password,productId,proxy)
					else:
						self.rakutenDiscussion.mDiscussions(username,password,productId)
					quantity = 1 # which is default
					commission_fee = 0 # as there is no such field in rakuten api response
					marketplace_order_state =  sale['items']['item'][item_count]['itemstatus']
					net_profit = None	
					price =  sale['items']['item'][item_count]['price']['amount']
					amazon_vat_rate= None
					gmail_status = None
					tracking_number = None # as initially we don't know
					tracking_carrier = None # unknown later will be changed e.g  bluecare 
					tracking_url = None # may be we just put bluecare url
					amazon_vat_number = None
					item_count =  item_count+1
					''' saving individual product details in product table for a given order '''
					self.Queries.saveProducts(marketplace_order_number,ean,asin,amazon_price,keepa_price,
					date_created,date_updated,productId,quantity,commission_fee,marketplace_order_state,
					net_profit,price,amazon_vat_rate,gmail_status,tracking_carrier,tracking_number,tracking_url,amazon_vat_number)

			except:
				''' except case if there is a single product in an order '''
				marketplace_order_number = sale['purchaseid']
				ean = sale['items']['item']['ean']  
				try:
					asin = self.Queries.extractAsin(ean)
				except:
					self.logError(self.get_line(), sys.exc_info()[1])
					print(traceback.print_exc())
				amazon_price = None #as this can be filled after placing order
				keepa_price = self.Queries.getKeepaPrice(ean,catalog)
				temp_date = sale['purchasedate']
				date_created = temp_date[6:10]+"-"+temp_date[3:5]+"-"+temp_date[0:2]
				date_updated =  None # there is no field like  that in api response for product
				productId = sale['items']['item']['itemid']
				''' Modification for discussion of each item '''
				if proxy is not None:
					self.rakutenDiscussion.mDiscussions(username,password,productId,proxy)
				else:
					self.rakutenDiscussion.mDiscussions(username,password,productId)
				quantity = 1 # which is default
				commission_fee = 0 # as there is no such field in rakuten api response
				marketplace_order_state =  sale['items']['item']['itemstatus']
				net_profit = None
				amazon_vat_rate = None
				price =  sale['items']['item']['price']['amount']
				gmail_status = None
				tracking_number = None # as initially we don't know
				tracking_carrier = None # unknown later will be changed e.g  bluecare 
				tracking_url = None # may be we just put bluecare url
				amazon_vat_number = None
				item_count =  item_count+1
				''' saving individual product details in product table for a given order '''
				self.Queries.saveProducts(marketplace_order_number,ean,asin,amazon_price,keepa_price,
				date_created,date_updated,productId,quantity,commission_fee,marketplace_order_state,
				net_profit,price,amazon_vat_rate,gmail_status,tracking_carrier,tracking_number,tracking_url,amazon_vat_number)


			autobuy_id  = None # Todo: will set it to a default autoincrement number
			marketplace_order_number = resp_dict['getnewsalesresult']['response']['sales']['sale']['purchaseid']
			amazon_order_number = None # as this can be filled after placing order
			marketplace  = "RAKUTEN"
			number_messages = self.Queries.getMessageCount(marketplace_order_number)
			ordered_date = resp_dict['getnewsalesresult']['response']['sales']['sale']['purchasedate']
			ordered_date = ordered_date[6:10]+'-'+ordered_date[3:5]+'-'+ordered_date[0:2]
			marketplace_fees = None # couldn't find this in rakauten, its not there in response neither in doc
			autobuy_action = None # it will be reviewed, accepted, refused
			autobuy_status = None # accepted, shipped etc
			date_created =  ordered_date[6:10]+'-'+ordered_date[3:5]+'-'+ordered_date[0:2]
			date_updated = None # there was no field like this neither in response nor in doc
			price = None # no price for whole order
			order_status = None
			try:
				email =resp_dict['getnewsalesresult']['response']['sales']['sale']['deliveryinformation']['Purchasebuyeremail']
			except:
				email = None # not available right now but doc shows it should be here
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
			if saletype == 'getnewsalesresult':
				order_status = 'ACTIVE' # not available for whole order in rakuten, ask ben to suggest, may be we put status of last itme in order
			else:
				order_status = 'HISTORY'
			amazon_price = None  # autobuy job will fill it
			keepa_price = self.Utils.CalculateKeepaPrice(product_price_array)
			refunded_price = None
			net_profit = self.Queries.calculateOrderProfit(marketplace_order_number,price,marketplace_fees)
			
			''' saving the order detail for an order '''
			self.Queries.saveOrders(autobuy_id,marketplace_order_number,amazon_order_number,
			marketplace,number_messages,ordered_date,marketplace_fees,autobuy_action,autobuy_status,
			date_created,date_updated,net_profit,price,email,order_status,amazon_price,keepa_price,refunded_price,catalog)
			sale= resp_dict['getnewsalesresult']['response']['sales']['sale']

			address = '' # first try delivery address otherwise save billing address
			try:
				sale['deliveryinformation']['deliveryaddress']['address1']
				address = 'deliveryaddress'
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
				address = 'billingaddress'

			marketplace_order_number = sale['purchaseid']
			shipping_marketplace_info =  None # couldn't find similar field in cdiscount + ben told its optional
			address1 = sale['deliveryinformation'][address]['address1']
			address2 = sale['deliveryinformation'][address]['address2']
			apartmentNumber = None
			building = None
			city =  sale['deliveryinformation'][address]['city']
			civility =sale['deliveryinformation'][address]['civility']
			companyName = None # this is not provided by rakauten
			country = sale['deliveryinformation'][address]['country']
			firstname = sale['deliveryinformation'][address]['firstname']
			lastname = sale['deliveryinformation'][address]['lastname']
			instructions = None #couldn't find this in respons neither in doc
			placename = None
			street = sale['deliveryinformation'][address]['address1']
			zipcode = sale['deliveryinformation'][address]['zipcode']
			try:
				mobilephone = sale['deliveryinformation'][address]['phonenumber1'] 
				phone = sale['deliveryinformation'][address]['phonenumber2']
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
				# as it will pick default values given above
			shippingFirstName =  sale['deliveryinformation'][address]['firstname']
			shippingLastName = sale['deliveryinformation'][address]['lastname']
			date_created =   sale['purchasedate']
			date_created = date_created[6:10]+'-'+date_created[3:5]+'-'+date_created[0:2]
			date_updated = None # there was no field like this neither in response nor in doc

			''' saving the shipping details for order '''
			self.Queries.saveOrderShipping(marketplace_order_number,shipping_marketplace_info,address1,address2,apartmentNumber,building,city,civility,companyName,country,firstname,lastname,instructions,placename,street,zipcode,mobilephone,phone,shippingFirstName,shippingLastName,date_created,date_updated)
			order_count = order_count+1 # get next sale data 
	
	def RakutenNewSales(self, username,password,catalog,proxy=None):
		''' For getting latest orders which are not yet accepted by seller, (newsales)'''

		url  =Constants.rakuten_base_url+'getnewsales&login='+username+'&pwd='+password+'&version=2013-06-25'
		payload={}
		response = ''
		headers = {
		}

		''' checking if there is any proxy '''
		try:
			if proxy is not None:
				response = requests.request("GET", url, headers=headers, data=payload, proxies=proxy)
			else:
				response = requests.request("GET", url, headers=headers, data=payload)
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())

		o = xmltodict.parse(response.text)
		jsonResponse =  json.dumps(o)
		resp_dict = json.loads(jsonResponse)

		print("Rakuten Orders")
		sale= resp_dict['getnewsalesresult']['response']['sales']
		if sale is not None:
			if str(type(resp_dict['getnewsalesresult']['response']['sales']['sale'])) == "<class 'list'>":
				self.rakutenMultiSale(resp_dict,'getnewsalesresult',catalog, username,password,proxy=None)
			else:
				self.rakutenSingleSale(resp_dict,'getnewsalesresult',catalog, username,password,proxy=None)


	def rakutenResetCall(self, username,password,catalog, proxy=None):
		
		def rakutenResetCall(nextToken):
			''' reset call means it will get orders from starting, (current sales, it uses token for next page) '''
			response = ''
			url = Constants.rakuten_base_url+"getcurrentsales&login="+username+"&pwd="+password+"&version=2013-06-25&purchasedae=2011-01-01"+nextToken
			payload={}
			headers = {
			}

			try:
				if proxy is not None:
					response =  requests.request("GET", url, headers =headers, data=payload, proxies=proxy)
				else:
					response = requests.request("GET", url, headers=headers, data=payload)
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())

			o = xmltodict.parse(response.text)
			jsonResponse =  json.dumps(o)
			
			resp_dict = json.loads(jsonResponse)
			# print("here is response",resp_dict)
			
			if resp_dict['getcurrentsalesresult']['response']['sales'] is not None:
				if str(type(resp_dict['getcurrentsalesresult']['response']['sales']['sale'])) == "<class 'list'>":
					self.rakutenMultiSale(resp_dict,'getcurrentsalesresult',catalog, username,password,proxy=None)
				else:
					self.rakutenSingleSale(resp_dict,'getcurrentsalesresult',catalog, username,password,proxy=None)
	
			next_token = resp_dict['getcurrentsalesresult']['response']['nexttoken']
			if next_token is not None:
				print("next token is: ", next_token)
				variable = 'nexttoken='+next_token
				rakutenResetCall(variable)
			else:
				return

		def rakutenpagination():
			''' pagination is implemented from this function and then function itself recursively '''
			variable=''
			rakutenResetCall(variable)


		rakutenpagination()


'''uncomment the following for testing individually '''

# if __name__ == '__main__':
# 	mOrder =  RakutenOrder()
# 	# mOrder.RakutenCurrentSales()
# 	# mOrder.RakutenNewSales()
# 	mOrder.rakutenResetCall()


