from OrodaelTurrim.Structure.Utils import ClassAttributeDefault


class Config(metaclass=ClassAttributeDefault):
    # ----------------- Random seeds -------------------------------------------
    MAP_RANDOM_SEED = None
    AI_RANDOM_SEED = None
    UNCERTAINTY_RANDOM_SEED = None

    # ----------------- Players configuration ---------------------------------
    DEFENDER_STARTING_MONEY = 100
    DEFENDER_INCOME = 10

    ATTACKER_STARTING_MONEY = 200
    ATTACKER_INCOME = 30
    ATTACKER_INCOME_INCREASE = 1

    # ----------------- Map generator configuration ----------------------------

    # Probability that river will be on the map
    RIVER_ON_MAP_PROBABILITY = 0.9

    # Frequency of each terran type
    MOUNTAIN_FREQUENCY = 0.1
    FIELD_FREQUENCY = 0.5
    HILL_FREQUENCY = 0.1
    FOREST_FREQUENCY = 0.2
    VILLAGE_FREQUENCY = 0.01

    # Percentage bonus for neighbour with same type
    NEIGHBOUR_ADD = 0.01

    MAP_HEIGHT = 13
    MAP_WIDTH = 13
    GAME_MAP = None
