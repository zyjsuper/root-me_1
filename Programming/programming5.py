import base64
import urllib.request
from bs4 import BeautifulSoup
from PIL import Image
import subprocess

#know'n stuff
url = "http://challenge01.root-me.org/programmation/ch8/"

def b64toimg(imgstring):
    '''converts a bytestring into a image'''
    print("Convert bytestring to image!")
    imgdata = base64.b64decode(imgstring)
    filename = "temp1.png"
    with open(filename, "wb") as f:
        f.write(imgdata)

def tesseract():
    try:
        print("Running Tesseract...");
        #Run Tesseract, -psm 8, tells Tesseract we are looking for a single word 
        subprocess.call(['C:\\Program Files (x86)\\Tesseract-OCR\\tesseract.exe', 'C:\\Users\\p1ng\\Documents\\Code\\root-me\\programming1\\programming1\\programming1\\temp2.png', 'output', '-psm', '8'])
        f = open ("C:\\Users\\p1ng\\Documents\\Code\\root-me\\programming1\\programming1\\programming1\\output.txt","r")
        global cvalue
  #Remove whitespace and newlines from Tesseract output
        cvaluelines = f.read().replace(" ", "").split('\n')
        cvalue = cvaluelines[0]
        print("--- Captcha: " + cvalue); 
    except Exception as e:
        print ("Error: " + str(e))

def resize():
    print("Resizing")
    img1 = Image.open("temp1.png")
    width, height = img1.size
    img2 = img1.resize((int(width*5), int(height*5)), Image.BICUBIC)
    img2.save("temp2.png")

def getCaptchaByteString():
    print("Get captcha bytestring")
    #get from the webpage
    with urllib.request.urlopen(url) as response:
        html = response.read()
        page = BeautifulSoup(html, 'html.parser')
        src_dict = page.findAll("img")[0].attrs

        imgstring = src_dict["src"].split(",")[1]
        bytestring = bytes(imgstring, encoding="UTF-8")
        return bytestring


print("--- Start:")
# get the Bytestring from the Captcha
captcha_bytestring = getCaptchaByteString()
# recreate the img from bytestring
b64toimg(captcha_bytestring)
# resize image for tesseract
resize()
# run tesseract to get string
#tesseract()


