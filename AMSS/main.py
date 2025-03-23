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
    print(Fore.GREEN + pyfiglet.figlet_format("Made by Shaurya Chauhan", font="contessa", justify="center") + Style.RESET_ALL)
    logging.info("Please report any bugs to the developer.")
    logging.info("Version: 1.0.2")
    logging.debug("Shown all intro elements successfully")

try:
    logger_setup.logger_setup()
    show_intro()
    choices: server_setup.ChoicesDict = server_setup.choice()
    server_directory_path: str = server_setup.setup_directory()
    server_setup.download(url = choices["version_url"])
    server_setup.configure_properties(choices)
    server_setup.create_start_server_batch_file(Xms_ram = choices["Xms_ram"], Xmx_ram = choices["Xmx_ram"])
    playit_choice: bool = server_setup.ask_playit()

    if playit_choice:
        setup_playit.download_playit(server_directory_path)
        setup_playit.run_playit(server_directory_path)
        input(Fore.YELLOW + "Press enter to start the server after you've completed the playit.gg setup..." + Style.RESET_ALL)
        server_setup.start_server(server_directory_path)
    else:
        print(Fore.GREEN + "Server setup completed successfully." + Style.RESET_ALL)
        print(Fore.YELLOW + "You can start the server by running the 'start_server.bat' file." + Style.RESET_ALL)
        input("Press enter to start the server...")
        server_setup.start_server(server_directory_path)
        
except KeyboardInterrupt:
    logging.critical(Fore.RED + "\nKeyboard Interrupt by the user\nExiting the program." + Style.RESET_ALL)
    sys.exit()
finally:
    logging.debug("Exiting the program")
    logging.debug("Resetting all coloroma styles")
    print(Style.RESET_ALL)
    logging.debug("All colorama styles resetted successfully")