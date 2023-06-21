# 导入必要的库
import cv2
import time
import os
from flask import Flask, render_template, Response, request
from faster_whisper import WhisperModel
import pyaudio
import wave

# 创建Flask应用程序
app = Flask(__name__)

# 创建全局的cv2.VideoCapture对象
camera_1 = cv2.VideoCapture(0)
# camera_2 = cv2.VideoCapture(0)
# camera_3 = cv2.VideoCapture(0)
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
    fps = 20
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
    return Response(video_stream(camera_1), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_stream2')
def stream2():
    return Response(video_stream(camera_1), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/video_stream3')
def stream3():
    return Response(video_stream(camera_1), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/start_recording', methods=['POST'])
def start_recording():
    global recording, start_time
    frames_1 = []
    frames_2 = []
    frames_3 = []
    start_time = time.time()
    recording = True

    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    RECORD_SECONDS = 10
    #         WAVE_OUTPUT_FILENAME = "output2.wav"
    MP3_OUTPUT_FILENAME = "output.mp3"

    # 创建PyAudio对象
    audio = pyaudio.PyAudio()

    # 打开音频流
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("开始录音...")
    audio_frames = []
    while True:
        data = stream.read(CHUNK)
        audio_frames.append(data)
        success_1, frame_1 = camera_1.read()
        # success_2, frame_2 = camera_2.read()
        # success_3, frame_3 = camera_3.read()
        if not success_1:
            break
        frames_1.append(frame_1)
        # frames_2.append(frame_2)
        # frames_3.append(frame_3)
        if time.time() - start_time > 10000:
            break

    filename_1 = f'recordings/camera1/record_{int(time.time())}.avi'
    os.makedirs(os.path.dirname(filename_1), exist_ok=True)
    save_video(frames_1, filename_1)
    # filename_2 = f'recordings/camera2/record_{int(time.time())}.avi'
    # os.makedirs(os.path.dirname(filename_2), exist_ok=True)
    # save_video(frames_2, filename_2)
    # filename_3 = f'recordings/camera3/record_{int(time.time())}.avi'
    # os.makedirs(os.path.dirname(filename_3), exist_ok=True)
    # save_video(frames_3, filename_3)

    stream.stop_stream()
    stream.close()
    audio.terminate()
    WAVE_OUTPUT_FILENAME = f'recordings/audio/record_{int(time.time())}.wav'
    os.makedirs(os.path.dirname(WAVE_OUTPUT_FILENAME), exist_ok=True)
    # 保存音频数据为WAV文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(audio_frames))
    wf.close()

    recording = False
    start_time = None
    return 'Recording started'


@app.route('/record', methods=['POST'])
def record_audio():
    # save_audio()
    return 'Recorded audio successfully!'


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
