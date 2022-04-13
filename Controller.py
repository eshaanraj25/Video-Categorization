# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 18:06:54 2021

@author: Sai Ji
"""
from flask import *  
import os
from werkzeug.utils import secure_filename
import urllib.request
import shutil
import classify_nsfw_video
import service

app = Flask(__name__)  
app.secret_key = "secret key"
SRC = ''
DATA = ''
CATEGORY = ''
ALLOWED_EXTENSIONS = set(['mp4', '3gp', 'mpeg'])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
	return render_template('upload.html')

@app.route('/final')
def final_page():
    print("DATA:: ",DATA)
    print("CATEGORY:: ",CATEGORY)
    return render_template('success.html', data=service.getdata(), category=service.getCategory())

@app.route('/process')
def script_call():
	return redirect(service.main("D:/Degree/7thSem/Minorproject/VideoCategorisation/videos/",app.config['SRC']))

@app.route('/download')
def file_download():
	path="D:/Degree/7thSem/Minorproject/VideoCategorisation/"+app.config['SRC']
	return send_file(path, as_attachment=True)

@app.route('/success', methods=['POST'])
def upload_file():
	if request.method == 'POST':
        # check if the post request has the file part
		if 'file' not in request.files:
			flash('No file part')
			return redirect(request.url)
		file = request.files['file']
		if file.filename == '':
			flash('No file selected for uploading')
			return redirect(request.url)
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(filename)
			shutil.copy(filename, 'D:/Degree/7thSem/Minorproject/VideoCategorisation/videos')
			app.config['SRC']=filename
			os.remove(filename)
			flash('File successfully uploaded')
			return redirect('/process')
		else:
			flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
			return redirect(request.url)

if __name__ == "__main__":
    app.run()
   