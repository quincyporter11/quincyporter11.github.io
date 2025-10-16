---
title: "Blackjack Game"
slug: "blackjack-game"
date: "2025-10-02"
tags: ["python", "game"]
---

Here is a fun terminal based blackjack game I made. It supports multiple players and is a fun way to learn the game. I'd like to make a GUI version eventually but this was a fun project to make.

```python
import os, platform, random, time

# clear console
def clear_console():
    command = 'cls' if platform.system() == 'Windows' else 'clear'
    os.system(command)

# Card values
card_values = {
    '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
    '7': 7, '8': 8, '9': 9, '10': 10,
    'J': 10, 'Q': 10, 'K': 10, 'A': 11
}

# Create and shuffle a deck
def create_deck():
    deck = [rank for rank in card_values for _ in range(4)]  # 4 suits
    random.shuffle(deck)
    return deck

# Calculate hand score
def calculate_score(hand):
    score = sum(card_values[card] for card in hand)
    # Adjust for Aces
    ace_count = hand.count('A')
    while score > 21 and ace_count:
        score -= 10
        ace_count -= 1
    return score

# display hand
def display_hand(name, hand):
    print(f"{name}'s hand: {hand} | Score: {calculate_score(hand)}")

# Deal initial hands
def deal_initial(deck):
    return [deck.pop(), deck.pop()]

# scoreboard function
def scoreboard(players):
    width = 60
    print("\n" + "-" * width)
    print("Current Standings".center(width))
    print("-" * width)
    print("{:<15} {:>10} {:>10} {:>12}".format("Player", "Balance", "Score", "Result"))
    print("-" * width)
    for player in players:
        if player['result'] == "Blackjack!":
            print("{:<19} ${:<12} {:<8} {:>10}".format(
                player['name'], player['balance'], player['score'], player['result']))
        else:
            print("{:<19} ${:<7} {:>7} {:>11}".format(
                player['name'], player['balance'], player['score'], player['result']))
    print("-" * width + "\n")

# Add insurance function
def add_insurance_logic(players, dealer):
    # Check if dealer's visible card is an Ace
    if dealer[1] == 'A':
        for player in players:
            while True:
                print(f"\n{player['name']}, dealer shows an Ace.")
                print(f"Your balance: ${player['balance']}")
                choice = input(f"Do you want to buy insurance for ${player['bet']}? (y/n): ").lower()
                if choice == 'y':
                    if player['balance'] >= player['bet']:
                        player['insurance'] = player['bet']
                        player['balance'] -= player['bet']
                        print(f"Insurance purchased for ${player['bet']}.")
                    else:
                        print("Not enough balance for insurance.")
                        player['insurance'] = 0
                    break
                elif choice == 'n':
                    player['insurance'] = 0
                    break
                else:
                    print("Invalid input. Please enter 'y' or 'n'.")
    else:
        for player in players:
            player['insurance'] = 0

    return players

# Resolve insurance function
def resolve_insurance(players, dealer_score):
    if dealer_score == 21:
        for player in players:
            if player.get('insurance', 0) > 0:
                print(f"{player['name']} wins insurance bet!")
                player['balance'] += player['insurance'] * 2
    else:
        for player in players:
            if player.get('insurance', 0) > 0:
                print(f"{player['name']} loses insurance bet.")

    # Clear insurance field
    for player in players:
        player['insurance'] = 0

    return players

# main game loop ------------------------------------------------------------------------
def play_blackjack(players):
    deck = create_deck()
    dealer = []

    # Clear previous hands
    for player in players:
        player['hand'] = []
        player['result'] = ""
    dealer.clear()

    # Prompt for bets
    for player in players:
        while True:
            print(f"{player['name']} has ${player['balance']}")
            bet = input(f"{player['name']}, enter your bet:\t")
            if bet.isdigit() and 0 < int(bet) <= player['balance']:
                player['bet'] = int(bet)
                break
            else:
                print("Invalid bet.")

    clear_console()

    # Deal two cards to each player and the dealer
    for _ in range(2):
        for player in players:
            player['hand'].append(deck.pop())
        dealer.append(deck.pop())
    
    # Display dealer’s visible card
    print(f"Dealer's hand: [?, {dealer[1]}]")
    if dealer[1] == 'A':
        add_insurance_logic(players, dealer)

    for player in players:
        display_hand(player['name'], player['hand'])
    

    # Player's turn
    for player in players:
        time.sleep(2)
        first_action = True
        while True:
            print(f"\n{player['name']}'s turn")
            display_hand(player['name'], player['hand'])
            if calculate_score(player['hand']) == 21:
                print("Blackjack!")
                break
            # offer double down on first move onely
            if first_action and len(player['hand']) == 2:
                move = input("Hit, Stay, or Double:\t").lower()
            else:
                move = input("Hit or Stay:\t").lower()

            if move == "double" and first_action and len(player['hand']) == 2:
                if player['balance'] >= player['bet']:
                    player['bet'] *= 2
                    player['hand'].append(deck.pop())
                    display_hand(player['name'], player['hand'])
                    break
                else:
                    print("Insufficient balance to double down.")
            elif move == "hit":
                player['hand'].append(deck.pop())
                display_hand(player['name'], player['hand'])
                if calculate_score(player['hand']) > 21:
                    print("You bust!")
                    break
            elif move == "stay":
                break

            first_action = False

    # Dealer's turn
    print("\nDealer reveals second card:")
    display_hand("Dealer", dealer)
    dealer_score = calculate_score(dealer)
    resolve_insurance(players, dealer_score)
    while calculate_score(dealer) < 17:
        time.sleep(2)
        dealer.append(deck.pop())
        print("Dealer hits...")
        time.sleep(2)
        display_hand("Dealer", dealer)

    # Final results for all players
    dealer_score = calculate_score(dealer)
    dealer_blackjack = (dealer_score == 21 and len(dealer) == 2)

    for player in players:
        time.sleep(2)
        player['score'] = calculate_score(player['hand'])
        player_blackjack = (player['score'] == 21 and len(player['hand']) == 2)

        if player_blackjack and not dealer_blackjack:
            player['result'] = "Blackjack!"
            player['balance'] += int(player['bet'] * 1.5)
        elif player['score'] > 21:
            player['result'] = "Bust"
            player['balance'] -= player['bet']
        elif dealer_score > 21:
            player['result'] = "Win"
            player['balance'] += player['bet']
        elif player['score'] > dealer_score:
            player['result'] = "Win"
            player['balance'] += player['bet']
        elif dealer_score > player['score']:
            player['result'] = "Lose"
            player['balance'] -= player['bet']
        else:
            player['result'] = "Push"

    # display scorboard after round
    scoreboard(players)

# initailize players and start game-----------------------------------------------------------------

# get number of players at first start
while True:
    clear_console()
    numPlayers = input("Enter number of players:\t")

    if numPlayers.isdigit():
        numPlayers = int(numPlayers)
        if numPlayers > 5 or numPlayers < 1:
            print("Invalid Input")
            numPlayers = input("Enter number of players (Max 5):\t")
        else:
            break
    else:
        print("Invalid Input")
        numPlayers = input("Enter number of players (Max 5):\t")

# create player dict
players = [{'name': f'Player {i+1}', 'hand': [], 'balance': 1000, 'score' : 0, 'result' : ""} for i in range(numPlayers)]

# Run the game in while loop ----------------------------------------------------------------------
while True:
    # Remove bankrupt players
    players = [p for p in players if p['balance'] > 0]

    # End game if no players remain
    if not players:
        print("All players are out of money. Game over.")
        break

    play_blackjack(players)

    play_again = input("Play Again (y/n):\t").lower()
    if play_again == "n":
        break
    elif play_again == 'y':
        clear_console()
```