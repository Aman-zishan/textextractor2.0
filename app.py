
from flask import Flask, render_template, request, url_for, Response
import pytesseract
import cv2
from PIL import Image
import os
from math import floor

#pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe' 

REDUCTION_COEFF = 0.9
QUALITY = 85

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    try:
        imagefile = request.files.get('imagefile', '')
        imagefile.save(os.path.join('./static/images/',imagefile.filename))
        img = Image.open(imagefile)
        img1 = img.convert('LA')
        print("Before reducing",img1.size)
        imgsize=os.path.getsize(os.path.join('./static/images/',imagefile.filename))>>20
        if imgsize>2:
            x, y = img1.size
            x *= REDUCTION_COEFF
            y *= REDUCTION_COEFF
            img1 = img1.resize((floor(x),floor(y)), Image.BICUBIC)
            print("Img reduced",img1.size)
        text = pytesseract.image_to_string(img1)
        f = open("sample.txt", "a")
        f.truncate(0)
        f.write(text)
        f.close()
        filename=img.filename
        return render_template('result.html', var=text,filename=imagefile.filename)
    except Exception as e:
        print(e) 
        return render_template('error.html')
    
@app.route("/gettext")
def gettext():
        with open("sample.txt") as fp:
            src = fp.read()
        return Response(
            src,
            mimetype="text/csv",
            headers={"Content-disposition":
                     "attachment; filename=sample.txt"})
    
 
        
if __name__ == "__main__": 
        app.run()


    
    
