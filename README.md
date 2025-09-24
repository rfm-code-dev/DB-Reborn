
<h2 style="font-family:verdana;">DB Reborn</h2>
<h3 style="font-family:verdana;">A tool to convert Dragonbones ".json" 3.3 in ".spinejson" for use in the Defold Game Engine.
</h3>

<h3>Intro</h3>
Cutout animations are widely used in games and other media for their versatility and visual impact. They allow you to use a small number of sprites and reuse them, instead of importing hundreds of animation frames, which takes up a lot of disk space and can cause performance issues. I've been using the Defold Game Engine for some time and unfortunately it doesn't have built-in Cutout animation features — it only imports JSON from Spine, a paid application, through a plugin. Since I'm just a hobbyist and don't have the budget to invest in a copy of Spine, I searched for a free alternative to use Cutout animations and came across Dragonbones, which previously supported export Spine JSON. Dragonbones hasn't been updated for almost ten years and has been somewhat forgotten, but it remains a good Cutout animation program, bringing together the basics for anyone to make Cut Out bone animations. However, today, due to the various updates and features in Spine's JSON file, it's no longer possible to export Dragonbones JSON and use it directly in Defold. Since JSON is an open text file containing data, I developed a Python tool that can convert and update Dragonbones JSON to a version compatible with the Defold plugin. I've named this app DB Reborn. It's still experimental and may not be suitable for all types of projects. Furthermore, it has some limitations, as it's based on Dragonbones, which is an older application and won't deliver all the features that Spine offers. Therefore, I recommend that if you're looking for something more powerful and professional, get Spine. If you're looking for a free tool to test your animations in Defold and perform simpler tasks, go for DB Reborn. In my tests, I was able to convert Dragonbones animations satisfactorily, which gives me enough confidence to move forward and develop a more polished project. Give it a try and let me know your experience. I hope you enjoy DB Reborn and have fun!

<h3>**IMPORTANT NOTICE:**</h3> This project is a file format conversion tool and is not affiliated with Esoteric Software. The purpose of generating files in the Spine JSON format is to enable interoperability. Please remember that to use the exported animations in your game with the official Spine Runtimes, you and/or your company may need to purchase an appropriate Spine license, in accordance with Esoteric Software's terms of service.

<h3>Tutorial</h3>
1-Create your animation in Dragonbones 5.6.2.

2-Export it as JSON 3.3 with images in 100% of the size in a folder. After export, you will get the YOUR_FILE.json and a folder called
  YOUR_FILE_TEXTURES with your character images inside. Atlas textures won't work, only individual .png sprites.
  Note: The generated JSON must have these minimum arguments:
  - At least 1 armature.
  - At least 1 bone.
  - At least 1 slot with 1 skin.
  - At least 1 animation.

3-The easy way to run DB Reborn is to download the app for Linux or Windows. Go to the Github project address and download it. MacOS users and others can download the "Source" folder and execute the main.py file in the Python enviroment. Make sure you have all Python 3 modules installed.

  DB Reborn GUI was made in Qt6 (Pyside 6). If you have problems displaying
  the GUI, it can be executed in the command line. Do the following:
  - Download the "Source" folder.
  - Make sure to have the last Python3 version installed in your system.
    Note: You must have all the Python3 modules required by the app to run.
  - Open your system terminal inside the extracted "Source" folder and type these
    commands in the right order:
    ___    
    **python3 db_reborn.py "JSON PATH" "SPINEJSON PATH" "SPINE VERSION" "EASE"**
    ___
    JSON PATH: Path to the location of the JSON file, in quotation marks.
    
    SPINEJSON PATH: Path to folder where the app will generate the "spinejson" file, inside quotation marks.
    
    SPINE VERSION: Type "4.2.22".

    EASE: Type "curve" for ease curves or "linear". 

4-Open DB Reborn. The main window will appear.
  
  ![alt text][app_window]

5-Select the ".json" file (must be in the same folder of YOUR_FILE_TEXTURES). Click in the three dots button, on the right side of the section.

6-Select the output folder for the "YOUR_FILE.spinejson". Click in the three dots button, on the right side of the section. Don't change the "Version" field number and let the "Force Linear" checkbox unchecked.

7-Click "Convert!" and let the app process the file.

8-Copy “YOUR_FILE.spinejson” and the "YOUR_FILE_TEXTURES" folder to your Defold project folder.

9-When Defold opens, do the following:
  - Install the dependencies for Defold Spine (3.6.5) in game.project.
  - Create an Atlas texture and import all images of YOUR_FILE_TEXTURES.
  - Create a "Spine Scene" and choose YOUR_FILE.spinejson and Atlas.
  - Create a Game Object > Add Component > Spine Model. Select the default Animation.
  - Create a script to play the animation and see the result.

Note 1: If your animation has easy in/out curves, the script will try to convert the curve values. If somehow Defold crashes, check "Force Linear" to turn all ease curve animations to linear ease animations.

  ![alt text][force_linear]

Note 2: DragonBones doesn't have the "Shear" controls in the interface. But when "json" is generated, DragonBones automatically creates the "shear" time keys and sometimes puts "curves" in keys without the inclination "x" or "y" key. To avoid future problems, I decided to delete all the "shear" curves in the ".spinejson" output file, leaving only the "time" keys, since they don't interfere in the final animations.

 ![alt text][dragonbones_properties]

For more info and tutorials, visit the <a href='https://www.youtube.com/@rfmcodedev'>Youtube Channel</a>.

Please report any bugs via <a href="mailto:rfm.code.dev@gmail.com">e-mail</a>.
 
Enjoy!

[app_window]: /images/db_reborn_window.png "DB Reborn Main Window"
[force_linear]: /images/force_linear.png "DB Reborn Force Linear Checked"
[dragonbones_properties]: /images/dragonbones_properties.png "DragonBones Properties"
