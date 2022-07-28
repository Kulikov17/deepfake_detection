import tempfile
from flask import Flask, jsonify, Response
from flask_cors import CORS, cross_origin
from flask import request
from pathlib import Path

from preprocessing_video import prediction_videoclass

app = Flask(__name__, static_folder='static', static_url_path='')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

@app.after_request
def after_request(response):
  response.headers.add('Accept-Ranges', 'bytes')
  return response

@app.route('/api/video/predict', methods=['POST'])
@cross_origin()
def video_predict():
  uploaded_file = request.files['file']

  with tempfile.TemporaryDirectory() as td:
    tmp_dir_name = td    
    path_dir = Path(td)
    temp_filename = str(path_dir) + uploaded_file.filename
    uploaded_file.save(temp_filename)
    prediction = prediction_videoclass(str(temp_filename))

  return jsonify({'videoClass': prediction})

if __name__ == '__main__':
    app.run(threaded=True)