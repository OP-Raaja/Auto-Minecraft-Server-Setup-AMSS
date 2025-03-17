import logger_setup
import server_setup
import setup_playit
import logging
import pyfiglet
from colorama import Fore, Style
import sys

def show_intro():
    '''Shows the intro elements'''

    logging.debug("Showing intro elements")
    print(pyfiglet.figlet_format("Auto Minecraft Server Setup", justify="center"))
    print(Fore.GREEN+pyfiglet.figlet_format("Made by Shaurya Chauhan", font="contessa", justify="center")+Style.RESET_ALL)
    logging.info("Please report any bugs to the developer.")
    logging.info("Version: 1.0.1")
    logging.debug("Shown all intro elements successfully")

try:
    logger_setup.logger_setup()
    show_intro()
    cracked_choice, max_ram, min_ram, version_url=server_setup.choice()
    server_directory_path=server_setup.setup_directory()
    server_setup.download(version_url)
    server_setup.configure_properties(cracked_choice)
    server_setup.create_start_server_batch_file(max_ram, min_ram)
    playit_choice=server_setup.ask_playit()

    if playit_choice:
        setup_playit.download_playit(server_directory_path)
        setup_playit.run_playit()
        input(Fore.YELLOW+"Press enter to start the server after you've completed the playit.gg setup..."+Style.RESET_ALL)
        server_setup.start_server(server_directory_path)
    else:
        print(Fore.GREEN+"Server setup completed successfully."+Style.RESET_ALL)
        print(Fore.YELLOW+"You can start the server by running the 'start_server.bat' file."+Style.RESET_ALL)
        input("Press enter to start the server...")
        server_setup.start_server(server_directory_path)
        
except KeyboardInterrupt:
    logging.critical(Fore.RED+"\nKeyboard Interrupt by the user\nExiting the program."+Style.RESET_ALL)
    sys.exit()
finally:
    logging.debug("Resetting all coloroma styles")
    print(Style.RESET_ALL)
    logging.debug("All colorama styles resetted successfully")