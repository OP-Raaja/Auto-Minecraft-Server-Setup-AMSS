import requests
import os
import subprocess
import sys
from colorama import Fore, Style, Back
import logging
from tqdm import tqdm


def download_playit(download_directory_path):
    '''This function download and install playit.gg'''

    try:
        logging.info("Downloading playit.gg.\nPlease wait...")
        response = requests.get("https://github.com/playit-cloud/playit-agent/releases/download/v0.15.26/playit-windows-x86_64-signed.msi", stream = True)
        file_size = int(response.headers.get("Content-Length"))
        chunk_size = 32768

        with open(os.path.join(download_directory_path, "playit.msi"), "ab") as downloaded_file:

            try:
                logging.debug("Creating progress bar")
                progress_bar = tqdm(total = file_size, unit = "B", unit_scale = True)
                logging.debug("Progress bar created successfully")

                for data in response.iter_content(chunk_size):
                    downloaded_file.write(data)
                    progress_bar.update(len(data))
                logging.debug(f"All contents written successfully, downloaded file size = {file_size}B")
            finally:
                if progress_bar:
                    progress_bar.close()

    except:
        logging.critical(Fore.RED + "Failed to download playit.gg" + Style.RESET_ALL)
        sys.exit()
    else:
        logging.info(Fore.GREEN + "playit.gg downloaded successfully." + Style.RESET_ALL)
    
    try:
        logging.info("Installing playit.gg")
        print(Fore.BLUE+"Follow the installation steps on the installer window which popped up on the screen." + Style.RESET_ALL)
        logging.debug("Opening donwloaded playit.msi")
        result = subprocess.run(["msiexec", "/i", os.path.join(download_directory_path, "playit.msi")], check=False)
        logging.debug("Playit.msi ran successfully")
        logging.debug(f"Installer returncode is {result.returncode}")

        if result.returncode == 0:
            logging.info(Fore.GREEN + "Playit.gg installed successfully." + Style.RESET_ALL)
            os.remove("playit.msi")
        else:
            logging.error(Fore.RED + "An error occurred while installing playit.gg or the user cancelled the installation.", extra={"show_in_console": True})
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
        logging.error(Fore.RED + f"Failed to install Playit.gg\n{e}" + Style.RESET_ALL, extra={"show_in_console": True})
    finally:
        if os.path.exists("playit.msi"):
            os.remove("playit.msi")


def run_playit():
    '''This function run installed playit.gg exe file located in the default install location'''

    logging.debug("Showing playit.gg setup instructions on console.")

    print(Back.GREEN + "After playit.gg is installed, please follow the steps given below to forward the port for the server."+Style.RESET_ALL)
    print(Fore.BLUE + "1. A link will appear on the console, copy it and paste it in any web browser or click on the link.")
    print(Fore.BLUE + "2. A page will open, you can create a new account or use a guest account under create new account.")
    print(Fore.BLUE + "3. You'll be prompted to add a new agent, click on continue and then click on add agent without changing any settings.")
    print(Fore.BLUE + "4. Wait for a few seconds, then you'll be prompted to create tunnel, click on that.")
    print(Fore.BLUE + "5. Under 'use shared ip' section, select the region to 'Global Anycast(free)' and under 'tunnel type, select 'Minecraft java(game)'.")
    print(Fore.BLUE + "6. Click on 'Add tunnel'.")
    print(Fore.BLUE + "7. The 'Shareable Address' is your server's IP address, copy it and share it with your friends to play on the server.")
    print(Fore.YELLOW + "Note: You can run playit.gg anytime to get the server's IP address, it's installed as a normal application on your system." + Style.RESET_ALL)
    
    logging.info("Shown all instructions successfully")
    
    input(Fore.YELLOW + "Press enter to continue after you've read and noted the steps given above..." + Style.RESET_ALL)
 
    if os.path.exists(r"C:\\Program Files\\playit_gg\\bin\\playit.exe"):
        logging.info("Starting playit.gg")

        path = "C:\\Program Files\\playit_gg\\bin\\playit.exe"
        path = path.split("\\")
        final_path = path[0] + "\\"
        for part in path[1:]:
            quoted_part = f'"{part}"'
            final_path = os.path.join(final_path, quoted_part)

        logging.debug("Starting playit.gg process")
        try:
            subprocess.run(f"start {final_path}", shell=True)
        except:
            logging.info(Fore.RED + "An error occured while starting playit.gg" + Style.RESET_ALL)

    else:
        while True:
            logging.error(Fore.RED + "Cannot locate playit.gg, please reinstall it in the default location." + Style.RESET_ALL, extra = {"show_in_console":True})
            logging.debug("Asking the user to reinstall playit.gg")

            while True:
                choice = input(Fore.YELLOW + "Do you want to reinstall playit.gg now? (Yes/No): " + Style.RESET_ALL)
                logging.debug(f"User choice: {choice}")

                if choice == "Yes" or choice == "yes":
                    logging.debug("Calling download_playit and run_playit function.")
                    download_playit()
                    run_playit()
                elif choice == "No" or choice == "no":
                    logging.info(Fore.RED + "Exiting the program." + Style.RESET_ALL)
                    sys.exit()
                else:
                    logging.info(Fore.RED + "Invalid choice, enter 'Yes' or 'No'" + Style.RESET_ALL)