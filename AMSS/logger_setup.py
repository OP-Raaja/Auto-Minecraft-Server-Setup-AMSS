import logging
import os
from colorama import Fore, Style, Back
import sys

def logger_setup() -> None:

    logger: logging.Logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    '''
    Getting directory path to creating log files:
    The following line of code gets the directory path of the current file
    '''
    try:
        '''Gets the absolute path of the executable file or the python file.'''
        if getattr(sys, "frozen", False):
            path = os.path.dirname(os.path.abspath(sys.executable))
        else:
            path = os.path.dirname(__file__)
    except OSError as e:
        logging.critical(Fore.RED + f"Unable to get the file path\n{e}" + Style.RESET_ALL)
        input("Press enter to exit...")
        sys.exit()

    #Creating a file handler to manage log in files
    file_handler = logging.FileHandler(f"{path}\\logs.log", "w")
    file_handler.setLevel(logging.DEBUG)

    #This file formatter uses CustomFormatter class which removes colorama colour characters from the logs
    file_formatter = CustomFormatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    #Creating a stream handler for displaying info on console
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)

    stream_formatter = logging.Formatter("%(message)s")
    stream_handler.setFormatter(stream_formatter)

    #Adding CustomErrorFilter to the stream handler to only print intended error messages on the console
    stream_handler.addFilter(CustomErrorFilter())

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)


'''
This CustomFormatter class inherits the Formatter class form the logging module.
It cleans any ANSI sequence from the log message which is to be saved in the file.
It sends the log message to clean_message function to remove any ANSI sequence from the logs which is given by colorama.
This class is used in setting the file_handler format in file_formatter.
'''
class CustomFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        original_message = record.msg
        try:
            record.msg = clean_message(record.msg)
            return super().format(record)
        finally:
            record.msg = original_message

ANSI_seq: list[str] = [Fore.GREEN, Fore.RED, Fore.CYAN, Fore.YELLOW, Fore.BLUE, Back.GREEN, Style.RESET_ALL]

'''
Creating a new function to remove the ANSI sequence form logs before saving it to the log.log file.
This function runs a for loop which takes each ANSI sequence defined in ANSI_seq and replaces it with an empty string in the log message.
'''
def clean_message(msg: str) -> str:
    for seq in ANSI_seq:
        msg = msg.replace(seq, "")
    return msg

'''
Creating a new class CustomErrorFilter which filters out error messages from being displayed on the console unless explicitly allowed.
This class inherits from the logging.Filter class and overrides the filter method.
The filter method checks if the log record's level is ERROR and if it has an attribute 'show_in_console' set to True.
If both conditions are met, the error message will be shown in the console; otherwise, it will be filtered out.
'''
class CustomErrorFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelno == logging.ERROR:
            return getattr(record, "show_in_console", False)
        return True