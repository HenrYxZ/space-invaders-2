# Window

SCALE = 1
CELL_WIDTH = 32 * SCALE
CELL_HEIGHT = 21 * SCALE
NUM_CELLS = 28
WIDTH = CELL_WIDTH * NUM_CELLS
HEIGHT = CELL_HEIGHT * NUM_CELLS
UI_WIDTH = 200 * SCALE
UI_HEIGHT = 68 * SCALE
WINDOW_WIDTH = WIDTH + UI_WIDTH
WINDOW_HEIGHT = HEIGHT + UI_HEIGHT
UI_COLOR = (150, 75, 0)
CLOCK_INTERVAL = 1 / 60
TEXT_COLOR = (0, 0, 0, 255)
FONT_SIZE = 12


# Game

PLAYER_HP = 5
PLAYER_ROW = 3
PLAYER_CELLS_HEIGHT = 3

FACTORY_START_POS = 25
FACTORY_HP = 10

MINE_RESOURCES = 1000

TRUCK_COST = 10
MAX_TRUCKS = 6
TRUCK_LOAD = 5
TRUCK_TIME_TO_MOVE = 0.5
TRUCK_START_POS = FACTORY_START_POS - 1
TRUCK_END_POS = 3

LASER_ID = 0
LASER_PACK_UNITS = 10
LASER_PACK_COST = 10
LASER_DAMAGE = 1
LASER_START_COUNT = 25

MISSILE_ID = 1
MISSILE_PACK_UNITS = 6
MISSILE_PACK_COST = 10
MISSILE_DAMAGE = 2

PLASMA_ID = 2
PLASMA_PACK_UNITS = 3
PLASMA_PACK_COST = 10
PLASMA_DAMAGE = 3

NUKE_ID = 3
NUKE_PACK_UNITS = 1
NUKE_PACK_COST = 40

SHIELD_COST = 1
SHIELD_START_ROW = PLAYER_ROW + PLAYER_CELLS_HEIGHT
SHIELD_MAX_ROWS = 3

TIME_UNIT = 1
NEXT_LEVEL_TIME = 70 * TIME_UNIT

# Probability of enemy spawn by current level. Each key is enemy level.
ENEMY_SPAWN_PROB = [
    0,
    {1: 0.5},
    {1: 0.3, 2: 0.3},
    {1: 0.2, 2: 0.2, 3: 0.1},
    {1: 0.1, 2: 0.2, 3: 0.2, 4: 0.1},
    {2: 0.1, 3: 0.2, 4: 0.2, 5: 0.1},
    {2: 0.1, 3: 0.1, 4: 0.2, 5: 0.2, 6: 0.1},
    {3: 0.1, 4: 0.2, 5: 0.2, 6: 0.2, 7: 0.1},
    {3: 0.1, 4: 0.1, 5: 0.1, 6: 0.2, 7: 0.2, 8: 0.1},
    {4: 0.1, 5: 0.1, 6: 0.2, 7: 0.2, 8: 0.2, 9: 0.1},
    {5: 0.1, 6: 0.1, 7: 0.2, 8: 0.2, 9: 0.2, 10: 0.1},
    {5: 0.1, 6: 0.1, 7: 0.2, 8: 0.2, 9: 0.2, 10: 0.2}
]
ENEMY_CELLS_WIDTH = 2
ENEMY_CELLS_HEIGHT = 3

PROJECTILE_SPEED = HEIGHT
PROJECTILE_RADIUS = 5
NORMAL_DIRECTION = 1
OPPOSITE_DIRECTION = -1
