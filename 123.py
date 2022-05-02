import os

current_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
print(current_directory)
action = QAction(QIcon(os.path.join(current_directory, "icons", 
 "LogoSenara.png")),"&RiegoSenara", self.iface.mainWindow())