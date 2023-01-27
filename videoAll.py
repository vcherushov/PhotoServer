import cv2
import threading
from datetime import datetime, timedelta
import os

class camThread(threading.Thread):
    def __init__(self, previewName, camID):
        threading.Thread.__init__(self)
        self.previewName = previewName
        self.camID = camID
    def run(self):
        print("Starting " + self.previewName)
        camPreview(self.previewName, self.camID)

def createFolder():
    current_date = datetime.now()
    current_y = current_date.strftime('%y')
    current_m = current_date.strftime('%m')
    current_d = current_date.strftime('%d')
    if not os.path.isdir(f'media/video/{current_y}'):
        os.mkdir(f'media/video/{current_y}')

    if not os.path.isdir(f'media/video/{current_y}/{current_m}'):
        os.mkdir(f'media/video/{current_y}/{current_m}')

    if not os.path.isdir(f'media/video/{current_y}/{current_m}/{current_d}'):
        os.mkdir(f'media/video/{current_y}/{current_m}/{current_d}')

def camPreview(previewName, camID):

    current_date = datetime.now()
    current_date_string = current_date.strftime('%m_%d_%y_%H_%M_%S')
    current_y = current_date.strftime('%y')
    current_m = current_date.strftime('%m')
    current_d = current_date.strftime('%d')
    old_date = current_date + timedelta(minutes=20)

    video_name = f'bus_1_{previewName}_{current_date_string}.mp4'

    cap = cv2.VideoCapture(camID)

    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    frame_size = (frame_width, frame_height)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    folder = f'media/video/{current_y}/{current_m}/{current_d}/{video_name}'
    out = cv2.VideoWriter(folder, fourcc, 20, frame_size)

    while True:
        ret, frame = cap.read()

        if not cap.isOpened():
            print('No')

        else:
            if datetime.now() <= old_date:
                out.write(frame)
            else:
                current_date = datetime.now()
                current_date_string = current_date.strftime('%m_%d_%y_%H_%M_%S')
                old_date = current_date + timedelta(minutes=20)
                video_name = f'bus1_{previewName}_{current_date_string}.mp4'
                folder = f'media/video/{current_y}/{current_m}/{current_d}/{video_name}'
                out = cv2.VideoWriter(folder, fourcc, 20, frame_size)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyWindow(previewName)

# Create two threads as follows
createFolder()
thread1 = camThread("door_1", 'rtsp://admin:@192.168.229.240:554/channel=1_stream=1.sdp')
thread2 = camThread("door_2", 'rtsp://admin:@192.168.229.242:554/channel=1_stream=1.sdp')
thread3 = camThread("door_3", 'rtsp://admin:@192.168.229.243:554/channel=1_stream=1.sdp')
thread1.start()
thread2.start()
thread3.start()
