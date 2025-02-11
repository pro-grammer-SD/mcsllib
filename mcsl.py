from urllib.request import urlretrieve
from pathlib import Path
import subprocess

class ServerEntity:
    
    def __init__(self):
        print("Welcome from MCSL!\n")

    def launch(self, loader_type: str, gui: bool, min_mem: int, max_mem: int, online: bool) -> str:
        jar_urls = {
            "normal": "https://piston-data.mojang.com/v1/objects/4707d00eb834b446575d89a61a11b5d548d8c001/server.jar",
            "fabric": "https://meta.fabricmc.net/v2/versions/loader/1.21.4/0.16.10/1.0.1/server/jar",
            "papermc": "https://api.papermc.io/v2/projects/paper/versions/1.21.4/builds/144/downloads/paper-1.21.4-144.jar",
        }
        
        jar_files = {
            "normal": "server.jar",
            "fabric": "fabric-server-mc.1.21.4-loader.0.16.10-launcher.1.0.1.jar",
            "papermc": "paper-1.21.4-144.jar",
        }
        
        if loader_type not in jar_urls:
            return "Invalid loader type."

        jar_file = jar_files[loader_type]

        if not Path(jar_file).is_file():
            urlretrieve(jar_urls[loader_type], jar_file)
            print(f"Downloaded {loader_type} server jar.")

        # Update eula.txt to accept EULA
        eula_file = Path("eula.txt")
        eula_file.write_text("eula=true\n")

        # Modify server.properties for online mode
        properties_file = Path("server.properties")
        if properties_file.is_file():
            properties = properties_file.read_text().splitlines()
            properties = [line if not line.startswith("online-mode=") else f"online-mode={'true' if online else 'false'}" for line in properties]
            properties_file.write_text("\n".join(properties) + "\n")

        # Construct Java command
        command = f"java -Xmx{max_mem}M -Xms{min_mem}M -jar {jar_file}"
        if not gui:
            command += " nogui"

        subprocess.run(command, shell=True, text=True)
