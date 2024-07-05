import typing

from BaseClasses import Location


class LocData(typing.NamedTuple):
    id: int
    region: str
    mission: int
    score: int


class YachtDiceLocation(Location):
    game: str = "Yacht Dice"

    def __init__(self, player: int, name: str, score: int, mission: int, address: typing.Optional[int], parent):
        super().__init__(player, name, address, parent)
        self.yacht_dice_score = score
        self.mission_number = mission


all_locations = {}
starting_index = 16871244500  # 500 more than the starting index for items (not necessary, but this is what it is now)


def all_locations_fun(max_score, num_missions):
    """
    Function that is called when this file is loaded, which loads in ALL possible locations, score 1 to 1000
    """
    
    return {
        f"Mission {mission+1}, {score} score": 
            LocData(starting_index + mission * 10000000 + score, "Board", mission + 1, score)
        for mission in range(num_missions)
        for score in range(1, max_score + 1)
    }


def ini_locations(goal_score, max_score, number_of_locations, dif):
    """
    function that loads in all locations necessary for the game, so based on options.
    will make sure that goal_score and max_score are included locations
    """
    
    scaling = 2  # parameter that determines how many low-score location there are.
    # need more low-score locations or lower difficulties:
    if dif == 1:
        scaling = 3
    elif dif == 2:
        scaling = 2.3

    scores = {}
    # the scores follow the function int( 1 + (percentage ** scaling) * (max_score-1) )
    # however, this will have many low values, sometimes repeating.
    # to avoid repeating scores, highest_score keeps tracks of the highest score location
    # and the next score will always be at least highest_score + 1
    # note that current_score is at most max_score-1
    for mission, num_locs in enumerate(number_of_locations):
        highest_score = 0
        scores_mission = []
        for i in range(num_locs-1):
            percentage = i / (num_locs-1)
            current_score = int(1 + (percentage**scaling) * (max_score - 2))
            if current_score <= highest_score:
                current_score = highest_score + 1
            highest_score = current_score
            scores_mission.append(current_score)

        if mission == len(number_of_locations)  - 1 and goal_score != max_score:
            # if the goal score is not in the list, find the closest one and make it the goal.
            if goal_score not in scores_mission:
                closest_num = min(scores_mission, key=lambda x: abs(x - goal_score))
                scores_mission[scores_mission.index(closest_num)] = goal_score
              
        scores_mission.append(max_score)
        scores[mission] = scores_mission
        
    location_table = {f"Mission {mission+1}, {score} score": LocData(starting_index + mission * 10000000 + score, "Board", mission + 1, score) for mission, locations in scores.items() for score in locations}


    return location_table


# we need to run this function to initialize all scores from 1 to 1000, even though not all are used
all_locations = all_locations_fun(1000, 10)
