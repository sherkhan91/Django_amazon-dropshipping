
# import here
import sys
sys.path.append(".")
from datetime import datetime, timedelta
import base64


class MarketPlaceUtils():

	def __init__(self):
		# print("marketplace utils")
		# logging
		# self.LoggerClass = myLogger()  
		# LOG = "marketplace.log"  
		pass                                                   

	def CalculateKeepaPrice(self,product_price_array):
		'''Calculate keepa price for orders by taking each product price from keepa table '''
		total_keepa_price = 0
		for i in range(len(product_price_array)):
			try:
				total_keepa_price = total_keepa_price+product_price_array[i]
			except:
				total_keepa_price = 0
		
		return total_keepa_price

	def calculateProductProfit(self,KeepaPrice,marketPrice, commissionPrice):
		'''Calculate profit for each product and this is available only for worten as there is no comission for rest '''
		profit = 0
		# cdiscount and rakuten does not provide commission for individual product
		# try:
		# 	AmazonKeepaPrice = 2/0
		# except:
		# AmazonKeepaPrice = self.Queries.getKeepaPrice(ean)
		# print(AmazonKeepaPrice)
		
		if KeepaPrice is not None:
			profit = float(marketPrice)-(float(KeepaPrice)+float(commissionPrice))
		else:
			# print("price can not be calculated due to no EAN found in catalogue table.")
			profit = None
		return profit

	def cdiscountFormatDate(self,date_string):
		''' changing format for date cdiscount '''
		return date_string[:10]
	
	def cdiscountGetLastHourTime(self):
		''' Get last hour date time and then converting it from python date time object to cdiscount format datetime '''

		datetimevar = datetime.now()-timedelta(hours=1)
		datetimevar =  str(datetimevar)
		datetimevar =  datetimevar[0:10]+"T"+datetimevar[11:]
		# datetimevar =  '2011-02-02'+"T"+datetimevar[11:] # used this for testing with old date
		# print(datetimevar)
		return datetimevar

	def getLastHourWorten(self):
		''' Get last hour date time from cdiscount function and then converting it to worten format datetime '''

		wortenFormat = self.cdiscountGetLastHourTime()
		return  wortenFormat[0:19]+"Z"

	def logthis(self, myerror):
		''' log functions temporarly not working out of order '''
		save_Str = self.file_name+" : "+myerror
		self.LoggerClass.logevent(save_Str)
		# usage exmaple
		# self.logthis(self.get_line()+": file name and line number")

	def convertToAuthorization(self,username,password):
		''' converting marketplace username and passwords into base64 string for authorization purpose.  '''
		# username = 'mymdin26-api'
		# password = 'Aqwzsxedc26.'
		byteString = base64.b64encode(bytes(username+":"+password,'utf-8'))
		userAndPass = (byteString.decode('ascii'))
		return userAndPass






