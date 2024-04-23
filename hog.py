import random


def game() -> None:
    scores = [0, 0]
    player = 0
    while(max(scores) < 100):
        # prompt player for their play this turn
        choice = input(
            f"\n- Player {player+1:d}: choose number of dice to roll this turn (0 to 10).\n"
        )
        while not (choice := parse_input(choice)):
            choice = input(
                f"\n- You must choose a number between 0 and 10. Try again.\n"
            )

        # add turn score
        if choice == 100: # free bacon rule
            score = free_bacon(scores[not player])
            print(f"\n- Player {player+1:d} scored {score} points from the Free Bacon rule!\n")
        else: # dice roll
            dx = 4 if (scores[0] + scores[1]) > 0 and (scores[0] + scores[1]) % 7 == 0 else 6 # hog wild rule
            if dx == 4:
                print(f"\n- Hog Wild rule activated, rolling d4's instead of d6's.\n")
            score = turn_score(choice, dx)
            print(f"\n- Player {player+1:d} scored {score} points in {choice} rolls!\n")
        scores[player] += score
        print(f"\n- Current score\nPlayer 1: {scores[0]} X Player 2: {scores[1]}\n")

        # swine swap rule
        if scores[0] == 2 * scores[1] or scores[1] == 2 * scores[0]:
            scores[0], scores[1] = scores[1], scores[0]
            print(f"\n- Swine Swap rule activated, player scores have been swapped.\n")
            print(f"\n- Current score\nPlayer 1: {scores[0]} X Player 2: {scores[1]}\n")

        # switch player
        player = not player

    print(f"\n- Player {(not player)+1:d} is the winner!\nPlayer 1: {scores[0]} X Player 2: {scores[1]}\n")


def parse_input(choice: str) -> int:
    try:
        choice = int(choice)
        if choice < 0 or choice > 10:
            return 0
        elif choice == 0:
            return 100
        return choice
    except ValueError:
        return 0


def turn_score(n: int, dx: int) -> int:
    score = 0
    for i in range(n):
        roll = random.randint(1, dx)
        if roll == 1: # pig out
            return 1
        score += roll
    return score


def free_bacon(score: int) -> int:
    max_digit = 0
    while score:
        score, digit = score // 10, score % 10
        max_digit = max(max_digit, digit) 
    return max_digit + 1 


if __name__ == "__main__":
    game()
