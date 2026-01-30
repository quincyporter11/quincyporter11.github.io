---
title: "Number Guessing Game"
slug: "number-guessing-game"
date: "2025-10-16"
tags: ["python", "game"]
---

Here is a simple number guessing game I created. I implemented a class to practice object oriented programming. It is currently a simple version with no error handling and three difficulty options.

```python
import random
from os import system, name

# class to hold basic game functions
class game():

    # init function to generate number
    def __init__(self, x, y):
        self.number = random.randint(x, y)

    # function to return number
    def getNumber(self):
        return(self.number)
    
    def higherOrLower(self, x):
        if x > self.number:
            return "My number is lower"
        elif x < self.number:
            return "My number is higher"
        else:
            return "You guessed my number"
    
# function to clear terminal
def clearTerminal():
    if name == 'nt':
        _ = system('cls')
    else:
        _ = system('clear')

# main function
def main():
    # initialize variables
    MAX_ATTEMPT = 3
    attempt = 1
    correct = False

    # start with clear terminal
    clearTerminal()

    dificulty = int(input("Select Dificulty 1, 2, 3:\t"))

    if dificulty == 1:
        number = game(1, 10)
        print("Try to guess my number from 1-10")
    elif dificulty == 2:
        number = game(1, 15)
        print("Try to guess my number from 1-15")
    elif dificulty == 3:
        number = game(1, 20)
        print("Try to guess my number from 1-20")

    # while loop to play number guessing game
    while attempt <= MAX_ATTEMPT:
        guess = int(input(f"Guess {attempt}:\t"))

        # if statement to break loop on successfull guess
        if guess == number.getNumber():
            correct = True
            break

        print(f"{number.higherOrLower(guess)}")
        attempt += 1

    if correct == True:
        print("You Won! Would you like to play again?")
        playAgain = input("y/n:\t")
    else:
        print(f"You lost. My number was {number.getNumber()}. Would you like to play again?")
        playAgain = input("y/n:\t")

    if playAgain == "y":
        clearTerminal()
        main()
    else:
        print("Goodbye!")

if __name__ == "__main__":
    main()
```
