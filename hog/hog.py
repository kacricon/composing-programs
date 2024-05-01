"""The Game of Hog."""

from dice import four_sided, six_sided
from ucb import main
from typing import Callable, Tuple, Any

GOAL_SCORE = 100  # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

# Taking turns


def roll_dice(num_rolls: int, dice: Callable[[], int] = six_sided) -> int:
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert isinstance(num_rolls, int), "num_rolls must be an integer."
    assert num_rolls > 0, "Must roll at least once."

    # roll dice `num_rolls` times
    score = 0
    pig_out_flag = 0
    for _ in range(0, num_rolls):
        roll = dice()
        if roll == 1:  # check pig out rule
            pig_out_flag = 1
        score += roll
    return score if not pig_out_flag else 1


def free_bacon(opponent_score: int) -> int:
    """Calculates turn score using the Free bacon rule.

    This rule finds the largest digit in the opponent's
    score and returns that digit + 1.

    opponent_score:  The opponent's current score.
    """
    # These assert statements ensure that opponent_score is an int between 0 and 99.
    assert isinstance(opponent_score, int), "opponent_score must be an integer."
    assert opponent_score >= 0 and opponent_score < 100, "opponent_score must be valid."

    # calculate score using free bacon rule
    max_digit = 0
    while opponent_score:
        opponent_score, digit = opponent_score // 10, opponent_score % 10
        max_digit = max(max_digit, digit)
    return max_digit + 1


def take_turn(
    num_rolls: int, opponent_score: int, dice: Callable[[], int] = six_sided
) -> int:
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert isinstance(num_rolls, int), "num_rolls must be an integer."
    assert num_rolls >= 0, "Cannot roll a negative number of dice."
    assert num_rolls <= 10, "Cannot roll more than 10 dice."
    assert opponent_score >= 0, "Score should be valid."
    assert opponent_score < 100, "The game should be over otherwise."

    return roll_dice(num_rolls, dice) if num_rolls > 0 else free_bacon(opponent_score)


# Playing a game


def select_dice(score: int, opponent_score: int) -> Callable[[], int]:
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).

    >>> select_dice(4, 24) == four_sided
    True
    >>> select_dice(16, 64) == six_sided
    True
    >>> select_dice(0, 0) == four_sided
    True
    """
    total_score = score + opponent_score
    return four_sided if total_score % 7 == 0 else six_sided


def other(who: int) -> int:
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who


def play(
    strategy0: Callable[[int, int], int],
    strategy1: Callable[[int, int], int],
    goal: int = GOAL_SCORE,
) -> Tuple[int, int]:
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first.
    strategy1:  The strategy function for Player 1, who plays second.
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    score, opponent_score = 0, 0

    while max(score, opponent_score) < GOAL_SCORE:
        # take turn
        dice = select_dice(score, opponent_score)
        if who == 0:  # player 0
            num_rolls = strategy0(score, opponent_score)
            score += take_turn(num_rolls, opponent_score, dice)
        else:  # player 1
            num_rolls = strategy1(opponent_score, score)
            opponent_score += take_turn(num_rolls, score, dice)

        # swine swap rule
        if score == 2 * opponent_score or 2 * score == opponent_score:
            score, opponent_score = opponent_score, score

        # switch to the other player
        who = other(who)

    return score, opponent_score


#######################
# Phase 2: Strategies #
#######################

# Basic Strategy

BASELINE_NUM_ROLLS = 5
BACON_MARGIN = 8


def always_roll(n: int) -> Callable[[int, int], int]:
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """

    def strategy(score, opponent_score):
        return n

    return strategy


# Experiments


def make_averaged(
    fn: Callable[..., int | float], num_samples: int = 10000
) -> Callable[..., float]:
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> from dice import make_test_dice
    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """

    def averaged(*args):
        results = 0
        for _ in range(num_samples):
            results += fn(*args)
        return results / num_samples

    return averaged


def max_scoring_num_rolls(dice: Callable[[], int] = six_sided) -> int:
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> from dice import make_test_dice
    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    1 dice scores 3.0 on average
    2 dice scores 6.0 on average
    3 dice scores 9.0 on average
    4 dice scores 12.0 on average
    5 dice scores 15.0 on average
    6 dice scores 18.0 on average
    7 dice scores 21.0 on average
    8 dice scores 24.0 on average
    9 dice scores 27.0 on average
    10 dice scores 30.0 on average
    10
    """
    average_roll = make_averaged(roll_dice, 1000000)
    best_play = 0
    best_roll = 0.0
    for num_rolls in range(1, 11):
        roll = average_roll(num_rolls, dice)
        print(f"{num_rolls} dice scores {roll:.1f} on average")
        if roll > best_roll:
            best_play, best_roll = num_rolls, roll
    return best_play


def winner(
    strategy0: Callable[[int, int], int], strategy1: Callable[[int, int], int]
) -> int:
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1


def average_win_rate(
    strategy: Callable[[int, int], int],
    baseline: Callable[[int, int], int] = always_roll(BASELINE_NUM_ROLLS),
) -> float:
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2  # Average results


def run_experiments() -> None:
    """Run a series of strategy experiments and report results."""
    if False:  # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print("Max scoring num rolls for six-sided dice:", six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print("Max scoring num rolls for four-sided dice:", four_sided_max)

    if True:  # Change to True to test always_roll(8)
        print("always_roll(8) win rate:", average_win_rate(always_roll(8)))

    if True:  # Change to True to test bacon_strategy
        print("bacon_strategy win rate:", average_win_rate(bacon_strategy))

    if True:  # Change to True to test swap_strategy
        print("swap_strategy win rate:", average_win_rate(swap_strategy))

    if True:  # Change to True to test final_strategy
        print("final_strategy win rate:", average_win_rate(final_strategy))


# Strategies


def bacon_strategy(score: int, opponent_score: int) -> int:
    """This strategy rolls 0 dice if that gives at least BACON_MARGIN points,
    and rolls BASELINE_NUM_ROLLS otherwise.

    >>> bacon_strategy(0, 0)
    5
    >>> bacon_strategy(70, 50)
    5
    >>> bacon_strategy(50, 70)
    0
    """
    return 0 if free_bacon(opponent_score) >= BACON_MARGIN else BASELINE_NUM_ROLLS


def swap_strategy(score: int, opponent_score: int) -> int:
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls BASELINE_NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least BACON_MARGIN points and rolls
    BASELINE_NUM_ROLLS otherwise.

    >>> swap_strategy(23, 60) # 23 + (1 + max(6, 0)) = 30: Beneficial swap
    0
    >>> swap_strategy(27, 18) # 27 + (1 + max(1, 8)) = 36: Harmful swap
    5
    >>> swap_strategy(50, 80) # (1 + max(8, 0)) = 9: Lots of free bacon
    0
    >>> swap_strategy(12, 12) # Baseline
    5
    """
    # check for swine swap rule
    fb_score = free_bacon(opponent_score)
    if 2 * (score + fb_score) == opponent_score:
        return 0
    elif (score + fb_score) == 2 * opponent_score:
        return BASELINE_NUM_ROLLS
    else:
        return 0 if fb_score >= BACON_MARGIN else BASELINE_NUM_ROLLS


def final_strategy(score: int, opponent_score: int) -> int:
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls BASELINE_NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least BACON_MARGIN points. Finally, if no other
    condition is met, roll 6 if six-sided or 4 if four-sided dice are being used.
    """
    baseline_roll = 6 if select_dice(score, opponent_score) == six_sided else 4
    baseline_roll += -1 if score >= (opponent_score + 30) else 0  # risk adjustment

    # use free bacon to force or avoid unfavorable rules
    #    check for swine swap rule
    fb_score = free_bacon(opponent_score)
    if 2 * (score + fb_score) == opponent_score:
        return 0
    elif (score + fb_score) == 2 * opponent_score:
        return baseline_roll
    #    check for hog wild
    elif select_dice(score + fb_score, opponent_score) == four_sided:
        return 0
    # use free bacon for the high points value
    elif fb_score >= BACON_MARGIN:
        return 0
    # use roll optimized for the die
    else:
        return baseline_roll


##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


def get_int(prompt: str, min: int) -> int:
    """Return an integer greater than or equal to MIN, given by the user."""
    choice = input(prompt)
    while not choice.isnumeric() or int(choice) < min:
        print("Please enter an integer greater than or equal to", min)
        choice = input(prompt)
    return int(choice)


def interactive_dice() -> int:
    """A dice where the outcomes are provided by the user."""
    return get_int("Result of dice roll: ", 1)


def make_interactive_strategy(player: int) -> Callable[[int, int], int]:
    """Return a strategy for which the user provides the number of rolls."""
    prompt = "Number of rolls for Player {0}: ".format(player)

    def interactive_strategy(score: int, opp_score: int) -> int:
        if player == 1:
            score, opp_score = opp_score, score
        print(score, "vs.", opp_score)
        choice = get_int(prompt, 0)
        return choice

    return interactive_strategy


def roll_dice_interactive() -> None:
    """Interactively call roll_dice."""
    num_rolls = get_int("Number of rolls: ", 1)
    turn_total = roll_dice(num_rolls, interactive_dice)
    print("Turn total:", turn_total)


def take_turn_interactive() -> None:
    """Interactively call take_turn."""
    num_rolls = get_int("Number of rolls: ", 0)
    opp_score = get_int("Opponent score: ", 0)
    turn_total = take_turn(num_rolls, opp_score, interactive_dice)
    print("Turn total:", turn_total)


def play_interactive() -> None:
    """Interactively call play."""
    strategy0 = make_interactive_strategy(0)
    strategy1 = make_interactive_strategy(1)
    score0, score1 = play(strategy0, strategy1)
    print("Final scores:", score0, "to", score1)


@main
def run(*args: Tuple[Any, ...]) -> None:
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse

    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument(
        "--interactive",
        "-i",
        type=str,
        help="Run interactive tests for the specified question",
    )
    parser.add_argument(
        "--run_experiments", "-r", action="store_true", help="Runs strategy experiments"
    )
    parsed_args = parser.parse_args()

    if parsed_args.interactive:
        test = parsed_args.interactive + "_interactive"
        if test not in globals():
            print("To use the -i option, please choose one of these:")
            print("\troll_dice", "\ttake_turn", "\tplay", sep="\n")
            exit(1)
        try:
            globals()[test]()
        except (KeyboardInterrupt, EOFError):
            print("\nQuitting interactive test")
            exit(0)
    elif parsed_args.run_experiments:
        run_experiments()
