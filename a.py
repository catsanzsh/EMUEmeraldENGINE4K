import pygame
import time
import random

# --- Game Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
TILE_SIZE = 32
DIALOGUE_BOX_HEIGHT = 120
GAME_AREA_HEIGHT = SCREEN_HEIGHT - DIALOGUE_BOX_HEIGHT
VIEWPORT_WIDTH_TILES = SCREEN_WIDTH // TILE_SIZE
VIEWPORT_HEIGHT_TILES = GAME_AREA_HEIGHT // TILE_SIZE
FPS = 60
MAX_PLAYER_NAME_LENGTH = 7

# --- Colors ---
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
C_PATH_GRASS = (136, 192, 112)
C_GRASS_REGULAR = (104, 168, 88)
C_TALL_GRASS = (64, 128, 72)
C_TREE_TRUNK = (112, 80, 48)
C_TREE_LEAVES = (48, 96, 48)
C_WATER = (80, 128, 200)
C_FLOWER_RED = (208, 72, 48)
C_FLOWER_YELLOW = (248, 224, 96)
C_SAND = (216, 200, 160)
C_BUILDING_WALL_LIGHT = (200, 160, 120)
C_BUILDING_WALL_DARK = (160, 128, 96)
C_ROOF_RED = (192, 80, 48)
C_ROOF_BLUE = (80, 96, 160)
C_ROOF_GRAY = (128, 128, 128)
C_ROOF_MART = (60, 120, 180)
C_DOOR = (96, 64, 32)
C_SIGN = (144, 112, 80)
C_LEDGE = (120, 176, 104)
C_FENCE = (160, 144, 128)
C_PLAYER = (224, 80, 64)
C_PLAYER_GIRL = (230, 120, 150)
C_NPC = (80, 144, 224)
C_PROF = (100, 100, 180)
C_DIALOGUE_BG = (40, 40, 40)
C_DIALOGUE_TEXT = WHITE
C_DIALOGUE_BORDER = (100, 100, 100)
C_PC_WALL = (230, 190, 190)
C_MART_WALL = (180, 200, 230)
C_BUTTON = (70, 70, 150)
C_BUTTON_HOVER = (100, 100, 180)
C_BUTTON_TEXT = WHITE
C_TEXT_INPUT_BG = (60, 60, 60)
C_TEXT_INPUT_BORDER = (120, 120, 120)
C_CURSOR = (220, 220, 20)

# --- Tile Types ---
T_PATH_GRASS = 0
T_GRASS_REGULAR = 1
T_TALL_GRASS = 2
T_WATER = 3
T_TREE = 4
T_FLOWER_RED = 5
T_FLOWER_YELLOW = 6
T_SAND = 7
T_BUILDING_WALL = 10
T_PLAYER_HOUSE_WALL = 11
T_PLAYER_HOUSE_DOOR = 12
T_RIVAL_HOUSE_WALL = 13
T_RIVAL_HOUSE_DOOR = 14
T_LAB_WALL = 15
T_LAB_DOOR = 16
T_ROOF_PLAYER = 17
T_ROOF_RIVAL = 18
T_ROOF_LAB = 19
T_SIGN = 20
T_LEDGE_JUMP_DOWN = 21
T_FENCE = 22
T_PC_WALL = 23
T_PC_DOOR = 24
T_MART_WALL = 25
T_MART_DOOR = 26
T_ROOF_PC = 27
T_ROOF_MART = 28
T_NPC_SPAWN = 98
T_PLAYER_SPAWN = 99

# --- Helper Variables ---
PHW, PHD = T_PLAYER_HOUSE_WALL, T_PLAYER_HOUSE_DOOR
RHW, RHD = T_RIVAL_HOUSE_WALL, T_RIVAL_HOUSE_DOOR
LBW, LBD = T_LAB_WALL, T_LAB_DOOR
PCW, PCD = T_PC_WALL, T_PC_DOOR
MRW, MRD = T_MART_WALL, T_MART_DOOR
RPL, RRV, RLB, RPC, RMR = T_ROOF_PLAYER, T_ROOF_RIVAL, T_ROOF_LAB, T_ROOF_PC, T_ROOF_MART
TRE, PTH, SGN, FNC, WTR, TLG, FLR, FLY, LJD, NSP, PSP = \
    T_TREE, T_PATH_GRASS, T_SIGN, T_FENCE, T_WATER, T_TALL_GRASS, \
    T_FLOWER_RED, T_FLOWER_YELLOW, T_LEDGE_JUMP_DOWN, T_NPC_SPAWN, T_PLAYER_SPAWN
GRS = T_GRASS_REGULAR

# --- Map IDs ---
MAP_LITTLEROOT = 0

# --- Map Data (Completed, simple rectangular map for demo) ---
littleroot_town_map_data = [
    [TRE]*30,
    [TRE] + [PTH]*28 + [TRE],
    [TRE, PTH, FLY, PTH] + [PTH]*24 + [PTH, TRE],
    [TRE, PTH] + [TRE]*2 + [PTH]*24 + [PTH, TRE],
    [TRE] + [PTH]*28 + [TRE],
    [TRE]*30,
    [TRE, FNC, FNC, FNC, FNC, FNC, PTH, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, PTH, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, FNC, PTH, TRE],
    [TRE] + [PTH]*28 + [TRE],
    [TRE]*30,
    [TRE] + [PTH]*28 + [TRE],
    [TRE]*30
]

MAPS = {
    MAP_LITTLEROOT: littleroot_town_map_data,
}

# --- Drawing Helper ---
def draw_tile(surface, tile, x, y):
    colors = {
        T_PATH_GRASS: C_PATH_GRASS,
        T_GRASS_REGULAR: C_GRASS_REGULAR,
        T_TALL_GRASS: C_TALL_GRASS,
        T_TREE: C_TREE_LEAVES,
        T_WATER: C_WATER,
        T_FLOWER_RED: C_FLOWER_RED,
        T_FLOWER_YELLOW: C_FLOWER_YELLOW,
        T_SAND: C_SAND,
        T_BUILDING_WALL: C_BUILDING_WALL_LIGHT,
        T_PLAYER_HOUSE_WALL: C_BUILDING_WALL_LIGHT,
        T_PLAYER_HOUSE_DOOR: C_DOOR,
        T_RIVAL_HOUSE_WALL: C_BUILDING_WALL_DARK,
        T_RIVAL_HOUSE_DOOR: C_DOOR,
        T_LAB_WALL: C_BUILDING_WALL_LIGHT,
        T_LAB_DOOR: C_DOOR,
        T_PC_WALL: C_PC_WALL,
        T_PC_DOOR: C_DOOR,
        T_MART_WALL: C_MART_WALL,
        T_MART_DOOR: C_DOOR,
        T_ROOF_PLAYER: C_ROOF_RED,
        T_ROOF_RIVAL: C_ROOF_BLUE,
        T_ROOF_LAB: C_ROOF_GRAY,
        T_ROOF_PC: C_ROOF_RED,
        T_ROOF_MART: C_ROOF_MART,
        T_SIGN: C_SIGN,
        T_LEDGE_JUMP_DOWN: C_LEDGE,
        T_FENCE: C_FENCE,
        T_NPC_SPAWN: C_NPC,
        T_PLAYER_SPAWN: C_PLAYER,
    }
    color = colors.get(tile, BLACK)
    rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(surface, color, rect)
    if tile == T_TREE:
        pygame.draw.rect(surface, C_TREE_TRUNK, (x + TILE_SIZE//4, y + TILE_SIZE//2, TILE_SIZE//2, TILE_SIZE//2))
    if tile == T_SIGN:
        pygame.draw.rect(surface, BLACK, (x+TILE_SIZE//4, y+TILE_SIZE//4, TILE_SIZE//2, TILE_SIZE//2))
    if tile == T_NPC_SPAWN:
        pygame.draw.circle(surface, C_NPC, (x+TILE_SIZE//2, y+TILE_SIZE//2), TILE_SIZE//3)
    if tile == T_PLAYER_SPAWN:
        pygame.draw.circle(surface, C_PLAYER, (x+TILE_SIZE//2, y+TILE_SIZE//2), TILE_SIZE//3)

# --- Main Game Loop ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Pokemon Overworld Demo - No PNGs")
    clock = pygame.time.Clock()

    # Spawn player at a player spawn tile or top left
    player_x, player_y = 2, 2
    player_color = C_PLAYER
    map_data = MAPS[MAP_LITTLEROOT]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            if player_y > 0: player_y -= 1
            time.sleep(0.1)
        elif keys[pygame.K_DOWN]:
            if player_y < len(map_data)-1: player_y += 1
            time.sleep(0.1)
        elif keys[pygame.K_LEFT]:
            if player_x > 0: player_x -= 1
            time.sleep(0.1)
        elif keys[pygame.K_RIGHT]:
            if player_x < len(map_data[0])-1: player_x += 1
            time.sleep(0.1)
        # --- Draw ---
        screen.fill(BLACK)
        # Draw visible map
        for y in range(len(map_data)):
            for x in range(len(map_data[0])):
                draw_tile(screen, map_data[y][x], x*TILE_SIZE, y*TILE_SIZE)
        # Draw player
        pygame.draw.circle(screen, player_color, (player_x*TILE_SIZE+TILE_SIZE//2, player_y*TILE_SIZE+TILE_SIZE//2), TILE_SIZE//2-2)
        # Draw dialogue box
        pygame.draw.rect(screen, C_DIALOGUE_BG, (0, GAME_AREA_HEIGHT, SCREEN_WIDTH, DIALOGUE_BOX_HEIGHT))
        pygame.draw.rect(screen, C_DIALOGUE_BORDER, (0, GAME_AREA_HEIGHT, SCREEN_WIDTH, DIALOGUE_BOX_HEIGHT), 4)
        # Example dialogue
        font = pygame.font.SysFont(None, 36)
        txt = font.render("Welcome to Littleroot Town! (NO PNGS)", True, C_DIALOGUE_TEXT)
        screen.blit(txt, (30, GAME_AREA_HEIGHT+40))
        pygame.display.flip()
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    main()
