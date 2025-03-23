import requests
import os
import sys
import subprocess
from colorama import Fore, Style, Back
from tqdm import tqdm
import logging
from typing import Dict, TypedDict, Literal


class ChoicesDict(TypedDict):
    version_url: str
    Xms_ram: int
    Xmx_ram: int
    difficulty: str
    cracked: str
    gamemode: str
    seed: int | str    #if user dosen't enter a seed then seed = ""

def choice() -> ChoicesDict:
    '''This function prompts the user to select various configuration options for the Minecraft server, 
    including the server version, RAM allocation, game mode, difficulty, cracked mode, and world seed. 
    It validates user input and returns a dictionary containing the selected choices.'''
    
    choices_dict: ChoicesDict = {
        "version_url": "",  
        "Xms_ram": 0,      
        "Xmx_ram": 0,
        "difficulty": "",      
        "cracked": "",      
        "gamemode": "",     
        "seed": ""
    }

    versions: Dict[str, str] = {"1.21.4":"https://piston-data.mojang.com/v1/objects/4707d00eb834b446575d89a61a11b5d548d8c001/server.jar",
              "1.21.3":"https://piston-data.mojang.com/v1/objects/45810d238246d90e811d896f87b14695b7fb6839/server.jar",
              "1.21.2":"https://piston-data.mojang.com/v1/objects/7bf95409b0d9b5388bfea3704ec92012d273c14c/server.jar",
              "1.21.1":"https://piston-data.mojang.com/v1/objects/59353fb40c36d304f2035d51e7d6e6baa98dc05c/server.jar",
              "1.21":"https://piston-data.mojang.com/v1/objects/450698d1863ab5180c25d7c804ef0fe6369dd1ba/server.jar"}

    logging.debug("Showing prompt -> Choose from the list of available versions given below: ")
    print(Fore.YELLOW + "Choose from the list of available versions given below: ")

    for key in versions.keys():
        print(Fore.BLUE+ key)
    while True:
        selected_version: str = input(Fore.YELLOW + "Enter a Minecraft version: " + Style.RESET_ALL)
        logging.debug(f"User entered: {selected_version}")

        if selected_version in versions.keys():
            print(Fore.GREEN + f"You've chosen version {selected_version}")
            break
        else:
            print(Fore.RED + "Invalid version, choose from the list of versions given above.")
            logging.error(f"Invalid version chosen by the user, user choosen version={selected_version}")

    choices_dict["version_url"] = versions[selected_version]

    def validate_choice(prompt: str, choice_name: Literal["cracked", "gamemode", "difficulty"], choices: list[str]) -> None:
        '''This function validates the user input based on the list of choices passed as a parameter'''

        while True:
            normalized_choices: list[str] = [choice.lower() for choice in choices]

            logging.debug(f"Showing prompt -> {prompt}")
            user_input: str = input(Fore.YELLOW + prompt + Style.RESET_ALL). strip()
            logging.debug(f"User entered: {user_input}")

            normalized_input = user_input.lower()

            if normalized_input in normalized_choices:
                choices_dict[choice_name] = normalized_input
                break
            else:
                print(Fore.RED + "Invalid Choice" + Style.RESET_ALL)
                logging.error(f"User entered invalid choice: {user_input}")

    while True:
        try:
            logging.debug("Showing prompt -> How much minimum amount of ram(in megabytes) do you want to allocate to the server: ")
            Xms_ram: int = int(input(Fore.YELLOW + "How much minimum amount of ram(in megabytes) do you want to allocate to the server: " + Style.RESET_ALL))
            logging.debug(f"User entered: {Xms_ram}")

            logging.debug("Showing prompt -> How much maximum amount of ram(in megabytes) do you want to allocate to the server: ")
            Xmx_ram: int = int(input(Fore.YELLOW + "How much maximum amount of ram(in megabytes) do you want to allocate to the server: " + Style.RESET_ALL))
            logging.debug(f"User entered: {Xmx_ram}")

            if Xms_ram > Xmx_ram:
                print(Fore.RED + "Minimum RAM cannot be greater than Maximum RAM." + Style.RESET_ALL)
                logging.error(f"Invalid RAM allocation: Xms_ram={Xms_ram}, Xmx_ram={Xmx_ram}")
            
            else:
                choices_dict["Xms_ram"] = Xms_ram
                choices_dict["Xmx_ram"] = Xmx_ram
                break

        except ValueError as e:
            print(Fore.RED + "Please enter an integer value.")
            logging.error(f"RAM value error: {e}")
    
    while True:
        try:
            seed: int | str = ""
            logging.debug("Showing prompt -> Enter seed for the world generation, leave this field blank if you want a random seed: ")
            seed = input("Enter seed for the world generation, leave this field blank if you want a random seed: ").strip()
            logging.debug(f"User entered: {seed}")
            if seed == "":
                logging.info(Fore.GREEN + "Random seed selected" + Style.RESET_ALL)
                choices_dict["seed"] = ""
                break
            seed = int(seed)
            if -9223372036854775808 <= seed <= 9223372036854775807:
                choices_dict["seed"] = seed
                break
            else:
                logging.error(f"{seed} is not a valid Minecraft seed, enter a seed ranging from -9223372036854775808 to 9223372036854775807", extra={"show_in_console": True})
        except ValueError:
            logging.error(Fore.RED + f"{seed} is not a valid Minecraft seed, enter an integer value" + Style.RESET_ALL, extra={"show_in_console": True})
    
    #Asking and validating user's choices
    validate_choice("Do you want to configure the server as cracked (Yes/No): ", "cracked", ["Yes", "yes", "No", "no"])
    validate_choice("Enter server gamemode (Survival, Creative, Adventure, Hardcore): ", "gamemode", ["Survival", "Creative", "Adventure", "Hardcore"])
    if choices_dict["gamemode"] != "hardcore":
        validate_choice("Enter game difficulty (peaceful, easy, normal, hard): ", "difficulty", ["Peaceful", "Easy", "Normal", "Hard"])

    logging.debug(f"Choices dict -> {choices_dict}")
    return choices_dict


def setup_directory() -> str:
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


def download(url: str) -> None:
    '''This function downloads the server.jar file'''

    try:
        logging.info("Downloading the server.jar file, this could take a few minutes.\nPlease wait...")
        response = requests.get(url, stream = True)
        file_size = int(response.headers.get("Content-Length", 0))
        chunk_size = 32768

        with open("server.jar", "ab") as downloaded_file:

            try:
                logging.debug("Creating progress bar")
                progress_bar: tqdm = tqdm(total = file_size, unit = "B", unit_scale = True)
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


def configure_properties(choices: ChoicesDict) -> None:
    '''This function configures the server properties file based on the user input form "choice()" funciton'''

    difficulty = choices["difficulty"]
    cracked = choices["cracked"]
    gamemode = choices["gamemode"]
    seed=choices["seed"]

    if gamemode == "hardcore":
        gamemode = ""
        hardcore = "true"
        difficulty = ""
    else:
        hardcore = "false"

    logging.info("Creating server.properties file.")
    if cracked == "yes":
        mode = "false"
    elif cracked == "no":
        mode = "true"
    
    with open("server.properties", "w") as server_properties:
        properties = [
            f"difficulty={difficulty}",
            f"gamemode={gamemode}",
            f"hardcore={hardcore}",
            f"level-seed={seed}",
            f"online-mode={mode}"
        ]
        server_properties.write("\n".join(properties))
    logging.info(Fore.GREEN + "server.properties file created successfully."+ Style.RESET_ALL)


def create_start_server_batch_file(Xmx_ram: int, Xms_ram: int) -> None:
    '''This function creates the batch file to start the server, the ammount of RAM is asked from the user in "choice()" funciton'''

    logging.info("Generating eula.txt file, auto setting 'eula=true', you can reffer to 'https://aka.ms/MinecraftEULA' to see the Minecraft EULA.")
    with open("eula.txt", "w") as eula_file:
        eula_file.write("eula=true")
        logging.info(Fore.GREEN + "eula.txt generated successfully"+Style.RESET_ALL)
        logging.info("Generating start_server.bat file.")
    with open("start_server.bat", "w") as bat_file:
        bat_file.write(f"java -Xmx{Xmx_ram}M -Xms{Xms_ram}M -jar server.jar nogui")
    logging.info(Fore.GREEN + "start_server.bat created successfully."+Style.RESET_ALL)


def ask_playit() -> bool:
    '''Asks user to download playit.gg'''

    logging.debug("Asking the user to download playit.gg")
    print(Fore.BLUE + "If you want to play with your friends on the server, you need to port forward the server.")
    print(Fore.BLUE + "You can use playit.gg to port forward the server.")
    print(Fore.BLUE + "If you've already done port forwarding, you can start the server now and select 'No' when asked to install playit.gg.")
    while True:
        choice: str = input(Fore.YELLOW + "Do you want to install playit.gg now? (Yes/No): " + Style.RESET_ALL).strip().lower()
        if choice == "yes":
            return True
        elif choice == "no":
            return False
        else:
            print(Fore.RED + "Invalid choice, please enter 'Yes' or 'No'.")
            logging.error(f"Player choose invalid choice for playit.gg download, user choice={choice}")


def start_server(server_directory_path: str) -> None:
    '''This function starts the server'''

    logging.info(Fore.BLUE + "Starting the server." + Style.RESET_ALL)

    logging.debug(f"Changing current directory to {server_directory_path}")
    os.chdir(server_directory_path)
    logging.debug("Changed server directory successfully")

    logging.debug("Starting 'start_server.bat' in new cmd window")
    subprocess.Popen("start cmd.exe /k start_server.bat", shell=True)
    logging.debug("start_server.bat ran successfully in new cmd window")

    print(Fore.BLUE + "You can access the server on your local machine by entering 'localhost' in the server address.")
    print(Fore.BLUE + "To access the server from another device, you need to port forward the server, you can use playit.gg to do that.")
    logging.info(Fore.GREEN + "Server setup completed successfully." + Style.RESET_ALL)
    print(Fore.BLUE + Back.GREEN + "Note:\n1.You can start the server by running the 'start_server.bat' file located in the 'Minecraft_server' directory." + Style.RESET_ALL)
    print(Fore.BLUE + Back.GREEN + "2.You can confiugre the server settings by editing the 'server.properties' file located in the 'Minecraft_server' directory." + Style.RESET_ALL)
    input(Fore.YELLOW + "Press enter to exit the setup..." + Style.RESET_ALL)
    logging.info("Exiting the program.")
    sys.exit()