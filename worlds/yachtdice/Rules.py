import math
from collections import Counter, defaultdict
from typing import List, Optional

from BaseClasses import MultiWorld

from worlds.generic.Rules import set_rule

from .YachtWeights import yacht_weights

# This module adds logic to the apworld.
# In short, we ran a simulation for every possible combination of dice and rolls you can have, per category.
# This simulation has a good strategy for locking dice.
# This gives rise to an approximate discrete distribution per category.
# We calculate the distribution of the total score.
# We then pick a correct percentile to reflect the correct score that should be in logic.
# The score is logic is *much* lower than the actual maximum reachable score.


class Category:
    def __init__(self, name, quantity=1):
        self.name = name
        self.quantity = quantity  # how many times you have the category

    # return mean score of a category
    def mean_score(self, num_dice, num_rolls):
        if num_dice <= 0 or num_rolls <= 0:
            return 0
        mean_score = 0
        for key, value in yacht_weights[self.name, min(8, num_dice), min(8, num_rolls)].items():
            mean_score += key * value / 100000
        return mean_score


class ListState:
    def __init__(self, state: List[str]):
        self.state = state
        self.item_counts = Counter(state)

    def count(self, item: str, player: Optional[str] = None) -> int:
        return self.item_counts[item]


def extract_progression(state, player, frags_per_dice, frags_per_roll, allowed_categories):
    """
    method to obtain a list of what items the player has.
    this includes categories, dice, rolls and score multiplier etc.
    First, we convert the state if it's a list, so we can use state.count(item, player)
    """
    if isinstance(state, list):
        state = ListState(state=state)

    number_of_dice = state.count("Dice", player) + state.count("Dice Fragment", player) // frags_per_dice
    number_of_rerolls = state.count("Roll", player) + state.count("Roll Fragment", player) // frags_per_roll
    number_of_fixed_mults = state.count("Fixed Score Multiplier", player)
    number_of_step_mults = state.count("Step Score Multiplier", player)

    categories = [
        Category(category_name, state.count(category_name, player))
        for category_name in allowed_categories
        if state.count(category_name, player)  # want all categories that have count >= 1
    ]

    extra_points_in_logic = state.count("1 Point", player)
    extra_points_in_logic += state.count("10 Points", player) * 10
    extra_points_in_logic += state.count("100 Points", player) * 100

    return (
        categories,
        number_of_dice,
        number_of_rerolls,
        number_of_fixed_mults * 0.1,
        number_of_step_mults * 0.01,
        extra_points_in_logic,
    )


border_values = [0, [.22, .41], [.41, .51], [.51, .64], [.64, .76], [.76, .88], [.88, .94], [.94, .98]]
def dice_simulation_strings(categories, num_dice, num_rolls, fixed_mult, step_mult, diff):
    """
    Function that returns the feasible score in logic based on items obtained.
    """
    tup = (
        tuple([c.name + str(c.quantity) for c in categories]),
        num_dice,
        num_rolls,
        fixed_mult,
        step_mult,
        diff,
    )  # identifier

    # sort categories because for the step multiplier, you will want low-scoring categories first
    # to avoid errors with order changing when obtaining rolls, we order assuming 4 rolls
    if step_mult > 0:
        categories.sort(key=lambda category: category.mean_score(num_dice, 4))

    total_score = 0
    bv1 = border_values[diff][0]
    bv2 = border_values[diff][1]
    
    if num_dice <= 0 or num_rolls <= 0:
        return 0
    
    dice_limited = min(8, num_dice)
    rolls_limited = min(8, num_rolls)
    

    for j, category in enumerate(categories):
        dist = yacht_weights[category.name, dice_limited,rolls_limited]
        
        def find_percentile(distribution, percentile):
            perc = percentile * 100000
            cumulative_prob = 0
            for key, value in distribution.items():
                cumulative_prob += value
                if cumulative_prob >= perc:
                    return key
            return 0
        
        cat_mult = 2 ** (category.quantity - 1)

        mult = (1 + fixed_mult + step_mult * j) * cat_mult 
        
        v1 = find_percentile(dist, bv1)
        v2 = find_percentile(dist, bv2)
        total_score += math.floor( ( v1 + v2 ) * mult) / 2

    return max(5, total_score)


def dice_simulation_fill_pool(state, frags_per_dice, frags_per_roll, allowed_categories, difficulty):
    """
    Returns the feasible score that one can reach with the current state, options and difficulty.
    This function is called with state being a list, during filling of item pool.
    """
    categories, num_dice, num_rolls, fixed_mult, step_mult, expoints = extract_progression(
        state, "state_is_a_list", frags_per_dice, frags_per_roll, allowed_categories
    )
    return (
        dice_simulation_strings(categories, num_dice, num_rolls, fixed_mult, step_mult, difficulty) + expoints
    )


def dice_simulation_state_change(state, player, frags_per_dice, frags_per_roll, allowed_categories, difficulty):
    """
    Returns the feasible score that one can reach with the current state, options and difficulty.
    This function is called with state being a AP state object, while doing access rules.
    """

    if state.prog_items[player]["state_is_fresh"] == 0:
        state.prog_items[player]["state_is_fresh"] = 1
        categories, num_dice, num_rolls, fixed_mult, step_mult, expoints = extract_progression(
            state, player, frags_per_dice, frags_per_roll, allowed_categories
        )
        state.prog_items[player]["maximum_achievable_score"] = (
            dice_simulation_strings(categories, num_dice, num_rolls, fixed_mult, step_mult, difficulty)
            + expoints
        )

    return state.prog_items[player]["maximum_achievable_score"]


def set_yacht_rules(world: MultiWorld, player: int, frags_per_dice, frags_per_roll, allowed_categories, difficulty):
    """
    Sets rules on reaching scores
    """

    for location in world.get_locations(player):
        set_rule(
            location,
            lambda state, curscore=location.yacht_dice_score, player=player: dice_simulation_state_change(
                state, player, frags_per_dice, frags_per_roll, allowed_categories, difficulty
            )
            >= curscore,
        )


def set_yacht_completion_rules(world: MultiWorld, player: int):
    """
    Sets rules on completion condition
    """
    world.completion_condition[player] = lambda state: state.has("Victory", player)
