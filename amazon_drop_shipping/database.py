import mysql.connector as mysql
from constant import Constants
from Logging_Program import myLogger
from inspect import currentframe
import sys
import traceback


class DatabaseQueries():

	def __init__(self, logger):
		print("database operations started..")
		self.filename = self.get_filename()
		self.logger = logger
		try:
			self.db = self.getConnection()
		except:
			self.logError(self.get_line(), sys.exc_info()[1])



	def opendb(self):
		try:
			# self.db = self.getConnection()
			self.cursor = self.db.cursor()
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())


	def getConnection(self):
		db_connection = mysql.connect(host=Constants.mhost, port= Constants.mport, database=Constants.mdatabase, user=Constants.muser, passwd=Constants.mpassword)
		# print("Connected to: ",db_connection.get_server_info())
		return db_connection
		
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


	def saveDiscussions(self,subject,disccussion_id,status,marketplace_order_number,marketplace,date_created,date_updated):
		self.opendb()
		sql = "SELECT * from app_discussions WHERE marketplace_order_number=%s and disccussion_id=%s"
		value = (marketplace_order_number,disccussion_id, )
		try:
			self.cursor.execute(sql, value)
			entry = self.cursor.fetchall()
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
	

		if self.cursor.rowcount>0:
			# self.cursor.fetchall()
			# self.opendb()
			try:
				sql = "UPDATE app_discussions SET subject=%s,disccussion_id=%s,status=%s,marketplace_order_number=%s,marketplace=%s,date_created=%s,date_updated=%s WHERE marketplace_order_number=%s"
				value= (subject,disccussion_id,status,marketplace_order_number,marketplace,date_created,date_updated,marketplace_order_number)
				self.cursor.execute(sql,value)
				self.db.commit()
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
			print("successfully updated discussions details")
			# print(self.cursor.rowcount,"record(s) affected.")
		else:
			# self.cursor.fetchall()
			try:
				sql = "INSERT into app_discussions(subject,disccussion_id,status,marketplace_order_number,marketplace,date_created,date_updated)VALUES(%s,%s,%s,%s,%s,%s,%s)"		
				value= (subject,disccussion_id,status,marketplace_order_number,marketplace,date_created,date_updated)
				# print("printing values discussions:",value)
				self.cursor.execute(sql,value)
				self.db.commit()
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
			print("successfully saved discussion.")
		self.cursor.close()

	def saveMessage(self,disccussion_id,content,sender,mtimestamp,message_id):
		self.opendb()
		try:
			sql = "SELECT * from app_messages WHERE message_id=%s"
			value = (message_id, )
			self.cursor.execute(sql, value)
			entry = self.cursor.fetchall()
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())

		if self.cursor.rowcount>0:
			print("message already exists updating fields.")
			try:
				sql = "UPDATE app_messages SET disccussion_id=%s,content=%s,sender=%s,mtimestamp=%s WHERE message_id=%s"
				value= (disccussion_id,content,sender,mtimestamp,message_id)
				self.cursor.execute(sql,value)
				self.db.commit()
				print("successfully updated message details")
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
			# print(self.cursor.rowcount,"record(s) affected.")
		else:
			try:
				sql = "INSERT into app_messages(disccussion_id,content,sender,mtimestamp,message_id)VALUES(%s,%s,%s,%s,%s)"		
				value= (disccussion_id,content,sender,mtimestamp,message_id)
				# print("printing values:",value)
				cursor1 = self.db.cursor()
				cursor1.execute(sql,value)
				self.db.commit()
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
			self.cursor.close()
			print("successfully saved message.")

	def saveProductImage(self,ean, image_url):
		self.opendb()
		try:
			sql = "UPDATE worten_brands SET image=%s WHERE ean=%s"
			value = (image_url,ean, )
			self.cursor.execute(sql,value)
			self.db.commit()
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
		self.cursor.close()

	def getMessageCount(self, order_number):
		message_count = 0
		self.opendb()
		try:
			message_count = 0 
			sql = "SELECT disccussion_id, count(*) as id FROM `keepa-dev`.app_messages  where disccussion_id=(SELECT disccussion_id FROM `keepa-dev`.app_discussions where marketplace_order_number = %s) GROUP BY disccussion_id"
			value = (order_number, )
			self.cursor.execute(sql,value)
			entry = self.cursor.fetchall()
			for e in entry:
				message_count = e[1]
				# print("message count: ", message_count," for order: ",order_number)
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
		return message_count

	def getProductCommission(self, ean, order_number):
		self.opendb()
		try:
			productCommission = 0
			sql = "SELECT commission_fee from app_products WHERE ean=%s and marketplace_order_number=%s"
			value = (ean,order_number, )
			self.cursor.execute(sql,value)
			entry = self.cursor.fetchall()
			try:
				for e in entry:
					productCommission = e[0]
			except:
				productCommission = 0	
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
		self.cursor.close()
		return productCommission

	def calculateOrderProfit(self,order_number,price,marketplace_fees):
		self.opendb()
		net_profit = 0

		try:
			net_profit = None
			order_keepa_price = 0
			keepa_prices = []
			sql = "SELECT keepa_price from app_products WHERE marketplace_order_number=%s"
			value = (order_number, )
			self.cursor.execute(sql,value)
			entry = self.cursor.fetchall()
			for e in entry:
				keepa_prices.append(e[0])
			try:
				for i in range(len(keepa_prices)):
					order_keepa_price = order_keepa_price + keepa_prices[i]
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
			try:
				net_profit = float(price) - ((float(order_keepa_price)+float(marketplace_fees)))
			except:
				net_profit = None
				print(traceback.print_exc())
				# print("profit can not be calculated due to no matching EAN and keepa price from product table found.")
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
		self.cursor.close()
		return net_profit

	def testdb(self):
		self.opendb()
		# self.cursor.execute('SELECT marketplace_order_number from app_orders WHERE marketplace_order_number=?',"(`2011081954R2HI4313`)")
		order_number = '2011081954R2HI43d13'
		sql = "SELECT marketplace_order_number from app_orders WHERE marketplace_order_number=%s"
		value = (order_number, )
		self.cursor.execute(sql, value)
		entry = self.cursor.fetchone()
		if entry is not None:
			print("entry already exists")
		else:
			print("save the entry its a new entry")
		self.cursor.close()

	def testupdate(self):
		self.opendb()
		autobuy_id  = '111'
		amazon_order_number = '222'
		marketplace = '333'
		number_messages = '444'
		ordered_date = '555'
		sql = "UPDATE app_orders SET autobuy_id=%s,amazon_order_number=%s,marketplace=%s,number_messages=%s,ordered_date=%s,marketplace_fees=%s,autobuy_action=%s,autobuy_status=%s,date_created=%s,date_updated=%s,net_profit=%s,price=%s,email=%s,order_status=%s,amazon_price=%s,keepa_price=%s,refunded_price=%s WHERE marketplace_order_number=%s"
		value= (autobuy_id,amazon_order_number,marketplace,number_messages,ordered_date,marketplace_fees,autobuy_action,autobuy_status,date_created,date_updated,net_profit,price,email,order_status,amazon_price,keepa_price,marketplace_order_number,refunded_price)
		print("database: ",number_messages)
		self.cursor.execute(sql,value)
		self.db.commit()
		self.cursor.close()

	def saveOrders(self,autobuy_id,marketplace_order_number,amazon_order_number,marketplace,number_messages,ordered_date,marketplace_fees,autobuy_action,autobuy_status,date_created,date_updated,net_profit,price,email,order_status,amazon_price,keepa_price,refunded_price,catalog):
		self.opendb()
		entry = None
		try:
			sql = "SELECT marketplace_order_number from app_orders WHERE marketplace_order_number=%s"
			value = (marketplace_order_number, )
			self.cursor.execute(sql, value)
			entry = self.cursor.fetchone()
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
		
		if entry is not None:
			try:
				sql = "UPDATE app_orders SET autobuy_id=%s,amazon_order_number=%s,marketplace=%s,number_messages=%s,ordered_date=%s,marketplace_fees=%s,autobuy_action=%s,autobuy_status=%s,date_created=%s,date_updated=%s,net_profit=%s,price=%s,email=%s,order_status=%s,amazon_price=%s,keepa_price=%s,refunded_price=%s, catalog=%s WHERE marketplace_order_number=%s"
				value= (autobuy_id,amazon_order_number,marketplace,number_messages,ordered_date,marketplace_fees,autobuy_action,autobuy_status,date_created,date_updated,net_profit,price,email,order_status,amazon_price,keepa_price,refunded_price,catalog,marketplace_order_number)
				# print("database: ",number_messages)
				self.cursor.execute(sql,value)
				self.db.commit()
				print("successfully updated order details")
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
		else:
			try:
				sql = "INSERT into app_orders(autobuy_id,marketplace_order_number,amazon_order_number,marketplace,number_messages,ordered_date,marketplace_fees,autobuy_action,autobuy_status,date_created,date_updated,net_profit,price,email,order_status,amazon_price,keepa_price,refunded_price,catalog)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				value= (autobuy_id,marketplace_order_number,amazon_order_number,marketplace,number_messages,ordered_date,marketplace_fees,autobuy_action,autobuy_status,date_created,date_updated,net_profit,price,email,order_status,amazon_price,keepa_price,refunded_price,catalog)
				self.cursor.execute(sql,value)
				self.db.commit()
				print("successfully saved new order details")
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
		self.cursor.close()

	def saveProducts(self,marketplace_order_number,ean,asin,amazon_price,keepa_price,date_created,date_updated,productId,quantity,commission_fee,marketplace_order_state,net_profit,price,amazon_vat_rate,gmail_status,tracking_carrier,tracking_number,tracking_url,amazon_vat_number):
		self.opendb()
		try:
			sql = "SELECT * from app_products WHERE marketplace_order_number=%s AND productId=%s"
			value = (marketplace_order_number,productId, )
			self.cursor.execute(sql, value)
			entry = self.cursor.fetchall()
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
			
		if self.cursor.rowcount>0:
			try:
				self.cursor.execute("""UPDATE app_products SET ean=%s, asin=%s, amazon_price=%s, keepa_price=%s, date_created=%s, date_updated=%s, quantity=%s, commission_fee=%s, marketplace_order_state=%s, net_profit=%s, price=%s,amazon_vat_rate=%s,gmail_status=%s,tracking_number=%s,tracking_carrier=%s,tracking_url=%s,amazon_vat_number=%s WHERE marketplace_order_number=%s AND productId=%s;""",
				(ean,asin,amazon_price,keepa_price,date_created,date_updated,quantity,commission_fee,marketplace_order_state,net_profit,price,amazon_vat_rate,gmail_status,tracking_number,tracking_carrier,tracking_url,amazon_vat_number,marketplace_order_number,productId))
				self.db.commit()
				print("successfully updated product details")
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
		else:
			try:
				sql = "INSERT into app_products(marketplace_order_number,ean,asin,amazon_price,keepa_price,date_created,date_updated,productId,quantity,commission_fee,marketplace_order_state,net_profit,price,amazon_vat_rate,gmail_status,tracking_carrier,tracking_number,tracking_url,amazon_vat_number)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				value= (marketplace_order_number,ean,asin,amazon_price,keepa_price,date_created,date_updated,productId,quantity,commission_fee,marketplace_order_state,net_profit,price,amazon_vat_rate,gmail_status,tracking_carrier,tracking_number,tracking_url,amazon_vat_number)
				self.cursor.execute(sql,value)
				self.db.commit()
				print("successfully saved new product details")
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
		self.cursor.close()

	def saveOrderShipping(self,marketplace_order_number,shipping_marketplace_info,address1,address2,apartmentNumber,building,city,civility,companyName,country,firstname,lastname,instructions,placename,street,zipcode,mobilephone,phone,shippingFirstName,shippingLastName,date_created,date_updated):
		self.opendb()
		try:
			sql = "SELECT marketplace_order_number from app_order_shipping_address WHERE marketplace_order_number=%s"
			value = (marketplace_order_number, )
			self.cursor.execute(sql, value)
			entry = self.cursor.fetchone()
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
			
		if entry is not None:
			try:
				sql = "UPDATE app_order_shipping_address SET marketplace_order_number=%s,shipping_marketplace_info=%s,address1=%s,address2=%s,apartmentNumber=%s,building=%s,city=%s,civility=%s,companyName=%s,country=%s,firstname=%s,lastname=%s,instructions=%s,placename=%s,street=%s,zipcode=%s,mobilephone=%s,phone=%s,shippingFirstName=%s,shippingLastName=%s,date_created=%s,date_updated=%s WHERE marketplace_order_number=%s"
				value= (marketplace_order_number,shipping_marketplace_info,address1,address2,apartmentNumber,building,city,civility,companyName,country,firstname,lastname,instructions,placename,street,zipcode,mobilephone,phone,shippingFirstName,shippingLastName,date_created,date_updated,marketplace_order_number)
				self.cursor.execute(sql,value)
				self.db.commit()
				print("successfully updated shipping details")
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
		else:
			try:
				sql = "INSERT into app_order_shipping_address(marketplace_order_number,shipping_marketplace_info,address1,address2,apartmentNumber,building,city,civility,companyName,country,firstname,lastname,instructions,placename,street,zipcode,mobilephone,phone,shippingFirstName,shippingLastName,date_created,date_updated)VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
				value= (marketplace_order_number,shipping_marketplace_info,address1,address2,apartmentNumber,building,city,civility,companyName,country,firstname,lastname,instructions,placename,street,zipcode,mobilephone,phone,shippingFirstName,shippingLastName,date_created,date_updated)
				self.cursor.execute(sql,value)
				self.db.commit()
				print("successfully saved new shipping details")
			except:
				self.logError(self.get_line(), sys.exc_info()[1])
				print(traceback.print_exc())
		self.cursor.close()

	def getKeepaPrice(self,ean,catalog):
		# print("ean being searched for keepa price:", ean)
		self.opendb()
		price = 0
		try:
			self.cursor.fetchall()
		except:
			pass
		sql = "SELECT price_ttc from "+catalog+" WHERE ean=%s"
		value = (ean, )
		self.cursor.execute(sql, value)
		if self.cursor.rowcount>0:
			keepa_price = self.cursor.fetchall()	
			for a in keepa_price:
				price = a
		
		try:
			self.cursor.close()
		except:
			self.cursor.fetchall()
			self.cursor.close()

		return price

	def getamazonprice(self,marketplace_order_number):
		self.opendb()
		amazon_price = 0
		try:
			sql = "SELECT amazon_price from app_products WHERE marketplace_order_number=%s"
			value = (marketplace_order_number, )
			m_price = self.cursor.fetchone()
			if m_price is None:
				amazon_price = None
			else:
				for a in m_price:
					amazon_price = a
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
			amazon_price = 0
		self.cursor.close()
		return amazon_price
	
	def getmarketplaceprice(self,marketplace_order_number):
		self.opendb()
		marketplace_price = 0
		try:
			sql = "SELECT price from app_products WHERE marketplace_order_number=%s"
			value = (marketplace_order_number, )
			self.cursor.execute(sql, value)
			m_price = self.cursor.fetchone()
			if m_price is None:
				price = None
			else:
				for a in m_price:
					marketplace_price = a
		except:
			marketplace_price = 0
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
		self.cursor.close()
		return marketplace_price

	def gettotalcommission(self,marketplace_order_number):
		self.opendb()
		total_commission = 0
		try:
			sql = "SELECT marketplace_fees from app_orders WHERE marketplace_order_number=%s"
			value = (marketplace_order_number, )
			self.cursor.execute(sql,value)
			c_price = self.cursor.fetchone()
			if c_price is None:
				total_commission = None
			else:
				for a in c_price:
					total_commission = a
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
			total_commission = 0
		self.cursor.close()
		return total_commission

	def closedb(self):
		self.db.close()

	def extractAsin(self,ean,catalog):
		self.opendb()
		asin=None
		asin_value = 0
		try:
			sql = "SELECT asin FROM "+catalog+" WHERE ean=%s"
			value = (ean, )
			self.cursor.execute(sql, value)
			asin_value = self.cursor.fetchone()
			if asin_value is not None:
				for a in asin_value:
					asin = a
			else:
				asin=None
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())
		self.cursor.close()
		return asin


# if __name__ == '__main__':
# 	query =  DatabaseQueries()

