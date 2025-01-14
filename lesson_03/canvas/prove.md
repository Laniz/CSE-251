# Lesson 3 Prove: Video Frame Processing

### Overview

Processing videos can take a great deal of processing time and resources. You will be combining two videos together by taking one video and placing it inside another in place of a green screen that is in the video. The results of your assignment will be a new combined video. The goal of the assignment is to use all of the CPU cores on your computer for the video processing.

### Software Required for the Assignment

**Pillow**

The Python package `pillow` needs to be installed for this assignment. Follow the same steps when you installed `numpy` and `matplotlib`.

**FFmpeg**

FFmpeg is a free open-course video and image converter. It is included in the github files for the assignment and should automatically work. If you run into any errors check the [lesson_03/library](../prove/library/) directory and make sure the zip folder has been extracted first. In case you need to manually install or move the ffmpeg library read below:

#### Windows Installation

1. The `ffmpeg.exe` file is already included in this weeks `prove` directory.
2. As long as you run the `prove.py` assignment with the `prove` directory as the root folder it should automatically be detected.

#### Mac Installation

1. The `ffmpeg` file is already included in this weeks `prove` directory.
2. As long as you run the `prove.py` assignment with the `prove` directory as the root folder it should automatically be detected.

**NOTE:** You will most likely encounter a permissions error on Mac. See the [Assignment Setup](#assignment-setup) section below for help.

#### Linux Installation

1. You will have to manually install ffmpeg globally to your system with a command similar to: `sudo apt install ffmpeg`
2. Make sure to close and reopen any terminals you had open so ffmpeg can now be detected. You may have to manually add `ffmpeg` to your `$PATH` variable.

### Assignment Setup

We have included a `setup.py` script that will automatically setup various directories and files needed for this assignment when you run your `prove.py` file for the first time.

If you are using Mac OS you might encounter a catastrophic error where the folders are created but python crashes with a cryptic error. You will need to go to the `ffmpeg` (not the one with `.exe`) file in your Finder and follow these steps:

1. Open Finder and navigate to the `library` folder where `ffmpeg` is located.
2. Right-click on the executable and select "Get Info".
3. In the "Get Info" window, click on the lock icon in the bottom-left corner and enter your administrator password to unlock it.
4. Under "Sharing & Permissions", click on the "+" button and add your user account to the list of permissions.
5. Make sure that the "Read & Write" permission is selected for your user account.
6. Click on the lock icon again to lock the permissions.

If you are still getting errors after doing this you will need to navigate to the `ffmpeg` file in your terminal and run this command: `sudo chmod 777 ffmpeg`.

---

If are on an older Mac computer you may receive the following warning message:

![](assets/mac-step-1.png)

If this box popped up click on `cancel` and go to the `Security & Privacy` options in the settings app.

![](assets/mac-step-2.png)

Click on the `Allow Anyway` button. Then close this window and return to the Python program. When you run it, might still get this warning message. Click on `open` to continue.

![](assets/mac-step-3.png)

### Assignment Files

**`setup.py`**

This file will automatically setup any missing assignment dependencies when you run your `prove.py` file for the first time. 

You must have the program `ffmpeg` in the `library` directory at the root of your `prove` assignment.

**`prove.py`**

This is the assignment file that you will write your program. Look for the `TODO` in comments. The code in the main function will create a plot of the number of frames that you process and their times.

**`elephants.mp4`**

Short video of elephants.

**`green.mp4`**

Short video of a TV with the screen all green.

**`create_final_video.py`**

Once you have created all of the frames in the `processed` folder, run this program. It will create a video based on the images found in `processed`. The video that is created will be called `final.mp4`. You are not submitting this final video file, only your Python code.

Note, I had problems viewing the final video using the default video player in Windows. I downloaded **VLC Player** and was able to view the video.

### Directory Structure

After the `setup.py` script automatically runs you will have the following directory structure:

```text
prove
  |- elephant (Contains elephant frames)
  |- green (Contains green screen frames)
  |- library (Contains the ffmpeg executables for Windows and Mac)
  |- processed (Contains your processed frame images that you create)
```

**NOTE:** There is sample code in `prove.py` that uses these folders to help you get your bearings.

### Assignment

1. Take a look at the code in `prove.py` and the `TODO` in the comments. Your goal is to process all 300 frames from the `elephant` and `green` folders to create 300 new (combined) frames in the `processed` folder.
2. You must use the `map()` function in `mp.pool()` for this assignment. (ie., p.map(function, data))
3. Your program will process all of the frames using 1 CPU core. You will need to keep track of the time it took to process all of the frames. See the main code for the variables that will be used.
4. Then, you will process all of the frames using 2 CPU cores and record to the time it took. Then 3 CPU cores, 4 CPU cores, etc... until you reach `CPU_COUNT` CPU cores.

On my computer, I have 12 CPU cores. The const variable `CPU_COUNT` is set to 4 more the number of CPU cores on your computer. So for me CPU_COUNT equals 16. Here is a example of the plot that is created for 16 CPU cores. Notice that the processing time decreases with more CPU cores. Your results might/should be different on your computer.

![](assets/16-cpu-cores-300-frames.png)

Here is a example log file for 16 CPUs

```
10:50:35| Time for 300 frames using 1 processes: 101.8020556
10:51:46| Time for 300 frames using 2 processes: 71.93878520000001
10:52:45| Time for 300 frames using 3 processes: 58.97159289999999
10:53:31| Time for 300 frames using 4 processes: 45.3859032
10:54:07| Time for 300 frames using 5 processes: 36.22025639999998
10:54:41| Time for 300 frames using 6 processes: 34.265467599999965
10:55:11| Time for 300 frames using 7 processes: 29.98336469999998
10:55:42| Time for 300 frames using 8 processes: 31.0306688
10:56:14| Time for 300 frames using 9 processes: 32.005908199999965
10:56:44| Time for 300 frames using 10 processes: 30.009154299999977
10:57:14| Time for 300 frames using 11 processes: 29.614024700000016
10:57:44| Time for 300 frames using 12 processes: 29.636116699999945
10:58:12| Time for 300 frames using 13 processes: 28.241375600000083
10:58:41| Time for 300 frames using 14 processes: 28.767867000000024
10:59:07| Time for 300 frames using 15 processes: 26.312874100000045
10:59:34| Time for 300 frames using 16 processes: 27.02049850000003
10:59:34| Total Time for ALL processing: 641.3756915
```

You will be creating a plot graph image and a log file. Both of these will be submitted with your Python program in I-Learn.

### Rubric

Assignments are not accepted late. Instead, you should submit what you have completed by the due date for partial credit. **Do not use different videos than the ones included in this assignment.**

Assignments are individual and not team based. Any assignments found to be  plagiarized will be graded according to the `ACADEMIC HONESTY` section in the syllabus. The Assignment will be graded in broad categories as outlined in the syllabus:

### Submission

When finished, you will be uploading the following in Canvas. **DO NOT** zip your files.

1. Your Python program.
2. Plot graph (image) generated by your program.
3. Log file created by your program for generating the plot graph image.
