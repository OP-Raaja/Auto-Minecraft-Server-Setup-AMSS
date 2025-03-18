import requests
import os
import sys
import subprocess
from colorama import Fore, Style, Back
from tqdm import tqdm
import logging


def choice():
    '''This function takes the user's choice for Minecraft version, server type, and RAM allocation.'''


    versions={"1.21.4":"https://piston-data.mojang.com/v1/objects/4707d00eb834b446575d89a61a11b5d548d8c001/server.jar",
              "1.21.3":"https://piston-data.mojang.com/v1/objects/45810d238246d90e811d896f87b14695b7fb6839/server.jar",
              "1.21.2":"https://piston-data.mojang.com/v1/objects/7bf95409b0d9b5388bfea3704ec92012d273c14c/server.jar",
              "1.21.1":"https://piston-data.mojang.com/v1/objects/59353fb40c36d304f2035d51e7d6e6baa98dc05c/server.jar",
              "1.21":"https://piston-data.mojang.com/v1/objects/450698d1863ab5180c25d7c804ef0fe6369dd1ba/server.jar"}

    print(Fore.YELLOW + "Choose from the list of available versions given below: ")
    for key in versions.keys():
        print(Fore.BLUE+ key)
    while True:
        choice = input(Fore.YELLOW + "Enter a Minecraft version: " + Style.RESET_ALL)
        if choice in versions.keys():
            print(Fore.GREEN + f"You've chosen version {choice}")
            break
        else:
            print(Fore.RED + "Invalid version, choose from the list of versions given above.")
            logging.error(f"Invalid version chosen by the user, user choosen version={choice}")
    cracked = None

    while True:
        cracked = input(Fore.YELLOW + "Do you want to configure the server as cracked (Yes/No): " + Style.RESET_ALL)
        if cracked == "Yes" or cracked == "yes" or cracked == "No" or cracked == "no":
            break
        else:
            print(Fore.RED + "Invalid choice, answer in 'Yes' or 'No'.")
            logging.error(f"User choose an invalid choice for cracked, user choice={cracked}")

    while True:
        try:
            Xms_ram = input(Fore.YELLOW + "How much minimum amount of ram(in megabytes) do you want to allocate to the server: " + Style.RESET_ALL)
            Xmx_ram = input(Fore.YELLOW + "How much maximum amount of ram(in megabytes) do you want to allocate to the server: " + Style.RESET_ALL)

            if int(Xms_ram) > int(Xmx_ram):
                print(Fore.RED + "Minimum RAM cannot be greater than Maximum RAM." + Style.RESET_ALL)
                logging.error(f"Invalid RAM allocation: Xms_ram={Xms_ram}, Xmx_ram={Xmx_ram}")
                continue

            break
        except ValueError:
            print(Fore.RED + "Please enter an integer value.")
            logging.error(f"RAM value error Xms_ram={Xms_ram}, Xmx_ram={Xmx_ram}")

    version_url = versions[choice]
    return cracked, Xmx_ram, Xms_ram, version_url


def setup_directory():
    '''This funciton creates a new directory named "Minecraft_Server" in which the server will be set up'''

    logging.info("Creating a directory for the server.")
    try:
        if getattr(sys, "frozen", False):
            base_path = os.path.dirname(os.path.abspath(sys.executable))
        else:
            base_path = os.path.dirname(__file__)

        server_directory_path = os.path.join(base_path, "Minecraft_Server")

        if os.path.exists(server_directory_path):
            logging.info(Fore.GREEN + "Directory already exists." + Style.RESET_ALL)
        else:
            os.makedirs(server_directory_path, exist_ok=True)
            logging.info(Fore.GREEN + "Directory created successfully."+ Style.RESET_ALL)

        logging.debug(f"Changing current directory to {server_directory_path}")
        os.chdir(server_directory_path)
        logging.debug(f"Changed the current directory to {server_directory_path}")

        return server_directory_path
    
    except OSError as e:
        logging.critical(Fore.RED + "Failed to create the directory.\nExiting the program" + Style.RESET_ALL)
        logging.debug(f"Error:\n{e}")
        sys.exit()


def download(url):
    '''This function downloads the server.jar file'''

    try:
        logging.info("Downloading the server.jar file, this could take a few minutes.\nPlease wait...")
        response = requests.get(url, stream = True)
        file_size = int(response.headers.get("Content-Length", 0))
        chunk_size = 32768

        with open("server.jar", "ab") as downloaded_file:

            try:
                logging.debug("Creating progress bar")
                progress_bar = tqdm(total = file_size, unit = "B", unit_scale = True)
                logging.debug("Progress bar created successfully")

                logging.debug("Downloading contents of the file and writing it to the file")
                for data in response.iter_content(chunk_size):
                    downloaded_file.write(data)
                    progress_bar.update(len(data))
                logging.debug(f"All contents written successfully, downloaded file size = {file_size}B")
            finally:
                if progress_bar:
                    progress_bar.close()


        logging.info(Fore.GREEN + "server.jar downloaded successfully." + Style.RESET_ALL)
    except requests.RequestException as e:
        logging.error(Fore.RED + "Failed to download the server.jar:\n{e}" + Style.RESET_ALL)


def configure_properties(cracked_choice):
    '''This function configures the server properties file based on the user input form "choice()" funciton'''

    logging.info("Creating server.properties file.")
    if cracked_choice == "Yes" or cracked_choice == "yes":
        mode = "false"
    elif cracked_choice == "No" or cracked_choice == "no":
        mode = "true"
    else:
        logging.error(Fore.RED + "Invalid choice, please enter 'Yes' or 'No'.")
    with open("server.properties", "w") as server_properties:
        server_properties.write("online-mode=" + mode)
    logging.info(Fore.GREEN + "server.properties file created successfully."+ Style.RESET_ALL)


def create_start_server_batch_file(Xmx_ram, Xms_ram):
    '''This function creates the batch file to start the server, the ammount of RAM is asked from the user in "choice()" funciton'''

    logging.info("Generating eula.txt file, auto setting 'eula=true', you can reffer to 'https://aka.ms/MinecraftEULA' to see the Minecraft EULA.")
    with open("eula.txt", "w") as eula_file:
        eula_file.write("eula=true")
        logging.info(Fore.GREEN + "eula.txt generated successfully"+Style.RESET_ALL)
        logging.info("Generating start_server.bat file.")
    with open("start_server.bat", "w") as bat_file:
        bat_file.write("java -Xmx" + Xmx_ram + "M -Xms" + Xms_ram + "M -jar server.jar nogui")
    logging.info(Fore.GREEN + "start_server.bat created successfully."+Style.RESET_ALL)


def ask_playit():
    '''Asks user to download playit.gg'''

    logging.debug("Asking the user to download playit.gg")
    print(Fore.BLUE + "If you want to play with your friends on the server, you need to port forward the server.")
    print(Fore.BLUE + "You can use playit.gg to port forward the server.")
    print(Fore.BLUE + "If you've already done port forwarding, you can start the server now and select 'No' when asked to install playit.gg.")
    while True:
        choice = input(Fore.YELLOW + "Do you want to install playit.gg now? (Yes/No): " + Style.RESET_ALL)
        if choice == "Yes" or choice == "yes":
            return True
        elif choice == "No" or choice == "no":
            return False
        else:
            print(Fore.RED + "Invalid choice, please enter 'Yes' or 'No'.")
            logging.error(f"Player choose invalid choice for playit.gg download, user choice={choice}")


def start_server(server_directory_path):
    '''This function starts the server'''

    logging.info(Fore.BLUE + "Starting the server." + Style.RESET_ALL)

    logging.debug(f"Changing current directory to {server_directory_path}")
    os.chdir(server_directory_path)
    logging.debug("Changed server directory successfully")

    logging.debug("Starting 'start_server.bat' in new cmd window")
    subprocess.run("start cmd.exe @cmd /k start_server.bat", shell=True)
    logging.debug("start_server.bat ran successfully in new cmd window")

    print(Fore.BLUE + "You can access the server on your local machine by entering 'localhost' in the server address.")
    print(Fore.BLUE + "To access the server from another device, you need to port forward the server, you can use playit.gg to do that.")
    logging.info(Fore.GREEN + "Server setup completed successfully."+Style.RESET_ALL)
    print(Back.GREEN+"Note:\n1.You can start the server by running the 'start_server.bat' file located in the 'Minecraft_server' directory.")
    print(Back.GREEN+"2.You can confiugre the server settings by editing the 'server.properties' file located in the 'Minecraft_server' directory."+Style.RESET_ALL)
    input(Fore.YELLOW + "Press enter to exit the setup..."+Style.RESET_ALL)
    logging.info("Exiting the program.")
    sys.exit()