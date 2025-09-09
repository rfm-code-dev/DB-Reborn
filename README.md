
<h2 style="font-family:verdana;">DB Reborn</h2>
<h3 style="font-family:verdana;">A tool to convert Dragonbones ".json" 3.3 in ".spinejson" for use in the Defold Game Engine.
</h3>

<h3>How to Export Animations</h3>
1-Create your animation in Dragonbones 5.6.2.

2-Export it as JSON 3.3 with images in 100% of the size in a folder.
  After export, you will get the YOUR_FILE.json and a folder called
  YOUR_FILE_TEXTURES with your character images inside.
  Atlas textures won't work, only individual .png sprites.
  Note: The generated JSON must have these minimum arguments:
  - At least 1 armature.
  - At least 1 bone.
  - At least 1 slot with 1 skin.
  - At least 1 animation.

3-The easy way to run DB Reborn is to download the app for Linux or Windows.
  Go to the Github project address and download it.
  MacOS users and others can download the "Source" folder and execute the
  main.py file in the Python enviroment. Make sure you have all Python3
  modules installed.

  DB Reborn GUI was made in Qt6 (Pyside 6). If you have problems displaying
  the GUI, it can be executed in the command line. Do the following:
  - Download the "Source" folder.
  - Make sure to have the last Python3 version installed in your system.
    Note: You must have all the Python3 modules required by the app to run.
  - Open your system terminal inside the extracted "Source" folder and type these
    commands in the right order:
    
    python3 db_reborn.py "JSON PATH" "SPINEJSON PATH" "SPINE VERSION" "EASE"

    Where:
     JSON PATH: Path to the location of the JSON file, including the file.
     SPINEJSON PATH: Folder where the app will generate the "spinejson" file.
     SPINE VERSION: Type "4.2.22"
     EASE: Type "curve" for ease curves or "linear". 

4-Open DB Reborn. Select the ".json" file (must be in the same folder
  of YOUR_FILE_TEXTURES).
  ![alt text][app_window]

5-Select the output folder for the "YOUR_FILE.spinejson".

6-Copy “YOUR_FILE.spinejson” and the "YOUR_FILE_TEXTURES" folder
  to your Defold project folder.

7-When Defold opens, do the following:
  - Install the dependencies for Defold Spine (3.6.5) in game.project.
  - Create an Atlas texture and import all images of YOUR_FILE_TEXTURES.
  - Create a "Spine Scene" and choose YOUR_FILE.spinejson and Atlas.
  - Create a Game Object > Add Component > Spine Model. Select the
    default Animation.
  - Create a script to play the animation and see the result.

Note 1: If your animation has easy in/out curves, the script will try to
  convert the curve values. If somehow Defold crashes, check "Force Linear"
  to turn all ease curve animations to linear ease animations.

Note 2: Dragonbones doesn't have the "Shear" controls in the interface,
  so it's impossible for the user to put X or Y values for the "Shear" effect.
  But somehow Dragonbones generates the "shear" keys and curves in the
  output "json". To avoid future problems, I decided to delete all the
  "shear" curves in the ".spinejson" output file, leaving only the "time" keys,
  since they don't interfere in the final animations.

For more info and tutorials, visit the <a href='https://www.youtube.com/@rfmcodedev'>Youtube Channel</a>.

[app_window]: https://github.com/rfm-code-dev/DB-Reborn/tree/main/images/db_reborn_window.png "DB Reborn Main Window"

Please report any bugs via <a href="mailto:rfm.code.dev@gmail.com">e-mail</a>.
 
Enjoy!
