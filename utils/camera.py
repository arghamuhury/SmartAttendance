import cv2

class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. 
        self.video = cv2.VideoCapture(0)

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if not success:
            return None
        
        # We can add drawing or processing here if needed, 
        # but for raw feed we just encode it.
        ret, jpeg = cv2.imencode('.jpg', image)
        return jpeg.tobytes()

    def get_raw_frame(self):
        success, image = self.video.read()
        if not success:
            return None
        return image
