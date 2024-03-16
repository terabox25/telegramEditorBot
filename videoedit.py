from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.editor import *
import os

def cropvideo(video, startingtime, endingtime, id):
    croppedvideo = video.subclip(startingtime, endingtime)
    croppedvideo.write_videofile(f'OutputFiles/{id}.mp4')
    croppedvideo.close()

def speedupvideo(video, speed, id):
    spedupvideo = video.fx(vfx.speedx, speed)
    spedupvideo.write_videofile(f'OutputFiles/{id}.mp4')
    spedupvideo.close()

def mergevideos(id):
    files = os.listdir('InputFiles/')
    outputlist = [VideoFileClip('InputFiles/' + file_) for file_ in files if file_.startswith(str(id))]
    finalvideo = concatenate_videoclips(outputlist, method='compose')
    finalvideo.write_videofile(f'OutputFiles/{id}.mp4')
    finalvideo.close()