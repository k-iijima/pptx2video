# pptx2video 
[![Docker Image CI](https://github.com/k-iijima/pptx2video/actions/workflows/docker-image.yml/badge.svg?branch=main)](https://github.com/k-iijima/pptx2video/actions/workflows/docker-image.yml)

pptx2video extracts the note description portion of a PowerPoint slide, synthesizes the voice and generates a video file.
only Japanese note descriptions are supported so far.


# Usage

## format

docker run -it --rm -v "$(pwd):/root/work/" iijimas60/pptx2video:0.0.4 python3 pptx2video.py _path(input pptx)_ _path(mp4 output)_ _time(transition)_

## example

Example of converting sample.pptx to video with sound with a transition latency of 2 seconds between slides.

```
docker run -it --rm -v "$(pwd):/root/work/" iijimas60/pptx2video:0.0.4 python3 pptx2video.py /root/work/sample.pptx /root/work/sample.mp4 2
```

# modules

## Extract slides and note descriptions

python-pptx
* https://python-pptx.readthedocs.io/en/latest/
* https://github.com/scanny/python-pptx

## Convert PPTX to PDF
unoserver
* https://github.com/unoconv/unoserver

libreoffice
* https://ja.libreoffice.org/
* https://packages.ubuntu.com/search?keywords=libreoffice

## Convert Slide to Image
ImageMagick
* https://imagemagick.org/index.php

## TTS
ESPNET
* https://github.com/espnet/espnet

model
tts_finetune_jvs010_jsut_vits_raw_phn_jaconv_pyopenjtalk_prosody_latest
* https://zenodo.org/record/5521494#.ZGVxG3bP1PY

## Video generation from image data
OpebCV
* https://opencv.org/
* https://pypi.org/project/opencv-python/

## Voice data processing
moviepy
* https://github.com/Zulko/moviepy
* https://zulko.github.io/moviepy/

soundfile
* https://pypi.org/project/soundfile/
* https://pysoundfile.readthedocs.io/en/latest/

pydub
* https://github.com/jiaaro/pydub
* https://pypi.org/project/pydub/

## h264 encoding of video
ffmpeg
* https://ffmpeg.org/

ffmpeg-python
* https://github.com/kkroening/ffmpeg-python

## See other detailed ones here.
Dockerfile
requirements.txt