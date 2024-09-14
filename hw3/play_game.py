from DeckOfCards import *

# Function to calculate the score of either player based on the cards with Ace handling
def calculate_score(cards):
    score = sum(card.val for card in cards)
    # Handle Aces: if score > 21 and there's an Ace, count the Ace as 1 instead of 11
    aces = len([card for card in cards if card.face == "Ace"])
    
    # Foreach Ace we will convert their values to 1 only while the score is greater than 21
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    
    return score

# Function to display the player's hand and score by player name
def display_hand(player_name, cards):
    if player_name == 'Dealer':
        # print(f"{player_name}'s cards: ", ', '.join([str(card) for card in cards]))
        print(f"{player_name}'s score: ", calculate_score(cards))
    else:
        # print(f"Your cards: ", ', '.join([str(card) for card in cards]))
        print(f"Your total score is: ", calculate_score(cards))

# Main game function
def play_blackjack():
    print("Welcome to BlackJack!")
    
    deck = DeckOfCards()
    
    while True:
        # Shuffle and print the deck
        print("\nDeck before shuffle:")
        deck.print_deck()
        deck.shuffle_deck()
        print("\nDeck after shuffle:")
        deck.print_deck()
        
        # Deal initial cards to player and dealer
        player_cards = [deck.get_card('Your', 1), deck.get_card('Your', 2)]
        dealer_cards = [deck.get_card('Dealer', 1), deck.get_card('Dealer', 2)]

        # Display player's hand
        display_hand("Player", player_cards)

        # Player's turn - this will keep going until breaked
        while True:
            hit = input("Would you like a hit? (y/n): ").lower()
            if hit == 'y':
                player_cards.append(deck.get_card('Your', len(player_cards) + 1))
                display_hand("Player", player_cards)
                if calculate_score(player_cards) > 21:
                    print("You busted! Dealer wins.")
                    break
            else:
                break
        
        # If player hasn't busted, proceed with the dealer's turn
        if calculate_score(player_cards) <= 21:
            print("\nDealer's turn...")
            display_hand("Dealer", dealer_cards)

            # Dealer keeps hitting until their score is 17 or higher or if player's score is higher
            while calculate_score(dealer_cards) < 17 or (calculate_score(player_cards) > calculate_score(dealer_cards)):
                print("Dealer hits...")
                dealer_cards.append(deck.get_card('Dealer', len(dealer_cards) + 1))
                display_hand("Dealer", dealer_cards)
            
            # Determine the winner
            player_score = calculate_score(player_cards)
            dealer_score = calculate_score(dealer_cards)
            
            if dealer_score > 21:
                print("Dealer busted! You win!")
            elif player_score > dealer_score:
                print("You win! Your score is higher.")
            elif player_score == dealer_score:
                print("It's a tie! Dealer wins!")
            else:
                print("Dealer wins with a higher score.")
        
        # Ask if the player wants to play again
        again = input("Would you like to play again? (y/n): ").lower()
        if again != 'y':
            break

# Start the game
play_blackjack()
