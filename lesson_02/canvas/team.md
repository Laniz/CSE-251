# Lesson 2 Team Teaching: Playing Cards

### Overview

The website [http://deckofcardsapi.com](http://deckofcardsapi.com) allows us to make Internet requests for a deck of cards. You will be using the [http://deckofcardsapi.com](http://deckofcardsapi.com) website to implement some Python classes to retrieve playing card information.

The main goal of the team activity is to use the requests package and also have experience using classes in 
Python.

### Instructions:

- Do not include any other packages/modules.
- Use the website [http://deckofcardsapi.com](http://deckofcardsapi.com) to implement the methods below. You will need to review the documentation on what API calls are available/allowed.

### Core Requirements

1. Run the `team_get_deck_id.py` script from `lesson_02/team` to get an ID for a deck of playing cards. You will be using this ID in your `team.py` code. You only need to run this program once.
2. Implement the `Request_thread` class where it can be created with a URL and it will return the results. See the example in the reading material for this lesson.
3. Implement the `Deck` class methods. Make sure that the code in `main()` can run and display card values.


### Stretch Challenge

1. Talk with your team if a `Card` class needs to be created for your game. What are the pros and cons?
2. Question: Would the class `Deck` be faster if you retrieved all of the cards for the deck when you reshuffle instead of making an API call for draw every card?  If you have the time, implement this feature.
3. Question: Why do you think that it's important to have the `Request_thread` class?  Why not just make the API calls in `Deck` directly?

### Sample Solution

When your program is finished, please view the sample solution for this program to compare it to your approach.

You should work to complete this team activity for the one hour period first, without looking at the sample solution. However, if you have worked on it for at least an hour and are still having problems, you may feel free to use the sample solution to help you finish your program.

- Sample solution (Core requirements): [Solution](../team/team_solution.py)

### Submission

When complete, please report your progress in the associated Canvas quiz.
