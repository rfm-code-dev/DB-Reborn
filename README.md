
<h2 style="font-family:verdana;">DB Reborn</h2>
<h3 style="font-family:verdana;">A tool to convert Dragonbones ".json" 3.3 in ".spinejson" for use in the Defold Game Engine.
</h3>

<h3>How to Export Animations</h3>
1-Create your animation in Dragonbones 5.6.2.

2-Export it as Spine Json 3.3 with images in 100% of the size in a folder.
  After export, you will get the YOUR_FILE.json and a folder called
  YOUR_FILE_TEXTURES with your character images inside.
  Atlas texture won't work, only individual .png sprites.
  Note: The Json generated must have the minimum of arguments:
  - At least 1 armature.
  - At least 1 bone.
  - At least 1 slot with 1 skin.
  - At least 1 animation.

3-Download a copy of DB-Reborn on your PC for Linux, Windows or MacOS.
  Go to the Github project address and download it.

4-Open DB-Reborn. Select the ".json" file (must be in the same folder
  of YOUR_FILE_TEXTURES).

5-Select the output folder for the "YOUR_FILE.spinejson".

6-Copy “YOUR_FILE.spinejson” and the "YOUR_FILE_TEXTURES" folder
  to your Defold project folder.

7-When Defold opens, do the following:
  - Install the dependencies for Defold Spine (3.6.5) in game.project.
  - Create an Atlas texture and import all images of YOUR_FILE_TEXTURES.
  - Create a "Spine Scene" and choose YOUR_FILE.spinejson and Atlas.
  - Create a Game Object > Add Component > Spine Model. Select the
    Default Animation.
  - Create a Script to play the animation and see the result.

Note 1: If your animation has easy in/out curves, the script will try to
  convert the curve values. If somehow Defold crashes, check "Force Linear"
  to turn all ease curve animations to linear ease animations.

Note 2: Dragonbones doesn't have the "Shear" controls in the interface,
  so it's impossible for the user to put X or Y values for "Shear" effect.
  But somehow Dragonbones generates the "shear" keys and curves in the
  output json. To avoid future problems, I decided to delete the "shear"
  "curves" in the ".spinejson" output file, letting only the "time" keys,
  since they don't interfere in the final animations.

For more info and tutorials, visit the <a href='https://www.youtube.com/@rfmcodedev'>Youtube Channel</a>.

Please report any bugs via <a href="mailto:rfm.code.dev@gmail.com">e-mail</a>.
 
Enjoy!
