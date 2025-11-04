# DB Reborn

### A tool to convert DragonBones JSON (v3.3) to Spine JSON for the Defold Game Engine.

## Introduction

Cutout animation is a powerful technique in game development, allowing for rich, fluid animations while using a small number of sprites. This saves disk space and improves performance compared to traditional frame-by-frame animation.

I've been using the [Defold Game Engine](https://defold.com/), which has excellent features but lacks a built-in cutout animation editor. It primarily supports Spine JSON files via an official extension. As a hobbyist developer without the budget for a Spine license, I looked for free alternatives and found DragonBones.

DragonBones is a great, albeit older, animation tool that once had a direct export-to-Spine feature. However, due to the evolution of the Spine JSON format, animations created in the last stable version of DragonBones (v5.6) are no longer directly compatible with Defold's Spine extension.

Since JSON is an open data format, I developed **DB Reborn**: a Python tool that converts and updates DragonBones JSON files to a format compatible with Defold.

**Who is this for?**

- **DB Reborn is ideal for:** Hobbyists and developers looking for a free way to create and test simple cutout animations in Defold.
- **For professional work:** If you need advanced features, professional support, and a more powerful workflow, I highly recommend purchasing a [Spine license](http://esotericsoftware.com/).

This tool is still experimental. While it worked well in my tests, it may have limitations. Please give it a try and share your experience!

## **IMPORTANT NOTICE**

This project is a file format conversion tool and is not affiliated with Esoteric Software. The purpose of generating files in the Spine JSON format is to enable interoperability. Please remember that to use the exported animations in your game with the official Spine Runtimes, you and/or your company may need to purchase an appropriate Spine license, in accordance with Esoteric Software's terms of service.

## How to Use

### 1. Create Your Animation

- Create your animation in **DragonBones 5.6.2**.
- **Requirements:** Your project must contain at least 1 armature, 1 bone, 1 slot with 1 skin, and 1 animation.

### 2. Export from DragonBones

- Export your project with **Data Type: `JSON`** and **Data Version: `3.3`**.
- Ensure images are exported at **100% scale**.
- **Important:** Do not use texture atlases during export. The tool requires individual `.png` sprites.
- After exporting, you will have a `YOUR_FILE.json` and a `YOUR_FILE_TEXTURES` folder.

### 3. Run DB Reborn

You have two options to run the application:

**Option A: Download the App (Easy Way)**

1. Go to the [Releases page](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY/releases) on GitHub.
2. Download the executable for Windows or Linux.
3. Run the app.

**Option B: Run from Source (for macOS or advanced users)**

1. Download the `Source` folder.

2. Make sure you have Python 3 installed on your system.

3. Install the required modules by running:
   
   Bash
   
   ```
   pip install PySide6
   ```

4. You can then run the GUI or use the command line.

**Using the Command Line Interface (CLI):** Open your terminal inside the `Source` folder and run the script with the following arguments:

Bash

```
python3 db_reborn.py "path/to/your.json" "path/to/output_folder" "4.2.22" "ease_type"
```

- `"path/to/your.json"`: The full path to the input DragonBones JSON file.
- `"path/to/output_folder"`: The folder where the `.spinejson` file will be saved.
- `"4.2.22"`: The target Spine version (currently fixed).
- `"ease_type"`: Use `"curve"` to convert easing or `"linear"` to force linear transitions.

### 4. Convert the File

1. Open DB Reborn.

2. Click the "..." button to select your input `.json` file.
   ![DB Reborn Main Window](images/1_db_reborn_window.png)
   
   *Note: After selecting the `.json` file, DB Reborn will perform a series of checks to ensure it meets the required standard for a successful conversion. Three pop-up windows will appear in sequence: one indicating that the `.json` file appears to be OK, another confirming that the `YOUR_FILE_TEXTURES` folder was found, and a final one verifying that this folder contains the project's images. Simply click the "OK" button on each pop-up to proceed.*

3. Click the second "..." button to select the output folder for the `.spinejson` file.
   ![DB Reborn Main Window](images/2_db_reborn_window_copy_texture_folder.png)
   
   *Note: If you choose an output folder different from the one where the input `.json` is located, DB Reborn will offer an option to copy the `YOUR_FILE_TEXTURES` folder to the new location. Just check the corresponding checkbox. If you only wish to generate the `.spinejson` file without copying the textures, leave the checkbox unchecked.*

4. Click **Convert!**
   ![DB Reborn Main Window](images/3_db_reborn_window_success.png)

### 5. Import into Defold

1. Copy the generated `YOUR_FILE.spinejson` and the `YOUR_FILE_TEXTURES` folder into your Defold project.
2. In your `game.project` file, add the [Spine extension dependency](https://defold.com/manuals/spine/).
3. Create a new **Atlas** in Defold and add all the images from the `YOUR_FILE_TEXTURES` folder.
4. Create a new **Spine Scene** (`.spinescene`) and assign your `.spinejson` file and the Atlas you just created.
5. Add a **Spine Model** component to a Game Object and select the new Spine Scene.
6. Use a script to play your animation, e.g., `spine.play("#spinemodel", "your_animation_name")`.

## Known Issues & Limitations

- **Easing Curves:** The script attempts to convert easing curves. If your animation causes Defold to crash, try re-converting with the **"Force Linear"** checkbox enabled. This will change all transitions to be linear.
  
  ![DB Reborn Main Window](images/4_force_linear.png)

- **Shear Properties:** DragonBones automatically generates "shear" keyframes in its JSON output, even though there is no interface to control them. To prevent potential issues in Defold, DB Reborn removes all shear *curves*, leaving only the base time keys, which do not affect the final animation.
  
  ![DB Reborn Main Window](images/5_dragonbones_properties.png)

## Support & Contribution

- For tutorials and updates, visit the [YouTube Channel](https://www.youtube.com/@rfmcodedev).
- Please report any bugs by sending an email to [rfm.code.dev@gmail.com](mailto:rfm.code.dev@gmail.com).

Enjoy!
