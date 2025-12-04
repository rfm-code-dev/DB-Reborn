#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
DB Reborn 1.0.0 - GUI
Dragonbones to Spine Converter for Defold
For use in Defold Extension-Spine 3.6.5
Compatible with Spine 4.2.22
"""

import sys, os
from gc import enable
from pathlib import Path

from PySide6 import QtWidgets, QtGui, QtMultimedia
from PySide6.QtMultimedia import QAudioOutput
from PySide6.QtGui import QPixmap, QIcon, QTextFormat, QPalette, QColor, QFont, QFontDatabase
from PySide6.QtWidgets import QApplication, QFileDialog, QLabel, QLineEdit, QMessageBox, QGraphicsTextItem, QTextEdit
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QFile, QIODevice, QUrl, QCoreApplication, QSize, Qt
from PySide6.QtMultimedia import QSoundEffect
from db_reborn import *
import resources_compiled # Import Compiled Resources .qrc from Qt Designer - Fonts

global easing_type
global old_json_path
global old_json_file_name
global spinejson_path
spinejson_path = ""
global spinejson_path_file
spinejson_path_file = ""
global sound
global sound_success
global sound_ok
global copy_textures_folder
copy_textures_folder = False
global output_ok_write
output_ok_write = False
global conflict_overwrite
conflict_overwrite = False

try:
    from ctypes import windll  # Only exists on Windows.
    #myapp_id = 'mycompany.myproduct.subproduct.version'
    myapp_id = 'rfmcodedev.dbreborn.converter.version1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myapp_id)
except ImportError:
    pass

def exit_app():
    sys.exit()

# Setup Code for calculate font size
if sys.platform == "darwin":
    font_offset = 3 # Add 2 points to the font size on macOS
else:
    font_offset = 0

help_text = """<html>
<body>
<pre style="text-align: center; font-family: Helvetica-Regular; font-size: 14px; font-weight: 400;">
How to Export Animations
</pre>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 100;">
1-Create your animation in DragonBones 5.6.2.
2-Export it as JSON 3.3 with images in 100% of the size in a folder.
  After export, you will get the YOUR_FILE.json and a folder called
  YOUR_FILE_TEXTURES with your character images inside.
  Atlas textures won't work, only individual .png sprites.
  Note: The generated JSON must have these minimum arguments:
  - At least 1 armature
  - At least 1 bone
  - At least 1 slot with 1 skin.
  - At least 1 animation.

3-Download a copy of DB Reborn on your PC from the Github
  Project page.

4-Open DB Reborn. Select the '.json' file (must be in the same folder
  of YOUR_FILE_TEXTURES).

5-Select the output folder for the 'YOUR_FILE.spinejson'.

6-Click 'Convert!' and let the app process the file.

7-Copy “YOUR_FILE.spinejson” and the 'YOUR_FILE_TEXTURES' folder
  to your Defold project folder.

8-When Defold opens, do the following:
  - Install the dependencies for Defold Spine (3.6.5) in game.project.
  - Create an Atlas texture and import all images of YOUR_FILE_TEXTURES.
  - Create a 'Spine Scene' and choose 'YOUR_FILE.spinejson' and Atlas.
  - Create a Game Object > Add Component > Spine Model. Select the
    Default Animation.
  - Create a script to play the animation and see the result.

<u>Note 1</u>: If your animation has easy in/out curves, the script will try
  to convert the curve values. If somehow Defold crashes, check
  'Force Linear' to turn all ease curve animations to linear
  ease animations.

<u>Note 2</u>: DragonBones doesn't have the 'Shear' controls in the interface,
  so it's impossible for the user to put X or Y values for the 'Shear'
  effect. But somehow DragonBones automatically generates the 'Shear'
  keys and curves in the output 'json'. ontTo avoid future problems,
  I decided to delete all the 'shear' curves in the '.spinejson'
  output file, leaving only the 'time' keys, since they don't
  interfere in the final animations.

For more info and tutorials, visit the <a href='https://www.youtube.com/@rfmcodedev' alt='Buy Me a Coffee at ko-fi.com'>YouTube channel</a>
or the <a href='https://github.com/rfm-code-dev/DB-Reborn'>GitHub project</a> page.
Please report any bugs by <a href='mailto:rfm.code.dev@gmail.com'>e-mail</a>.

If this project helped you, consider <a href='https://ko-fi.com/rfmcodedev'>buying me a coffee</a>!
Every little bit helps me dedicate more time to open-source development.
 
Enjoy!
</pre>
</body>
</html>"""

about_text = about_text = """<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 13px; font-weight: 400;">
DB Reborn 1.0.0
.json to .spinejson converter
</pre>

<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 100; ">
Developed by:
Copyright © 2025 Rodrigo Fontanella Machado

License: GNU GENERAL PUBLIC LICENSE Version 3
</pre>
</body>
</html>"""

congratulation_text = """<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
Success!
Conversion Completed!
</pre>
</body>
</html>"""

check_passed_text_json = """<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
Json appeared OK!
This Json you selected is compatible
with Dragonbones Json 3.3 file.
</pre>
</body>
</html>"""

check_passed_text_texture_folder = """<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
Detected Texture Folder in Place!
</pre>
</body>
</html>"""

check_not_passed_text = """<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
Attention:
This Json you selected is not compatible
with Dragonbones Json 3.3 file.
</pre>
</body>
</html>"""

empty_input_field = """<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
Attention:
Empty Json file input field.
Please choose a valid Dragonbones
Json 3.3 file to continue.
</pre>
</body>
</html>"""

empty_output_field = """<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
Attention:
Empty Spinejson file output field.
Please choose a valid output folder
to continue.
</pre>
</body>
</html>"""

select_json_file_first = """<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
Attention:
Please select a valid Json file first.
</pre>
</body>
</html>"""

empty_all_fields = """<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
Attention:
Please select a valid Json file
and a Output Folder.
</pre>
</body>
</html>"""

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Get the real app path
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            self.app_dir = Path(sys._MEIPASS)
        else:
            self.app_dir = Path(__file__).parent
        #print(self.app_dir)

        self.loader = QUiLoader()
        self.ui_file_name = os.path.join(self.app_dir, "db_ui.ui")
        self.ui_file = QFile(self.ui_file_name)
        self.window = self.loader.load(self.ui_file)
        self.window.setWindowTitle("DB REBORN 1.0.0")
        self.spine_version = "4.2.22"

        #Background Window Image
        self.background = QPixmap(os.path.join(self.app_dir, "images", "background.png"))
        self.window.background.setPixmap(self.background)

        self.setFixedSize(QSize(700, 300))

        # Disable the minimize button
        #self.window.setWindowFlag(Qt.WindowType.WindowMinimizeButtonHint, False)

        # Disable the maximize button (and implicitly the restore button)
        self.window.setWindowFlag(Qt.WindowType.WindowMaximizeButtonHint, False)

        #self.window.setWindowFlag(Qt.WindowType.WindowCloseButtonHint, False)

        self.input_field = False
        self.output_field = False

        self.converted = ""

        # Db Reborn Icon
        #app.setWindowIcon(QtGui.QIcon('images/icon.svg'))
        self.window.setWindowIcon(QtGui.QIcon(os.path.join(self.app_dir, "images", "icon256x256.png")))

        # DB Reborn Logo
        self.icon_path = os.path.join(self.app_dir, "images", "db_reborn_symbol.png")
        self.icon_pixmap = QPixmap(self.icon_path)

        # Yes and No Icons
        self.icon_ok_path = os.path.join(self.app_dir, "images", "ok.png")
        self.icon_no_path = os.path.join(self.app_dir, "images", "no.png")

        self.icon_ok_pixmap = QPixmap(self.icon_ok_path)
        self.icon_no_pixmap = QPixmap(self.icon_no_path)

        #Message Box
        self.about_box = QMessageBox()
        self.help_box =  QMessageBox()

        #Opening Sound
        filepath_opening = os.path.join(self.app_dir, "sounds", "opening.wav")
        sound_opening = QSoundEffect(QCoreApplication.instance())
        sound_opening.setSource(QUrl.fromLocalFile(filepath_opening))
        sound_opening.play()

        #Set Labels fonts
        font_path = os.path.join(self.app_dir, "fonts/Helvetica Regular.otf")
        #print(font_path)

        font_id = QFontDatabase.addApplicationFont(font_path)
        #print(font_id)

        font_families = QFontDatabase.applicationFontFamilies(font_id)
        #print(font_families[0])

        self.font_header = QFont(font_families, 12 + font_offset)
        self.font_header.setHintingPreference(QFont.PreferNoHinting)

        self.font_regular = QFont(font_families, 9 + font_offset)
        #self.font_regular.setBold(False)
        self.font_regular.setHintingPreference(QFont.PreferNoHinting)

        self.font_regular_info = QFont(font_families, 8 + font_offset)
        self.font_regular_info.setHintingPreference(QFont.PreferNoHinting)
        #self.font_regular_info.setBold(False)

        self.window.text_header.setFont(self.font_header)
        self.window.input_json.setFont(self.font_regular)
        self.window.json_path.setFont(self.font_regular)
        self.window.output_spinejson.setFont(self.font_regular)
        self.window.output_path.setFont(self.font_regular)
        self.window.spine_version_label.setFont(self.font_regular)
        self.window.spine_version_text.setFont(self.font_regular)
        self.window.convert_linear.setFont(self.font_regular)
        self.window.copy_textures_folder.setFont(self.font_regular)

        self.window.help.setFont(self.font_regular)
        self.window.about.setFont(self.font_regular)
        self.window.convert.setFont(self.font_regular)
        self.window.exit.setFont(self.font_regular)

        self.window.copy_textures_folder.setVisible(True)
        self.window.copy_textures_folder.setEnabled(True)
        copy_textures_folder = False

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

        # Copy Textures Folder
        self.window.copy_textures_folder.checkStateChanged.connect(self.copy_textures_folder)

        self.window.help.clicked.connect(self.help)
        self.window.about.clicked.connect(self.about)

        # Convert/Exit Buttons
        self.window.convert.clicked.connect(self.convert)
        self.window.exit.clicked.connect(exit_app)

        self.ui_file.close()
        self.window.show()

        # Setting up all Message Boxes to the same color layout
        QMessageBox.setStyleSheet(self, "background-color: rgb(42, 42, 42); color: rgb(255, 255, 255)")

        # Create an Instance to store the images in the Texture folder
        self.texture_list_folder = []

        if not self:
            #print(self.loader.errorString())
            sys.exit(-1)

        if not self.ui_file.open(QIODevice.ReadOnly):
            #print(f"Cannot open {self.ui_file_name}: {self.ui_file.errorString()}")
            sys.exit(-1)

        sys.exit(app.exec())

    def play_sound_alert(self):
        filepath = os.path.join(self.app_dir, "sounds", "blip.wav")
        global sound
        sound = QSoundEffect(QCoreApplication.instance())
        sound.setSource(QUrl.fromLocalFile(filepath))
        sound.play()

    def play_sound_sucess(self):
        filepath_success = os.path.join(self.app_dir, "sounds", "success.wav")
        global sound_success
        sound_success = QSoundEffect(QCoreApplication.instance())
        sound_success.setSource(QUrl.fromLocalFile(filepath_success))
        sound_success.play()

    def play_sound_ok(self):
        filepath_ok = os.path.join(self.app_dir, "sounds", "ok.wav")
        global sound_ok
        sound_ok = QSoundEffect(QCoreApplication.instance())
        sound_ok.setSource(QUrl.fromLocalFile(filepath_ok))
        sound_ok.play()

    def checked(self):
        global easing_type
        if self.window.convert_linear.isChecked():
            easing_type = 'linear'
            #print('linear')
        else:
            easing_type = 'curve'
            #print('curve')

    def copy_textures_folder(self):
        global copy_textures_folder
        if self.window.copy_textures_folder.isChecked():
            copy_textures_folder = True
            if self.input_field and self.output_field:
                instance_check = DbJsonCheck(old_json_path)
                overwrite_texture_folder = (
"""<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
<b>Attention</b>: Do you really want to replace the Texture Folder
""" + "'" + instance_check.texture_folder_name + "'? This action cannot be undone\n"
+ """after pressing 'Convert'. Uncheck 'Copy Texture Folder'
if you do not want to overwrite its contents.
</pre>
</body>
</html>""")
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Overwrite Texture Folder")
                msg_box.setText(overwrite_texture_folder)
                # Set the custom icon pixmap
                msg_box.setIconPixmap(self.icon_no_pixmap)
                msg_box.StandardButton.Ok
                msg_box.exec()


            #print("Copy Texture folder")
        else:
            copy_textures_folder = False
            #print("Not Copy Texture folder")

    def check_overwrite(self):
        global copy_textures_folder
        global spinejson_path
        global spinejson_path_file
        global old_json_file_name
        global old_json_path
        global output_ok_write
        global conflict_overwrite

        spinejson_path_archive = Path(spinejson_path_file)
        #print(spinejson_path_file)
        # If there's conflict with same file names
        if spinejson_path_archive.is_file():
            conflict_overwrite = True
            #print("Conflict Overwrite?", conflict_overwrite)
            self.play_sound_alert()
            # self.alert.play()
            alert_overwrite = (
"""<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
Attention: Detected a .spinejson file
""" + "'" + spinejson_path_archive.name + "'\n"
+ " " + """with the same name. Replace it?.
</pre>
</body>
</html>""")
            msg_box = QMessageBox.question(
                self,
            'Same Output Filename',
            alert_overwrite,
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No # Set 'No' as the default button
            )

            #msg_box.setWindowTitle("File with same name in place")
            #msg_box.setText(alert_overwrite)
            # Set the custom icon pixmap
            # msg_box.setIconPixmap(self.icon_no_pixmap)
            #msg_box.StandardButton.Ok
            #msg_box.exec()

            # If the user decides to overwrite
            if msg_box == QMessageBox.Yes:
                self.output_field = True
                output_ok_write = True

                # Turn False the conflict var to write over the .spinejson file in folder
                conflict_overwrite = False

                # Get the texture name folder
                texture_name = DbJsonCheck(old_json_path)
                texture_folder_path = (Path(spinejson_path) / texture_name.texture_folder_name)

                #print(texture_folder_path)
                #texture_folder = Path(str(texture_name.texture_folder_name))
                #print(texture_folder)
                # Is Copy texture folder is selected and there is a sema folder there an warning appear
                instance_check = DbJsonCheck(old_json_path)
                if texture_folder_path.is_dir():
                    if copy_textures_folder:
                        self.play_sound_alert()
                        # self.alert.play()
                        overwrite_texture_folder = (
"""<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
<b>Attention</b>: Do you really want to replace the Texture Folder
""" + "'" + instance_check.texture_folder_name + "'? This action cannot be undone\n"
+ """after pressing 'Convert'. Uncheck 'Copy Texture Folder'
if you do not want to overwrite its contents.
</pre>
</body>
</html>""")
                        msg_box_new = QMessageBox()
                        msg_box_new.setWindowTitle("Texture Folder Overwrite")
                        msg_box_new.setText(overwrite_texture_folder)
                        # Set the custom icon pixmap
                        msg_box_new.setIconPixmap(self.icon_no_pixmap)
                        msg_box_new.StandardButton.Ok
                        msg_box_new.exec()
                        self.input_field = False
            else:
                # If select not overwrite
                #print("Not Overwrite. Choose another place", self.default_output_text)
                self.window.output_path.setText(self.default_output_text) 
                output_ok_write = False
                self.output_field = False
                # The var persists ON
                conflict_overwrite = True
        else:
            conflict_overwrite = False
            output_ok_write = True
            self.output_field = True

    def locate_json(self):
        global old_json_file_name
        global old_json_path
        #print("locate")
        #self.json.delete(0, "end")
        old_json_path, _ = QFileDialog.getOpenFileName(self, "Open Json",
                                                       str(self.app_dir), "Json Files (*.json)")
        if old_json_path:
            self.window.json_path.setText(old_json_path)
            old_json_file_name = os.path.basename(old_json_path)
            old_json_file_name = os.path.splitext(old_json_file_name)
            #print(old_json_file_name[0])
            instance_check = DbJsonCheck(old_json_path)
            #print(instance_check.json_state)

            # If Json is OK, proceed next check
            if instance_check.json_state:
                self.play_sound_ok()
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Json Check Passed")
                msg_box.setText(check_passed_text_json)
                # Set the custom icon pixmap
                msg_box.setIconPixmap(self.icon_ok_pixmap)
                msg_box.StandardButton.Ok
                msg_box.exec()

                # Store in this var the path of all images found
                self.texture_list_folder = instance_check.texture_list
                #print(self.texture_list_folder)

                self.input_field = True

                # Check if there's a Texture Folder
                if not instance_check.texture_folder_in_place:
                    self.play_sound_alert()
                    # self.alert.play()
                    no_texture_folder_in_place = (
"""<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
Attention: Check if the Texture Folder:
""" + "'" + instance_check.texture_folder_name + "'\n"
+ " " + """is in the same place of the JSON file.
</pre>
</body>
</html>""")

                    self.window.json_path.setText(self.default_input_text)
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("No Texture Folder in Place")
                    msg_box.setText(no_texture_folder_in_place)
                    # Set the custom icon pixmap
                    msg_box.setIconPixmap(self.icon_no_pixmap)
                    msg_box.StandardButton.Ok
                    msg_box.exec()
                    self.input_field = False
                else:
                    self.play_sound_ok()
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("Texture Folder in Place")
                    msg_box.setText(check_passed_text_texture_folder)
                    # Set the custom icon pixmap
                    msg_box.setIconPixmap(self.icon_ok_pixmap)
                    msg_box.StandardButton.Ok
                    msg_box.exec()
                    self.input_field = True

                # Check if there's images in Texture Folder
                if not instance_check.images_in_texture_folder:
                    self.play_sound_alert()
                    # self.alert.play()
                    no_images_in_textures_folder = (
"""<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF;">
Attention: Check if the Texture Folder:
""" + "'" + instance_check.texture_folder_name + "'\n"
+ " " + """has the project images inside.
</pre>
</body>
</html>""")
                    self.window.json_path.setText(self.default_input_text)
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("No Images in Texture Folder")
                    msg_box.setText(no_images_in_textures_folder)
                    # Set the custom icon pixmap
                    msg_box.setIconPixmap(self.icon_no_pixmap)
                    msg_box.StandardButton.Ok
                    msg_box.exec()
                    self.input_field = False
                else:
                    self.play_sound_ok()
                    msg_box = QMessageBox()
                    msg_box.setWindowTitle("Found Images in Texture Folder")
                    images_in_textures_folder = (
"""<html>
<body>
<pre style="font-family: Helvetica-Regular; font-size: 11px; font-weight: 400; color: #FFFFFF; ">
Images located in """ + "'" + instance_check.texture_folder_name + "'" """.
Now select the Output Folder\nto generate your "spinejson" file.
</pre>
</body>
</html>""")
                    msg_box.setText(images_in_textures_folder)
                    # Set the custom icon pixmap
                    msg_box.setIconPixmap(self.icon_ok_pixmap)
                    msg_box.StandardButton.Ok
                    msg_box.exec()
                    self.input_field = True
            else:
                self.play_sound_alert()
                self.window.json_path.setText(self.default_input_text)
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Json Check Failed")
                msg_box.setText(check_not_passed_text)
                # Set the custom icon pixmap
                msg_box.setIconPixmap(self.icon_no_pixmap)
                msg_box.StandardButton.Ok
                msg_box.exec()
                self.input_field = False
        else:
            self.window.json_path.setText(self.default_input_text)
            self.input_field = False

    def output_spinejson(self):
        global old_json_file_name
        global spinejson_path
        global copy_textures_folder
        global output_ok_write
        global conflict_overwrite
        global spinejson_path_file

        # If Input field was filled
        if self.input_field:
            spinejson_path = QFileDialog.getExistingDirectory(self, "Spinejson Output")

            # If the user cancel the window, returns the default text
            if spinejson_path == "":
                self.window.output_path.setText(self.default_output_text)
                self.output_field = False
            else:
                spinejson_path_file = spinejson_path + "/" + old_json_file_name[0] + ".spinejson"
                #print(spinejson_path, spinejson_path_file)

                # Call function to check overwrite conflicts
                self.check_overwrite()

                # If the output folder is OK, add the .spinejson filename to path
                if output_ok_write:
                    self.play_sound_ok()
                    self.window.output_path.setText(spinejson_path_file)
                    self.output_field = True
                    # print(os.path.dirname(old_json_path))
                    # print(os.path.dirname(spinejson_path))
                else:
                    spinejson_path = ""
                    spinejson_path_file = ""
                #print("Output Selected?", output_ok_write, "Conflict?", conflict_overwrite, spinejson_path)
        else:
            self.play_sound_alert()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Please Select Json File")
            msg_box.setText(select_json_file_first)
            # Set the custom icon pixmap
            msg_box.setIconPixmap(self.icon_no_pixmap)
            msg_box.StandardButton.Ok
            msg_box.exec()

    def convert(self):
        global easing_type
        global old_json_path
        global spinejson_path
        global spinejson_path_file
        global copy_textures_folder
        global output_ok_write
        global conflict_overwrite
        #print(copy_textures_folder)
        #error_detection = DbJsonConverter.db_error
        #error_detection_type = DbJsonConverter.db_error_type

        if not self.input_field and self.output_field:
            self.play_sound_alert()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Input Json File Required")
            msg_box.setText(empty_input_field)
            # Set the custom icon pixmap
            msg_box.setIconPixmap(self.icon_no_pixmap)
            msg_box.StandardButton.Ok
            msg_box.exec()

        if not self.output_field and self.input_field:
            self.play_sound_alert()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Output Folder Required")
            msg_box.setText(empty_output_field)
            # Set the custom icon pixmap
            msg_box.setIconPixmap(self.icon_no_pixmap)
            msg_box.StandardButton.Ok
            msg_box.exec()

        if not self.output_field and not self.input_field:
            self.play_sound_alert()
            msg_box = QMessageBox()
            msg_box.setWindowTitle("Input and Output Folder Required")
            msg_box.setText(empty_all_fields)
            # Set the custom icon pixmap
            msg_box.setIconPixmap(self.icon_no_pixmap)
            msg_box.StandardButton.Ok
            msg_box.exec()

        # If all fields are filled, proceed
        if self.output_field and self.input_field:
            #print("Call conflict", conflict_overwrite, output_ok_write)
            # If the output folder is OK

            #print("Output Selected?", output_ok_write, "Conflict?", conflict_overwrite)
            # If after generate .spinejson the user try again, check conflict
            if conflict_overwrite:
                self.check_overwrite()

            if output_ok_write:
                self.play_sound_sucess()
                self.spine_version = self.window.spine_version_text.text()
                # print(self.spine_version)
                #print(copy_textures_folder)
                self.converted = DbJsonConverter(old_json_path, spinejson_path_file, self.spine_version, easing_type,
                                                 copy_textures_folder)
                msg_box = QMessageBox()
                msg_box.setWindowTitle("Conversion Completed")
                msg_box.setText(congratulation_text)
                # Set the custom icon pixmap
                msg_box.setIconPixmap(self.icon_ok_pixmap)
                msg_box.StandardButton.Ok
                msg_box.exec()

                # Once the .spinejson is created, turn output_ok_write var to False and conflict_overwrite True
                output_ok_write = False
                conflict_overwrite = True
                # print("CONVERT: Output Selected?", output_ok_write, "Conflict?", conflict_overwrite, spinejson_path)
                return self.converted

    def help(self):
        #QMessageBox.about(self,"DB Reborn Help", help_text)
        self.help_box.setWindowTitle("DB Reborn Help")
        self.help_box.setText(help_text)
        self.help_box.setFont(self.font_regular_info)
        self.help_box.setStyleSheet("background-color: rgb(42, 42, 42); color: rgb(255, 255, 255)")
        self.help_box.setStandardButtons(QMessageBox.Ok)
        self.help_box.exec()

    def about(self):
        self.about_box.setIconPixmap(self.icon_pixmap)
        self.about_box.setWindowTitle("About DB Reborn")
        self.about_box.setStyleSheet("background-color: rgb(42, 42, 42); color: rgb(255, 255, 255)")
        self.about_box.setText(about_text)
        self.about_box.setFont(self.font_regular_info)
        self.about_box.setStandardButtons(QMessageBox.Ok)
        self.about_box.exec()


if __name__ == "__main__":
    # The default of easing_type is 'curve'
    copy_texture_folder = False
    easing_type = 'curve'
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()

