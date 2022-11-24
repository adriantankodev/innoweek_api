from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from evaluate_result import evaluate
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = "uploads/"
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/upload')
def upload():
   return render_template('upload.html')
	
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(app.config['UPLOAD_FOLDER'] + secure_filename(f.filename))
      results = evaluate(app.config['UPLOAD_FOLDER'] + secure_filename(f.filename))
      return render_template('result.html', path='/runs/detect/exp/enzo.jpg')

		
if __name__ == '__main__':
   app.run(debug = True)