# Lesson 6 Team Teaching: Copying a File

### Overview

Your team will be using two processes to copy the contents of a text file.

### Assignment

Text files just contain ASCII characters. You will be implementing a program that copies the content of a text file to another text file. The program will need to copy the text file **exactly**. There is a function in the `team.py` program that will check to make sure that the two files are exact.

### Requirements

1. Implement the function `sender` and `receiver` to get the contents of the text file copied. Don't worry about counting the items sent over the pipe or that the copied file isn't the same as the original. Focus on having both processes exit correctly when all of the contents of the file is transferred. You must only send words (a word can have punctuation with it) over the pipe; **hint**: break up the text file into words. You might need to send other characters over the pipe too (ie., spaces, line feed, etc.).
2. Work on making the copied file exact to the original.
3. Count the number of items sent over the pipe.
4. After you get the program working, change the program to copy the file over the pipe faster. You can change your program to copy a binary file exactly using any method you want to use.

### Sample Solution

We will go over the solution in the last class of this week.

### Submission

When complete, please report your progress in the associated Canvas quiz.

If you decided to do additional work on the program after your team activity, either by yourself or with others, feel free to include that additional work when you report on your progress in Canvas.
