from PIL import Image, ImageColor
import math
from tkinter import filedialog
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
def dimension(textlength):
    a = math.sqrt(textlength)
    b = round(a)
    c = textlength/b
    d = math.ceil(c)
    return d, b

def cleantext(message):
    cleanedtext = []
    changechar = [["—", "--"], ["…", "..."], ["", ""], ["™", " TM"], ["", ""], ["’", "'"], ["", ""], ["“", '"'], ["”", '"'], ["­", ""], ["é", "e"], ["γ", "y"], ["ï", "i"], ["è", "e"], ["–", "--"]]
    for m in message:
        for word in changechar:
            if m == word[0]:
                m = word[1]
        cleanedtext.append(m)
    return cleanedtext

def branch(askforthis):
    if askforthis == "y":
        file = filedialog.askopenfilename(title="Open File To Encode/Decode", filetypes=(("Text/Image File", "*.txt *.png"),))
        filen = os.path.basename(file)
        suffix = filen.split(".")[1]
        if suffix == "png":
            decode(file,filen)
        if suffix == "txt":
            encode(file,filen)

def encode(filepath, file_name):
    file2 = file_name.split(".")[0]
    messagefile = open(filepath, 'r', encoding='utf-8')
    message = messagefile.read()

    n = 3
    newmessage = "".join(cleantext(message))
    textsegments = [newmessage[i:i+n] for i in range(0, len(newmessage), n)]
    dimx, dimy = dimension(len(textsegments))
    img = Image.new("RGB", (dimx, dimy))
    imgpixel = img.load()
    coords = [0,0]
    for i in textsegments:
        # print(i) Use this if you get an encoding error
        hexnumber = i.encode('utf-8').hex()
        if len(hexnumber) == 4:
            hexnumber += "00"
        if len(hexnumber) == 2:
            hexnumber += "0000"
        hashtaghex = '#' + hexnumber
        rgb = ImageColor.getrgb(hashtaghex)
        if coords[0] <= dimy:
            if coords[1] <= dimx:
                imgpixel[coords[0], coords[1]] = rgb
                coords[0] += 1
            if coords[0] == dimx:
                coords[0] = 0
                coords[1] += 1
    img.save(file2 + ".png")
    print(bcolors.OKGREEN + file_name + bcolors.ENDC, "has been successfully encoded.")
    tryagain = input("Would you like to encode/decode another file? (Y/N)\n")
    if tryagain.lower() == "y":
        branch("y")

def decode(decodefilep, file_name):
    file2 = file_name.split(".")[0]
    img = Image.open(decodefilep)
    imgpixel = img.load()
    dimx, dimy = img.size
    message = []
    coords = [0,0]

    for i in range(dimx * dimy):
        if coords[0] <= dimy:
            if coords[1] <= dimx:
                r, g, b = imgpixel[coords[0], coords[1]]
                if not (r,g,b) == (0,0,0):
                    if r == 0:
                        r = 32
                    if g == 0:
                        g = 32
                    if b == 0:
                        b = 32

                    hex = ('{:02x}' * 3).format(r, g, b)
                    hexstring = bytes.fromhex(hex).decode('utf-8')
                    message.append(hexstring)
                    coords[0] += 1
            if coords[0] == dimx:
                coords[0] = 0
                coords[1] += 1
    realtext = "".join(message)
    with open(file2 + ".txt", 'w', encoding="utf-8") as f:
        f.write(realtext)
    print(bcolors.OKGREEN + file_name + bcolors.ENDC, "has been successfully decoded.")
    tryagain = input("Would you like to encode/decode another file? (Y/N)\n")
    if tryagain.lower() == "y":
        branch("y")

askfor = input(bcolors.WARNING + "PLEASE READ BEFORE PROCEEDING" + bcolors.ENDC + "\nThis program was created with the purpose of encoding/decoding data.\nIf you select a png file, this program will automatically decode the file into text.\nIf you select a txt file, it will automatically encode the file into an image.\nFiles you want to encode/decode should be kept in a separate in order to avoid files being overwritten during the encoding/decoding process.\nType 'y' to proceed.\n")
branch(askfor.lower())