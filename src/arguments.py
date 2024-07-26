import os
import sys
import argparse
import logging

logger = logging.getLogger('pptx2video.Arguments')

def parse():
    parser = argparse.ArgumentParser(
                prog='pptx2video.py',
                usage='pptx2video.py [-h] inputfile outputpath',
                description='pptx2video extracts the note description portion of a PowerPoint slide, synthesizes the voice and generates a video file',
                add_help=True,
                )
    parser.add_argument('input', help='target powerpoint file')
    parser.add_argument('output', help='video file output destination path')
    parser.add_argument('-t','--transition', help='slide transition time(sec)', default=2, type=int)
    parser.add_argument('-d', '--debug', action='store_true', default=False) 
    parser.add_argument('--width', default=1270, type=int)
    parser.add_argument('--height', default=720, type=int)
    parser.add_argument('--density', default=144, type=int)
    parser.add_argument('--tag', default='', type=str)
    parser.add_argument('--tempdir', default='')

    return parser.parse_args()

def check(args):
    setting = {}
    # debug
    setting['debug']=args.debug
    logger.debug(str(setting['debug']))
    if setting['debug']:
        logger.setLevel(logging.DEBUG)

    # input
    if not os.path.exists(args.input):
        logger.error(f'{args.input} is not exist!')
        return False
    if os.path.isdir(args.input):
        logger.error(f'{args.input}. specified path must be a file')
        return False
    setting['input'] = args.input
    logger.debug(setting['input'])

    # output
    output_path = args.output
    if len(output_path) <= 0:
        logger.error(f'output cannot be empty.')
        return False        
    if os.path.isdir(args.output):
        basename_without_ext = os.path.splitext(os.path.basename(args.input))[0]
        output_path = os.path.join(args.output, basename_without_ext + '.mp4')
        logger.debug(f'{args.output} is directory , so use the input file name -> {output_path}')
    setting['output'] = output_path
    logger.debug(setting['output'])

    # transition time
    if not (args.transition >= 0):
        logger.error(f'slide transition time cannot be minus value')
        return False        
    setting['transition']=args.transition
    logger.debug(str(setting['transition']))

    # width
    if not (args.width >= 0):
        logger.error(f'width cannot be minus value')
        return False
    setting['width']=args.width
    logger.debug(str(setting['width']))

    # height
    if not (args.height >= 0):
        logger.error(f'height cannot be minus value')
        return False
    setting['height']=args.height
    logger.debug(str(setting['height']))

    # density
    if not (args.density >= 0):
        logger.error(f'density cannot be minus value')
        return False
    setting['density']=args.density
    logger.debug(str(setting['density']))
    
    # tag
    setting['tag']=args.tag
    logger.debug(str(setting['tag']))

    if len(args.tempdir) >= 0:
        setting['tempdir']=args.tempdir
        logger.debug(str(setting['tempdir']))
    return setting