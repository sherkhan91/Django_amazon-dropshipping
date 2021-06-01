import sys
import pathlib
import threading
import time
import schedule
from constant import Constants
from database import DatabaseQueries
from marketplaces.cdiscount.cOrder import CdiscountOrder
from marketplaces.cdiscount.cDiscussion import CdiscountDiscussions
from marketplaces.rakuten.rOrder import RakutenOrder
from marketplaces.rakuten.rDiscussion import RakutenDiscussions
from marketplaces.worten.wOrder import WortenOrder
from marketplaces.worten.wDiscussion import WortenDiscussions
from utils import MarketPlaceUtils
from Logging_Program import myLogger
from inspect import currentframe
import traceback
parentsDirectory = pathlib.Path(__file__).parent
parentsDirectory1 = str(parentsDirectory)+"/marketplaces/cdiscount"
parentsDirectory2 = str(parentsDirectory)+"/marketplaces/rakuten"
parentsDirectory3 = str(parentsDirectory)+"/marketplaces/worten"
# print("parent: ",parentsDirectory)
sys.path.append(str(parentsDirectory1))
sys.path.append(str(parentsDirectory2))
sys.path.append(str(parentsDirectory3))



class MainClass():

	#test commit ui upload on git
	def __init__(self):
		""" Initialization of all marketplaces goes here as it will be done only once """
		print("started")
		self.logger = myLogger()
		# self.cdiscountOrders = CdiscountOrder(logger=self.logger)
		# self.cdiscountDiscussions = CdiscountDiscussions(logger=self.logger)

		self.rakutenOrders = RakutenOrder(logger=self.logger)
		''' Discussions commited out here because we put it inside orders due to item id issue '''
		# self.rakutendiscussions = RakutenDiscussions(logger=self.logger) 
		# #
		# self.wortenOrders = WortenOrder(logger=self.logger)
		# self.wortendiscussions  = WortenDiscussions(logger=self.logger)

		self.Utils = MarketPlaceUtils()

		self.filename = self.get_filename()
		print("finisheds")

	def get_filename(self):
		''' this is to get file name for logger to better identify the error '''
		return sys.argv[0]

	def get_line(self):
		''' getting line where error occured will be used later '''
		cf = currentframe()
		return str(cf.f_back.f_lineno)

	def logError(self, line, errorStr):
		''' Format for logging the error '''
		self.logger.logevent("File: "+str(self.filename)+ "  Line: "+str(line)+ "  Description: "+str(errorStr))


	def cdiscountMarketPlace(self,username,password,resetParam,catalog,proxy=None):
		"""Marketplace calls without threading for debuging and development purpose"""
		authString = self.Utils.convertToAuthorization(username,password)

		"""Marketplace calls with threading"""
		if resetParam:
			print("reset parameter")
			try:
				threading.Thread(target=self.cdiscountOrders.cdiscountResetOrders, args=(authString,catalog,proxy, )).start()
				threading.Thread(target=self.cdiscountDiscussions.resetDiscussions, args=(authString,proxy,)).start()
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
		else:
			try:
				threading.Thread(target=self.cdiscountOrders.cDiscountCall, args=(authString,catalog,proxy, )).start()
				threading.Thread(target=self.cdiscountDiscussions.mDiscussions, args=(authString,proxy,)).start()
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())

	
	def rakutenMarketPlace(self, username, password,resetParam,catalog,proxy=None):
		"""Marketplace calls with threading"""
		if resetParam:
			try:
				threading.Thread(target=self.rakutenOrders.rakutenResetCall, args=(username,password,catalog,proxy, )).start()
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
		else:
			try:
				threading.Thread(target=self.rakutenOrders.RakutenNewSales, args=(username,password,catalog,proxy, )).start()
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
	

	def wortenMarketPlace(self, shopkey, resetParam,catalog,proxy=None):
		"""Marketplace calls with threading"""
		if resetParam:
			try:
				threading.Thread(target=self.wortenOrders.wortenResetCall, args=(shopkey,catalog,proxy,)).start() # uncomment this for reset call
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
		else:
			try:
				threading.Thread(target=self.wortenOrders.WortenCall, args=(shopkey,catalog,proxy,)).start()
				threading.Thread(target=self.wortendiscussions.mDiscussions, args=(shopkey,proxy, )).start()
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
		
		

	def main(self):
		"""This is scheduling function which run the jobs after interval """
		# self.multiaccount() # it is here for deubgging

		self.multiaccount()

		# try:
		# 	schedule.every(1).minutes.do(self.multiaccount) # change to 5 just used 1 for testing
		# except:
		# 		self.logError(self.get_line(), sys.exc_info()[1])

		# while True:
		# 	schedule.run_pending()
		# 	time.sleep(1)




	def multiaccount(self):
		""" This will iterate over that JSON/Dict given in constant to take out account info """
		for i in range(len(Constants.testingaccounts['accounts'][0])):
			print("account sequence: ",i)
			cproxy = None
			rproxy = None
			wproxy = None
			catalog = None
		
			catalog = "catalog"+str(i+1)
			# print(catalog)
			# info = Constants.testingaccounts['accounts'][0]['catalog'+str(i+1)]['cdiscount'+str(i+1)]
			cusername =Constants.testingaccounts['accounts'][0]['catalog'+str(i+1)]['cdiscount'+str(i+1)]['username']
			cpass = Constants.testingaccounts['accounts'][0]['catalog'+str(i+1)]['cdiscount'+str(i+1)]['password']
			try:
				cproxy = Constants.testingaccounts['accounts'][0]['catalog'+str(i+1)]['cdiscount'+str(i+1)]['proxy']
			except:
				pass
				# print(traceback.print_exc())
			rusername = Constants.testingaccounts['accounts'][0]['catalog'+str(i+1)]['rakuten'+str(i+1)]['username']
			rpass = Constants.testingaccounts['accounts'][0]['catalog'+str(i+1)]['rakuten'+str(i+1)]['password']
			try:
				rproxy = Constants.testingaccounts['accounts'][0]['catalog'+str(i+1)]['rakuten'+str(i+1)]['proxy']
			except:
				pass
				# print(traceback.print_exc())
			wshopkey = Constants.testingaccounts['accounts'][0]['catalog'+str(i+1)]['worten'+str(i+1)]['shopkey']
			try:
				wproxy =   Constants.testingaccounts['accounts'][0]['catalog'+str(i+1)]['worten'+str(i+1)]['proxy']
			except:
				pass
				# print(traceback.print_exc())

			'''Last parameter is for reset purpsose if it is true then reset order functions will be called'''
			'''put true or false for one by one so that we can call individual function reset for each function'''
			# try:
			# 	self.cdiscountMarketPlace(cusername,cpass,False,catalog,cproxy)
			# except:
			# 	print(traceback.print_exc())
			# 	self.logError(self.get_line(), sys.exc_info()[1])
			try:
				self.rakutenMarketPlace(rusername,rpass,False,catalog,rproxy)
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
			# try:
			# 	self.wortenMarketPlace(wshopkey,True,catalog, wproxy)
			# except:
			# 	print("something went wrong")
			# 	self.logError(self.get_line(), sys.exc_info()[1])



if __name__ == '__main__':
	MainClass().main()




