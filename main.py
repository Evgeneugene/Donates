import cv2

video_path = 'video/video2.mp4'
video = cv2.VideoCapture(video_path)

video.set(cv2.CAP_PROP_POS_MSEC, current_time)

height, width, channels = image.shape  # Get the shape of the image
ytop = int(height * 0.01)
ybot = int(height * 0.03)
xleft = int(width * 0)
xright = int(width * 0.15)

ret, frame = video.read()

