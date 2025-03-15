import requests
import os
import subprocess
import sys
from colorama import Fore, Style, Back
import logging

def download_playit():
    try:
        logging.info("Downloading playit.gg.\nPlease wait...")
        downloaded_contents = requests.get("https://github.com/playit-cloud/playit-agent/releases/download/v0.15.26/playit-windows-x86_64-signed.msi")
        with open("playit.msi", "wb") as downloaded_file:
            downloaded_file.write(downloaded_contents.content)
    except:
        logging.critical(Fore.RED + "Failed to download playit.gg" + Style.RESET_ALL)
        sys.exit()
    else:
        logging.info(Fore.GREEN + "playit.gg downloaded successfully." + Style.RESET_ALL)
    
    try:
        logging.info("Installing playit.gg")
        print(Fore.BLUE+"Follow the installation steps on the installer window which popped up on the screen.")
        logging.debug("Opening donwloaded playit.msi")
        result = subprocess.run(["msiexec", "/i", "playit.msi"], check=False)
        logging.debug("Playit.msi ran successfully")
        if result.returncode == 0:
            logging.info(Fore.GREEN+"Playit.gg installed successfully."+Style.RESET_ALL)
            os.remove("playit.msi")
        else:
            logging.error(Fore.RED + "An error occurred while installing playit.gg or the user cancelled the installation.")
            print(Fore.RED + "An error occurred while installing playit.gg or the user cancelled the installation.")
            os.remove("playit.msi")
            while True:
                choice = input(Fore.YELLOW + "Do you want to try again? (Yes/No): " + Style.RESET_ALL)
                if choice == "Yes" or choice == "yes":
                    download_playit()
                elif choice == "No" or choice == "no":
                    print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
                    sys.exit()
                else:
                    print("Invalid choice, enter 'Yes' or 'No'")
                    logging.error(f"User entered invalid choice for trying again installing playit.gg, user enter choice={choice}")
    except subprocess.SubprocessError as e:
        logging.error(Fore.RED + f"Failed to install Playit.gg\n{e}" + Style.RESET_ALL, extra="show_in_console")
        print(Fore.RED + f"Failed to install Playit.gg\n{e}" + Style.RESET_ALL)
    finally:
        if os.path.exists("playit.msi"):
            os.remove("playit.msi")

def run_playit():
    print(Back.GREEN + "After playit.gg is installed, please follow the steps given below to forward the port for the server."+Style.RESET_ALL)
    print(Fore.BLUE + "1. A link will appear on the console, copy it and paste it in any web browser or click on the link.")
    print(Fore.BLUE + "2. A page will open, you can create a new account or use a guest account under create new account.")
    print(Fore.BLUE + "3. You'll be prompted to add a new agent, click on continue and then click on add agent without changing any settings.")
    print(Fore.BLUE + "4. Wait for a few seconds, then you'll be prompted to create tunnel, click on that.")
    print(Fore.BLUE + "5. Under 'use shared ip' section, select the region to 'Global Anycast(free)' and under 'tunnel type, select 'Minecraft java(game)'.")
    print(Fore.BLUE + "6. Click on 'Add tunnel'.")
    print(Fore.BLUE + "7. The 'Shareable Address' is your server's IP address, copy it and share it with your friends to play on the server.")
    print(Fore.YELLOW + "Note: You can run playit.gg anytime to get the server's IP address, it's installed as a normal application on your system." + Style.RESET_ALL)

    input(Fore.YELLOW + "Press enter to continue after you've read and noted the steps given above..." + Style.RESET_ALL)
 
    if os.path.exists(r"C:\\Program Files\\playit_gg\\bin\\playit.exe"):
        print("Starting playit.gg")
        path = "C:\\Program Files\\playit_gg\\bin\\playit.exe"
        path = path.split("\\")
        final_path = path[0] + "\\"
        for part in path[1:]:
            quoted_part = f'"{part}"'
            final_path = os.path.join(final_path, quoted_part)
        subprocess.run(f"start {final_path}", shell=True)
    else:
        while True:
            print(Fore.RED + "Cannot locate playit.gg, please reinstall it in the default location.")
            choice = input(Fore.YELLOW + "Do you want to reinstall playit.gg now? (Yes/No): " + Style.RESET_ALL)
            if choice == "Yes" or choice == "yes":
                download_playit()
                run_playit()
            elif choice == "No" or choice == "no":
                print(Fore.RED + "Exiting the program." + Style.RESET_ALL)
                sys.exit()
            else:
                print(Fore.RED + "Invalid choice, exiting the program." + Style.RESET_ALL)