import requests
from bs4 import BeautifulSoup
from sys import path
import sys
sys.path.append(".")
from urllib3 import ProxyManager, PoolManager
import time
import json
import xmltodict
from constant import Constants
import os
from os import getcwd
import sys
import pathlib
parentsDirectory = pathlib.Path(__file__).parent.parent.parent.absolute()
# print("parent: ",parentsDirectory)
sys.path.append(str(parentsDirectory))
from database import DatabaseQueries
from utils import MarketPlaceUtils
from inspect import currentframe



class CdiscountDiscussions():

	def __init__(self, logger):
		os.system("clear")
		os.system("clear")
		self.logger = logger
		self.Queries = DatabaseQueries(logger=self.logger)
		self.Utils = MarketPlaceUtils()
		self.filename = self.get_filename()


	def logError(self, line, errorStr):
		''' Format for logging the error '''
		self.logger.logevent("File: "+str(self.filename)+ "  Line: "+str(line)+ "  Description: "+str(errorStr))

	def get_filename(self):
		''' this is to get file name for logger to better identify the error '''
		return sys.argv[0]

	def get_line(self):
		''' getting line where error occured will be used later '''
		cf = currentframe()
		return str(cf.f_back.f_lineno)


	def parseDiscussions(self, soup):
		''' parsing the cdiscount discussion response '''

		if soup.GetDiscussionListResponse.GetDiscussionListResult.DiscussionList.get_text() is not None:
			for discussion in soup.GetDiscussionListResponse.GetDiscussionListResult.DiscussionList:
				subject =  discussion.Subject.get_text()
				disccussion_id = discussion.Id.get_text()
				status = discussion.Status.get_text()
				marketplace_order_number = discussion.OrderNumber.get_text()
				marketplace = 'CDISCOUNT'
				date_created =  discussion.CreationDate.get_text()[0:10]
				date_updated = discussion.LastUpdatedDate.get_text()[0:10]
				
				''' saving the discussion into discussion table'''
				self.Queries.saveDiscussions(subject,disccussion_id,status,marketplace_order_number,marketplace,date_created,date_updated)

				''' Looping over for messages in a single discussion'''
				for mmessage in discussion.Messages:
					disccussion_id = discussion.Id.get_text() #(reference to DISCUSSIONS TABLE)
					content = mmessage.Content.get_text()
					sender =  discussion.Messages.Message.SenderType.get_text()  #(can be SELLER or BUYER)
					if sender == 'Customer':
						sender = 'BUYER'
					else:
						sender = 'SELLER'
					mtimestamp = discussion.Messages.Message.Timestamp.get_text()[0:10]
					message_id = discussion.Messages.Message.Timestamp.get_text()
					self.Queries.saveMessage(disccussion_id,content,sender,mtimestamp,message_id)
	

	def mDiscussions(self,convertedAuthString,proxyUrls=None):

		''' call to api for getting token for discussion call '''
		token= 0
		response = ''
		payload={}
		headers = {
		'Authorization': 'Basic %s'%convertedAuthString }

		try:
			if proxyUrls is not None:
				response = requests.request("GET", Constants.cdiscount_token_url, headers=headers, data=payload,proxies=proxyUrls)
			else:
				response = requests.request("GET", Constants.cdiscount_token_url, headers=headers, data=payload)
				

			xmlText = BeautifulSoup(response.text,'xml')
			token = xmlText.string
			print("here is token:",token)
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())

		time.sleep(3)


		''' call to get discussions'''
		payload="<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:arr=\"http://schemas.microsoft.com/2003/10/Serialization/Arrays/\">\r\n\t<s:Body>\r\n\t\t<GetDiscussionList xmlns=\"http://www.cdiscount.com\">\r\n\t\t\t<headerMessage xmlns:a=\"http://schemas.datacontract.org/2004/07/Cdiscount.Framework.Core.Communication.Messages\" xmlns:i=\"http://www.w3.org/2001/XMLSchema-instance\">\r\n\t\t\t\t<a:Context>\r\n\t\t\t\t\t<a:CatalogID>1</a:CatalogID>\r\n\t\t\t\t\t<a:CustomerPoolID>1</a:CustomerPoolID>\r\n\t\t\t\t\t<a:SiteID>100</a:SiteID>\r\n\t\t\t\t</a:Context>\r\n\t\t\t\t<a:Localization>\r\n\t\t\t\t\t<a:Country>Fr</a:Country>\r\n\t\t\t\t\t<a:Currency>Eur</a:Currency>\r\n\t\t\t\t\t<a:DecimalPosition>2</a:DecimalPosition>\r\n\t\t\t\t\t<a:Language>Fr</a:Language>\r\n\t\t\t\t</a:Localization>\r\n\t\t\t\t<a:Security>\r\n\t\t\t\t\t<a:DomainRightsList i:nil=\"true\" />\r\n\t\t\t\t\t<a:IssuerID i:nil=\"true\" />\r\n\t\t\t\t\t<a:SessionID i:nil=\"true\" />\r\n\t\t\t\t\t<a:SubjectLocality i:nil=\"true\" />\r\n\t\t\t\t\t<a:TokenId>"+token+"</a:TokenId>\r\n\t\t\t\t\t<a:UserName i:nil=\"true\" />\r\n\t\t\t\t</a:Security>\r\n\t\t\t\t<a:Version>1.0</a:Version>\r\n\t\t\t</headerMessage>\r\n\t\t\t<discussionFilter>\r\n\t\t\t\t<BeginCreationDate>"+self.Utils.cdiscountGetLastHourTime()+"</BeginCreationDate>\r\n\t\t\t\t<StatusList>\r\n\t\t\t\t\t<DiscussionStateFilter>All</DiscussionStateFilter>\r\n\t\t\t\t</StatusList>\r\n\t\t\t\t<DiscussionType>Discussion</DiscussionType>\r\n\t\t\t\r\n\t\t\t</discussionFilter>\r\n\t\t</GetDiscussionList>\r\n\t</s:Body>\r\n</s:Envelope>"
		headers = {
		'Content-Type': 'text/xml;charset=UTF-8',
		'Accept-Encoding': 'gzip, deflate',
		'SOAPAction': 'http://www.cdiscount.com/IMarketplaceAPIService/GetDiscussionList',
		'Authorization': 'Basic %s'%convertedAuthString		
		}
		''' checking if there is proxy or no'''
		if proxyUrls is not None:
			try:
				response = requests.request("POST", Constants.cdiscount_base_url, headers=headers, data=payload, proxies=proxyUrls)
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
		else:
			try:
				response = requests.request("POST", Constants.cdiscount_base_url, headers=headers, data=payload)
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())		

	
		soup  = BeautifulSoup(response.content,'xml')
		self.parseDiscussions(soup)
	
		
	def resetDiscussions(self, convertedAuthString,proxyUrls=None):
		''' cdiscount reset of discussions '''
		response =''
		token = 0
		payload={}
		headers = {
		'Authorization': 'Basic %s'%convertedAuthString }

		try:
			if proxyUrls is not None:
				response = requests.request("GET", Constants.cdiscount_token_url , headers=headers, data=payload,proxies=proxyUrls)
			else:
				response = requests.request("GET", Constants.cdiscount_token_url, headers=headers, data=payload)
				
			xmlText = BeautifulSoup(response.text,features="lxml")
			token = xmlText.html.body.string
			print("here is token:",token)
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())

		time.sleep(3)

		''' call to get discussions'''	
		payload="<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\" xmlns:arr=\"http://schemas.microsoft.com/2003/10/Serialization/Arrays/\">\r\n\t<s:Body>\r\n\t\t<GetDiscussionList xmlns=\"http://www.cdiscount.com\">\r\n\t\t\t<headerMessage xmlns:a=\"http://schemas.datacontract.org/2004/07/Cdiscount.Framework.Core.Communication.Messages\" xmlns:i=\"http://www.w3.org/2001/XMLSchema-instance\">\r\n\t\t\t\t<a:Context>\r\n\t\t\t\t\t<a:CatalogID>1</a:CatalogID>\r\n\t\t\t\t\t<a:CustomerPoolID>1</a:CustomerPoolID>\r\n\t\t\t\t\t<a:SiteID>100</a:SiteID>\r\n\t\t\t\t</a:Context>\r\n\t\t\t\t<a:Localization>\r\n\t\t\t\t\t<a:Country>Fr</a:Country>\r\n\t\t\t\t\t<a:Currency>Eur</a:Currency>\r\n\t\t\t\t\t<a:DecimalPosition>2</a:DecimalPosition>\r\n\t\t\t\t\t<a:Language>Fr</a:Language>\r\n\t\t\t\t</a:Localization>\r\n\t\t\t\t<a:Security>\r\n\t\t\t\t\t<a:DomainRightsList i:nil=\"true\" />\r\n\t\t\t\t\t<a:IssuerID i:nil=\"true\" />\r\n\t\t\t\t\t<a:SessionID i:nil=\"true\" />\r\n\t\t\t\t\t<a:SubjectLocality i:nil=\"true\" />\r\n\t\t\t\t\t<a:TokenId>"+token+"</a:TokenId>\r\n\t\t\t\t\t<a:UserName i:nil=\"true\" />\r\n\t\t\t\t</a:Security>\r\n\t\t\t\t<a:Version>1.0</a:Version>\r\n\t\t\t</headerMessage>\r\n\t\t\t<discussionFilter>\r\n\t\t\t\t<!--<BeginCreationDate>2020-02-18T07:55:12.033</BeginCreationDate>\r\n\t\t\t\t\t<BeginModificationDate>2020-02-29T00:13:07.253</BeginModificationDate>\r\n\t\t\t\t\t<EndCreationDate>2020-02-18T07:55:12.033</EndCreationDate>\r\n\t\t\t\t\t<EndModificationDate>2020-02-29T00:13:07.253</EndModificationDate>-->\r\n\t\t\t\t<StatusList>\r\n\t\t\t\t\t<DiscussionStateFilter>All</DiscussionStateFilter>\r\n\t\t\t\t</StatusList>\r\n\t\t\t\t<DiscussionType>Discussion</DiscussionType>\r\n\t\t\t\t<!--<OrderNumberList>\r\n\t\t\t\t\t<arr:string>2002142050MW871</arr:string>\r\n\t\t\t\t</OrderNumberList>-->\r\n\t\t\t\t<!--<ProductEanList>\r\n\t\t\t\t\t<arr:string></arr:string>\r\n\t\t\t\t</ProductEanList>\r\n\t\t\t\t<ProductSellerReferenceList>\r\n\t\t\t\t\t<arr:string&lt;&lt;/arr:string>\r\n\t\t\t\t</ProductSellerReferenceList>-->\r\n\t\t\t</discussionFilter>\r\n\t\t</GetDiscussionList>\r\n\t</s:Body>\r\n</s:Envelope>"
		headers = {
		'Content-Type': 'text/xml;charset=UTF-8',
		'Accept-Encoding': 'gzip, deflate',
		'SOAPAction': 'http://www.cdiscount.com/IMarketplaceAPIService/GetDiscussionList',
		'Authorization': 'Basic %s'%convertedAuthString,
		}

		try:
			if proxyUrls is not None:
				response = requests.request("POST", Constants.cdiscount_base_url, headers=headers, data=payload, proxies=proxyUrls)
			else:
				response = requests.request("POST", Constants.cdiscount_base_url, headers=headers, data=payload)
				

			soup  = BeautifulSoup(response.text,'xml')
			# print("soup is : ", soup)
			self.parseDiscussions(soup)
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
	

	


'''uncomment the following for testing individually '''
# if __name__ == '__main__':
# 	myDiscussions = CdiscountDiscussions()
# 	myDiscussions.mDiscussions()
