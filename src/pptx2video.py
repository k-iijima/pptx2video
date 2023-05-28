#!/usr/bin/python3
# coding: utf-8

import sys
import logging

import arguments as arg
import pptx2jpg as p2j
import pptx2audio as p2a

# power point
#from pptx import Presentation
import glob
import re
import os
import tempfile

# Video 
import cv2
import numpy as np
import ffmpeg
import torch

# audio
#import soundfile
#from espnet_model_zoo.downloader import ModelDownloader
#from espnet2.bin.tts_inference import Text2Speech
#from espnet2.utils.types import str_or_none
from pydub import AudioSegment
import math
from pydub import AudioSegment
from moviepy.editor import *

setting = {}
logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('pptx2video')

device = "cpu"
if torch.cuda.is_available():
    device ="cuda"
    logger.info(torch.cuda.get_device_name())

def searchfiles(targetdir,ext):
    def atoi(text):
        return int(text) if text.isdigit() else text

    def natural_keys(text):
        return [ atoi(c) for c in re.split(r'(\d+)', text) ]

    files = sorted(glob.glob(targetdir + "/*" + ext), key=natural_keys)
    for file in files:
        logger.info(file)

    return files

def jpg2video(setting,imagedir):

    tagetfile = setting.get('input')
    slide_time = setting.get('transition')
    outputpath = setting.get('output')
    density = setting.get('density')

    output_audio_files,notes = p2a.pptx_note2_audio(tagetfile,imagedir,device)
    p2j.pptx2jpg(tagetfile,density,imagedir)
    files = searchfiles(imagedir,".jpg")
    if len(files) <=0:
        logger.error("page image not found.")
        return False

    outputvideopath = os.path.join(imagedir , '/output.mp4')
    outputvideotmppath = os.path.join(imagedir ,'/output_tmp.mp4')

    fourcc = cv2.VideoWriter_fourcc('m','p','4', 'v')
    w = setting.get('width')
    h = setting.get('height')
    fps = 20
    video  = cv2.VideoWriter(outputvideotmppath, fourcc,fps, (w, h))

    audio_index =0
    final_sound = None
    for img_file in files:
        logger.info("read:" + img_file)
        img = cv2.imread(img_file)
        img1 = cv2.resize( img, (w, h) ) 
        if img1 is None:
            logger.error("can't read")
            break    

        frame_num = fps*slide_time
        # Adjust the number of frames to match the audio content
        audio_path = output_audio_files[audio_index]
        if audio_path and os.path.exists(audio_path):
            sound1 = AudioSegment.from_file(audio_path)
            logger.info(str(sound1.duration_seconds))
            padding = slide_time - sound1.duration_seconds
            if padding > 0.0:
                sound1 += AudioSegment.silent(duration=padding*1000)
            else:
                frame_num += int(fps*abs(padding))
            if final_sound == None:
                final_sound = sound1
            else:
                final_sound += sound1
        else:
            if final_sound== None:
                final_sound = AudioSegment.silent(duration=slide_time*1000)
            else:
                final_sound += AudioSegment.silent(duration=slide_time*1000)

        #final_sound += AudioSegment.silent(duration=1000)
        #frame_num += fps
        logger.info("frame count:" + str(frame_num) )
        for i in range(frame_num):
            video.write(img1)
        audio_index+=1
    video.release()
    convertfile = imagedir + "/audio_conv.wav"
    final_sound.export(convertfile, format='wav')

    logger.info(outputvideotmppath)
    # H.264 
    ffmpeg.input(outputvideotmppath).output(outputvideopath, vcodec='libx264').run(overwrite_output=True)
    os.remove(outputvideotmppath)

    video_clip = VideoFileClip(outputvideopath)
    concat_clip = AudioFileClip(convertfile)
    final_clip = video_clip.set_audio(concat_clip)
    final_clip.write_videofile(outputpath)


if __name__ == "__main__":

    setting = arg.check(arg.parse())
    if not setting:
        sys.exit(1)
    if setting.get('debug'):
        logger.setLevel(logging.DEBUG)
    if len(setting.get('tempdir')) > 0:
        if not jpg2video(setting,setting.get('tempdir')):
            sys.exit(1)
    else:
        with tempfile.TemporaryDirectory() as dname:
            if not jpg2video(setting,dname):
                sys.exit(1)
    sys.exit(0)

