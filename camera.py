import cv2
import time
import os

if __name__ == '__main__':
    camera_id = 0
    frame_count = 0
    cam = cv2.VideoCapture(camera_id)
    frames = []
    timestamp = time.time()
    str_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime(timestamp))
    filename = f'recordings/camera{int(camera_id)}/record_{str_time}.avi'
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    while True:
        success, frame = cam.read()
        frame_count += 1
        if time.time() - timestamp > 1:
            fps = frame_count
            frame_count = 0
            timestamp = time.time()
            print('fps:{}'.format(fps))
        frames.append(frame)
        cv2.imshow('recording...', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if not success:
            break

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    fps = 20
    out = cv2.VideoWriter(filename, fourcc, fps, (640, 480))
    for frame in frames:
        out.write(frame)
    out.release()
