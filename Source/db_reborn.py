#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
DB Reborn 1.0
Dragonbones to Spine Converter for Defold
For use in Defold Extension-Spine 3.6.5
Compatible with Spine 4.2.22
"""

import json
from PIL import Image
import os.path



"""
############################# BEGIN OF FUNCTIONS THAT CALC BEZIER CURVE #################################
"""

def bezier_curve_calc_begin_values(ini_value, last_value, vector):
    # Formula for Values (X1 and Y1) in the 'curve' list
    result = ini_value + ((last_value - ini_value) * vector)
    return result

def bezier_curve_calc_end_values_x(ini_value, last_value, vector):
    # Formula for Values (X1 and Y1) in the 'curve' list
    result = last_value - ((last_value - ini_value) * vector)
    return result

def bezier_curve_calc_end_values_y(last_value, vector):
    # Formula for Values (X2 and Y2) in the 'curve' list
    result = last_value * vector
    return result

def convertion_completed(value):
    conv_completed = value
    return conv_completed


"""
############################# END OF FUNCTIONS THAT CALC BEZIER CURVE #################################
"""

"""
###################### BEGIN DB CHECK - CHECK IF JSON WAS GENERATED FROM DRAGONBONES ##########################
"""
class DbJsonCheck:
    def __init__(self, json_file):
        self.json_file = json_file
        self.json_state = False
        #print(self.json_file_check)
        self.basic_key_pattern_list_json = ['skeleton', 'bones', 'slots', 'skins', 'animations']
        self.json_keys = []
        # Open Json
        with (open(self.json_file, 'r') as file_check):
            self.json_data_check = json.load(file_check) # The json we will check if it has the minimum arguments
        #Create a list of Json keys
        for key_to_check in self.json_data_check:
            #print(key_to_check)
            self.json_keys.append(key_to_check)
        self.check()

    def check(self):
        #print(self.basic_key_pattern_list_json, self.json_keys)
        #print(set(self.basic_key_pattern_list_json).intersection(self.json_keys))
        if set(self.basic_key_pattern_list_json).intersection(self.json_keys) == {'animations', 'skins', 'bones',
                                                                                  'skeleton', 'slots'}:
            self.json_state = True
        else:
            self.json_state = False

"""
###################### END OF DB CHECK - CHECK IF JSON WAS GENERATED FROM DRAGONBONES ##########################
"""

"""
###################################### BEGIN OF SCRIPT PROCESS #############################################
"""
class DbJsonConverter:

    def __init__(self, old_json_file_name, new_spinejson, spine_version, easing_type):
        self.old_json_file_name = old_json_file_name
        self.new_spinejson = new_spinejson
        self.spine_version = spine_version
        self.easing_type = easing_type
        self.file_converted = False
        self.conversion()

    def conversion(self):

        #print(old_json_file)
        # Open and read the JSON file
        with open(self.old_json_file_name, 'r') as file:
            json_data = json.load(file) # The json we will work

        with open(self.old_json_file_name, 'r') as file:
            old_json_data = json.load(file)  # The json we will get old curve data

        # Add Spine Version to the file
        json_data['skeleton']['spine'] = self.spine_version
        # print(json_data['skeleton'])

        # Add argument "order" to the bones. The base bone stay without it
        # print(len(json_data['ik']))
        if 'ik' in json_data:
            ik_len = len(json_data['ik'])
            #print(ik_len, json_data['ik'][0]['bones'][0][-1])
            for number in reversed(range(ik_len)):
                if number == 0:
                    continue
                #print(json_data['ik'][number]['bones'][0][-1])
                json_data['ik'][number]['order'] = number

        # Change skins section to a new configuration
        new_skins_structure = [{'name': 'default', 'attachments':{}}]
        # print(len(json_data['skins']['default']))

        # Copy Default Skins to the Attachments Dict
        new_skins_structure[0]['attachments'].update(json_data['skins']['default'])
        #print(new_skins_structure)

        #Replacing Skins Section to new_skins_structure
        json_data['skins'] = new_skins_structure
        skins_attachments = json_data['skins'][0]['attachments']
        # print(json_data['skins'])

        # Add Skins Keys into a dictionary with number of dictionaries inside each one
        skins_keys = {}
        list_of_skins = []
        for key in skins_attachments:
            skins_keys[key] = skins_attachments[key]
        #print(skins_keys)
        for k, v in skins_keys.items():
            #del values["name"]
            #print(k, v)
            for key, values in v.items():
                # Removing the Key "Name" -> It's not necessary
                # del values["name"]
                #print(key, values)
                list_of_skins.append(values)
        #print(list_of_skins)

        # Get the list of images in image folder
        imgs = []
        path = self.old_json_file_name[:-5]+"_texture/"
        valid_images = [".jpg",".gif",".png",".tga"]
        for file_name in os.listdir(path):
            #print(file_name)
            # Extension of image file
            ext = os.path.splitext(file_name)[1]
            # Get Each image name without extension do fill with the structure of skins
            image_name = os.path.splitext(file_name)[0]
            #print(ext, image_name)

            # Add Width and Height for each image
            image_size = Image.open(f"{path}/{file_name}")
            # print(image_name, type(image_name))
            # print(image.width, image.height, type(image.width), type(image.height) )

            # Add Width and Height for each image
            for key in list_of_skins:
                #print(key['name'])
                if image_name == key['name']:
                    # print(image_name, key)
                    key.update(width=image_size.width)
                    key.update(height=image_size.height)

            # If the extension is not in valid images, then exit
            if ext.lower() not in valid_images:
                continue
            imgs.append(Image.open(os.path.join(path,file_name)))
        temp_json_data = json_data  # Create a copy o json_data to work with
        old_temp_json_data = old_json_data # Make a copy to get the old curve values

        """
        ########################### ANIMATION SECTION ##################################
        
        ######################### BEGIN OF CURVE SECTION ###############################
        
        """
        if self.easing_type == 'curve':
            #print("Easy Type: Curve")

            #ROTATE Vars
            time_value_data_rotate = []
            db_time_value_data_rotate = []
            counter = 0
            step_curve = 0
            ini_value_original = 0

            # TRANSLATE Vars
            db_time_value_data_translate = []
            db_time_data_translate = []
            xy_data = []
            time_counter = 0
            time_counter_xy = 0
            counter_translate = 0
            temp_curve = 0
            ini_value_original_x = 0
            ini_value_original_y = 0

            # SCALE Vars
            db_time_value_data_scale = []
            db_time_data_scale = []
            xy_data_scale = []
            time_counter_scale = 0
            time_counter_xy_scale = 0
            counter_scale = 0
            temp_curve_scale = 0
            ini_value_original_x_scale = 0
            ini_value_original_y_scale = 0

            # SHEAR Vars
            db_time_value_data_shear = []
            db_time_data_shear = []
            xy_data_shear = []
            time_counter_shear = 0
            time_counter_xy_shear = 0
            counter_shear = 0
            temp_curve_shear = 0
            ini_value_original_x_shear = 0
            ini_value_original_y_shear = 0

            # This part gets the info of curve Vectors from de Old Dragonbones Json and put into a List
            # Loop in Animation Keys
            for anim_key_old in old_temp_json_data["animations"]:
                for bone_key_old in old_temp_json_data["animations"][anim_key_old]["bones"]:
                    attributes_old = old_temp_json_data["animations"][anim_key_old]["bones"][bone_key_old]
                    # Detecting if there's specific animation attributes in the Json

                    try:
                        attrib_rotate_old = attributes_old["rotate"]
                    except (Exception,):
                       attrib_rotate_old = []

                    try:
                        attrib_translate_old = attributes_old["translate"]
                    except (Exception,):
                        attrib_translate_old = []

                    try:
                        attrib_scale_old = attributes_old["scale"]
                    except (Exception,):
                        attrib_scale_old = []

                    try:
                        attrib_shear_old = attributes_old["shear"]
                    except (Exception,):
                        attrib_shear_old = []

                    ####### APPEND ALL CURVE LISTS INTO A "db_time_value_data_rotate" GLOBAL LIST
                    if attrib_rotate_old:
                        for items_old in attrib_rotate_old:
                            # print(items_old)
                            if 'curve' in items_old:
                                #print(dict_old['curve'])
                                if items_old['curve'] != 'stepped':
                                    #print(dict_old['curve'])
                                    # Get the original DB Vector Coordinates
                                    db_time_value_data_rotate.append(items_old['curve'])

                    if attrib_translate_old:
                        #print(attrib_translate_old[0]['curve'])

                        # The last time key frame doesn't have associated curve value. We need this to make calc later
                        # So I created a temp var that stores the ini curve of each animation
                        # At the bottom we will insert each curve value at the end of each animation
                        #print(attrib_translate_old[0])
                        # Get the list of 'easies' of Dragonbones, excluding the 'stepped' curves
                        if 'curve' in attrib_translate_old[0] and isinstance(attrib_translate_old[0]['curve'], list):
                            temp_curve = attrib_translate_old[0]['curve']
                        #print(temp_curve)
                        #print(attrib_translate_old)
                        for items_old in attrib_translate_old:
                            # Create a list of Translate X and Y values to use in future
                            # If there's not X and/or Y value, insert 0
                            #print(items_old)
                            if 'x' in items_old:
                                xy_data.append(items_old['x'])
                            if not 'x' in items_old:
                                xy_data.append(0)
                            if 'y' in items_old:
                                xy_data.append(items_old['y'])
                            if not 'y' in items_old:
                                xy_data.append(0)

                            if 'time' and 'curve' in items_old:
                                # Creating a list of translate times
                                db_time_data_translate.append(items_old['time'])
                                #if items_old['curve'] != 'stepped':
                                if isinstance(items_old['curve'], list):
                                    #print(items_old['curve'])
                                    # Get the original DB Vector Coordinates and put it into a var
                                    db_time_value_data_translate.append(items_old['curve'])
                            if 'time' and not 'curve' in items_old:
                                # The last time key in animation that doesn't have curve
                                db_time_data_translate.append(items_old['time'])
                                db_time_value_data_translate.append(temp_curve)
                    #print(db_time_value_data_translate)

                    if attrib_scale_old:
                        # Get the list of 'easies' of Dragonbones, excluding the 'stepped' curves
                        if 'curve' in attrib_scale_old[0] and isinstance(attrib_scale_old[0]['curve'], list):
                            temp_curve_scale = attrib_scale_old[0]['curve']

                        for items_old in attrib_scale_old:
                            # Create a list of Scale X and Y values to use in future
                            # If there's not X and/or Y value, insert 0
                            # print(items_old)
                            if 'x' in items_old:
                                xy_data_scale.append(items_old['x'])
                            if not 'x' in items_old:
                                xy_data_scale.append(0)
                            if 'y' in items_old:
                                xy_data_scale.append(items_old['y'])
                            if not 'y' in items_old:
                                xy_data_scale.append(0)

                            if 'time' and 'curve' in items_old:
                                # Creating a list of translate times
                                db_time_data_scale.append(items_old['time'])
                                # if items_old['curve'] != 'stepped':
                                if isinstance(items_old['curve'], list):
                                    # print(items_old['curve'])
                                    # Get the original DB Vector Coordinates and put it into a var
                                    db_time_value_data_scale.append(items_old['curve'])
                            if 'time' and not 'curve' in items_old:
                                # The last time key in animation that doesn't have curve
                                db_time_data_scale.append(items_old['time'])
                                db_time_value_data_scale.append(temp_curve_scale)

                    if attrib_shear_old:
                        # Get the list of 'easies' of Dragonbones, excluding the 'stepped' curves
                        if 'curve' in attrib_shear_old[0] and isinstance(attrib_shear_old[0]['curve'], list):
                            temp_curve_shear = attrib_shear_old[0]['curve']

                        for items_old in attrib_shear_old:
                            # Create a list of Scale X and Y values to use in future
                            # If there's not X and/or Y value, insert 0
                            # print(items_old)
                            if 'x' in items_old:
                                xy_data_shear.append(items_old['x'])
                            if not 'x' in items_old:
                                xy_data_shear.append(0)
                            if 'y' in items_old:
                                xy_data_shear.append(items_old['y'])
                            if not 'y' in items_old:
                                xy_data_shear.append(0)

                            if 'time' and 'curve' in items_old:
                                # Creating a list of translate times
                                db_time_data_shear.append(items_old['time'])
                                # if items_old['curve'] != 'stepped':
                                if isinstance(items_old['curve'], list):
                                    # print(items_old['curve'])
                                    # Get the original DB Vector Coordinates and put it into a var
                                    db_time_value_data_shear.append(items_old['curve'])
                            if 'time' and not 'curve' in items_old:
                                # The last time key in animation that doesn't have curve
                                db_time_data_shear.append(items_old['time'])
                                db_time_value_data_shear.append(temp_curve_shear)

            #time_counter = len(db_time_data_translate)
            #print(len(db_time_data_translate))
            # print(db_time_value_data_rotate, len(db_time_value_data_rotate))
            #print(db_time_value_data_translate, len(db_time_value_data_translate))
            # print(db_time_value_data_scale, len(db_time_value_data_scale))
            # print(db_time_value_data_shear, len(db_time_value_data_shear))

            ##### END ####
            # This part gets the info of curve Vectors from de Old Dragonbones Json and put into a List

            ########################## Loop in Animation Keys #####################################
            for anim_key in temp_json_data["animations"]:
                #print(anim_key)
                # Loop in all Bone Keys
                for bone_key in temp_json_data["animations"][anim_key]["bones"]:
                    #print(bone_key)
                    #print(temp_json_data["animations"][anim_key]["bones"])
                    attributes = temp_json_data["animations"][anim_key]["bones"][bone_key]
                    #print(attributes)

                    #Detecting if there's specific animation attributes in the Json
                    try:
                        attrib_rotate = attributes["rotate"]
                    except (Exception,):
                        attrib_rotate = []

                    try:
                        attrib_translate = attributes["translate"]
                    except (Exception,):
                        attrib_translate = []

                    try:
                        attrib_scale = attributes["scale"]
                    except (Exception,):
                        attrib_scale = []

                    try:
                        attrib_shear = attributes["shear"]
                        #del attributes['shear']
                    except (Exception,):
                        attrib_shear = []

                    """
                     >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> BEGIN OF ROTATE CURVE CALCULATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    """

                    if attrib_rotate:
                        #print(attrib_rotate)
                        # Replacing all 'angle' keys for 'value'
                        for dict_rot in attrib_rotate:
                            #print(dict)
                            #for keys in dict:
                            if 'angle' in dict_rot.keys():
                                    # Replacing all keys 'angle' to 'value' to make rotations works
                                dict_rot['value'] = dict_rot.pop('angle', None)

                            # Changing the order os keys to 'time', 'value', 'curve'
                            if 'curve' in dict_rot:
                                #print(dict)
                                key_dict = list(dict_rot.keys())
                                key_dict[0] = 'time'
                                key_dict[1] = 'value'
                                key_dict[2] = 'curve'
                                # Reorder 'time', 'value' and 'curve'
                                for k in key_dict:
                                    #print(k)
                                    dict_rot[k] = dict_rot.pop(k)
                                #print(dict['curve'])
                        # Create a list with the 'curve' 2 and 3 values to add in the next step
                        for step in range(len(attrib_rotate)):
                            # print(step)
                            if step < len(attrib_rotate) - 1: # Jump the last key, because it doesn't have curve
                                # If is there 3 arguments ('time', 'value' and 'curve') continues
                                if len(attrib_rotate[step]) >= 3:
                                    # If there's stepped curve, the script ignores
                                    if attrib_rotate[step]['curve'] != 'stepped':
                                        #print(attrib_rotate[step]['curve'])
                                        jump = step + 1
                                        #print(jump)
                                        next_time = attrib_rotate[jump]['time']
                                        next_value = attrib_rotate[jump]['value']
                                        #print(next_time, next_value)
                                        time_value_data_rotate.append(next_time)
                                        time_value_data_rotate.append(next_value)

                                # If is there only 2 values ('time' and 'value' ONLY, JUMP to next value)
                                # elif len(attrib_rotate[step]) <= 2:
                                #     jump = step + 1

                        for k in attrib_rotate:
                            #print(k.keys())
                            #Apply the actual 'time' and 'value' in the first two items (time1, value1) in the list 'curve'
                            if 'curve' in k:
                                #print(k)
                                # The script ignores the stepped curve
                                if k['curve'] != 'stepped':
                                    #print(k['curve'])
                                    k['curve'][0] = k['time']
                                    k['curve'][1] = k['value']

                        for val in attrib_rotate:
                            if len(val) >= 3:
                                #print(val)
                            # Apply the actual 'time' and 'value' in the last two items (time2, value2) in the list 'curve'
                                if 'curve' in val:
                                    # The script ignores the stepped curve
                                    if val['curve'] != 'stepped':
                                        #print(val['curve'])
                                        val['curve'][2] = time_value_data_rotate[step_curve]
                                        step_curve += 1
                                        val['curve'][3] = time_value_data_rotate[step_curve]
                                        step_curve += 1

                        #Apply a Function to calculate the Bézier curve from the Old Dragonbones Vector List
                        for element_dict in attrib_rotate:
                            #print(element_dict)
                            if 'curve' in element_dict:
                                if element_dict['curve'] != 'stepped':
                                    counter += 1
                                    # print(counter - 1)
                                    #print(element_dict['curve'])
                                    #print(db_time_value_data_rotate[counter - 1])
                                    for values in range(0, 4):
                                        #print(values)
                                        if values == 0: # Time 1
                                            # The format of Rotate is [time1, value1(angle1), time2, value2(angle2)]
                                            # For each curve gets the correspondent value to make calculations and change
                                            # Create temp vars to store the original values
                                            ini_value = element_dict['curve'][values]
                                            # Get the original value to calc later
                                            ini_value_original = element_dict['curve'][values]
                                            last_value = element_dict['curve'][values + 2]
                                            vector = db_time_value_data_rotate[counter - 1][values]
                                            #print(ini_value, last_value, vector)
                                            element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                ini_value, last_value, vector)

                                        if values == 1: # Value1
                                            ini_value = element_dict['curve'][values]
                                            last_value = element_dict['curve'][values + 2]
                                            vector = db_time_value_data_rotate[counter - 1][values]
                                            element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                ini_value, last_value, vector)

                                        if values == 2: # Time2
                                            #ini_value_original = element_dict['curve'][values - 2]
                                            last_value = element_dict['curve'][values]
                                            vector = db_time_value_data_rotate[counter - 1][values]
                                            # Use the original value to correct curve calculation
                                            element_dict['curve'][values] = bezier_curve_calc_end_values_x(
                                                ini_value_original, last_value, vector)

                                        if values == 3: # Value 2
                                            last_value = element_dict['curve'][values]
                                            vector = db_time_value_data_rotate[counter - 1][values]
                                            element_dict['curve'][values] = bezier_curve_calc_end_values_y(
                                                last_value, vector)
                    # print(db_time_value_data_rotate)
                    # print(time_value_data_rotate)
                    # print(attrib_rotate)
                    """
                    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END OF ROTATE CURVE CALCULATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    """

                    """
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>> BEGIN OF TRANSLATE CURVE CALCULATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    """

                    if attrib_translate:
                        # Reorder the key attributes
                        for dictx in attrib_translate:
                            #print(dict)
                            # Changing the order os keys to 'time', 'x', 'y' and 'curve'
                            key_dict = list(dictx.keys())
                            #print(key_dict, len(key_dict))
                            if len(key_dict) == 4:
                                key_dict[0] = 'time'
                                key_dict[1] = 'x'
                                key_dict[2] = 'y'
                                key_dict[3] = 'curve'

                            if len(key_dict) == 3:
                                key_dict[0] = 'time'
                                if 'x' and not 'y' in dictx.keys():
                                    key_dict[1] = 'x'
                                if 'y' and not 'x' in dictx.keys():
                                    key_dict[1] = 'y'
                                if 'y' and 'x' in dictx.keys():
                                    key_dict[1] = 'x'
                                    key_dict[2] = 'y'
                                if 'curve' in dictx.keys():
                                    key_dict[2] = 'curve'

                            if len(key_dict) == 2:
                                key_dict[0] = 'time'
                                if 'x' in dictx.keys():
                                    key_dict[1] = 'x'
                                if 'y' in dictx.keys():
                                    key_dict[1] = 'y'
                                if 'curve' in dictx.keys():
                                    key_dict[1] = 'curve'

                            for k in key_dict:
                                dictx[k] = dictx.pop(k)
                                # print(k)

                            # Add 4 more items in list 'curve'
                            try:
                                if dictx['curve'] != 'stepped':
                                    if 'curve' in dictx:
                                        # Add 4 more items in each 'curve' to use later. I choose 999 to be more visible.
                                        dictx['curve'].append(999)
                                        dictx['curve'].append(999)
                                        dictx['curve'].append(999)
                                        dictx['curve'].append(999)

                                    # Add initial time1 to the positions 0 and 4 of the curve list
                                        dictx['curve'][0] = dictx['time']
                                        dictx['curve'][4] = dictx['time']
                            except (Exception,):
                                pass

                            #print(key_dict)
                            #print(dict)
                            # Get initial x1 and y1 values if there's x or y values. If not, they are 0.
                            if len(key_dict) == 4:  # There time, curve, x and y
                                # Use this to get 'curve' that has a list, not "stepped"
                                if isinstance(dictx['curve'], list):
                                    dictx['curve'][1] = dictx['x']
                                    dictx['curve'][5] = dictx['y']

                            if len(key_dict) == 3: # There time and/or curve and/or x and/or y
                                try:
                                    if isinstance(dictx['curve'], list):
                                        if 'x' in dictx:
                                            dictx['curve'][1] = dictx['x']
                                        else:
                                            dictx['curve'][1] = 0
                                        if 'y' in dictx:
                                            #if 'curve' in dict:
                                            dictx['curve'][5] = dictx['y']
                                        else:
                                            dictx['curve'][5] = 0
                                except (Exception,):
                                    pass

                            if len(key_dict) == 2: # There only time plus curve or x or y
                                try:
                                    if isinstance(dictx['curve'], list):
                                        #If not x or y, the x and y initial values in curve are 0.
                                        dictx['curve'][1] = 0
                                        dictx['curve'][5] = 0
                                except (Exception,):
                                    pass
                            #print(dict)
                        #print(attrib_translate)
                        # Add time2 to the specific positions( 2 and 6) of the list
                        for d in attrib_translate:
                            #print(d)
                            if 'curve' in d:
                                if isinstance(d['curve'], list):
                                    #print(d['curve'], time_counter, db_time_data_translate[time_counter + 1])
                                    #print(db_time_data_translate)
                                    d['curve'][2] = db_time_data_translate[time_counter + 1]
                                    d['curve'][6] = db_time_data_translate[time_counter + 1]
                            if 'time' in d:
                                time_counter += 1
                        #print('xy data', xy_data)
                        for item in attrib_translate:
                            #print(item)
                            if item['time'] == 0: # If the script reaches the first item in the list, jump 2
                                #print(item)
                                time_counter_xy += 2
                            # If the first item doesn't have curve, jump 2
                            if item['time'] == 0 and not 'curve' in item:
                                time_counter_xy += 2

                            # If there's curve in an item, proceed with the insert o data
                            if 'curve' in item:
                                # if the curve is a list, insert items
                                if isinstance(item['curve'], list):
                                    item['curve'][3] = xy_data[time_counter_xy]
                                    time_counter_xy += 1
                                    item['curve'][7] = xy_data[time_counter_xy]
                                    time_counter_xy += 1
                                    #print(xy_data[time_counter_xy], time_counter_xy)

                                # If there's a "stepped" curve, jump 2
                                if isinstance(item['curve'], str):
                                    time_counter_xy += 2

                            # If there's keyframes that doesn't have curves list, and they don't locate in the
                            # beginning or the last keyframe, jump 2
                            if not 'curve' in item and item['time'] != 0 and item != attrib_translate[-1]:
                                #print(item)
                                time_counter_xy += 2
                                # print(time_counter_xy)
                                # print(xy_data)
                                #print(type(item['curve']))
                            #print(item)

                        # The Translation Curve format is: [time1, x1, time2, x2, time1, y1, time2, y2]
                        # Apply a Function to calculate the Bézier curve from the Old Dragonbones Vector List
                        for element_dict in attrib_translate:
                            #print(element_dict)
                            if 'curve' in element_dict:
                                if isinstance(element_dict['curve'], list): # Using element_dict != 'stepped'
                                    counter_translate += 1
                                    #print(counter_translate - 1)
                                    #print(element_dict['curve'])
                                    #print(db_time_value_data_translate)
                                    for values in range(0, 8):
                                        #print(values)
                                        if isinstance(db_time_value_data_translate, list):
                                            if values == 0:  # Time1

                                                #print(element_dict)
                                                ini_value = element_dict['curve'][values]
                                                # Get the original value to use later
                                                ini_value_original_x = element_dict['curve'][values]
                                                last_value = element_dict['curve'][values + 2]
                                                vector = db_time_value_data_translate[counter_translate - 1][values]
                                                #print(db_time_value_data_translate)
                                                #print(type(ini_value), type(last_value), type(vector))
                                                #print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value, last_value, vector)
                                                #print(db_time_value_data_translate[counter][values])

                                            if values == 1:  # X1
                                                ini_value = element_dict['curve'][values]
                                                last_value = element_dict['curve'][values + 2]
                                                vector = db_time_value_data_translate[counter_translate - 1][values]
                                                #print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value, last_value, vector)

                                            if values == 2: # Time2
                                                #print(element_dict)
                                                #ini_value = element_dict['curve'][values - 2]
                                                last_value = element_dict['curve'][values]
                                                vector = db_time_value_data_translate[counter_translate - 1][values]
                                                #print(ini_value, last_value, vector)
                                                # Use the original value to correct curve calculation
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_x(
                                                    ini_value_original_x, last_value, vector)

                                            if values == 3: # X2
                                                last_value = element_dict['curve'][values]
                                                vector = db_time_value_data_translate[counter_translate - 1][values]
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_y(
                                                    last_value, vector)

                                            # As db_time_value_data_translate curve has only 4 values,
                                            # we begin values from 0
                                            if values == 4:  # Time1 --Get 0
                                                ini_value = element_dict['curve'][values]
                                                ini_value_original_y = element_dict['curve'][values]
                                                last_value = element_dict['curve'][values + 2]
                                                vector = db_time_value_data_translate[counter_translate
                                                                                      - 1][values - values]
                                                #print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value, last_value, vector)

                                            if values == 5:  # Y1 - -Get 1
                                                ini_value = element_dict['curve'][values]
                                                last_value = element_dict['curve'][values + 2]
                                                vector = db_time_value_data_translate[counter_translate
                                                                                      - 1][values - values + 1]
                                                #print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value, last_value, vector)

                                            if values == 6:  # Time2 - - Get 2
                                                #ini_value = element_dict['curve'][values - 2]
                                                last_value = element_dict['curve'][values]
                                                vector = db_time_value_data_translate[counter_translate
                                                                                      - 1][values - values + 2]
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_x(
                                                    ini_value_original_y, last_value, vector)

                                            if values == 7:  # Y2 - - Get 3
                                                last_value = element_dict['curve'][values]
                                                vector = db_time_value_data_translate[counter_translate
                                                                                      - 1][values - values + 3]
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_y(
                                                    last_value, vector)

                    """
                    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END OF TRANSLATE CURVE CALCULATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    """

                    """
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>> BEGIN OF SCALE CURVE CALCULATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    """
                    if attrib_scale:
                        # Reorder the key attributes
                        for dict_sc in attrib_scale:
                            # print(dict)
                            # Changing the order os keys to 'time', 'x', 'y' and 'curve'
                            key_dict = list(dict_sc.keys())
                            # print(key_dict, len(key_dict))
                            if len(key_dict) == 4:
                                key_dict[0] = 'time'
                                key_dict[1] = 'x'
                                key_dict[2] = 'y'
                                key_dict[3] = 'curve'

                            if len(key_dict) == 3:
                                key_dict[0] = 'time'
                                if 'x' and not 'y' in dict_sc.keys():
                                    key_dict[1] = 'x'
                                if 'y' and not 'x' in dict_sc.keys():
                                    key_dict[1] = 'y'
                                if 'y' and 'x' in dict_sc.keys():
                                    key_dict[1] = 'x'
                                    key_dict[2] = 'y'
                                if 'curve' in dict_sc.keys():
                                    key_dict[2] = 'curve'

                            if len(key_dict) == 2:
                                key_dict[0] = 'time'
                                if 'x' in dict_sc.keys():
                                    key_dict[1] = 'x'
                                if 'y' in dict_sc.keys():
                                    key_dict[1] = 'y'
                                if 'curve' in dict_sc.keys():
                                    key_dict[1] = 'curve'

                            for k in key_dict:
                                dict_sc[k] = dict_sc.pop(k)
                                # print(k)

                            # Add 4 more items in list 'curve'
                            try:
                                if dict_sc['curve'] != 'stepped':
                                    if 'curve' in dict_sc:
                                        # Add 4 more items in each 'curve' to use later. I choose 999 to be more visible.
                                        dict_sc['curve'].append(999)
                                        dict_sc['curve'].append(999)
                                        dict_sc['curve'].append(999)
                                        dict_sc['curve'].append(999)

                                        # Add initial time1 to the positions 0 and 4 of the curve list
                                        dict_sc['curve'][0] = dict_sc['time']
                                        dict_sc['curve'][4] = dict_sc['time']
                            except (Exception,):
                                pass

                            # print(key_dict)
                            # print(dict)
                            # Get initial x1 and y1 values if there's x or y values. If not, they are 0.
                            if len(key_dict) == 4:  # There time, curve, x and y
                                # Use this to get 'curve' that has a list, not "stepped"
                                if isinstance(dict_sc['curve'], list):
                                    dict_sc['curve'][1] = dict_sc['x']
                                    dict_sc['curve'][5] = dict_sc['y']

                            if len(key_dict) == 3:  # There time and/or curve and/or x and/or y
                                try:
                                    if isinstance(dict_sc['curve'], list):
                                        if 'x' in dict_sc:
                                            dict_sc['curve'][1] = dict_sc['x']
                                        else:
                                            dict_sc['curve'][1] = 0
                                        if 'y' in dict_sc:
                                            # if 'curve' in dict:
                                            dict_sc['curve'][5] = dict_sc['y']
                                        else:
                                            dict_sc['curve'][5] = 0
                                except (Exception,):
                                    pass

                            if len(key_dict) == 2:  # There only time plus curve or x or y
                                try:
                                    if isinstance(dict_sc['curve'], list):
                                        # If not x or y, the x and y initial values in curve are 0.
                                        dict_sc['curve'][1] = 0
                                        dict_sc['curve'][5] = 0
                                except (Exception,):
                                    pass
                            # print(dict)
                        # print(attrib_scale)
                        # Add time2 to the specific positions( 2 and 6) of the list
                        for d in attrib_scale:
                            # print(d)
                            if 'curve' in d:
                                if isinstance(d['curve'], list):
                                    # if 'curve' in attrib_scale[step_scale] != 'stepped':
                                    # print(d['curve'], time_counter, db_time_data_scale[time_counter_scale + 1])
                                    # print(db_time_data_scale)
                                    d['curve'][2] = db_time_data_scale[time_counter_scale + 1]
                                    d['curve'][6] = db_time_data_scale[time_counter_scale + 1]
                            if 'time' in d:
                                time_counter_scale += 1
                        # print('xy data', xy_data)
                        for item in attrib_scale:
                            # print(item)
                            if item['time'] == 0:  # If the script reaches the first item in the list, jump 2
                                # print(item)
                                time_counter_xy_scale += 2
                            # If the first item doesn't have curve, jump 2
                            if item['time'] == 0 and not 'curve' in item:
                                time_counter_xy_scale += 2

                            # If there's curve in an item, proceed with the insert o data
                            if 'curve' in item:
                                # if the curve is a list, insert items
                                if isinstance(item['curve'], list):
                                    item['curve'][3] = xy_data_scale[time_counter_xy_scale]
                                    time_counter_xy_scale += 1
                                    item['curve'][7] = xy_data_scale[time_counter_xy_scale]
                                    time_counter_xy_scale += 1
                                    # print(xy_data[time_counter_xy], time_counter_xy)

                                # If there's a "stepped" curve, jump 2
                                if isinstance(item['curve'], str):
                                    time_counter_xy_scale += 2

                            # If there's keyframes that doesn't have curves list, and they don't locate in the
                            # beginning or the last keyframe, jump 2
                            if not 'curve' in item and item['time'] != 0 and item != attrib_scale[-1]:
                                # print(item)
                                time_counter_xy_scale += 2
                                # print(time_counter_xy)
                                # print(xy_data)
                                # print(type(item['curve']))
                            # print(item)

                        # The Scale Curve format is: [time1, x1, time2, x2, time1, y1, time2, y2]
                        # Apply a Function to calculate the Bézier curve from the Old Dragonbones Vector List
                        for element_dict in attrib_scale:
                            # print(element_dict)
                            if 'curve' in element_dict:
                                if isinstance(element_dict['curve'], list):  # Using element_dict != 'stepped'
                                    counter_scale += 1
                                    # print(counter_scale - 1)
                                    # print(element_dict['curve'])
                                    # print(db_time_value_data_scale)
                                    for values in range(0, 8):
                                        # print(values)
                                        if isinstance(db_time_value_data_scale, list):
                                            if values == 0:  # Time1

                                                # print(element_dict)
                                                ini_value_scale = element_dict['curve'][values]
                                                # Get the original value to use later
                                                ini_value_original_x_scale = element_dict['curve'][values]
                                                last_value_scale = element_dict['curve'][values + 2]
                                                vector_scale = db_time_value_data_scale[counter_scale - 1][values]
                                                # print(db_time_value_data_scale)
                                                # print(type(ini_value), type(last_value), type(vector))
                                                # print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value_scale, last_value_scale, vector_scale)
                                                # print(db_time_value_data_scale[counter][values])

                                            if values == 1:  # X1
                                                ini_value_scale = element_dict['curve'][values]
                                                last_value_scale = element_dict['curve'][values + 2]
                                                vector_scale = db_time_value_data_scale[counter_scale - 1][values]
                                                # print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value_scale, last_value_scale, vector_scale)

                                            if values == 2:  # Time2
                                                # print(element_dict)
                                                # ini_value = element_dict['curve'][values - 2]
                                                last_value_scale = element_dict['curve'][values]
                                                vector_scale = db_time_value_data_scale[counter_scale - 1][values]
                                                # print(ini_value, last_value, vector)
                                                # Use the original value to correct curve calculation
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_x(
                                                    ini_value_original_x_scale, last_value_scale, vector_scale)

                                            if values == 3:  # X2
                                                last_value_scale = element_dict['curve'][values]
                                                vector_scale = db_time_value_data_scale[counter_scale - 1][values]
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_y(
                                                    last_value_scale, vector_scale)

                                            # As db_time_value_data_scale curve has only 4 values, we begin values from 0
                                            if values == 4:  # Time1 --Get 0
                                                ini_value_scale = element_dict['curve'][values]
                                                ini_value_original_y_scale = element_dict['curve'][values]
                                                last_value_scale = element_dict['curve'][values + 2]
                                                vector_scale = db_time_value_data_scale[counter_scale
                                                                                        - 1][values - values]
                                                # print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value_scale, last_value_scale, vector_scale)

                                            if values == 5:  # Y1 - -Get 1
                                                ini_value_scale = element_dict['curve'][values]
                                                last_value_scale = element_dict['curve'][values + 2]
                                                vector_scale = db_time_value_data_scale[counter_scale
                                                                                        - 1][values - values + 1]
                                                # print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value_scale, last_value_scale, vector_scale)

                                            if values == 6:  # Time2 - - Get 2
                                                # ini_value = element_dict['curve'][values - 2]
                                                last_value_scale = element_dict['curve'][values]
                                                vector_scale = db_time_value_data_scale[counter_scale
                                                                                        - 1][values - values + 2]
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_x(
                                                    ini_value_original_y_scale, last_value_scale, vector_scale)

                                            if values == 7:  # Y2 - - Get 3
                                                last_value_scale = element_dict['curve'][values]
                                                vector_scale = db_time_value_data_scale[counter_scale
                                                                                        - 1][values - values + 3]
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_y(
                                                    last_value_scale, vector_scale)

                    """
                    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END OF SCALE CURVE CALCULATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    """

                    """
                    # >>>>>>>>>>>>>>>>>>>>>>>>>>> BEGIN OF SHEAR CURVE CALCULATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    """
                    if attrib_shear:
                        # Reorder the key attributes
                        for dict_sh in attrib_shear:
                            # print(dict)
                            # Changing the order os keys to 'time', 'x', 'y' and 'curve'
                            key_dict = list(dict_sh.keys())
                            # print(key_dict, len(key_dict))
                            if len(key_dict) == 4:
                                key_dict[0] = 'time'
                                key_dict[1] = 'x'
                                key_dict[2] = 'y'
                                key_dict[3] = 'curve'

                            if len(key_dict) == 3:
                                key_dict[0] = 'time'
                                if 'x' and not 'y' in dict_sh.keys():
                                    key_dict[1] = 'x'
                                if 'y' and not 'x' in dict_sh.keys():
                                    key_dict[1] = 'y'
                                if 'y' and 'x' in dict_sh.keys():
                                    key_dict[1] = 'x'
                                    key_dict[2] = 'y'
                                if 'curve' in dict_sh.keys():
                                    key_dict[2] = 'curve'

                            if len(key_dict) == 2:
                                key_dict[0] = 'time'
                                if 'x' in dict_sh.keys():
                                    key_dict[1] = 'x'
                                if 'y' in dict_sh.keys():
                                    key_dict[1] = 'y'
                                if 'curve' in dict_sh.keys():
                                    key_dict[1] = 'curve'

                            for k in key_dict:
                                dict_sh[k] = dict_sh.pop(k)
                                # print(k)

                            # Add 4 more items in list 'curve'
                            try:
                                if dict_sh['curve'] != 'stepped':
                                    if 'curve' in dict_sh:
                                        # Add 4 more items in each 'curve' to use later. I choose 999 to be more visible.
                                        dict_sh['curve'].append(999)
                                        dict_sh['curve'].append(999)
                                        dict_sh['curve'].append(999)
                                        dict_sh['curve'].append(999)

                                        # Add initial time1 to the positions 0 and 4 of the curve list
                                        dict_sh['curve'][0] = dict_sh['time']
                                        dict_sh['curve'][4] = dict_sh['time']
                            except (Exception,):
                                pass

                            # print(key_dict)
                            # print(dict)
                            # Get initial x1 and y1 values if there's x or y values. If not, they are 0.
                            if len(key_dict) == 4:  # There time, curve, x and y
                                # Use this to get 'curve' that has a list, not "stepped"
                                if isinstance(dict_sh['curve'], list):
                                    dict_sh['curve'][1] = dict_sh['x']
                                    dict_sh['curve'][5] = dict_sh['y']

                            if len(key_dict) == 3:  # There time and/or curve and/or x and/or y
                                try:
                                    if isinstance(dict_sh['curve'], list):
                                        if 'x' in dict_sh:
                                            dict_sh['curve'][1] = dict_sh['x']
                                        else:
                                            dict_sh['curve'][1] = 0
                                        if 'y' in dict_sh:
                                            # if 'curve' in dict:
                                            dict_sh['curve'][5] = dict_sh['y']
                                        else:
                                            dict_sh['curve'][5] = 0
                                except (Exception,):
                                    pass

                            if len(key_dict) == 2:  # There only time plus curve or x or y
                                try:
                                    if isinstance(dict_sh['curve'], list):
                                        # If not x or y, the x and y initial values in curve are 0.
                                        dict_sh['curve'][1] = 0
                                        dict_sh['curve'][5] = 0
                                except (Exception,):
                                    pass
                            # print(dict)
                        # print(attrib_shear)
                        # Add time2 to the specific positions( 2 and 6) of the list
                        for d in attrib_shear:
                            #print(d)
                            if 'curve' in d:
                                if isinstance(d['curve'], list):
                                    # print(d['curve'], time_counter_shear, db_time_data_shear[time_counter_shear + 1])
                                    #print(db_time_data_shear)
                                    d['curve'][2] = db_time_data_shear[time_counter_shear + 1]
                                    d['curve'][6] = db_time_data_shear[time_counter_shear + 1]
                            if 'time' in d:
                                time_counter_shear += 1
                        # print('xy data', xy_data)
                        for item in attrib_shear:
                            # print(item)
                            if item['time'] == 0:  # If the script reaches the first item in the list, jump 2
                                # print(item)
                                time_counter_xy_shear += 2
                            # If the first item doesn't have curve, jump 2
                            if item['time'] == 0 and not 'curve' in item:
                                time_counter_xy_shear += 2

                            # If there's curve in an item, proceed with the insert o data
                            if 'curve' in item:
                                # if the curve is a list, insert items
                                if isinstance(item['curve'], list):
                                    item['curve'][3] = xy_data_shear[time_counter_xy_shear]
                                    time_counter_xy_shear += 1
                                    item['curve'][7] = xy_data_shear[time_counter_xy_shear]
                                    time_counter_xy_shear += 1
                                    # print(xy_data[time_counter_xy], time_counter_xy)

                                # If there's a "stepped" curve, jump 2
                                if isinstance(item['curve'], str):
                                    time_counter_xy_shear += 2

                            # If there's keyframes that doesn't have curves list, and they don't locate in the
                            # beginning or the last keyframe, jump 2
                            if not 'curve' in item and item['time'] != 0 and item != attrib_shear[-1]:
                                # print(item)
                                time_counter_xy_shear += 2
                                # print(time_counter_xy)
                                # print(xy_data)
                                # print(type(item['curve']))
                            # print(item)

                        # The Shear Curve format is: [time1, x1, time2, x2, time1, y1, time2, y2]
                        # Apply a Function to calculate the Bézier curve from the Old Dragonbones Vector List
                        for element_dict in attrib_shear:
                            # print(element_dict)
                            if 'curve' in element_dict:
                                if isinstance(element_dict['curve'], list):  # Using element_dict != 'stepped'
                                    counter_shear += 1
                                    # print(counter_shear - 1)
                                    # print(element_dict['curve'])
                                    # print(db_time_value_data_shear)
                                    for values in range(0, 8):
                                        # print(values)
                                        if isinstance(db_time_value_data_shear, list):
                                            if values == 0:  # Time1

                                                # print(element_dict)
                                                ini_value_shear = element_dict['curve'][values]
                                                # Get the original value to use later
                                                ini_value_original_x_shear = element_dict['curve'][values]
                                                last_value_shear = element_dict['curve'][values + 2]
                                                vector_shear = db_time_value_data_shear[counter_shear - 1][values]
                                                # print(db_time_value_data_shear)
                                                # print(type(ini_value), type(last_value), type(vector))
                                                # print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value_shear, last_value_shear, vector_shear)
                                                # print(db_time_value_data_shear[counter][values])

                                            if values == 1:  # X1
                                                ini_value_shear = element_dict['curve'][values]
                                                last_value_shear = element_dict['curve'][values + 2]
                                                vector_shear = db_time_value_data_shear[counter_shear - 1][values]
                                                # print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value_shear, last_value_shear, vector_shear)

                                            if values == 2:  # Time2
                                                # print(element_dict)
                                                # ini_value = element_dict['curve'][values - 2]
                                                last_value_shear = element_dict['curve'][values]
                                                vector_shear = db_time_value_data_shear[counter_shear - 1][values]
                                                # print(ini_value, last_value, vector)
                                                # Use the original value to correct curve calculation
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_x(
                                                    ini_value_original_x_shear, last_value_shear, vector_shear)

                                            if values == 3:  # X2
                                                last_value_shear = element_dict['curve'][values]
                                                vector_shear = db_time_value_data_shear[counter_shear - 1][values]
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_y(
                                                    last_value_shear, vector_shear)

                                            # As db_time_value_data_shear curve has only 4 values, we begin values from 0
                                            if values == 4:  # Time1 --Get 0
                                                ini_value_shear = element_dict['curve'][values]
                                                ini_value_original_y_shear = element_dict['curve'][values]
                                                last_value_shear = element_dict['curve'][values + 2]
                                                vector_shear = db_time_value_data_shear[counter_shear
                                                                                        - 1][values - values]
                                                # print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value_shear, last_value_shear, vector_shear)

                                            if values == 5:  # Y1 - -Get 1
                                                ini_value_shear = element_dict['curve'][values]
                                                last_value_shear = element_dict['curve'][values + 2]
                                                vector_shear = db_time_value_data_shear[counter_shear
                                                                                        - 1][values - values + 1]
                                                # print(ini_value, last_value, vector)
                                                element_dict['curve'][values] = bezier_curve_calc_begin_values(
                                                    ini_value_shear, last_value_shear, vector_shear)

                                            if values == 6:  # Time2 - - Get 2
                                                # ini_value = element_dict['curve'][values - 2]
                                                last_value_shear = element_dict['curve'][values]
                                                vector_shear = db_time_value_data_shear[counter_shear
                                                                                        - 1][values - values + 2]
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_x(
                                                    ini_value_original_y_shear, last_value_shear, vector_shear)

                                            if values == 7:  # Y2 - - Get 3
                                                last_value_shear = element_dict['curve'][values]
                                                vector_shear = db_time_value_data_shear[counter_shear
                                                                                        - 1][values - values + 3]
                                                element_dict['curve'][values] = bezier_curve_calc_end_values_y(
                                                    last_value_shear, vector_shear)

                    """
                    >>>>>>>>>>>>>>>>>>>>>>>>>>>>>> END OF SHEAR CURVE CALCULATION <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                    """



        """
        ######################################## END OF CURVE#############################################
        """

        """
        ############################### BEGIN OF LINEAR SECTION #############################################
        """

        if self.easing_type == 'linear':
            #print("Easy Type: Linear")
            for anim_key in temp_json_data["animations"]:
                for bone_key in temp_json_data["animations"][anim_key]["bones"]:
                    #print(json_data["animations"][anim_key]["bones"][bone_key])
                    attributes = temp_json_data["animations"][anim_key]["bones"][bone_key]
                    #print(attributes)
                    for items in attributes.values():
                        #print(items)
                        for dictionary in items:
                            # print(dict)
                            if 'curve' in dictionary.keys():
                                del dictionary['curve']  # Delete all 'curve' attributes, making all animations linear.
                                # print(dict)
                            # Replacing all keys 'angle' to 'value' to make rotations works
                            if 'angle' in dictionary:
                                dictionary['value'] = dictionary.pop('angle', None)
        """
        ################################## END OF LINEAR SECTION #############################################
        """
        """
        ################################## END OF ANIMATIONS ##################################################
        """
        """
        ################################# BEGIN OF FILE SAVE ######################################################
        """
        # Copy the Temp Json back to the Json Data
        json_data = temp_json_data

        # Convert final Json file to Pretty JSON and save it with new extension (.spinejson) for use in Defold
        converted = json.dumps(json_data, indent=4)

        # Creating new filename with .spinejson extension from old json file
        # new_spinejson_file_name = self.old_json_file_name[:-5] + ".spinejson"
        new_spinejson_file_name = self.new_spinejson

        # Generate a new .spinejson file in the same folder of db_reborn
        with open(new_spinejson_file_name, 'w') as file:
            file.write(converted)

        #print("Success generate file " + new_spinejson_file_name, "from " + self.old_json_file_name)
        self.file_converted = True


        """
        ################################# END OF FILE SAVE ######################################################
        """

"""
###################################### END OF SCRIPT PROCESS #############################################
"""

"""
################################# BEGIN OF ENTER THE SCRIPT ##################################################
"""

# if __name__ == "__main__":
#     # If "linear", the script will erase all 'curve' dicts and put all animations linear to prevent crashes.
#     # If "curve", the script will convert the Dragonbones "easing" ('curve': [0, 0, 0.5, 1])
#     # to the format of Spine ('curve': [frame1, value1, frame2, value2]) in case of 'angle'.
#     # In case of 'translate', 'scale' and 'shear' there are the double of values: x and y
#     # ('curve': [frame1, value_x1, frame2, value_x2, frame1, value_y1, frame2, value_y2])
#
#     # Using arguments in command line
#     # old_json_file_name = sys.argv[1] # Using argument passed in command line
#     # easing_type = sys.argv[2] # Passing argument "linear" or "curve"
#
#     easing_type = 'curve'
#     #easing_type = 'linear'
#     old_json_file_name = 'Personagem_Coa_Tools_CURVE.json'
#     db_json_converter(old_json_file_name)

"""
################################# END OF ENTER THE SCRIPT ######################################################
"""


