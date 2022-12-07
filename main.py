import os, shutil, json, qdarkstyle, sys, webbrowser
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QListWidgetItem, QFileDialog, QMessageBox
from PyQt6.QtGui import QFont, QFontDatabase

app = QtWidgets.QApplication([])
ui = uic.loadUi(r"E:\Codes\RC\FSCP\main.ui")
edit = uic.loadUi(r"E:\Codes\RC\FSCP\value.ui")
app.setStyleSheet(qdarkstyle.load_stylesheet())
families = QFontDatabase.applicationFontFamilies(QFontDatabase.addApplicationFont('segoe_ui_var.ttf'))
if os.name == "posix":
    if os.path.exists(f"/home/{os.getlogin()}/.config/unity3d/Haze Games/Fractal Space/FractalSave.dat"):
        defaultFolder = f"/home/{os.getlogin()}/.config/unity3d/Haze Games/Fractal Space/"
        defaultFolder = os.path.normpath(defaultFolder)
        ui.folderStatus.setText("Found")
    else:
        ui.folderStatus.setText("Not found")
else:
    if os.path.exists(os.getenv("UserProfile") + "\AppData\LocalLow\Haze Games\Fractal Space"):
        defaultFolder = os.getenv("UserProfile") + "\AppData\LocalLow\Haze Games\Fractal Space"
        defaultFolder = os.path.normpath(defaultFolder)
        ui.folderStatus.setText("Found")
    else:
        ui.folderStatus.setText("Not found")

def selfile():
    global save, data
    save = QFileDialog.getOpenFileName(None, "Fractal Save", defaultFolder, "Data file (*.dat)")
    if save == '':
        pass
    else:
        try:
            with open(save[0], "r") as cfg:
                data = json.load(cfg)
                for i in range(len(data['keys'])):
                    ui.content.addItem(QListWidgetItem(data['keys'][i]))
                    cfg.close()
        except json.decoder.JSONDecodeError:
            dialog = QMessageBox()
            dialog.setWindowTitle("Error")
            dialog.setIcon(QMessageBox.Icon.Critical)
            dialog.setText("JSON Decoder Error! Error code: 15")
            dialog.exec()
        except KeyError:
            dialog = QMessageBox()
            dialog.setWindowTitle("Error")
            dialog.setIcon(QMessageBox.Icon.Critical)
            dialog.setText("Reading failed! Error code: 16")
            dialog.exec()           
        except FileNotFoundError:
            pass                 
if not os.path.exists(defaultFolder + "\FractalSave.bk"):
    shutil.copyfile(defaultFolder + "/FractalSave.dat", defaultFolder + "/FractalSave.bk")
def editButton():
    edit.show()
    edit.keyL.setText(data['keys'][ui.content.currentRow()])
    edit.valueL.setText(data['values'][ui.content.currentRow()])
def okayButton():
    data['values'][ui.content.currentRow()] = edit.valueL.text()
    with open(defaultFolder + "\FractalSave.dat", "w") as changedCFG: 
        json.dump(data, changedCFG, ensure_ascii=False)
        changedCFG.close()
    edit.close()

def requestSave():
    shutil.copyfile(defaultFolder + "/FractalSave.dat", defaultFolder + "/FractalSave.bk")
    dialog = QMessageBox()
    dialog.setWindowTitle("Backup")
    dialog.setIcon(QMessageBox.Icon.Information)
    dialog.setText("New backup saved!")
    dialog.exec()

ui.opensave.clicked.connect(selfile)
ui.content.itemDoubleClicked.connect(editButton)
ui.request_backup.triggered.connect(requestSave)
ui.actionError_codes.triggered.connect(lambda: webbrowser.open("https://github.com/Angularity-Space/fs-config-parser/tree/2.0-rewroten"))
edit.cancel.clicked.connect(lambda: edit.close())
edit.OK.clicked.connect(okayButton)
ui.show()
app.exec()