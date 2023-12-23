import heapq
import random

class PuzzleAStar15:
    def __init__(self, initial_state, goal_state="7eb58cda2x4f6391"):
        self.state = initial_state
        self.goal_state = goal_state

    def get_successors(self, state):
        successors = []
        zero_index = state.index('x')
        row, col = zero_index // 4, zero_index % 4

        directions = [('up', -1, 0), ('down', 1, 0), ('left', 0, -1), ('right', 0, 1)]
        for direction, row_change, col_change in directions:
            new_row, new_col = row + row_change, col + col_change
            if 0 <= new_row < 4 and 0 <= new_col < 4:
                new_zero_index = new_row * 4 + new_col
                new_state = list(state)
                new_state[zero_index], new_state[new_zero_index] = new_state[new_zero_index], 'x'
                successors.append(''.join(new_state))

        return successors

    def is_goal(self, state):
        return state == self.goal_state

    def heuristic(self, state):
        # 這裡可以根據需要選擇合適的啟發式函數
        return sum([1 if state[i] != self.goal_state[i] else 0 for i in range(16)])

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

def a_star_search(puzzle, start):
    if not is_solvable(start, puzzle.goal_state):
        return None

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}
    visited_states = set([start])

    while frontier:
        current_priority, current_state = heapq.heappop(frontier)

        if puzzle.is_goal(current_state):
            return reconstruct_path(came_from, current_state)

        for next_state in puzzle.get_successors(current_state):
            if next_state in visited_states:
                continue

            new_cost = cost_so_far[current_state] + 1
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + puzzle.heuristic(next_state)
                heapq.heappush(frontier, (priority, next_state))
                came_from[next_state] = current_state
                visited_states.add(next_state)

    return None

def reconstruct_path(came_from, end):
    path = []
    while end is not None:
        path.append(end)
        end = came_from[end]
    path.reverse()
    return path

def generate_random_state(base_state):
    state_list = list(base_state)
    random.shuffle(state_list)
    return ''.join(state_list)

# 使用示例
base_state = "7eb58cda2x4f6391"
start_state = generate_random_state(base_state)
print("Start state:", start_state)
puzzle = PuzzleAStar15(start_state)
solution = a_star_search(puzzle, start_state)

if solution:
    print("Solution found in {} steps:".format(len(solution) - 1))
    for state in solution:
        for i in range(0, 16, 4):
            print(state[i:i+4])
        print()
else:
    print("No solution found or the puzzle is unsolvable.")
