"""
Course: CSE 251
Lesson: L03 Prove
File:   create_final_video.py
Author: Brother Comeau / Brother Keers

A simple script that uses ffmpeg to automatically create a video (mp4) of
processed images if they exist.
"""

import os
import platform

def main():
    """ Attempt to create a video from previously processed images. """

    # The folder `processed`` must exist.
    if not os.path.exists('processed'):
        print('\nERROR: the folder "processed" doesn\'t exist\n')
        return 

    # Builds the OS specific ffmpeg command to process the images.
    if platform.system() == 'Windows':
        command = rf'.\library\ffmpeg.exe -y -i processed/image%3d.png final.mp4'
    elif platform.system() == 'Darwin':
        command = r'./library/ffmpeg -y -i processed/image%3d.png final.mp4'
    else:
        command = r'ffmpeg -y -i processed/image%3d.png final.mp4'
    os.system(command)

    print('\nThe video file final.mp4 has been created\n')
    print('DO NOT submit this video for your assignment!')

if __name__ == '__main__':
    main()
