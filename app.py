# 导入必要的库
import cv2
import time
import os
from flask import Flask, render_template, Response, request

# 创建Flask应用程序
app = Flask(__name__)

# 创建全局的cv2.VideoCapture对象
camera = cv2.VideoCapture(0)

# 初始化录像状态和已经录制的时间
recording = False
start_time = None


# 定义视频流读取函数
def video_stream(camera):
    while True:
        success, frame = camera.read()
        if not success:
            break
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# 定义录像保存函数
def save_video(frames, filename):
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    fps = 10
    out = cv2.VideoWriter(filename, fourcc, fps, (640, 480))
    for frame in frames:
        out.write(frame)
    out.release()


# 定义路由和视图函数
@app.route('/')
def index():
    return render_template('index.html', recording=recording, elapsed_time=get_elapsed_time())


@app.route('/video_stream1')
def stream1():
    return Response(video_stream(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_stream2')
def stream2():
    return Response(video_stream(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_stream3')
def stream3():
    return Response(video_stream(camera), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording, start_time
    frames = []
    start_time = time.time()
    recording = True
    while True:
        success, frame = camera.read()
        if not success:
            break
        frames.append(frame)
        if time.time() - start_time > 10: # 录制10秒钟
            break
    filename = f'recordings/record_{int(time.time())}.avi'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    save_video(frames, filename)
    recording = False
    start_time = None
    return 'Recording started'


# 定义函数来获取已经录制的时间
def get_elapsed_time():
    global start_time
    if start_time is None:
        return 0
    else:
        return int(time.time() - start_time)


# 运行Flask应用程序
if __name__ == '__main__':
    app.run(debug=True)
