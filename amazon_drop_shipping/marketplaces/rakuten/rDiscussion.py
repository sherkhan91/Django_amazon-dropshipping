import requests
from bs4 import BeautifulSoup
import sys
import pathlib
parentsDirectory = pathlib.Path(__file__).parent.parent.parent.absolute()
sys.path.append(str(parentsDirectory))
from database import DatabaseQueries
from utils import MarketPlaceUtils
from urllib3 import ProxyManager, PoolManager
import time
import json
import xmltodict
import os
from constant import Constants
import sys
sys.path.append(".")
from Logging_Program import myLogger
from inspect import currentframe

class RakutenDiscussions():

	def __init__(self, logger):
		self.logger = logger
		self.Queries = DatabaseQueries(logger=self.logger)
		self.filename = self.get_filename()

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



	def rakuten_mock_discussions(self):
		mock_response_string = """<getiteminfosresult xsi: schemaLocation = "http://fr.shopping.rakuten.com/res/schema/getiteminfos http://fr.shopping.rakuten.com/res/schema/getiteminfos/getiteminfos.2017-08-07. xsd "xmlns =" ​​http://fr.shopping.rakuten.com/res/schema/getiteminfos "xmlns: xsi =" http://www.w3.org/2001/XMLSchema-instance ">
		<request>
			<version> 2011-02-02 </version>
			<user> seller </user>
			<itemid> 1510836652 </itemid>
		</request>
		<response>
			<lastversion> 2011-02-02 </lastversion>
			<sellerid> 109698070 </sellerid>
			<item>
				<itemid> 1518036652 </itemid>
				<date> 02/10/2011 - 14:34 </date>
				<itemstatus> ON_HOLD </itemstatus>
				<shipped> 0 </shipped>
				<itemstate> CLAIMED_AMICABLE </itemstate>
				<itemstatelabel> <! [CDATA [Claim pending. Amicable treatment with the buyer]]> </itemstatelabel>
				<paymentstatus> Forthcoming </paymentstatus>
				<sellerscore />
				<claim>
				<creationdate> 02/15 / 2011-11: 46 </creationdate>
				<type> DAMAGED </type>
				<state> NEW </state>
				<amicable> Y </amicable>
				<claimcomment> <! [CDATA [damaged item, can you send me a new copy?]]> </claimcomment>
				</claim>
				<availableactions>
					<action>
					<title> Contact buyer1 </title>
					<description> <! [CDATA [To contact buyer1 about this item (shipping, operation, accessories ...)]]> </description>
					<actioncode> contactuseraboutitem </actioncode>
					</action>
					<action>
					<title> Contact Rakuten France </title>
					<description> <! [CDATA [To provide additional information regarding the buyer1 claim]]> </description>
					<actioncode> contactusaboutitem </actioncode>
					</action>
					<action>
					<title> Cancel the sale of this item </title>
					<description> <! [CDATA [To cancel the transaction and ask Rakuten France to reimburse buyer1]]> </description>
					<actioncode> cancelitem </actioncode>
					</action>
				</availableactions>
				<mail>
					<mailid>
					2906818102
					</mailid>
					<senddate>
					02/15 / 2011-11: 58
					</senddate>
					<sender>
					seller
					</sender>
					<recipient>
					Rakuten France
					</recipient>
					<object>
					<! [CDATA [Regarding the pending complaint (943746258/1510436652)]]>
					</object>
					<content>
					<! [CDATA [Hello, can you explain the procedure for returning a new item to the buyer? will I be reimbursed?]]>
					</content>
					<status>
					FEEL
					</status>
				</mail>
				<message>
					<sender>
					seller
					</sender>
					<recipient>
					Buyer1
					</recipient>
					<senddate>
					02/15 / 2011-11: 50
					</senddate>
					<content>
					<! [CDATA [Can you return the item to us at the address specified on the invoice? Sincerely,]]>
					</content>
					<status>
					FEEL
					</status>
				</message>
				<message>
					<sender>
					Buyer
					</sender>
					<recipient>
					seller
					</recipient>
					<senddate>
					02/15 / 2011-11: 47
					</senddate>
					<content>
					<! [CDATA [Thanks in advance for your help!]]>
					</content>
					<status>
					UNREAD
					</status>
				</message>
				<mail>
					<mailid> 2906185099 </mailid>
					<senddate> 02/15 / 2011-11: 46 </senddate>
					<sender> Rakuten France </sender>
					<recipient> seller </recipient>
					<object> <! [CDATA [Complaint on your sale (1551036652) - Rakuten France Customer Service]]> </object>
					<content> <! [CDATA [Hello seller,
					The buyer buyer19 has just made a complaint concerning your sale:
					Order: 943796258/9151036652 <http://fr.shopping.rakuten.com/purchase?action=itemmonitoring&itemid=1510346652>
					Item: Harry Potter And The Half-Blood Prince - Special Edition 2 Dvd (DVD Zone 2)
					Complaint: Damaged
					Comment: damaged article, can you send me a new copy?

					Buy-Sell Guaranteed]]> </content>
					<status> UNREAD </status>
				</mail>
				<itemlog>
					<creationdate> 02/15 / 2011-11: 46 </creationdate>
					<itemlogcode> AMICABLE_CLAIM_CREATION </itemlogcode>
					<description> <! [CDATA [BUYER1 has opened a complaint.]]> </description>
					<complement> <! [CDATA [Comment: damaged article, can you send me a new copy?]]> </complement>
				</itemlog>
				<itemlog>
					<creationdate> 02/15 / 2011-11: 08 </creationdate>
					<itemlogcode> ITEM_COMMITTED </itemlogcode>
					<description> <! [CDATA [You have confirmed the order and you have committed to deliver this item.]]> </description>
					<complement><!(CDATAogén L alborg> </complement>
				</itemlog>
				<itemlog>
					<creationdate> 02/15 / 2011-00: 08 </creationdate>
					<itemlogcode> PM_REMIND </itemlogcode>
					<description> <! [CDATA [An email reminder has been sent to you to confirm the order.]]> </description>
					<complement><!(CDATAogén L'alborg> </complement>
				</itemlog>
				<itemlog>
					<creationdate> 02/10 / 2011-14: 34 </creationdate>
					<itemlogcode> ITEM_REQUESTED </itemlogcode>
					<description> <! [CDATA [BUYER1 has ordered this item from you.]]> </description>
					<complement><!(CDATAogén L'alborg> </complement>
				</itemlog>
			</item>
		</response>
		</getiteminfosresult>"""

		return mock_response_string

	def mDiscussions(self,username,password,item_id,proxy=None):
		''' api call for getting discussions '''
		response = ''
		loginSeller = username
		#url = Constants.rakuten_base_url+"getiteminfos&login="+username+"&pwd="+password+"&version=2011-02-02&itemid=143008028"
		''' Dynamic item id  '''
		url = Constants.rakuten_base_url+"getiteminfos&login="+username+"&pwd="+password+"&version=2011-02-02&itemid="+str(item_id)
		payload={}
		headers = {
		}
		try:
			if proxy is not None:
				response = requests.request("GET", url, headers=headers, data=payload,proxies=proxy)
			else:
				response = requests.request("GET", url, headers=headers, data=payload)
		except:
			self.logError(self.get_line(), sys.exc_info()[1])
			print(traceback.print_exc())

		o = xmltodict.parse(response.text)
		jsonResponse =  json.dumps(o)
		resp_dict = json.loads(jsonResponse)
		print("Rakuten Discussions")
		subject =  resp_dict['getiteminfosresult']['response']['item']['itemstatelabel']
		disccussion_id = resp_dict['getiteminfosresult']['response']['item']['itemid'] 
		status = resp_dict['getiteminfosresult']['response']['item']['itemstatus']
		marketplace_order_number = resp_dict['getiteminfosresult']['response']['item']['itemid'] 
		marketplace = 'RAKUTEN'
		date_created =  resp_dict['getiteminfosresult']['response']['item']['date'] 
		date_created =  date_created[6:10]+"-"+date_created[3:5]+"-"+date_created[0:2]
		date_updated = resp_dict['getiteminfosresult']['response']['item']['date']
		date_updated =  date_updated[6:10]+"-"+date_updated[3:5]+"-"+date_updated[0:2]
		''' save discussions into discussions table '''
		self.Queries.saveDiscussions(subject,disccussion_id,status,marketplace_order_number,marketplace,date_created,date_updated)
		
		''' api call for getting messages '''
		for message in resp_dict['getiteminfosresult']['response']['item']['message']:
			disccussion_id = resp_dict['getiteminfosresult']['response']['item']['itemid']  #(reference to DISCUSSIONS TABLE)
			content =  message['content']
			sender =  message['sender']  #(can be SELLER or BUYER)
			if sender == loginSeller:
				sender = 'SELLER'
			else:
				sender = 'BUYER'
			mtimestamp = message['senddate']
			mtimestamp = mtimestamp[6:10]+"-"+mtimestamp[3:5]+"-"+mtimestamp[0:2]
			message_id = message['senddate']
			''' save messages for specific discussion into discussion table '''
			self.Queries.saveMessage(disccussion_id,content,sender,mtimestamp,message_id)
	

'''uncomment the following for testing individually '''
# if __name__ == '__main__':
# 	mDiscussions = RakutenDiscussions()
# 	mDiscussions.rakutendiscussions()
