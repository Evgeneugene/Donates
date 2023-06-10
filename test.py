import cv2
import pytesseract
import os
import re


def clear_folder():
    folder_path = 'imgs/'  # Specify the path to the folder you want to clear

    # Iterate over the files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)


video_path = 'video/video4.mp4'
video = cv2.VideoCapture(video_path)

# video.set(cv2.CAP_PROP_POS_MSEC, 413*1000)

image = video.read()[1]
height, width, channels = image.shape  # Get the shape of the image
ytop = int(height * 0.01)
ybot = int(height * 0.1)
xleft = int(width * 0)
xright = int(width * 0.3)

# cut = image[ytop:ybot, xleft:xright]
# cv2.imwrite('cut.png', cut)
#
#
# text1 = pytesseract.image_to_string(cut, lang='eng')
# print(text1)

interval = 5000  # sec

current_time = 0

donate_count = 0

clear_folder()
cash_sum = 0

while video.isOpened():
    video.set(cv2.CAP_PROP_POS_MSEC, current_time)

    ret, frame = video.read()


    if ret:
        hours = int(current_time / 1000 / 3600)
        minutes = int((current_time / 1000) / 60)
        seconds = int(current_time / 1000 % 60)

        if hours < 10:
            hours = '0' + str(hours)
        if minutes < 10:
            minutes = '0' + str(minutes)
        if seconds < 10:
            seconds = '0' + str(seconds)

        timestamp = f'{hours}:{minutes}:{seconds} = {cash_sum} ({donate_count})'
        position = (100, 100)  # Position of the text (top-left corner)
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 0.7
        gr = 0 if donate_count & 1 else 255
        bl = 255 if donate_count & 1 else 255

        color = (0, gr, bl)  # BGR color (red in this example)
        thickness = 2

        current_time += interval

        cut = frame[ytop:ybot, xleft:xright]
        text = pytesseract.image_to_string(cut)

        if text:
            split_list = text.split('-')
            stripped_list = [element.strip() for element in split_list]

            pattern = r'(\d+)[^\d\s]{0,2}$'
            matches = re.findall(pattern, text)

            cash = 0
            if matches and int(matches[0]) > 100:
                current_time += 16000
                cash = int(matches[0])
                cash_sum += cash
                donate_count += 1
                print(f'{hours}:{minutes}:{seconds} [{current_time}] == {cash} / {cash_sum}')
                cv2.imwrite(f'imgs/{hours}:{minutes}:{seconds}-{cash}.png', cut)

        cv2.putText(frame, timestamp, position, font, font_scale, color, thickness)
        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    else:
        break

file_path = 'result.txt'

with open(file_path, 'a') as f:
    f.write(f'{video_path} : {cash_sum}p.' + '\n')

video.release()
cv2.destroyAllWindows()
