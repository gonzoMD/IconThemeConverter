 # IconThemeConverter
A python script which helps to convert GNU/Linux icon themes to ReactOS/Windows compatible ones.
To use the script you have to create some definition files, which contain information of the source images and information about the icon properties like size, canvas, overlays and more. 

Here I will explain step by step how to prepare your computer to use this script and how to write a definition file.

## Preparation
### 3rd-party libraries
in order to use the script you have to install the following libraries:
- [Pillow:](https://pillow.readthedocs.io/en/stable/) an imaging library for python
- [CairoSVG:](https://cairosvg.org) an SVG converting library.
- the icon theme of your choice. in this example I'll use [Flat Remix](https://github.com/daniruiz/Flat-Remix)

### Setting up the script
Save the contents of this repo in a directory of your choice and open the file `settings.json` within the text editor of your choice. Youl find something like this:

    {
        "path_icontheme":"../flat-remix",
        "path_jsonfiles":"./icon_definitions"
    }
The first line contains the path to our source icon theme. Just use the path where you either checked out its repo or where you downloaded and extracted its files to.
The second line contains the path to our definition file directory. If no full path is specified, the directory where the script/settings file is inside, is the base path. In my case I just created a subdirectory called `icon_definitions` You can create multiple definition files and put them all inside this folder. More about this later. 
*AND YES: These are all slashes and NO backslashes!!! This is important!*

Now we installed all software and set up the script. Time to run the script. But wait..... beforehand we have to...
## Write the definition file
In this example I'll try to find alternative icons for shell32. I'll use the following pic as orientation:
![enter image description here](https://images-wixmp-ed30a86b8c4ca887773594c2.wixmp.com/f/b4321015-4362-4f77-84bd-72d7d618e212/d3dndrt-abacc20a-298f-440b-a0c8-6348ec8fa168.jpg?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ1cm46YXBwOjdlMGQxODg5ODIyNjQzNzNhNWYwZDQxNWVhMGQyNmUwIiwic3ViIjoidXJuOmFwcDo3ZTBkMTg4OTgyMjY0MzczYTVmMGQ0MTVlYTBkMjZlMCIsImF1ZCI6WyJ1cm46c2VydmljZTpmaWxlLmRvd25sb2FkIl0sIm9iaiI6W1t7InBhdGgiOiIvZi9iNDMyMTAxNS00MzYyLTRmNzctODRiZC03MmQ3ZDYxOGUyMTIvZDNkbmRydC1hYmFjYzIwYS0yOThmLTQ0MGItYTBjOC02MzQ4ZWM4ZmExNjguanBnIn1dXX0.v6l6iwiP12YbP95h13tFEt7vpe6syYfI30p6TMv-h7U)
We start to use equivalents for the first two icons. Create a json file in the directory, which you specified for the icon definitions before. The name doesn't matter, I called it `shell32.json`
Open it within your favourite text editor and add the following lines: 

    {
        "name": "shell32",
        "path_out_ico":"/icons",
        "icon": [
            {
                "file_out":"1.ico",
                "file_in":[
                    {"size": 16, "src": "Flat-Remix-Yellow/mimetypes/symbolic/text-x-generic-symbolic.svg"},
                    {"size": 32, "src": "Flat-Remix-Yellow/mimetypes/scalable/application.svg"},
                    {"size": 48, "src": "Flat-Remix-Yellow/mimetypes/scalable/application.svg"}
                ]
            },
            {
                "file_out":"2.ico",
                "file_in":[
                    {"size": 16, "src": "Flat-Remix-Yellow/mimetypes/symbolic/x-office-document-symbolic.svg"},
                    {"size": 32, "src": "Flat-Remix-Yellow/mimetypes/scalable/application-document.svg"},
                    {"size": 48, "src": "Flat-Remix-Yellow/mimetypes/scalable/application-document.svg"}
                ]
            }
        ]
    }
to be continued... At least, If you save this file and run the script, it should create 2 icons.