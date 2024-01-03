from copy import deepcopy

with open("reflector.in", "r") as f:
    data = [line.rstrip() for line in f]

def part1():
    output = 0
    for col in range(len(data[0])):
        rock_weight = len(data)
        for row in range(len(data)):
            if data[row][col] == "O":
                output += rock_weight
                rock_weight -= 1
            elif data[row][col] == "#":
                rock_weight = len(data) - row - 1

    print(output)

def cycle(board):
    board = deepcopy(board)
    for col in range(len(board[0])):
        rock_row = 0
        for row in range(len(board)):
            if board[row][col] == "O":
                board[row][col] = "."
                board[rock_row][col] = "O"
                rock_row += 1
            elif board[row][col] == "#":
                rock_row = row + 1
    for row in range(len(board)):
        rock_col = 0
        for col in range(len(board[0])):
            if board[row][col] == "O":
                board[row][col] = "."
                board[row][rock_col] = "O"
                rock_col += 1
            elif board[row][col] == "#":
                rock_col = col + 1
    for col in range(len(board[0])):
        rock_row = len(board) - 1
        for row in range(len(board)-1, -1, -1):
            if board[row][col] == "O":
                board[row][col] = "."
                board[rock_row][col] = "O"
                rock_row -= 1
            elif board[row][col] == "#":
                rock_row = row - 1
    for row in range(len(board)):
        rock_col = len(board[0]) - 1
        for col in range(len(board[0])-1, -1, -1):
            if board[row][col] == "O":
                board[row][col] = "."
                board[row][rock_col] = "O"
                rock_col -= 1
            elif board[row][col] == "#":
                rock_col = col - 1
    return board

def board_str(board):
    return "".join("".join(line) for line in board)

def board_points(board):
    total = 0
    weight = len(board)
    for line in board:
        total += line.count("O") * weight
        weight -= 1
    return total

def board_total(board):
    total = 0
    for line in board:
        total += line.count("O")
    return total

def print_board(board):
    for line in board:
        print("".join(line))

def part2():
    board = [[c for c in line] for line in data]
    turn = 0
    repeat_idx = None
    board_to_idx = {board_str(board): turn}
    idx_to_board = [board]
    for idx in range(1, 1_000_000_000+1):
        board = cycle(board)
        board_rep = board_str(board)
        if not board_rep in board_to_idx:
            board_to_idx[board_rep] = idx
            idx_to_board.append(board)
        else:
            repeat_idx = board_to_idx[board_rep]
            break
    if repeat_idx is None:
        assert len(idx_to_board) == 1_000_000_000 + 1
        output = board_points(idx_to_board[1_000_000_000])
    else:
        # board idx is the same as board repeat_idx
        last_board_idx = (1_000_000_000 - repeat_idx) % (idx - repeat_idx) + repeat_idx
        output = board_points(idx_to_board[last_board_idx])
    print(output)


part1()
part2()