import random

class PuzzleIDS:
    def __init__(self, initial_state, goal_state="7eb58cda2x4f6391"):
        self.initial_state = initial_state
        self.goal_state = goal_state

    def get_successors(self, state, last_move=None):
        successors = []
        zero_index = state.index('x')
        row, col = zero_index // 4, zero_index % 4

        # 新增一個映射，以防止重複的移動
        opposite_moves = {'up': 'down', 'down': 'up', 'left': 'right', 'right': 'left'}

        directions = [('up', -1, 0), ('down', 1, 0), ('left', 0, -1), ('right', 0, 1)]
        for direction, row_change, col_change in directions:
            if last_move and direction == opposite_moves[last_move]:
                continue  # 跳過將拼圖恢復到前一狀態的移動

            new_row, new_col = row + row_change, col + col_change
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_zero_index = new_row * 4 + new_col
                new_state = list(state)
                new_state[zero_index], new_state[new_zero_index] = new_state[new_zero_index], 'x'
                successors.append((''.join(new_state), direction))
        return successors

    def is_goal(self, state):
        return state == self.goal_state

def get_index_map(goal_state):
    return {char: index for index, char in enumerate(goal_state)}

def count_inversions(state, index_map):
    sequence = [c for c in state if c != 'x']
    mapped_sequence = [index_map[c] for c in sequence]
    inversions = sum(mapped_sequence[i] > mapped_sequence[j] for i in range(len(mapped_sequence)) for j in range(i + 1, len(mapped_sequence)))
    return inversions

def is_solvable(state, goal_state):
    index_map = get_index_map(goal_state)
    inversions = count_inversions(state, index_map)
    row_from_bottom = 4 - (state.index('x') // 4)
    return (inversions + row_from_bottom) % 2 == 0

def generate_random_state(base_state):
    while True:
        state_list = list(base_state)
        random.shuffle(state_list)
        random_state = ''.join(state_list)
        if is_solvable(random_state, base_state):
            return random_state

def depth_limited_search(puzzle, limit):
    def recursive_dls(node, depth, visited, last_move=None):
        if puzzle.is_goal(node):
            return [node]
        elif depth == 0:
            return None
        else:
            visited.add(node)
            for child, direction in puzzle.get_successors(node, last_move):
                if child in visited:
                    continue
                result = recursive_dls(child, depth - 1, visited, direction)
                if result is not None:
                    return [node] + result
            return None

    return recursive_dls(puzzle.initial_state, limit, set())

def iterative_deepening_search(puzzle):
    depth = 0
    while True:
        result = depth_limited_search(puzzle, depth)
        if result is not None:
            return result
        depth += 1

# 使用示例
base_state = "7eb58cda2x4f6391"
start_state = generate_random_state(base_state)
print("Start state:", start_state)
puzzle = PuzzleIDS(start_state)
solution = iterative_deepening_search(puzzle)

if solution:
    print("Solution found in {} steps:".format(len(solution) - 1))
    for state in solution:
        for i in range(0, 16, 4):
            print(state[i:i+4])
        print()
else:
    print("No solution found or the puzzle is unsolvable.")
