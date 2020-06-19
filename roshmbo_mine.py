import random

class Player():
    def __init__(self, name):
        self.name = name
        self.games_won = 0

    def play(self):
        pass

    def won_game(self):
        self.games_won += 1

    def get_score_value(self):
        return self.games_won

    def get_score_display(self):
        return f"Player {self.name} {self.get_score_value()}"


class HumanPlayer(Player):
    def play(self):
        while True:
            inp = input("Rock, paper, scissors? > ").lower()
            if inp in ["rock", "paper", "scissors"]:
                return inp


class ComputerPlayer(Player):
    def play(self):
        play = random.choice(["rock", "paper", "scissors"])
        return play


def score_round(players, p1_score, p2_score):
    outcomes = [["scissors", "paper"], ["rock", "scissors"], ["paper", "rock"]]

    if p1_score == p2_score:
        print("** TIE **")
        return

    for outcome in outcomes:
        if p1_score == outcome[0] and p2_score == outcome[1]:
            players[0].won_game()
            print("** PLAYER ONE WINS **")
            return
        elif p2_score == outcome[0] and p1_score == outcome[1]:
            players[1].won_game()
            print("** PLAYER TWO WINS **")
            return

def play_match():
    round = -1
    players = [HumanPlayer("One"), ComputerPlayer("Two")]

    print("Rock, Paper, Scissors, Go!")

    while True:
        round += 1
        idx = round % 1

        print(f"\nRound {round + 1} --")

        p1 = players[0].play()
        p2 = players[1].play()

        print(f"You played {p1}.")
        print(f"Opponent played {p2}.")

        score_round(players, p1, p2)

        p1_score = players[0].get_score_display()
        p2_score = players[1].get_score_display()
        print(f"Score: {p1_score}, {p2_score}")

        if players[0].get_score_value() == 3:
            print("\nPlayer 1 won the match.")
            break
        elif players[1].get_score_value() == 3:
            print("\nPlayer 2 won the match.")
            break


def play():
    while True:
        play_match()
        if "y" != input("Play again? (y/n)"):
            break


if __name__ == "__main__":
    play()
