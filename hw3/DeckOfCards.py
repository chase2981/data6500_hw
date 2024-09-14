import random


class Card():
    def __init__(self, suit, face, value):
        self.suit = suit
        self.face = face
        self.val = value
        
    def __str__(self):
        return self.face + " of " + self.suit + ", value: " + str(self.val)


class DeckOfCards():
    def __init__(self):
        self.deck = []
        self.suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
        self.faces = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
        self.values = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]
        self.play_idx = 0
        
        for suit in self.suits:
            i = 0
            for i in range(len(self.faces)):
                self.deck.append(Card(suit, self.faces[i], self.values[i]))
                
                
    def shuffle_deck(self):
        random.shuffle(self.deck)
        self.play_idx = 0
        
    def print_deck(self):
        for card in self.deck:
            print(card.face, "of", card.suit, end=", ")
        print("---")
        
    def get_card(self, name, idx):
        self.play_idx += 1
        card = self.deck[self.play_idx - 1]
        print('{0} card {1} is {2}'.format(name, idx, str(card)))
        return card
        
        

