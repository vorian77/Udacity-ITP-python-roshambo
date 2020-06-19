#!/usr/bin/env python3

"""
This program plays a game of Rock Paper Scissors Spock Lizard
between two players, and reports both player's scores each round.
It allows the user to select one of 5 different player types for
each competitor.
"""

import random
import time

moves = ["scissors", "paper", "rock", "lizard", "Spock"]


def print_pause(msg):
    print(msg.upper())
    time.sleep(0.5)


def intro():
    print_pause("This program plays a game of "
                "Rock Paper Scissors Spock Lizard")
    print_pause("between two players, "
                "and reports both player's scores each round.")
    print_pause("It allows the user "
                "to select one of 5 different player types for "
                "each competitor.")
    print_pause("\nRock Paper Scissors Spock Lizard, Go!")


class Player:
    # base Player class - only plays "rock" as a its move
    def __init__(self):
        self.score = 0

    def move(self):
        pass

    def learn(self, my_move, their_move):
        pass

    def add_win(self):
        self.score += 1

    def get_score(self):
        return self.score


class RockPlayer(Player):
    def __init__(self):
        super().__init__()

    def move(self):
        return "rock"


class HumanPlayer(Player):
    def __init__(self):
        super().__init__()

        self.prompt = ", ".join(moves)
        self.prompt = self.prompt[0].upper() + self.prompt[1:]
        self.prompt += "? > "

    def move(self):
        while True:
            inp = input(self.prompt)
            for move in moves:
                if inp.lower() == move.lower():
                    return inp


class RandomPlayer(Player):
    # moves by making random selection among move choices
    def move(self):
        return random.choice(moves)


class ReflectPlayer(Player):
    # current move is opponent's previous move
    # first move is random choice
    def __init__(self):
        super().__init__()
        self.last_opponent_move = random.choice(moves)  # first move random

    def move(self):
        return self.last_opponent_move

    def learn(self, my_move, their_move):
        self.last_opponent_move = their_move


class CyclePlayer(Player):
    # moves by cycling through the three possible moves
    # first move is random choice
    def __init__(self):
        super().__init__()
        self.move_cnt = -1

    def move(self):
        self.move_cnt += 1
        idx = self.move_cnt % 3
        return moves[idx]


def beats(p1, p1_move, p2, p2_move):
    outcomes = [["scissors", "paper", "cuts"],
                ["paper", "rock", "covers"],
                ["rock", "lizard", "crushes"],
                ["lizard", "spock", "poisons"],
                ["spock", "scissors", "smashes"],
                ["scissors", "lizard", "decapitates"],
                ["lizard", "paper", "eats"],
                ["paper", "spock", "disproves"],
                ["spock", "rock", "vaporizes"],
                ["rock", "scissors", "crushes"]]

    p1_move = p1_move.lower()
    p2_move = p2_move.lower()

    if p1_move == p2_move:
        print("** TIE **")
    else:
        for outcome in outcomes:
            if p1_move == outcome[0] and p2_move == outcome[1]:
                p1.add_win()
                print(f"** {p1_move} {outcome[2]} {p2_move} **".upper())
                print("** PLAYER ONE WINS **")
                return
            elif p1_move == outcome[1] and p2_move == outcome[0]:
                p2.add_win()
                print(f"** {p2_move} {outcome[2]} {p1_move} **".upper())
                print("** PLAYER TWO WINS **")
                return


class Game:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def play_round(self):
        # moves
        move1 = self.p1.move()
        move2 = self.p2.move()
        print(f"Player 1 played {move1}")
        print(f"Player 2 played {move2}")
        self.p1.learn(move1, move2)
        self.p2.learn(move2, move1)

        # scoring
        if move1 == move2:
            print("** TIE **")
        else:
            beats(self.p1, move1, self.p2, move2)
        print(f"Score: Player One {self.p1.get_score()}, "
              f"Player Two {self.p2.get_score()}")

    def play_match(self):
        SCORE_TO_WIN = 3
        round = 0
        while True:
            round += 1
            print(f"\nRound {round} --")
            self.play_round()

            # check: p1 won match
            if self.p1.get_score() == SCORE_TO_WIN:
                print("\nPlayer One won the match.")
                break
            # check: p2 won match
            elif self.p2.get_score() == SCORE_TO_WIN:
                print("\nPlayer Two won the match.")
                break


def select_player(player_desc, other_player):
    # allow user to select player type
    # but not a combination of player types
    # that will produce an infinite loop
    player_types = [["rock", RockPlayer()],
                    ["human", HumanPlayer()],
                    ["cycle", CyclePlayer()],
                    ["random", RandomPlayer()],
                    ["reflect", ReflectPlayer()]]
    prevent_duplicate_type = ""
    player_type_options = {}

    # if matching the type of the second player to the type of the first player
    # will cause the program to run in an infinite loop, don't include the
    # type of the first player in the options for the type of the second player
    cause_loop = ["rock", "cycle"]
    if other_player is not None:
        for item in cause_loop:
            if item in str(type(other_player)).lower():
                prevent_duplicate_type = item
                break

    # create player_type_options and user input prompt
    prompt = ""
    for player_type in player_types:
        player_type_name = player_type[0]
        player_type_object = player_type[1]
        if player_type_name != prevent_duplicate_type:
            player_type_options[player_type_name] = player_type_object
            if prompt != "":
                prompt += ", "
            prompt += player_type_name
    prompt = f"\nSelect type for player {player_desc} ({prompt}):"

    # get user input
    while True:
        inp = input(prompt).lower()
        if inp in player_type_options:
            return player_type_options[inp]


if __name__ == '__main__':
    while True:
        intro()

        # select player types
        p1 = select_player("one", None)
        p2 = select_player("two", p1)

        # init and play game
        game = Game(p1, p2)
        game.play_match()
        if "y" != input("\nPlay again? (y/n)"):
            break
