import cv2
import time
import shutil


_path = "./"

def _webcam(img, buffer_size = 20):

    #get device
    device = cv2.VideoCapture(0)
    _, frame = device.read()
    print(frame)
    cv2.imwrite(f"{_path}{img}.jpg", frame)

    #while True:
    for i in range(buffer_size):
        time.sleep(1)
        _, frame = device.read()
        shutil.move(f"{_path}{img}.jpg", f"{_path}{img}_{i}.jpg")
        cv2.imwrite(f"{_path}{img}.jpg", frame)


if __name__ == '__main__':
    _webcam('test')
