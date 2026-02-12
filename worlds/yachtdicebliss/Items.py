import typing

from BaseClasses import Item, ItemClassification


class ItemData(typing.NamedTuple):
    code: typing.Optional[int]
    classification: ItemClassification


class YachtDiceItem(Item):
    game: str = "Yacht Dice"


# A list of all possible categories.
all_categories = {
    "Category Ones": (("", 1), 1),
    "Category Twos": (("Category Ones", 2), 2),
    "Category Threes": (("Category Ones", 3), 3),
    "Category Fours": (("Category Ones", 4), 4),
    "Category Fives": (("Category Ones", 5), 5),
    "Category Sixes": (("Category Ones", 6), 6),
    "Category Choice": (("", 1), 7),
    "Category Inverse Choice": (("Category Choice", 1), 8),
    "Category Pair": (("", 1), 9),
    "Category Three of a Kind": (("", 1), 10),
    "Category Four of a Kind": (("", 1), 11),
    "Category Tiny Straight": (("", 1), 12),
    "Category Small Straight": (("", 1), 13),
    "Category Large Straight": (("", 1), 14),
    "Category Full House": (("", 1), 15),
    "Category Yacht": (("", 1), 16),
    "Category Distincts": (("", 1), 1.5),
    "Category Two times Ones": (("Category Ones", 2), 2.5),
    "Category Half of Sixes": (("Category Ones", 3), 3.5),
    "Category Twos and Threes": (("", 1), 4.5),
    "Category Sum of Odds": (("", 1), 5.5),
    "Category Sum of Evens": (("", 1), 6.5),
    "Category Double Threes and Fours": (("", 1), 7.5),
    "Category Quadruple Ones and Twos": (("", 1), 8.5),
    "Category Micro Straight": (("", 1), 9.5),
    "Category Three Odds": (("", 1), 10.5),
    "Category 1-2-1 Consecutive": (("", 1), 11.5),
    "Category Three Distinct Dice": (("", 1), 12.5),
    "Category Two Pair": (("", 1), 13.5),
    "Category 2-1-2 Consecutive": (("", 1), 14.5),
    "Category Five Distinct Dice": (("", 1), 15.5),
    "Category 4&5 Full House": (("", 1), 16.5),
    "Category Pair SUM": (("Category Pair", 1), 9.1),
    "Category Three of a Kind SUM": (("Category Three of a Kind", 1), 10.1),
    "Category Four of a Kind SUM": (("Category Four of a Kind", 1), 11.1),
    "Category Tiny Straight SUM": (("Category Tiny Straight", 1), 12.1),
    "Category Small Straight SUM": (("Category Small Straight", 1), 13.1),
    "Category Large Straight SUM": (("Category Large Straight", 1), 14.1),
    "Category Full House SUM": (("Category Full House", 1), 15.1),
    "Category Yacht SUM": (("Category Yacht", 1), 16.1),
    "Category Micro Straight SUM": (("Category Micro Straight", 1), 9.6),
    "Category 1-2-1 Consecutive SUM": (("Category 1-2-1 Consecutive", 1), 11.6),
    "Category Two Pair SUM": (("Category Two Pair", 1), 13.6),
    "Category 2-1-2 Consecutive SUM": (("Category 2-1-2 Consecutive", 1), 14.6),
}


def find_category_index(category):
    return all_categories[category][1]


def get_normal_categories():
    return {key: value for key, value in all_categories.items() if isinstance(value[1], int)}


def get_alt_categories():
    return {key: value for key, value in all_categories.items() if not isinstance(value[1], int)}


# the starting index is chosen semi-randomly to be 16871244000


item_table = {
    "Dice": ItemData(16871244000, ItemClassification.progression | ItemClassification.useful),
    "Dice Fragment": ItemData(16871244001, ItemClassification.progression),
    "Roll": ItemData(16871244002, ItemClassification.progression),
    "Roll Fragment": ItemData(16871244003, ItemClassification.progression),
    "Fixed Score Multiplier": ItemData(16871244005, ItemClassification.progression),
    "Step Score Multiplier": ItemData(16871244006, ItemClassification.progression),
    # categories are added below
    # filler items
    "Encouragement": ItemData(16871244200, ItemClassification.filler),
    "Fun Fact": ItemData(16871244201, ItemClassification.filler),
    "Story Chapter": ItemData(16871244202, ItemClassification.filler),
    "Good RNG": ItemData(16871244203, ItemClassification.filler),
    "Bad RNG": ItemData(16871244204, ItemClassification.trap),
    "Bonus Point": ItemData(16871244205, ItemClassification.useful),  # not included in logic
    # These points are included in the logic and might be necessary to progress.
    "1 Point": ItemData(16871244301, ItemClassification.progression_skip_balancing),
    "10 Points": ItemData(16871244302, ItemClassification.progression),
    "100 Points": ItemData(16871244303, ItemClassification.progression | ItemClassification.useful),
    "Key": ItemData(16871244304, ItemClassification.progression_skip_balancing),
}

for ind, cat in enumerate(all_categories):
    item_table[cat] = ItemData(16871244400 + ind, ItemClassification.progression)

# item groups for better hinting
item_groups = {
    "Score Multiplier": {"Step Score Multiplier", "Fixed Score Multiplier"},
    "Categories": all_categories,
    "Points": {"100 Points", "10 Points", "1 Point", "Bonus Point"},
}
