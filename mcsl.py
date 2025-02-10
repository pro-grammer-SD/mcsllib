from urllib.request import urlretrieve
from pathlib import Path
import subprocess

class ServerEntity:
    
    def __init__(self):
        self.wm = "Welcome from MCSL!\n"
        self.xtr = "It may take quite a while to download to needed files. After downloading, kindly adjust the eula.txt setting of eula=false to eula=true and after that if you want the server to be offline, edit the server.properties setting of online-mode=true to online-mode=false. All server settings are in server.properties. Please do kindly enjoy!\n"
        print(self.wm, end=self.xtr)

    def launch(self, loader_type: str, gui: bool, min_mem: int, max_mem: int) -> str:

        if loader_type == "normal":
            jar_file = "server.jar"

            if not Path(jar_file).is_file():
                urlretrieve("https://piston-data.mojang.com/v1/objects/4707d00eb834b446575d89a61a11b5d548d8c001/server.jar", jar_file)
                print("Downloaded normal server jar.")
            command = f"java -Xmx{max_mem}M -Xms{min_mem}M -jar {jar_file}"

            if not gui:
                command += " nogui"
            subprocess.run(command, shell=True, text=True)
        elif loader_type == "fabric":
            jar_file = "fabric-server-mc.1.21.4-loader.0.16.10-launcher.1.0.1.jar"

            if not Path(jar_file).is_file():
                urlretrieve("https://meta.fabricmc.net/v2/versions/loader/1.21.4/0.16.10/1.0.1/server/jar", jar_file)
                print("Downloaded Fabric server jar.")
            command = f"java -Xmx{max_mem}M -Xms{min_mem}M -jar {jar_file}"

            if not gui:
                command += " nogui"
            subprocess.run(command, shell=True, text=True)

        elif loader_type == "papermc":
            paper_jar = "paper-1.21.4-144.jar"

            if not Path(paper_jar).is_file():
                urlretrieve("https://api.papermc.io/v2/projects/paper/versions/1.21.4/builds/144/downloads/paper-1.21.4-144.jar", paper_jar)
                print("Downloaded PaperMC server jar.")
            command = f"java -Xms{min_mem}M -Xmx{max_mem}M -XX:+AlwaysPreTouch -XX:+DisableExplicitGC -XX:+ParallelRefProcEnabled -XX:+PerfDisableSharedMem -XX:+UnlockExperimentalVMOptions -XX:+UseG1GC -XX:G1HeapRegionSize=8M -XX:G1HeapWastePercent=5 -XX:G1MaxNewSizePercent=40 -XX:G1MixedGCCountTarget=4 -XX:G1MixedGCLiveThresholdPercent=90 -XX:G1NewSizePercent=30 -XX:G1RSetUpdatingPauseTimePercent=5 -XX:G1ReservePercent=20 -XX:InitiatingHeapOccupancyPercent=15 -XX:MaxGCPauseMillis=200 -XX:MaxTenuringThreshold=1 -XX:SurvivorRatio=32 -Dusing.aikars.flags=https://mcflags.emc.gs -Daikars.new.flags=true -jar {paper_jar}"
            
            if not gui:
                command += " nogui"
            subprocess.run(command, shell=True, text=True)

        else:
            return "Invalid loader type."
