import requests
import os
import sys
import subprocess
from colorama import Fore, Style, Back
import logging


def choice():
    versions={"1.21.4":"https://piston-data.mojang.com/v1/objects/4707d00eb834b446575d89a61a11b5d548d8c001/server.jar",
              "1.21.3":"https://piston-data.mojang.com/v1/objects/45810d238246d90e811d896f87b14695b7fb6839/server.jar",
              "1.21.2":"https://piston-data.mojang.com/v1/objects/7bf95409b0d9b5388bfea3704ec92012d273c14c/server.jar",
              "1.21.1":"https://piston-data.mojang.com/v1/objects/59353fb40c36d304f2035d51e7d6e6baa98dc05c/server.jar"}

    print(Fore.YELLOW+"Choose from the list of available versions given below: ")
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
        cracked = input(Fore.YELLOW + "Do you want to configure the server as cracked(Yes/No): " + Style.RESET_ALL)
        if cracked == "Yes" or cracked == "yes" or cracked == "No" or cracked == "no":
            break
        else:
            print(Fore.RED + "Invalid choice, answer in 'Yes' or 'No'.")
            logging.error(f"User choose an invalid choice for cracked, user choice={cracked}")

    while True:
        try:
            Xms_ram = input(Fore.YELLOW + "How much minimum amount of ram(in megabytes) do you want to allocate to the server: " + Style.RESET_ALL)
            Xmx_ram = input(Fore.YELLOW + "How much maximum amount of ram(in megabytes) do you want to allocate to the server: " + Style.RESET_ALL)
            int(Xms_ram)
            int(Xmx_ram)
            break
        except ValueError:
            print(Fore.RED + "Please enter an integer value.")
            logging.error(f"User entered wrong input type in RAM Xms_ram={Xms_ram}, Xmx_ram={Xmx_ram}")
    version_url = versions[choice]
    return cracked, Xmx_ram, Xms_ram, version_url

def setup_directory():
    logging.info("Creating a directory for the server.")
    try:
        server_directory_path = os.path.join(os.path.dirname(__file__), "Minecraft_Server")
        if os.path.exists(server_directory_path):
            logging.info(f"{Fore.GREEN} Directory already exists. {Style.RESET_ALL}")
        else:
            os.makedirs(server_directory_path, exist_ok=True)
            logging.info(Fore.GREEN + "Directory created successfully."+ Style.RESET_ALL)
            os.chdir(server_directory_path)
            return server_directory_path
    except:
        logging.critical(Fore.RED + "Failed to create the directory.\nExiting the program" + Style.RESET_ALL)
        sys.exit()

def download(url):
    try:
        logging.info("Downloading the server.jar file, this could take a few minutes.\nPlease wait...")
        downloaded_contents = requests.get(url)
        with open("server.jar", "wb") as downloaded_file:
            downloaded_file.write(downloaded_contents.content)
        logging.info(Fore.GREEN + "server.jar downloaded successfully."+Style.RESET_ALL)
    except:
        logging.error(Fore.RED + "Failed to download the server.jar")

def configure_properties(cracked_choice):
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
    logging.info("Generating eula.txt file, auto setting 'eula=true', you can reffer to 'https://aka.ms/MinecraftEULA' to see the Minecraft EULA.")
    with open("eula.txt", "w") as eula_file:
        eula_file.write("eula=true")
        logging.info(Fore.GREEN + "eula.txt generated successfully"+Style.RESET_ALL)
        logging.info("Generating start_server.bat file.")
    with open("start_server.bat", "w") as bat_file:
        bat_file.write("java -Xmx" + Xmx_ram + "M -Xms" + Xms_ram + "M -jar server.jar nogui")
    logging.info(Fore.GREEN + "start_server.bat created successfully."+Style.RESET_ALL)

def ask_playit():
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
    logging.info(Fore.BLUE + "Starting the server."+Style.RESET_ALL)
    logging.debug(f"Changing current directory to {server_directory_path}")
    os.chdir(server_directory_path)
    logging.debug("Changed server directory successfully")
    logging.debug("Starting 'start_server.bat' in new cmd window")
    subprocess.run("start cmd.exe @cmd /k start_server.bat", shell=True)
    logging.info(Fore.GREEN + "Server started successfully.")
    print(Fore.BLUE + "You can access the server on your local machine by entering 'localhost' in the server address.")
    print(Fore.BLUE + "To access the server from another device, you need to port forward the server, you can use playit.gg to do that.")
    logging.info(Fore.GREEN + "Server setup completed successfully."+Style.RESET_ALL)
    print(Back.GREEN+"Note:\n1.You can start the server by running the 'start_server.bat' file located in the 'Minecraft_server' directory.")
    print(Back.GREEN+"2.You can confiugre the server settings by editing the 'server.properties' file located in the 'Minecraft_server' directory."+Style.RESET_ALL)
    input(Fore.YELLOW + "Press enter to exit the setup..."+Style.RESET_ALL)
    logging.info("Exiting the program.")
    sys.exit()