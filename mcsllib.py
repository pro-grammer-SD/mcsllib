from pathlib import Path
from urllib.request import urlretrieve
import subprocess

class ServerEntity:
    "ServerEntity Class"
    
    def __init__(self,wm: bool) -> str:
        """
        Init class.
        
        Parameters:
            `wm` parameter of type `bool` controls whether the welcome message should be displayed or not.
        
        Returns:
            `str`: The welcome message data type
        """
        
        if wm:
            print("Welcome from MCSL!\n")

    def launch(self, loader_type: str, gui: bool, min_mem: int, max_mem: int, online: bool, lgui: bool) -> str:
        """
        Launches a Minecraft server based on the specified loader type and configuration options.

        Parameters:
            loader_type (str): The type of server loader to use. Can be one of: - "normal": Official Mojang server - "fabric": Fabric loader server - "papermc": PaperMC server
            gui (bool): If True, launches the server with a GUI; if False, launches without a GUI.
            min_mem (int): The minimum amount of memory (in MB) allocated to the server.
            max_mem (int): The maximum amount of memory (in MB) allocated to the server.
            online (bool): If True, the server will run in online mode; if False, offline mode.
            lgui (bool): If True, runs a graphical launcher GUI; if False, proceeds with the command-line interface.

        Returns:
            str: A message indicating the result of the launch operation.
    """
    
        if lgui:
            lgui_entity = LGUIEntity()
            lgui_entity.load()
        else:       
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

            jar_file = Path(jar_files[loader_type])

            if not jar_file.is_file():
                urlretrieve(jar_urls[loader_type], jar_file)
                print(f"Downloaded {loader_type} server jar.")

            Path("eula.txt").write_text("eula=true\n")

            properties_file = Path("server.properties")
            if properties_file.is_file():
                properties = properties_file.read_text().splitlines()
                properties = [
                    line if not line.startswith("online-mode=") 
                    else f"online-mode={'true' if online else 'false'}" 
                    for line in properties
                ]
                properties_file.write_text("\n".join(properties) + "\n")

            runjar_cmd = f"java -Xmx{max_mem}M -Xms{min_mem}M -jar {jar_file}"
            
            if not gui:
                runjar_cmd += " nogui"
            else:
                subprocess.run(runjar_cmd, shell=True, text=True)

class LGUIEntity:
    """GUI Server Launcher Class"""    
    
    def __init__(self):
        print("Launching the launcher!") # welcome message

    def load(self): 
        """loads up the gui launcher"""
        
        import sys
        import mcsllib
        import psutil
        from PyQt6.QtWidgets import (
            QApplication, QWidget, QVBoxLayout, QPushButton, QCheckBox,
            QSlider, QLabel, QComboBox, QMessageBox
        )
        from PyQt6.QtCore import Qt, QThread

        class ServerThread(QThread):
            def __init__(self, server, loader_type, gui, min_mem, max_mem, online):
                super().__init__()
                self.server = server
                self.loader_type = loader_type
                self.gui = gui
                self.min_mem = min_mem
                self.max_mem = max_mem
                self.online = online

            def run(self):
                """triggers the launch"""
                
                self.server.launch(
                    loader_type=self.loader_type,
                    gui=self.gui,
                    min_mem=self.min_mem,
                    max_mem=self.max_mem,
                    online=self.online,
                    lgui=False       
                )

        class ServerLauncherGUI(QWidget):
            def __init__(self):
                super().__init__()
                self.server = mcsllib.ServerEntity(wm=False)
                self.init_ui()

            def init_ui(self):
                layout = QVBoxLayout()

                self.loader_label = QLabel("Select Loader Type:")
                layout.addWidget(self.loader_label)

                self.loader_combo = QComboBox()
                self.loader_combo.addItems(["papermc", "fabric", "normal"])
                layout.addWidget(self.loader_combo)

                self.gui_checkbox = QCheckBox("Enable GUI")
                self.gui_checkbox.setChecked(True)
                layout.addWidget(self.gui_checkbox)

                self.online_checkbox = QCheckBox("Enable Online Mode")
                self.online_checkbox.setChecked(True)
                layout.addWidget(self.online_checkbox)

                total_ram = psutil.virtual_memory().total // (1024 * 1024)

                self.min_mem_label = QLabel("Min Memory: 512 MB")
                layout.addWidget(self.min_mem_label)

                self.min_mem_slider = QSlider(Qt.Orientation.Horizontal)
                self.min_mem_slider.setMinimum(0)
                self.min_mem_slider.setMaximum(total_ram)
                self.min_mem_slider.setValue(512)
                self.min_mem_slider.valueChanged.connect(self.update_min_mem_label)
                layout.addWidget(self.min_mem_slider)

                self.max_mem_label = QLabel("Max Memory: 2048 MB")
                layout.addWidget(self.max_mem_label)

                self.max_mem_slider = QSlider(Qt.Orientation.Horizontal)
                self.max_mem_slider.setMinimum(0)
                self.max_mem_slider.setMaximum(total_ram)
                self.max_mem_slider.setValue(2048)
                self.max_mem_slider.valueChanged.connect(self.update_max_mem_label)
                layout.addWidget(self.max_mem_slider)

                self.launch_button = QPushButton("Launch Server")
                self.launch_button.clicked.connect(self.launch_server)
                layout.addWidget(self.launch_button)

                self.setLayout(layout)
                self.setWindowTitle("Minecraft Server Launcher")

            def update_min_mem_label(self, value):
                self.min_mem_label.setText(f"Min Memory: {value} MB")

            def update_max_mem_label(self, value):
                self.max_mem_label.setText(f"Max Memory: {value} MB")

            def launch_server(self):
                min_mem = self.min_mem_slider.value()
                max_mem = self.max_mem_slider.value()

                if min_mem > max_mem:
                    QMessageBox.warning(self, "Invalid Memory Settings", "Min Memory must be lower than Max Memory!")
                    return

                self.launch_button.setEnabled(False)
                self.server_thread = ServerThread(
                    self.server,
                    self.loader_combo.currentText(),
                    self.gui_checkbox.isChecked(),
                    min_mem,
                    max_mem,
                    self.online_checkbox.isChecked()
                )
                self.server_thread.finished.connect(lambda: self.launch_button.setEnabled(True))
                self.server_thread.start()

        app = QApplication(sys.argv)
        window = ServerLauncherGUI()
        window.show()
        app.exec()