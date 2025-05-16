#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, os

from PySide6 import QtWidgets, QtGui, QtMultimedia
from PySide6.QtGui import QPixmap, QIcon, QTextFormat, QPalette, QColor
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QMessageBox, QGraphicsTextItem, QTextEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QUrl
from PySide6.QtMultimedia import QSoundEffect
from db_reborn import DbJsonConverter
from db_reborn import *


global easing_type
global old_json_path
global old_json_file_name
global new_spinejson
global spinejson_path

try:
    from ctypes import windll  # Only exists on Windows.
    #myapp_id = 'mycompany.myproduct.subproduct.version'
    myapp_id = 'rfmcodedev.dbreborn.converter.version1'

    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myapp_id)
except ImportError:
    pass


def exit_app():
    sys.exit()

help_text = """<html>
<body>
<h3 style="font-family:verdana;">DB Reborn - How to Export Animations</h3>
<pre style="font-family:verdana;">1-Create your Animation in Dragonbones 5.6.2.

2-Export it as Json 3.3 with images in 100% of size in a folder.
  After export, you will get the YOUR_FILE.json and a folder called
  YOUR_FILE_TEXTURES with of your character images inside.
  Atlas texture won't work, only individual .png sprites.
  Note: Json generated must has the minimum of arguments:
  - At least 1 Armature and 1 bone.
  - At least 1 Slot with 1 Skin.
  - At least 1 Animation.

3-Download a copy of DB-Reborn on your PC for Linux, Windows or MacOS.
  Go to the Github Project address and download it.

4-Open DB-Reborn. Select the .json file (Must be in the same folder
  of YOUR_FILE_TEXTURES).

5-Select the output folder for the YOUR_FILE.spinejson.

6-Copy “YOUR_FILE.spinejson” and the YOUR_FILE_TEXTURES folder
  to your Defold project folder.

7-When Defold opens, do the follow:
  - Install the dependencies for Defold Spine (3.6.5) in game.project.
  - Create an Atlas texture and import all images of YOUR_FILE_TEXTURES.
  - Create a "Spine Scene" and choose YOUR_FILE.spinejson and Atlas.
  - Create a Game Object > Add Component > Spine Model. Select the
    Default Animation.
  - Create an Script to play the animation and see the result.

Note: If your animation has easing in/out curves, the script will try to
  convert the curve values. If somehow Defold crashes, check "Force Linear"
  to turn all easing curve animations to linear.

For more info and tutorials, visit the <a href='https://www.youtube.com/@rfmcodedev'>Youtube Channel</a>
or the <a href='https://github.com/rfm-code-dev/DB-Reborn'>Github Project</a> page.
Please report any bugs by <a href="mailto:rfm.code.dev@gmail.com">e-mail</a>.
 
Enjoy!</pre>
</body>
</html>"""

about_text = """<html>
<body>
<pre style="font-family:verdana;">
DB Reborn 1.0
.json to .spinejson converter

Developed by:
Copyright © 2025 Rodrigo Fontanella Machado

License: GNU GENERAL PUBLIC LICENSE Version 3
</pre>
"""

congratulation_text = """Success!
Conversion Completed!"""

check_passed_text = """Json appeared OK!:
This Json you selected is compatible
with Dragonbones Json 3.3 file."""

check_not_passed_text = """Attention:
This Json you selected is not compatible
with Dragonbones Json 3.3 file."""

empty_input_field = """Attention:
Empty Json file input field.
Please choose a valid Dragonbones
Json 3.3 file to continue."""

empty_output_field = """Attention:
Empty Spinejson file output field.
Please choose a valid output folder
to continue."""

select_json_file_first = """Attention:
Please select a valid Json file first."""

empty_all_fields = """Attention:
Please select a valid Json file
and a Output Folder."""

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.app_dir = os.path.dirname(__file__)
        print(self.app_dir)
        self.loader = QUiLoader()
        self.ui_file_name = os.path.join(self.app_dir, "db_ui.ui")
        self.ui_file = QFile(self.ui_file_name)
        self.window = self.loader.load(self.ui_file)
        self.window.setWindowTitle("DB REBORN 1.0")
        self.spine_version = "4.2.22"

        #Background Window Image
        self.background = QPixmap(os.path.join(self.app_dir, "images", "background.png"))
        self.window.background.setPixmap(self.background)

        self.input_field = False
        self.output_field = False

        # Alert Sound
        self.alert = QSoundEffect()
        self.alert.setSource(QUrl.fromLocalFile(os.path.join(self.app_dir, "sounds", "blip.wav")))
        self.alert.setVolume(0.5)

        # Success Sound
        self.success = QSoundEffect()
        self.success.setSource(QUrl.fromLocalFile(os.path.join(self.app_dir, "sounds", "success.wav")))
        self.success.setVolume(0.5)

        self.converted = ""

        # Db Reborn Icon
        #app.setWindowIcon(QtGui.QIcon('images/icon.svg'))
        self.window.setWindowIcon(QtGui.QIcon(os.path.join(self.app_dir, "images", "icon256x256.png")))

        # DB Reborn Logo
        self.icon_path = os.path.join(self.app_dir, "images", "db_reborn_symbol.png")
        self.icon_pixmap = QPixmap(self.icon_path)
        self.about_box = QMessageBox()
        self.help_box =  QMessageBox()

        # Access widgets in the UI
        # Locate Json
        self.window.button_locate_json.clicked.connect(self.locate_json)

        self.default_input_text = self.window.json_path.text()
        self.default_output_text = self.window.output_path.text()
        #print(self.window.json_path.text())

        # Path to spinejson output
        self.window.button_output_spinejson.clicked.connect(self.output_spinejson)

        # Spine Version
        self.window.spine_version_text.setText(self.spine_version)

        # Convert Linear
        self.window.convert_linear.checkStateChanged.connect(self.checked)

        self.window.help.clicked.connect(self.help)
        self.window.about.clicked.connect(self.about)

        # Convert/Exit Buttons
        self.window.convert.clicked.connect(self.convert)
        self.window.exit.clicked.connect(exit_app)

        self.ui_file.close()
        self.window.show()

        # Setting up all Message Boxes to the same color layout
        QMessageBox.setStyleSheet(self, "background-color: rgb(42, 42, 42); color: rgb(255, 255, 255)")

        if not self:
            #print(self.loader.errorString())
            sys.exit(-1)

        if not self.ui_file.open(QIODevice.ReadOnly):
            #print(f"Cannot open {self.ui_file_name}: {self.ui_file.errorString()}")
            sys.exit(-1)

        sys.exit(app.exec())

    def checked(self):
        global easing_type
        if self.window.convert_linear.isChecked():
            easing_type = 'linear'
            #print('linear')
        else:
            easing_type = 'curve'
            #print('curve')

    def locate_json(self):
        global old_json_file_name
        global old_json_path
        #print("locate")
        #self.json.delete(0, "end")
        old_json_path, _ = QFileDialog.getOpenFileName(self, "Open Json", self.app_dir, "Json Files (*.json)")
        #print(old_json_path)
        if old_json_path:
            self.window.json_path.setText(old_json_path)
            old_json_file_name = os.path.basename(old_json_path)
            old_json_file_name = os.path.splitext(old_json_file_name)
            #print(old_json_file_name[0])
            instance_check = DbJsonCheck(old_json_path)
            #print(instance_check.json_state)
            if instance_check.json_state:
                self.alert.play()
                QMessageBox.information(self, "Check Json Passed", check_passed_text,
                                        buttons=QMessageBox.StandardButton.Ok)
                self.input_field = True

            else:
                self.alert.play()
                self.window.json_path.setText(self.default_input_text)
                QMessageBox.warning(self, "Check Json Failed", check_not_passed_text,
                                        buttons=QMessageBox.StandardButton.Ok)
                self.input_field = False

        else:
            self.window.json_path.setText(self.default_input_text)
            self.input_field = False


    def output_spinejson(self):
        global old_json_file_name
        global new_spinejson
        global spinejson_path

        if self.input_field:
            spinejson_path = QFileDialog.getExistingDirectory(self, "Spinejson Output")
            if spinejson_path:
                spinejson_path = spinejson_path + "/" + old_json_file_name[0] + ".spinejson"
                self.window.output_path.setText(spinejson_path)
                self.output_field = True
            else:
                self.window.output_path.setText(self.default_output_text)
        else:
            self.alert.play()

            QMessageBox.warning(self, "Please Select Json File", select_json_file_first,
                                buttons=QMessageBox.StandardButton.Ok)

    def convert(self):
        global easing_type
        global old_json_path
        global spinejson_path

        if not self.input_field and self.output_field:
            self.alert.play()

            #if self.window.json_path.text() == "Path to Dragonbones 3.3 Json":
            QMessageBox.warning(self, "Input Json File Required", empty_input_field,
                                    buttons=QMessageBox.StandardButton.Ok)

        if not self.output_field and self.input_field:
            self.alert.play()

            #self.window.output_path.text() == "Path where to save .spinejson file.":
            QMessageBox.warning(self, "Output Folder Required", empty_output_field,
                                    buttons=QMessageBox.StandardButton.Ok)

        if not self.output_field and not self.input_field:
            self.alert.play()

            #self.window.output_path.text() == "Path where to save .spinejson file.":
            QMessageBox.warning(self, "Output Folder Required", empty_all_fields,
                                    buttons=QMessageBox.StandardButton.Ok)

        if self.output_field and self.input_field:
            self.success.play()

            # print(old_json_path[0], spinejson_path, easing_type)
            self.spine_version = self.window.spine_version_text.text()
            # print(self.spine_version)
            self.converted = DbJsonConverter(old_json_path, spinejson_path, self.spine_version, easing_type)
            # DbJsonConverter(old_json_file_path, destiny_path, easing_type)
            # print(my_instance.file_converted)
            QMessageBox.information(self, "Conversion Completed", congratulation_text,
                                    buttons=QMessageBox.StandardButton.Ok)
            QMessageBox.setStyleSheet(self, "background-color: rgb(42, 42, 42); color: rgb(255, 255, 255)")

        return self.converted


    def help(self):
        #QMessageBox.about(self,"DB Reborn Help", help_text)
        self.help_box.setWindowTitle("DB Reborn Help")
        self.help_box.setText(help_text)
        self.help_box.setStyleSheet("background-color: rgb(42, 42, 42); color: rgb(255, 255, 255)")
        self.help_box.setStandardButtons(QMessageBox.Ok)
        self.help_box.exec()

    def about(self):
        self.about_box.setIconPixmap(self.icon_pixmap)
        self.about_box.setWindowTitle("About DB-Reborn")
        self.about_box.setStyleSheet("background-color: rgb(42, 42, 42); color: rgb(255, 255, 255)")
        self.about_box.setText(about_text)
        self.about_box.setStandardButtons(QMessageBox.Ok)
        self.about_box.exec()


if __name__ == "__main__":
    # The default of easing_type is 'curve'
    easing_type = 'curve'
    app = QtWidgets.QApplication(sys.argv)
    w = MainWindow()

