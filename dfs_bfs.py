import curses
from curses import wrapper
from collections import deque
import time

MAZE = [
    ["#", "S", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", " ", " ", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", "#", "#", "#", "#", "#", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", " ", " ", " ", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", "#", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "E"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]


START = "S"
END = "E"

def print_maze(maze, stdscr, path=[]):
    BLUE = curses.color_pair(1)
    RED = curses.color_pair(2)

    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i, j) in path:
                stdscr.addstr(i, j * 2, "X", RED)
            else:
                stdscr.addstr(i, j * 2, value, BLUE)

def find_start(maze):
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if value == START:
                return i, j
    return None

def find_neighbors(maze, row, col):
    neighbors = []

    if row > 0:  # UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neighbors.append((row + 1, col))
    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors

def bfs(maze, stdscr):
    start_pos = find_start(maze)
    if not start_pos:
        return []

    q = deque([(start_pos, [start_pos])])
    visited = set([start_pos])

    while q:
        current_pos, path = q.popleft()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.1)
        stdscr.refresh()

        if maze[row][col] == END:
            return path

        for r, c in find_neighbors(maze, row, col):
            if (r, c) not in visited and maze[r][c] != "#":
                visited.add((r, c))
                q.append(((r, c), path + [(r, c)]))

    return []

def dfs(maze, stdscr):
    start_pos = find_start(maze)
    if not start_pos:
        return []

    stack = [(start_pos, [start_pos])]
    visited = set([start_pos])

    while stack:
        current_pos, path = stack.pop()
        row, col = current_pos

        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.1)
        stdscr.refresh()

        if maze[row][col] == END:
            return path

        for r, c in find_neighbors(maze, row, col):
            if (r, c) not in visited and maze[r][c] != "#":
                visited.add((r, c))
                stack.append(((r, c), path + [(r, c)]))

    return []

def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    stdscr.clear()
    stdscr.addstr(0, 0, "Choose an algorithm:\n1. BFS\n2. DFS")
    stdscr.refresh()

    key = stdscr.getkey()
    if key == '1':
        find_path = bfs
    elif key == '2':
        find_path = dfs
    else:
        return

    path = find_path(MAZE, stdscr)
    stdscr.addstr(len(MAZE) + 1, 0, "Press any key to exit...")
    stdscr.refresh()
    stdscr.getch()

wrapper(main)
