
from flask import Flask, render_template, request, url_for
import pytesseract
import cv2
from PIL import Image

app = Flask(__name__)
@app.route('/')
def home():
    return render_template('index.html')
@app.route('/homepage/')
def homepage():
    return render_template('index.html')

@app.route('/about/')
def about():
    return render_template('about.html')

@app.route('/upload/', methods=['GET', 'POST'])
def upload():
    try:
        imagefile = request.files.get('imagefile', '') 
        img = Image.open(imagefile)
        text = pytesseract.image_to_string(img)
        return render_template('result.html', var=text)
    except:
            return render_template('error.html')
  
        
if __name__ == "__main__": 
        app.run()


    
    
