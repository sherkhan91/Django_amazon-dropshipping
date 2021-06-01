import requests
import time
import sys
import pathlib
import sys
import os
from bs4 import BeautifulSoup
from inspect import currentframe
from pydantic import BaseModel, EmailStr
from database import DatabaseQueries
from utils import MarketPlaceUtils
from constant import Constants
from typing import Optional
from Logging_Program import myLogger
import traceback

sys.path.append(".")
parentsDirectory = pathlib.Path(__file__).parent.parent.parent.absolute()
sys.path.append(str(parentsDirectory))


# import discussions
class CdiscountOrder():

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
        ''' this is to get file name for logger to better identify the error '''
        return sys.argv[0]

    def get_line(self):
        ''' getting line where error occured will be used later '''
        cf = currentframe()
        return str(cf.f_back.f_lineno)



    def cDiscountCall(self,convertedAuthString,catalog,proxyUrls=None):
        response = 0  #variable decalartion
        token = 0
        payload={}
        headers = {
          'Authorization': 'Basic %s'%convertedAuthString}

        try:
            if proxyUrls is not None:
                response = requests.request("GET", Constants.cdiscount_token_url, headers=headers, data=payload,proxies=proxyUrls)
            else:
                response = requests.request("GET", Constants.cdiscount_token_url, headers=headers, data=payload)

            xmlText = BeautifulSoup(response.text, features="lxml")
            token = xmlText.html.body.string
            print("here is token:",token)
        except:
            self.logError(self.get_line(), sys.exc_info()[1])
            print(traceback.print_exc())

        time.sleep(3)


        payload="<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">\n    <s:Body>\n        <GetOrderList xmlns=\"http://www.cdiscount.com\">\n            <headerMessage xmlns:a=\"http://schemas.datacontract.org/2004/07/Cdiscount.Framework.Core.Communication.Messages\" xmlns:i=\"http://www.w3.org/2001/XMLSchema-instance\">\n                <a:Context>\n                    <a:CatalogID>1</a:CatalogID>\n                    <a:CustomerPoolID>1</a:CustomerPoolID>\n                    <a:SiteID>100</a:SiteID>\n                </a:Context>\n                <a:Localization>\n                    <a:Country>Fr</a:Country>\n                    <a:Currency>Eur</a:Currency>\n                    <a:DecimalPosition>2</a:DecimalPosition>\n                    <a:Language>Fr</a:Language>\n                </a:Localization>\n                <a:Security>\n                    <a:DomainRightsList i:nil=\"true\" />\n                    <a:IssuerID i:nil=\"true\" />\n                    <a:SessionID i:nil=\"true\" />\n                    <a:SubjectLocality i:nil=\"true\" />\n                    <a:TokenId>"+token+"</a:TokenId>\n                    <a:UserName i:nil=\"true\" />\n                </a:Security>\n                <a:Version>1.0</a:Version>\n            </headerMessage>\n            <orderFilter xmlns:i=\"http://www.w3.org/2001/XMLSchema-instance\">\n                <BeginCreationDate>"+self.Utils.cdiscountGetLastHourTime()+"</BeginCreationDate>\n\n               <FetchOrderLines>true</FetchOrderLines>\n                <States>\n                    <OrderStateEnum>CancelledByCustomer</OrderStateEnum>\n                    <OrderStateEnum>WaitingForSellerAcceptation</OrderStateEnum>\n                    <OrderStateEnum>AcceptedBySeller</OrderStateEnum>\n                    <OrderStateEnum>PaymentInProgress</OrderStateEnum>\n                    <OrderStateEnum>WaitingForShipmentAcceptation</OrderStateEnum>\n                    <OrderStateEnum>Shipped</OrderStateEnum>\n                    <OrderStateEnum>RefusedBySeller</OrderStateEnum>\n                    <OrderStateEnum>AutomaticCancellation</OrderStateEnum>\n                    <OrderStateEnum>PaymentRefused</OrderStateEnum>\n                    <OrderStateEnum>ShipmentRefusedBySeller</OrderStateEnum>\n                    <OrderStateEnum>RefusedNoShipment</OrderStateEnum>\n                </States>\n            </orderFilter>\n        </GetOrderList>\n    </s:Body>\n</s:Envelope>"
        headers = {
          'Content-Type': 'text/xml;charset=UTF-8',
          'SoapAction': 'http://www.cdiscount.com/IMarketplaceAPIService/GetOrderList',
          'Authorization': 'Basic %s'%convertedAuthString		}

        try:
            if proxyUrls is not None:
                response = requests.request("POST", Constants.cdiscount_base_url, headers=headers, data=payload, proxies=proxyUrls)
            else:
                response = requests.request("POST", Constants.cdiscount_base_url, headers=headers, data=payload)

            string_xml = response.content

            print("Cdiscount Orders")
            self.parseCdiscountResponse(string_xml, catalog)
        except:
            self.logError(self.get_line(), sys.exc_info()[1])
            print(traceback.print_exc())

    def parseCdiscountResponse(self,string_xml,catalog):

        soup = BeautifulSoup(string_xml,'xml')
        asin = 'FAKEASIN123'
        order_status = 0

        count = 0
        email = 0
        product_price_array = []

        print("length of orders: ", str(len(soup.OrderList)))
        """Parsing the XML response to appropriate fields """
        for order in soup.OrderList:
            for OrderLine in order.OrderLineList:
                marketplace_order_number = order.OrderNumber.get_text()
                ean = OrderLine.ProductEan.get_text()
                try:
                    asin = self.Queries.extractAsin(ean,catalog)
                except:
                    self.logError(self.get_line(), sys.exc_info()[1])
                    print(traceback.print_exc())
                amazon_price = None
                keepa_price = self.Queries.getKeepaPrice(ean,catalog)
                product_price_array.append(keepa_price)
                date_created = order.CreationDate.get_text()[0:10] # only availabe for whole order cdiscount
                date_updated = order.LastUpdatedDate.get_text()[0:10]  # only availabe for whole order cdiscount
                productId =  OrderLine.ProductId.get_text()
                quantity = OrderLine.Quantity.get_text()
                commission_fee = 0 # as not provided by cdiscount api for individual product
                marketplace_order_state =  OrderLine.AcceptationState.get_text()
                price =  OrderLine.PurchasePrice.get_text()
                amazon_vat_rate = None
                gmail_status = None
                tracking_carrier = None # unknown later will be changed e.g  bluecare
                tracking_number = None # as initially we don't know
                tracking_url = None # may be we just put bluecare
                amazon_vat_number = None
                net_profit = self.Utils.calculateProductProfit(keepa_price,price,commission_fee) # we don't have commission in cdiscount so we don't calculate

                '''saving the product information into product table'''
                self.Queries.saveProducts(marketplace_order_number,ean,asin,amazon_price,keepa_price,
                date_created,date_updated,productId,quantity,commission_fee,marketplace_order_state,
                net_profit,price,amazon_vat_rate,gmail_status,tracking_carrier,tracking_number,tracking_url,amazon_vat_number)


            autobuy_id  = None
            marketplace_order_number =   order.OrderNumber.get_text()
            amazon_order_number = None # as this can be filled after placing order
            marketplace  = "CDISCOUNT"
            number_messages = self.Queries.getMessageCount(marketplace_order_number) # number of message, against this order number
            ordered_date = order.CreationDate.get_text()[0:10]
            marketplace_fees = order.SiteCommissionPromisedAmount.get_text()
            autobuy_action = None # it will be reviewed, accepted, refused
            autobuy_status = None # accepted, shipped etc
            date_created = order.CreationDate.get_text()[0:10]
            date_updated = order.LastUpdatedDate.get_text()[0:10]
            price =  order.ValidatedTotalAmount.get_text()
            email = order.Customer.Email.get_text()
            if len(email) == 0:
                email = order.Customer.EncryptedEmail.get_text()
            order_status = order.OrderState.get_text()
            ''' checking if order is active or history '''
            if order_status == 'WaitingForSellerAcceptation':
                order_status =  'ACTIVE'
            elif order_status == 'AcceptedBySeller':
                order_status =  'ACTIVE'
            elif order_status == 'PaymentInProgress':
                order_status =  'ACTIVE'
            else:
                order_status = 'HISTORY'
            amazon_price = None  # autobuy job will fill it
            keepa_price = self.Utils.CalculateKeepaPrice(product_price_array)
            refunded_price = None
            net_profit = self.Queries.calculateOrderProfit(marketplace_order_number,price,marketplace_fees)
            

            ''' saving order details into order table '''
            self.Queries.saveOrders(autobuy_id,marketplace_order_number,amazon_order_number,
            marketplace,number_messages,ordered_date,marketplace_fees,autobuy_action,autobuy_status,
            date_created,date_updated,net_profit,price,email,order_status,amazon_price,keepa_price,refunded_price,catalog)


            marketplace_order_number = order.OrderNumber.get_text()
            shipping_marketplace_info =  None # couldn't find similar field in cdiscount + ben told its optional
            address1 = order.ShippingAddress.Street.get_text()
            address2 = order.ShippingAddress.Address2.get_text()
            apartmentNumber = order.ShippingAddress.ApartmentNumber.get_text()
            building = order.ShippingAddress.Building.get_text()
            city =  order.ShippingAddress.City.get_text()
            civility = order.ShippingAddress.Civility.get_text()
            companyName = order.ShippingAddress.CompanyName.get_text()
            country = order.ShippingAddress.Country.get_text()
            firstname = order.ShippingAddress.FirstName.get_text()
            lastname = order.ShippingAddress.LastName.get_text()
            instructions = order.ShippingAddress.Instructions.get_text()
            placename = order.ShippingAddress.PlaceName.get_text()
            street = order.ShippingAddress.Street.get_text()
            zipcode = order.ShippingAddress.ZipCode.get_text()
            mobilephone = order.Customer.MobilePhone.get_text()
            phone =  order.Customer.Phone.get_text()
            shippingFirstName =  order.ShippingAddress.FirstName.get_text()
            shippingLastName =  order.ShippingAddress.LastName.get_text()
            date_created =  order.CreationDate.get_text()[0:10]
            date_updated = order.LastUpdatedDate.get_text()[0:10]

            ''' saving shipping details'''
            self.Queries.saveOrderShipping(marketplace_order_number,shipping_marketplace_info,address1,address2,apartmentNumber,building,city,civility,companyName,country,firstname,lastname,instructions,placename,street,zipcode,mobilephone,phone,shippingFirstName,shippingLastName,date_created,date_updated)

            count = count+1

    def cdiscountResetOrders(self,convertedAuthString,catalog,proxyUrls=None):
        response = 0  #variable decalartion
        token = 0
        '''call to get token for fetching order info '''
        payload={}
        headers = {
          'Authorization': 'Basic %s'%convertedAuthString}

        try:
            if proxyUrls is not None:
                response = requests.request("GET", Constants.cdiscount_token_url, headers=headers, data=payload,proxies=proxyUrls)
            else:
                response = requests.request("GET", Constants.cdiscount_token_url, headers=headers, data=payload)

            xmlText = BeautifulSoup(response.text, features="lxml")
            token = xmlText.html.body.string
            print("here is token:",token)
        except:
            self.logError(self.get_line(), sys.exc_info()[1])
            print(traceback.print_exc())



        time.sleep(3)


        '''call for fetching order info '''
        payload="<s:Envelope xmlns:s=\"http://schemas.xmlsoap.org/soap/envelope/\">\n    <s:Body>\n        <GetOrderList xmlns=\"http://www.cdiscount.com\">\n            <headerMessage xmlns:a=\"http://schemas.datacontract.org/2004/07/Cdiscount.Framework.Core.Communication.Messages\" xmlns:i=\"http://www.w3.org/2001/XMLSchema-instance\">\n                <a:Context>\n                    <a:CatalogID>1</a:CatalogID>\n                    <a:CustomerPoolID>1</a:CustomerPoolID>\n                    <a:SiteID>100</a:SiteID>\n                </a:Context>\n                <a:Localization>\n                    <a:Country>Fr</a:Country>\n                    <a:Currency>Eur</a:Currency>\n                    <a:DecimalPosition>2</a:DecimalPosition>\n                    <a:Language>Fr</a:Language>\n                </a:Localization>\n                <a:Security>\n                    <a:DomainRightsList i:nil=\"true\" />\n                    <a:IssuerID i:nil=\"true\" />\n                    <a:SessionID i:nil=\"true\" />\n                    <a:SubjectLocality i:nil=\"true\" />\n                    <a:TokenId>"+token+"</a:TokenId>\n                    <a:UserName i:nil=\"true\" />\n                </a:Security>\n                <a:Version>1.0</a:Version>\n            </headerMessage>\n            <orderFilter xmlns:i=\"http://www.w3.org/2001/XMLSchema-instance\">\n                <BeginCreationDate>2011-12-01T00:00:00.00</BeginCreationDate>\n\n                <FetchOrderLines>true</FetchOrderLines>\n                <States>\n                    <OrderStateEnum>CancelledByCustomer</OrderStateEnum>\n                    <OrderStateEnum>WaitingForSellerAcceptation</OrderStateEnum>\n                    <OrderStateEnum>AcceptedBySeller</OrderStateEnum>\n                    <OrderStateEnum>PaymentInProgress</OrderStateEnum>\n                    <OrderStateEnum>WaitingForShipmentAcceptation</OrderStateEnum>\n                    <OrderStateEnum>Shipped</OrderStateEnum>\n                    <OrderStateEnum>RefusedBySeller</OrderStateEnum>\n                    <OrderStateEnum>AutomaticCancellation</OrderStateEnum>\n                    <OrderStateEnum>PaymentRefused</OrderStateEnum>\n                    <OrderStateEnum>ShipmentRefusedBySeller</OrderStateEnum>\n                    <OrderStateEnum>RefusedNoShipment</OrderStateEnum>\n                </States>\n            </orderFilter>\n        </GetOrderList>\n    </s:Body>\n</s:Envelope>"
        headers = {
        'Content-Type': 'text/xml;charset=UTF-8',
        'SoapAction': 'http://www.cdiscount.com/IMarketplaceAPIService/GetOrderList',
        'Authorization': 'Basic %s'%convertedAuthString
                }

        try:
            if proxyUrls is not None:
                response = requests.request("POST", Constants.cdiscount_base_url, headers=headers, data=payload,proxies=proxyUrls)
            else:
                response = requests.request("POST", Constants.cdiscount_base_url, headers=headers, data=payload)
            print("encoding : ", response.encoding)
            self.parseCdiscountResponse(response.text,catalog)
        except:
            self.logError(self.get_line(), sys.exc_info()[1])
            print(traceback.print_exc())
            
           


    # return True # if wish to return something


'''uncomment the following for testing individually '''
# if __name__ == '__main__':

# 	mOrder =  CdiscountOrder()
# 	# mOrder.cDiscountCall()
# 	mOrder.cdiscountResetCall()
