import sys
import pygame
import copy
import time
import os
import queue
from collections import deque
import tracemalloc

from game import Game
from algorithms import *

#######################
#  THIẾT LẬP CHUNG    #
#######################

TIME_LIMITED = 1800
DEBUG = True  # Bật/mở log debug

# Thử import psutil để đo Memory
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

def current_memory_mb():
    if not HAS_PSUTIL:
        return 0.0
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info().rss  # bytes
    return mem_info / (1024.0 * 1024.0)

def log_debug(*args):
    if DEBUG:
        print("[DEBUG]", *args)

########################
#  HÀM ĐỌC FILE LEVEL  #
########################

def map_open(level):
    level_path = f"levels/input-{level}.txt"
    if not os.path.exists(level_path):
        print(f"ERROR: File {level_path} not found!")
        sys.exit(1)
    matrix = []
    box_positions = []
    box_weights = {}
    with open(level_path, 'r') as file:
        line_weights = file.readline().strip()
        try:
            weight_list = list(map(int, line_weights.split()))
        except ValueError:
            print(f"ERROR: Invalid weight format in {level_path}")
            sys.exit(1)
        y = 0
        for line in file:
            row = []
            content = line.rstrip('\n')
            x = 0
            for c in content:
                if c in [' ', '#', '@', '+', '.', '*', '$']:
                    row.append(c)
                    if c in ['$', '*']:
                        box_positions.append((x, y))
                else:
                    print(f"ERROR: Invalid character '{c}' in {level_path}")
                    sys.exit(1)
                x += 1
            if row:
                matrix.append(row)
                y += 1
    if len(box_positions) != len(weight_list):
        print(f"ERROR: Number of boxes ({len(box_positions)}) != number of weights ({len(weight_list)})")
        sys.exit(1)
    for i, pos in enumerate(box_positions):
        box_weights[pos] = weight_list[i]
    log_debug("Loaded level:", level, "Box weights:", box_weights)
    return matrix, box_weights


##############################
# HÀM KIỂM TRA DEADLOCK ĐƠN #
##############################

def get_cell(state, x, y):
    # Nếu (x, y) nằm ngoài biên, coi như là tường
    if x < 0 or y < 0 or y >= len(state.matrix) or x >= len(state.matrix[y]):
        return '#'
    return state.get_content(x, y)

def is_deadlock(state):
    # Duyệt qua tất cả các box.
    # Chỉ kiểm tra các box chưa ở dock (ký hiệu '$', không phải '*')
    for (x, y) in state.box_list():
        if state.get_content(x, y) != '$':
            continue
        # Kiểm tra góc trên bên trái
        if get_cell(state, x-1, y) == '#' and get_cell(state, x, y-1) == '#':
            return True
        # Kiểm tra góc trên bên phải
        if get_cell(state, x+1, y) == '#' and get_cell(state, x, y-1) == '#':
            return True
        # Kiểm tra góc dưới bên trái
        if get_cell(state, x-1, y) == '#' and get_cell(state, x, y+1) == '#':
            return True
        # Kiểm tra góc dưới bên phải
        if get_cell(state, x+1, y) == '#' and get_cell(state, x, y+1) == '#':
            return True
    return False


#######################################
#     HÀM TÍNH HEURISTIC ĐƠN GIẢN    #
#######################################

def get_distance(state):
    sum_dist = 0
    boxes = state.box_list()
    docks = state.dock_list()
    for b in boxes:
        best = 999999
        for d in docks:
            dist = abs(d[0] - b[0]) + abs(d[1] - b[1])
            if dist < best:
                best = dist
        sum_dist += best
    return sum_dist

def worker_to_box(state):
    w = state.worker()
    if not w:
        return 0
    wx, wy, _ = w
    min_dist = 999999
    for (bx, by) in state.box_list():
        dist = abs(wx - bx) + abs(wy - by)
        if dist < min_dist:
            min_dist = dist
    return min_dist

############################
#     REPLAY GIẢI PHÁP     #
############################

def replay_solution(original_game, solution_path):
    gcopy = copy.deepcopy(original_game)
    replayed = []
    total_weight = 0
    for mv in solution_path:
        dx, dy = 0, 0
        if mv == 'U':
            dx, dy = 0, -1
        elif mv == 'D':
            dx, dy = 0, 1
        elif mv == 'L':
            dx, dy = -1, 0
        elif mv == 'R':
            dx, dy = 1, 0
        cost = gcopy.move_with_cost(dx, dy, False)
        if cost > 1:
            total_weight += (cost - 1)
            replayed.append(mv.upper())
        else:
            replayed.append(mv.lower())
    return "".join(replayed), len(solution_path), total_weight



#########################
#  HÀM HỖ TRỢ PYGAME    #
#########################

def get_key():
    while True:
        event = pygame.event.poll()
        if event.type == pygame.KEYDOWN:
            return event.key
        time.sleep(0.01)

def display_box(screen, message):
    fontobject = pygame.font.Font(None, 18)
    rect = pygame.Rect((screen.get_width() / 2) - 100,
                       (screen.get_height() / 2) - 10,
                       200, 20)
    pygame.draw.rect(screen, (0, 0, 0), rect, 0)
    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
    if len(message) != 0:
        text_surface = fontobject.render(message, True, (255, 255, 255))
        screen.blit(text_surface, (rect.x + 2, rect.y + 2))
    pygame.display.flip()

def ask(screen, question):
    pygame.font.init()
    current_string = []
    display_box(screen, question + ": " + "".join(current_string))
    while True:
        inkey = get_key()
        if inkey == pygame.K_BACKSPACE:
            current_string = current_string[:-1]
        elif inkey == pygame.K_RETURN:
            break
        elif inkey <= 127:
            current_string.append(chr(inkey))
        display_box(screen, question + ": " + "".join(current_string))
    return "".join(current_string)

def display_end(screen, msg):
    if msg == "Done":
        message = "Level Completed"
    elif msg == "Cannot":
        message = "No Solution"
    elif msg == "Out":
        message = "Time Out!"
    else:
        message = msg
    fontobject = pygame.font.Font(None, 18)
    rect = pygame.Rect((screen.get_width() / 2) - 100,
                       (screen.get_height() / 2) - 10,
                       200, 20)
    pygame.draw.rect(screen, (0, 0, 0), rect, 0)
    pygame.draw.rect(screen, (255, 255, 255), rect, 1)
    text_surface = fontobject.render(message, True, (255, 255, 255))
    screen.blit(text_surface, (rect.x + 2, rect.y + 2))
    pygame.display.flip()

def start_game():
    start = pygame.display.set_mode((320, 240))
    level_str = ask(start, "Select Level")
    return level_str

###################
#  LOAD HÌNH ẢNH  #
###################

img_width = 32
img_height = 32

pygame.init()
wall = pygame.transform.scale(pygame.image.load('images/wall.png'), (img_width, img_height))
floor = pygame.transform.scale(pygame.image.load('images/floor.png'), (img_width, img_height))
box = pygame.transform.scale(pygame.image.load('images/stone.png'), (img_width, img_height))
box_docked = pygame.transform.scale(pygame.image.load('images/stone_on_switch.png'), (img_width, img_height))
worker = pygame.transform.scale(pygame.image.load('images/ares.png'), (img_width, img_height))
worker_docked = pygame.transform.scale(pygame.image.load('images/ares_on_switch.png'), (img_width, img_height))
docker = pygame.transform.scale(pygame.image.load('images/switch.png'), (img_width, img_height))
background = (255, 226, 191)

def print_game(matrix, screen):
    screen.fill(background)
    y = 0
    for row in matrix:
        x = 0
        for char in row:
            if char == ' ':
                screen.blit(floor, (x, y))
            elif char == '#':
                screen.blit(wall, (x, y))
            elif char == '@':
                screen.blit(worker, (x, y))
            elif char == '.':
                screen.blit(docker, (x, y))
            elif char == '*':
                screen.blit(box_docked, (x, y))
            elif char == '$':
                screen.blit(box, (x, y))
            elif char == '+':
                screen.blit(worker_docked, (x, y))
            x += 32
        y += 32

#########################
#  HÀM ĐO VÀ IN THỐNG KÊ  #
#########################

def run_and_measure(algorithm_name, solve_func, base_game):
    log_debug(f"--- {algorithm_name} start ---")
    start_time = time.time()
    start_mem = current_memory_mb()
    tracemalloc.start()
    # Tạo bản sao mới cho thuật toán
    game_copy = copy.deepcopy(base_game)
    solution_path, node_generated = solve_func(game_copy)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_time = time.time()
    end_mem = current_memory_mb()
    used_time = (end_time - start_time)*1000
    used_mem = end_mem - start_mem
    # Ghi kết quả ra file (append)
    with open("results.txt", "a", encoding="utf-8") as f:
        f.write(f"{algorithm_name}\n")
        if solution_path in ["NoSol", "TimeOut", ""]:
            f.write(f"Steps: 0, Weight: 0, Node: {node_generated}, Time (ms): 0.00, Memory (MB): 0.00\n")
            f.write(f"{solution_path}\n\n")
        else:
            # Dùng bản sao mới của base_game để replay
            replay_game = copy.deepcopy(base_game)
            replayed_path, steps, total_weight = replay_solution(replay_game, solution_path)
            f.write(f"Steps: {steps}, Weight: {total_weight}, Node: {node_generated}, Time (ms): {used_time:.2f}, Memory (MB): {peak / (1024*1024):.5f}\n")
            f.write(f"{replayed_path}\n\n")
    # Đồng thời in ra console
    print(f"{algorithm_name}")
    if solution_path in ["NoSol", "TimeOut", ""]:
        print(f"Steps: 0, Weight: 0, Node: {node_generated}, Time (ms): 0.00, Memory (MB): 0.00")
        print(solution_path, "\n")
    else:
        print(f"Steps: {len(solution_path)}, Weight: {total_weight}, Node: {node_generated}, Time (ms): {used_time:.2f}, Memory (MB): {peak / (1024*1024):.5f}")
        replay_game = copy.deepcopy(base_game)
        replayed_path, steps, total_weight = replay_solution(replay_game, solution_path)
    return (solution_path, node_generated)


