ranks = ["Ace", "Two", "Three", "Four", "Five", "Six",
         "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]

values = {
    "Ace": (1,11),
    "King": 10,
    "Queen": 10,
    "Jack": 10,
    "Ten": 10,
    "Nine": 9,
    "Eight": 8,
    "Seven": 7,
    "Six": 6,
    "Five": 5,
    "Four": 4,
    "Three": 3,
    "Two": 2,
}

suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

import random

class Cards:
    def __init__(self,rank,suit):
        self.rank = rank
        self.suit = suit
        self.value = values[rank]

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.deck = []

        for rank in ranks:
            for suit in suits:
                self.deck.append(Cards(rank,suit))

    def shuffle(self):
        random.shuffle(self.deck)

    def draw_one(self):
        return self.deck.pop(0)


class Bank:
    def __init__(self):
        self.money = 0

    def minus(self,amount):
        self.money -= amount
        return f"{amount} has been deducted."

    def add(self,amount):
        self.money += amount
        return f"{amount} has been added."

    def __str__(self):
        return f"${self.money} left in the bank."


class Hand:
    def __init__(self):
        self.hand = []

    def calculate(self):
        total = []
        for card in self.hand:
            total.append(card.value)
        if (1,11) not in total:
            return sum(total)
        else:
            while (1,11) in total:
                total.pop(total.index((1,11)))
                total.append(11)
            while (11 in total) and sum(total) > 21:
                total.pop(total.index(11))
                total.append(1)
            return sum(total)

    def __str__(self):
        string = ""
        for card in self.hand:
            string += f"{card.rank} of {card.suit} "
        return string

    def add_card(self,card):
        self.hand.append(card)

    def show_one(self):
        return f"{self.hand[0].rank} of {self.hand[0].suit}"

def game_on():
    while True:
        play = input("Do you want to play a game of blackjack? (Y/N)")
        if play not in ["Y", "N"]:
            print("This is not a acceptable input. Please try again.")
        else:
            if play == "Y":
                print("The game will begin.")
                return True
            else:
                print("Ok bye!")
                return False


def deposit(bank):
    while True:
        try:
            amount = int(input("How much do you want to deposit?"))
        except:
            print("This is not a acceptable input. Please try again.")
        else:
            bank.add(amount)
            print(f"{amount} has been added.")
            break

def bet_amount(bank):
    while True:
        try:
            amount = int(input("How much do you want to bet?"))
            if amount > bank.money:
                print(f"You only have {bank.money}. Please try again.")
            else:
                return amount
        except:
            print("This is not a acceptable input. Please try again.")


def hit_or_stay(player,deck,computer):
    while player.calculate() < 21:
        option = input("Do you want to hit or stay? (Hit/Stay)")
        if option not in ["Hit", "Stay"]:
            print("This is not a acceptable input. Please try again.")
        elif option == "Hit": #if player decides to hit, we show his cards and the dealer card
            player.add_card(deck.draw_one())
            print(f"Your cards are {player}. You have {player.calculate()} points.")
            print(f"The dealer has {computer.show_one()}.")
        elif option == "Stay": #if player decides to stay, we will break from this while True loop
            break


def dealer_draw(player,deck,computer):
    while computer.calculate() <= player.calculate():
        if computer.calculate() == player.calculate() == 21:
            break
        else:
            computer.add_card(deck.draw_one())
            print(f"The dealer has {computer}. Dealer has {computer.calculate()}")


def play_on():
    while True:
        play = input("Do you want to keep playing a game of blackjack? (Y/N)")
        if play not in ["Y", "N"]:
            print("This is not a acceptable input. Please try again.")
        else:
            if play == "Y":
                print("The game will continue.")
                return True
            else:
                print("Ok bye!")
                return False


if __name__ == "__main__":
    play_game = game_on()
    player_bank = Bank()
    deposit(player_bank)

    while play_game:
        if player_bank.money == 0:
            print("Please top up. You currently have $0.")
            deposit(player_bank)

        bet_placed = bet_amount(player_bank) #ask the player how much they want to bet

        player_hand = Hand() #crating of hand for player and computer
        computer_hand = Hand()

        playing_deck = Deck() #creating of deck and shuffling the deck
        playing_deck.shuffle()

        player_hand.add_card(playing_deck.draw_one() )#drawing two cards from the deck
        player_hand.add_card(playing_deck.draw_one())
        computer_hand.add_card(playing_deck.draw_one())
        computer_hand.add_card(playing_deck.draw_one())

        print(f"Your cards are {player_hand}. You have {player_hand.calculate()} points.") #show what hand the player and dealer has
        print(f"The dealer has {computer_hand.show_one()}.")

        hit_or_stay(player_hand,playing_deck,computer_hand) #player decides to hit for stay

        if player_hand.calculate() > 21: #player bust, instantly loses
            print(f"You have {player_hand.calculate()}, you have busted.")
            print(f"The dealer has {computer_hand}. Dealer has {computer_hand.calculate()} points.")
            print(f"The dealer wins")
            player_bank.minus(bet_placed)
        else: #player does not bust
            print(f"The dealer has {computer_hand}. Dealer has {computer_hand.calculate()} points.")
            dealer_draw(player_hand, playing_deck, computer_hand)
            if computer_hand.calculate() > 21: #dealer bust, player wins
                print(f"The dealer has lost. Player wins.")
                player_bank.add(bet_placed)
            elif computer_hand.calculate() == player_hand.calculate(): #dealer and player both have 21 points
                print(f"Both have {computer_hand.calculate()} points. It is a draw.")
            elif computer_hand.calculate() > player_hand.calculate(): #dealer has more than player
                print(f"The dealer has won. Player loses.")
                player_bank.minus(bet_placed)

        play_game = play_on()