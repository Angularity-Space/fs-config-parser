import qdarkstyle, os, shutil, json
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QListWidgetItem
app = QtWidgets.QApplication([])
configparse = uic.loadUi("configparser.ui")
values = uic.loadUi('value.ui')
app.setStyleSheet(qdarkstyle.load_stylesheet())
def openButtonCFG():
    os.system("explorer " + savefolder)
configparse.show()
if os.name == "posix":
    if os.path.exists(f"/home/{os.getlogin()}/.config/unity3d/Haze Games/Fractal Space/FractalSave.dat"):
        savefolder = f"/home/{os.getlogin()}/.config/unity3d/Haze Games/Fractal Space/"
        savefolder = os.path.normpath(savefolder)
    else:
        configparse.configT.setText("Missing")
else:
    if os.path.exists(os.getenv("UserProfile") + "\AppData\LocalLow\Haze Games\Fractal Space"):
        savefolder = os.getenv("UserProfile") + "\AppData\LocalLow\Haze Games\Fractal Space"
        savefolder = os.path.normpath(savefolder)
    else:
        configparse.configT.setText("Missing")
configparse.configT.setText("Found")
configparse.openB.setDisabled(False)
configparse.groupBox_2.setDisabled(False)
configparse.openB.clicked.connect(openButtonCFG)
if not os.path.exists(savefolder + "\FractalSave.bk"):
    shutil.copyfile(savefolder + "/FractalSave.dat", savefolder + "/FractalSave.bk")
with open(savefolder + "/FractalSave.dat", "r") as cfg:
    data = json.load(cfg)
    for i in range(len(data['keys'])):
        configparse.keyE.addItem(QListWidgetItem(data['keys'][i]))
        cfg.close()

def editButton():
    values.show()
    values.keyL.setText(data['keys'][configparse.keyE.currentRow()])
    values.valueL.setText(data['values'][configparse.keyE.currentRow()])
def okayButton():
    data['values'][configparse.keyE.currentRow()] = values.valueL.text()
    with open(savefolder + "\FractalSave.dat", "w") as changedCFG: 
        json.dump(data, changedCFG, ensure_ascii=False)
        changedCFG.close()
    values.close()
configparse.changeB.clicked.connect(editButton)
configparse.keyE.itemClicked.connect(lambda: configparse.changeB.setDisabled(False))
values.cancel.clicked.connect(lambda: values.close())
values.OK.clicked.connect(okayButton)

app.exec()