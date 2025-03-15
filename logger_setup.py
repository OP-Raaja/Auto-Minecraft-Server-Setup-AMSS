import logging
import os
from colorama import Fore, Style

def logger_setup():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    dir_path=os.path.dirname(__file__)

    file_handler = logging.FileHandler(f"{dir_path}\\log.log", "w")
    stream_handler = logging.StreamHandler()

    file_handler.setLevel(logging.DEBUG)
    stream_handler.setLevel(logging.INFO)

    file_formatter = CustomFormatter("%(asctime)s - %(levelname)s - %(message)s")
    console_formatter = logging.Formatter("%(message)s")

    stream_handler.addFilter(CustomErrorFilter())

    file_handler.setFormatter(file_formatter)
    stream_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

ANSI_sequences = [Fore.GREEN, Fore.RED, Fore.CYAN, Fore.YELLOW, Style.RESET_ALL]

def clean_message(message):
    for seq in ANSI_sequences:
            message = message.replace(seq, "")
    return message

class CustomFormatter(logging.Formatter):
    def format(self, record):
        original_msg = record.msg
        try:
            record.msg = clean_message(record.msg)
            return super().format(record)
        finally:
             record.msg = original_msg

class CustomErrorFilter(logging.Filter):
     def filter(self, record):
          if record.levelno == logging.ERROR:
            return getattr(record, "show_in_console", False)
          else:
               return True

