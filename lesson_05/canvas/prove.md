# Lesson 5 Prove: Factories and Dealers

### Overview

You will be using queue(s) and thread semaphore(s) to synchronize many threads in the production and selling of cars.

### Project Description

This is a continuation of the Lesson 4 Prove assignment. This time, instead of one factory and one dealership, you will have many different combinations. For example:

 Factories | Dealerships 
-----------|-------------
 1         | 1           
 1         | 2           
 2         | 1           
 2         | 2           
 2         | 5           
 5         | 2           
 10        | 10          

Your code must correctly account for these relationships. The restriction of only producing `MAX_QUEUE_SIZE` is still in place for all of the dealerships.

**NOTE:** We have removed the `size()` method from the `Queue251()` class because it is not needed in this assignment. It was only included in the previous assignment so you could easily create the *cars in queue* graph. You should not have relied on it in the previous prove for anything else.

**HINT:** If you find yourself drastically changing your code from the previous assignments solution you may be misunderstanding this weeks material. 

### Assignment

1. Review the instructions found in the Python file as well as the global constants.
2. The function `run_production()` will be passed different number of factories and dealerships that are to be created for a production run.
3. You must not use the Python queue object for this assignment. Use the class `Queue251()` instead.

Here is a sample run of the completed assignment. The number of cars each factory produces is random:

```
08:58:05| 248 cars have been created. = 2.85694300
08:58:05| Factories      : 1
08:58:05| Dealerships    : 1
08:58:05| Run Time       : 2.8569
08:58:05| Max queue size : 10
08:58:05| Factory Stats  : Made = 248 @ [248]
08:58:05| Dealer Stats   : Sold = 248 @ [248]
08:58:05| 
08:58:08| 225 cars have been created. = 2.45859890
08:58:08| Factories      : 1
08:58:08| Dealerships    : 2
08:58:08| Run Time       : 2.4586
08:58:08| Max queue size : 5
08:58:08| Factory Stats  : Made = 225 @ [225]
08:58:08| Dealer Stats   : Sold = 225 @ [113, 112]
08:58:08| 
08:58:14| 523 cars have been created. = 5.82195820
08:58:14| Factories      : 2
08:58:14| Dealerships    : 1
08:58:14| Run Time       : 5.8220
08:58:14| Max queue size : 10
08:58:14| Factory Stats  : Made = 523 @ [290, 233]
08:58:14| Dealer Stats   : Sold = 523 @ [523]
08:58:14| 
08:58:17| 484 cars have been created. = 3.32068590
08:58:17| Factories      : 2
08:58:17| Dealerships    : 2
08:58:17| Run Time       : 3.3207
08:58:17| Max queue size : 10
08:58:17| Factory Stats  : Made = 484 @ [277, 207]
08:58:17| Dealer Stats   : Sold = 484 @ [241, 243]
08:58:17| 
08:58:20| 478 cars have been created. = 3.05134620
08:58:20| Factories      : 2
08:58:20| Dealerships    : 5
08:58:20| Run Time       : 3.0513
08:58:20| Max queue size : 5
08:58:20| Factory Stats  : Made = 478 @ [225, 253]
08:58:20| Dealer Stats   : Sold = 478 @ [94, 98, 96, 94, 96]
08:58:20| 
08:58:28| 1299 cars have been created. = 7.39873040
08:58:28| Factories      : 5
08:58:28| Dealerships    : 2
08:58:28| Run Time       : 7.3987
08:58:28| Max queue size : 10
08:58:28| Factory Stats  : Made = 1299 @ [217, 291, 256, 285, 250]
08:58:28| Dealer Stats   : Sold = 1299 @ [647, 652]
08:58:28| 
08:58:31| 2528 cars have been created. = 3.58550450
08:58:31| Factories      : 10
08:58:31| Dealerships    : 10
08:58:31| Run Time       : 3.5855
08:58:31| Max queue size : 9
08:58:31| Factory Stats  : Made = 2528 @ [274, 250, 289, 265, 213, 246, 227, 231, 288, 245]
08:58:31| Dealer Stats   : Sold = 2528 @ [263, 258, 247, 257, 259, 247, 244, 253, 244, 256]
```

### Rubric

Assignments are not accepted late. Instead, you should submit what you have completed by the due date for partial credit. Assignments are individual and not team based. Any assignments found to be  plagiarized will be graded according to the `ACADEMIC HONESTY` section in the syllabus. The Assignment will be graded in broad categories as outlined in the syllabus.

### Submission

When finished, upload your Python file to Canvas.