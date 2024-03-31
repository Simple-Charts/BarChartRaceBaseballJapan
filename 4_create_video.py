import cv2
from tqdm import tqdm
import subprocess

movie_list=[]
for i in range(1950, 2024):
    movie_list.append(str(i) + '.mp4')

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')

movie = cv2.VideoCapture(movie_list[0])
fps = movie.get(cv2.CAP_PROP_FPS)
height = movie.get(cv2.CAP_PROP_FRAME_HEIGHT)
width = movie.get(cv2.CAP_PROP_FRAME_WIDTH)

output = cv2.VideoWriter('result_temp.mp4', int(fourcc), fps, (int(width), int(height)))

frame = None

for i in tqdm(movie_list):
    movie = cv2.VideoCapture(i)

    if movie.isOpened():
        ret, frame = movie.read()
    else:
        ret = False

    while ret:
        output.write(frame)
        ret, frame = movie.read()

output.release()

subprocess.call('ffmpeg -i ' + 'result_temp.mp4' + ' -crf 18 ' + 'result.mp4', shell=True)
