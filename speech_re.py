from faster_whisper import WhisperModel
import pyaudio
import wave
import subprocess


def save_audio(WAVE_OUTPUT_FILENAME="output2.wav"):
    # 配置音频输入参数
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

    # 存储音频数据
    frames = []

    # 录制音频数据
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        #             if (i * CHUNK) % RATE == 0:
        #                 print("seconds {}.........".format(i))
        data = stream.read(CHUNK)
        frames.append(data)

    print("录音结束！")

    # 停止音频流
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 保存音频数据为WAV文件
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print("WAV文件已保存！")


def speech_re(audio_file="output2.wav"):
    model_size = "small"

    # Run on GPU with FP16
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    # model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(audio_file, beam_size=5)

    print("Detected language '%s' with probability %f" % (info.language, info.language_probability))

    for segment in segments:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))


save_audio(WAVE_OUTPUT_FILENAME="output3.wav")
speech_re(audio_file="output3.wav")
