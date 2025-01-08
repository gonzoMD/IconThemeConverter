import os
import json
import cairosvg
from PIL import Image

# Helper function to calculate the position of overlays and icons inside a bigger canvas
def getposition(sizea, sizeb, gravity="center"):
    if gravity.lower()=="center":
        resxy = (((sizea - sizeb)//2),((sizea - sizeb)//2))
    elif gravity.lower()=="north":
        resxy = (((sizea - sizeb)//2),0)
    elif gravity.lower()=="east":
        resxy = ((sizea - sizeb),((sizea - sizeb)//2))
    elif gravity.lower()=="south":
        resxy = (((sizea - sizeb)//2),(sizea - sizeb))
    elif gravity.lower()=="west":
        resxy = (0,((sizea - sizeb)//2))
    elif gravity.lower()=="northwest":
        resxy = (0,0)
    elif gravity.lower()=="northeast":
        resxy = ((sizea - sizeb),0)
    elif gravity.lower()=="southwest":
        resxy = (0,(sizea - sizeb))
    elif gravity.lower()=="southeast":
        resxy = ((sizea - sizeb),(sizea - sizeb))
    else:
        resxy=(0,0)
    return resxy

# read the settings file
with open('settings.json', 'r') as f:
    settings = json.load(f)

# get the directory with the source files from the settings
icon_definition_dir = os.fsencode(settings["path_jsonfiles"])

# check if the directory exists. if yes, get a list of containing files, if not, quit with an error message
if os.path.exists(icon_definition_dir):
    icon_definitions = os.listdir(icon_definition_dir)
else:
    print("Error: The directory ", icon_definition_dir, " does not exist. Please check the value of 'path_jsonfiles' in settings.json!")
    quit()

# get the directory with the icon theme from the settings
icon_theme_dir = os.fsencode(settings["path_icontheme"])

# quit with an error message, if the directory doesn't exist
if not os.path.exists(icon_theme_dir):
    print("Error: The directory ", icon_theme_dir, " does not exist. Please check the value of 'path_icontheme' in settings.json!")
    quit()

# if we have no temp directory yet create one
if os.path.exists("./temp") == False:
    os.mkdir("./temp")

# process all icon definition files
for file in icon_definitions:
    if os.fsdecode(file).endswith(".json"):
        filename = os.path.join(icon_definition_dir, file)
        print("process icon definition file:", filename)
        with open(filename, 'r') as f:
            curfile = json.load(f)

        # get the output directory where the icons will be saved to from the icon definition file, and create it if it doesn't exist yet
        output_path = os.path.join("./output", curfile["path_out_ico"])
        print("target directory:", output_path)
        if os.path.exists(output_path) == False:
            os.makedirs(output_path)

        # process all icons in the current icon definition file
        for icon in curfile["icon"]:
            
            images=[]
            sizes=[]

            # read all inputfiles for this icon
            for inputfile in icon["file_in"]:
                imagefile = os.path.join(settings["path_icontheme"], inputfile["src"])
                if not os.path.exists(imagefile):
                    print("warning: unable to find source image file:", imagefile, "\n\t Skip it.")
                    continue
                tempfile = str(inputfile["size"]) + ".png"
                tempfile = os.path.join("./temp", tempfile)
                cairosvg.svg2png(url=imagefile, output_width = inputfile["size"], output_height = inputfile["size"], write_to=tempfile)
                tempsize=(inputfile["size"],inputfile["size"])

                # if we have a defined image as overlay, paste it, related to its gravity and size
                if "overlay" in inputfile:
                    ovlsrc = os.path.join(settings["path_icontheme"], inputfile["overlay"]["src"])
                    if os.path.exists(ovlsrc):

                        cairosvg.svg2png(url=ovlsrc, parent_width = inputfile["overlay"]["size"], parent_height = inputfile["overlay"]["size"], write_to="./temp/overlay.png")
                        icn = Image.open(tempfile)
                        icn.paste(Image.open("./temp/overlay.png"),getposition(inputfile["size"],inputfile["overlay"]["size"], inputfile["overlay"]["gravity"]),Image.open("./temp/overlay.png"))
                        icn.save(tempfile)
                    else:
                        print("warning: unable to find overlay image file:", ovlsrc, "\n\t Skip it and ignore the overlay.")

                # if we have a specific canvas size, create a new image of its size and there paste the icon related to the gravity
                if "canvas" in inputfile:
                    can = Image.new(mode="RGBA",size=(inputfile["canvas"]["size"],inputfile["canvas"]["size"]))
                    can.paste(Image.open(tempfile),getposition(inputfile["canvas"]["size"],inputfile["size"], inputfile["canvas"]["gravity"]))
                    can.save(tempfile)
                    tempsize=(inputfile["canvas"]["size"],inputfile["canvas"]["size"])

                # if there are different colordepths specified, convert to them
                if "colordepth" in inputfile:
                    for color in inputfile["colordepth"]:
                        if color == 32:
                            images.append(Image.open(tempfile))
                            sizes.append(tempsize)
                        else:
                            print(color)
                            #im = Image.new(mode="P", size=tempsize)
                            #images.append(im)
                            #sizes.append(tempsize)
                else:
                    images.append(Image.open(tempfile))
                    sizes.append(tempsize)

            # get the target filename and save the images into an .ico file        
            output_file = os.path.join(output_path, icon["file_out"])
            print("save icon:", output_file)
            im = Image.new(mode="RGBA", size=(48,48))
            im.save(output_file, format="ICO", sizes = sizes, append_images = images, bitmap_format="bmp")

        continue
    else:
        continue
