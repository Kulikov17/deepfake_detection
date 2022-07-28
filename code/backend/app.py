from flask import Flask, jsonify, Response
import random
import os
from flask_cors import CORS, cross_origin
from flask import request
import re
import face_recognition
import cv2

app = Flask(__name__, static_folder='static', static_url_path='')
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


def get_chunk(byte1=None, byte2=None, videoPath=''):
    file_size = os.stat(videoPath).st_size
    start = 0
    
    if byte1 < file_size:
        start = byte1
    if byte2:
        length = byte2 + 1 - byte1
    else:
        length = file_size - start

    with open(videoPath, 'rb') as f:
        f.seek(start)
        chunk = f.read(length)
    return chunk, start, length, file_size


def face_extract(videoPath):
    video_fd = cv2.VideoCapture(videoPath)
    if not video_fd.isOpened():
        print('Skpped: {}'.format(videoPath))
        return

    frame_width = int(video_fd.get(3))
    frame_height = int(video_fd.get(4))
    frame_size = (frame_width,frame_height)
    video_fps = int(video_fd.get(5))
    
    outputPath = './static/videoPredict.avi'
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_output = cv2.VideoWriter(outputPath, fourcc, video_fps, frame_size)

    frame_index = 0
    success, frame = video_fd.read()
    video_process_frame = []
    while success:
        vframe = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(vframe)
        locations = []
        for face_location in face_locations:
            top, right, bottom, left = face_location
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            locations.append([top, right, bottom, left])

        video_process_frame.append([frame, locations])
        frame_index += 1
        success, frame = video_fd.read()
        print("frame: ", frame_index)
    
    font = cv2.FONT_HERSHEY_DUPLEX

    for frame in video_process_frame:
      for location in frame[2]:
        cv2.putText(frame, 'fake', (location[3] + 6, location[2] - 6), font, 1.0, (255, 255, 255), 1)
      
      output.write(frame)

    video_fd.release()
    out.release()

    return 'fake'


@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response


@app.route('/api/video/predict', methods=['GET'])
@cross_origin()
def get_video_class():
    print('ok')
    prob = face_extract('./static/video.mp4')
    print('ok')
    return jsonify({'videoClass': prob})


@app.route('/api/video/upload', methods=['POST'])
@cross_origin()
def upload_file():
    if os.path.exists('./static/video.mp4'):
        os.remove('./static/video.mp4')
    
    if os.path.exists('./static/videoPredict.avi'):
        os.remove('./static/videoPredict.avi')

    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        uploaded_file.save('./static/video.mp4')
    return jsonify({'info': 'video was uploaded'})


@app.route('/api/video', methods=['DELETE'])
@cross_origin()
def clear_files():
    if os.path.exists('./static/video.mp4'):
        os.remove('./static/video.mp4')

    if os.path.exists('./static/videoPredict.avi'):
        os.remove('./static/videoPredict.avi')

    return jsonify({'info': 'videos was deleted'})


@app.route('/video/play/')
def play_video():
    range_header = request.headers.get('Range', None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])
       
    videoPath = './static/video.mp4'
       
    chunk, start, length, file_size = get_chunk(byte1, byte2, videoPath)
    resp = Response(chunk, 206, mimetype='video/mp4',
                      content_type='video/mp4', direct_passthrough=True)
    resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    return resp


@app.route('/video/play/predict/')
def play_predict():
    range_header = request.headers.get('Range', None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])
       
    videoPath = './static/videoPredict.avi'

    chunk, start, length, file_size = get_chunk(byte1, byte2, videoPath)
    resp = Response(chunk, 206, mimetype='video/avi',
                      content_type='video/avi', direct_passthrough=True)
    resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    return resp


if __name__ == '__main__':
    app.run(threaded=True)