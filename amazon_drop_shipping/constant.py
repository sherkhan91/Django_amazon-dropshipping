import requests

class Constants(object):

    '''Constant urls and proxy settings for marketplace, change accordingly when needed'''

    cdiscount_token_url = "https://sts.cdiscount.com/users/httpIssue.svc/?realm=https://wsvc.cdiscount.com/MarketplaceAPIService.svc"
    cdiscount_base_url = "https://wsvc.cdiscount.com/MarketplaceAPIService.svc"	
    url = "https://wsvc.cdiscount.com/MarketplaceAPIService.svc"
    rakuten_base_url = "https://sandbox.fr.shopping.rakuten.com/sales_ws?action="
    worten_order_url_lasthour = "https://worten-dev.mirakl.net/api/orders?start_date="
    worten_reset_order = "https://worten-dev.mirakl.net/api/orders?start_date=2011-01-01&max=100&paginate=true&offset="
    worten_discussions = "https://worten-dev.mirakl.net/api/inbox/threads"

    """example proxy """
    proxysetting = {'http': 'http://user:password@45.33.152.117:21242',
						'https': 'https://user:password@45.33.152.117:21242',
						'ftp': 'ftp://user:password@45.33.152.117:21242'} 

    ''' dataabse configuration files '''
    mhost = "192.168.0.1" # example if
    mdatabase = "database_name"
    muser = "databaselogin"
    mpassword ="database_password"
    mport  = "13526"

    ''' dataabse configuration files '''
    mhost = "192.168.0.1" # example if
    mdatabase = "database_name"
    muser = "databaselogin"
    mpassword ="database_password"
    mport  = "13526"

    ''' dataabse configuration files '''
     mhost = "192.168.0.1" # example if
    mdatabase = "database_name"
    muser = "databaselogin"
    mpassword ="database_password"
    mport  = "13526"

    testingaccounts = {
                "accounts":[
                                {
                                    "catalog1":{
                                                "cdiscount1":
                                                        {
                                                        "username":"cdiscount_user",
                                                        "password":"password",
                                                        "proxy":proxysetting
                                                        },
                                                "rakuten1":
                                                        {
                                                        "username":"rakuten_username",
                                                        "password":"password_token"
                                                        # "proxy":proxysetting
                                                        },
                                                "worten1":
                                                        {
                                                        "shopkey":'shopkey',
                                                        "proxy":proxysetting
                                                        }
                                                },
                                    # "catalog2":{
                                    #             "cdiscount2":
                                    #                     {
                                    #                     "username":"mymdin26-api",
                                    #                     "password":"Aqwzsxedc26.",
                                    #                     "proxy":proxysetting
                                    #                     },
                                    #             "rakuten2":
                                    #                     {
                                    #                     "username":"MDINpro",
                                    #                     "password":"e7b2d30e33c34259a362759c010bfb9e",
                                    #                     "proxy":proxysetting
                                    #                     },
                                    #             "worten2":
                                    #                     {
                                    #                     "shopkey":'2e87de07-6009-44ab-aaa5-84005c2b95e5',
                                    #                     "proxy":proxysetting
                                    #                     }
                                    #             }      
                                }
                            ]
                        }


    ''' Template dict to show that how to add multi accounts '''

    accountTemplate = {
                "accounts":[
                    {
                        "catalog1":{
                            "cdiscount1":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            },
                            "rakuten1":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            },
                            "worten1":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            }
                        },
                        "catalog2":{
                            "cdiscount2":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            },
                            "rakuten2":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            },
                            "worten2":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            }
                        },
                        "catalog3":{
                            "cdiscount3":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            },
                            "rakuten3":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            },
                            "worten3":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            }
                        },
                        "catalog4":{
                            "cdiscount4":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            },
                            "rakuten4":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            },
                            "worten4":{
                            "username":"cdiscountuser",
                            "password":"cdiscountpassword",
                            "proxy":"myproxy.com"
                            }
                        }
                    }
                ]
                }


    
   

    ''' Few class functions for debug and test purposes '''
    def __init__(self):
        print("this is constant constructor")
        pass
    
        #initialization of constant class
    
    def constantTest(self):
        print("this is constant test")

if __name__ == '__main__':
    myConstants = MarketplaceConstants()
    myConstants.constantTest()


