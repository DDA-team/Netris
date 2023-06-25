import cv2


def get_first_frame(video_destention, frame_name):
    cap = cv2.VideoCapture(video_destention)
    ret, frame = cap.read()
    cv2.imwrite(frame_name, frame)
    cap.release()
    return frame_name


def get_duration(video_destention):
    cap = cv2.VideoCapture(video_destention)
    frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    duration = frames / float(fps)
    cap.release()
    return duration


if __name__ == "__main__":
    get_first_frame("temp/test.mp4", "temp/test_frame.jpg")
