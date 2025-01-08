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

if os.path.exists("./temp") == False:
    os.mkdir("./temp")

icon_definition_dir = os.fsencode(settings["path_jsonfiles"])

# process all icon definition files
for file in os.listdir(icon_definition_dir):
    if os.fsdecode(file).endswith(".json"):
        filename = os.path.join(icon_definition_dir, file)
        with open(filename, 'r') as f:
            curfile = json.load(f)
        output_path = os.path.join("./output", curfile["path_out_ico"])
        print(f"process definition file {filename}")
        print(f"save icons to {output_path}")
        if os.path.exists(output_path) == False:
            os.makedirs(output_path)

        # process all icons in the current file
        for icon in curfile["icon"]:
            output_file = os.path.join(output_path, icon["file_out"])
            print(output_file)
            images=[]
            sizes=[]
            # read all inputfiles for this icon
            for inputfile in icon["file_in"]:
                imagefile = os.path.join(settings["path_icontheme"], inputfile["src"])
                tempfile = str(inputfile["size"]) + ".png"
                tempfile = os.path.join("./temp", tempfile)
                cairosvg.svg2png(url=imagefile, output_width = inputfile["size"], output_height = inputfile["size"], write_to=tempfile)
                tempsize=(inputfile["size"],inputfile["size"])

                # if we have a defined image as overlay, paste it, related to its gravity and size
                if "overlay" in inputfile:
                    ovlsrc = os.path.join(settings["path_icontheme"], inputfile["overlay"]["src"])
                    cairosvg.svg2png(url=ovlsrc, parent_width = inputfile["overlay"]["size"], parent_height = inputfile["overlay"]["size"], write_to="./temp/overlay.png")
                    icn = Image.open(tempfile)
                    icn.paste(Image.open("./temp/overlay.png"),getposition(inputfile["size"],inputfile["overlay"]["size"], inputfile["overlay"]["gravity"]),Image.open("./temp/overlay.png"))
                    icn.save(tempfile)

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

            im = Image.new(mode="RGBA", size=(48,48))
            im.save(output_file, format="ICO", sizes = sizes, append_images = images, bitmap_format="bmp")

        continue
    else:
        continue
