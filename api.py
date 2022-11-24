from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import torch
app = Flask(__name__, static_folder='interference', static_url_path='')

app.config['UPLOAD_FOLDER'] = "uploads/"
app.config['ALLOWED_EXTENSIONS'] = set(['png', 'jpg', 'jpeg', 'gif'])
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/')
def upload():
   return render_template('upload.html')
	
@app.route('/result', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      f.save(app.config['UPLOAD_FOLDER'] + secure_filename(f.filename))
      json_result = evaluate(app.config['UPLOAD_FOLDER'] + secure_filename(f.filename))
      path = secure_filename(f.filename).split('.')[0] + '.jpg'
      return render_template('result.html', path = path, result = json_result)

def evaluate(path):
    model = torch.hub.load('../yolov5', 'custom', path='../yolov5/runs/train/exp/weights/best.pt', source='local')
    results = model(path)
    results.save(save_dir='interference/', exist_ok=True)
    return results.pandas().xyxy[0].to_json(orient="records")
		
if __name__ == '__main__':
   app.run(debug = True)