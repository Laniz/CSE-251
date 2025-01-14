"""
Course: CSE 251
Lesson: L03 Prove
File:   setup.py
Author: Brother Comeau / Brother Keers

This file contains functions that will be automatically used by the prove.py
script to ensure necessary directories and files exist.
"""

import fnmatch
import os
import platform
import zipfile

def create_dir(folder):
    """
    Creates a directory if it does not already exist.
    
    Parameters:
        folder (str): The name of the directory to create if it does not exist.
    """
    if not os.path.exists(folder):
        os.makedirs(folder)


def create_images(video_file, folder):
    """
    Builds the OS specific ffmpeg command to create images from frames of an image.

    NOTE: We limit ffmpeg to 300 frames as a safety convenience

    Parameters:
        video_file (str): The name including path if necessary of the video file to process.
        folder (str):     The name of the directory to place processed images in.
    """
    if platform.system() == 'Windows':
        command = rf'.\library\ffmpeg.exe -i {video_file} -vframes 300 {folder}/image%3d.png'
    elif platform.system() == 'Darwin':
        command = rf'./library/ffmpeg -i {video_file} -vframes 300 {folder}/image%3d.png'
    else:
        command = rf'ffmpeg -i {video_file} -vframes 300 {folder}/image%3d.png'
    os.system(command)


def extract_ffmpeg():
    ffmpeg_zip = './library/ffmpeg.zip'
    if os.path.exists(ffmpeg_zip) and not os.path.exists('./library/ffmpeg') and not os.path.exists('./library/ffmpeg.exe'):
        with zipfile.ZipFile(ffmpeg_zip, "r") as zip_file:
            zip_file.extractall('library')


def get_png_file_count(dir_path):
    """Get the file count of png files in a directory.

    Parameters:
        dir_path (str): The path of the directory to count.

    Returns:
        int: The number of png files in the directory.
    """
    file_count = 0
    for file in os.listdir(dir_path):
        if fnmatch.fnmatch(file, "*.png"):
            file_count += 1
    return file_count


def setup():
    """ Make sure necessary assignment directories and files exist. """

    # Extract the ffmpeg libraries
    extract_ffmpeg()

    # Create assignment folders
    create_dir('green')
    create_dir('elephant')
    create_dir('processed')

    # Create the image files if needed
    if get_png_file_count('elephant') < 300:
        create_images('elephants.mp4', 'elephant')
    if get_png_file_count('green') < 300:
        create_images('green.mp4', 'green')


if __name__ == '__main__':
    setup()