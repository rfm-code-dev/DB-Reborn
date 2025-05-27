
<h2 style="font-family:verdana;">DB Reborn</h2>
<h3 style="font-family:verdana;">A tool to convert Dragonbones .json 3.3 in .spinejson for use in Defold Game Engine.
</h3>

<h3>How to Export Animations</h3>
1-Create your Animation in Dragonbones 5.6.2.

2-Export it as Spine Json 3.3 with images in 100% of size in a folder.
  After export, you will get the YOUR_FILE.json and a folder called
  YOUR_FILE_TEXTURES with of your character images inside.
  Atlas texture won't work, only individual .png sprites.
  Note: Json generated must has the minimum of arguments:
  - At least 1 Armature.
  - At least 1 bone.
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

Note: If your animation has easy in/out curves, the script will try to
  convert the curve values. If somehow Defold crashes, check "Force Linear"
  to turn all ease curve animations to linear ease animations.

For more info and tutorials, visit the <a href='https://www.youtube.com/watch?v=uowkgY5dFaI'>Youtube Channel</a>.

Please report any bugs via <a href="mailto:rodrigo.fontanella@gmail.com">e-mail</a>.
 
Enjoy!
