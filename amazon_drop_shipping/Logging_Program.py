import logging

class myLogger():
    def __init__(self):
        print("this is logger initialization....")
        self.logger =  logging.getLogger(__name__)
        self.logger = logging.getLogger('mylogger')


        # create handlers
        f_handler =  logging.FileHandler('logfile.log')
        f_handler.setLevel(logging.ERROR)

        # create a format and add it to handler
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        f_handler.setFormatter(f_format)

        # add handlers to loggers
        self.logger.addHandler(f_handler)

    def logevent(self, input_error_string):
        self.logger.error(input_error_string)

