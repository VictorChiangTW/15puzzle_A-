import heapq

class PuzzleAStar15:
    def __init__(self, initial_state):
        self.state = initial_state
        self.goal_state = "7eb58cda2x4f6391"  # 15-puzzle 的目標狀態

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
        return sum([1 if state[i] != self.goal_state[i] else 0 for i in range(16)])

def is_solvable(state):
    sequence = [c for c in state if c != 'x']
    inversions = sum(sequence[i] > sequence[j] for i in range(len(sequence)) for j in range(i + 1, len(sequence)))

    row_from_bottom = 4 - (state.index('x') // 4)
    return (inversions + row_from_bottom) % 2 == 0

def a_star_search(puzzle, start):
    if not is_solvable(start):
        return None

    frontier = []
    heapq.heappush(frontier, (0, start))
    came_from = {start: None}
    cost_so_far = {start: 0}

    while frontier:
        current_priority, current_state = heapq.heappop(frontier)

        if puzzle.is_goal(current_state):
            return reconstruct_path(came_from, current_state)

        for next_state in puzzle.get_successors(current_state):
            new_cost = cost_so_far[current_state] + 1
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost + puzzle.heuristic(next_state)
                heapq.heappush(frontier, (priority, next_state))
                came_from[next_state] = current_state

    return None

def reconstruct_path(came_from, end):
    path = []
    while end is not None:
        path.append(end)
        end = came_from[end]
    path.reverse()
    return path

# 使用示例
puzzle = PuzzleAStar15("7eb58cdax24f6391")
solution = a_star_search(puzzle, puzzle.state)

if solution:
    print("Solution found in {} steps:".format(len(solution) - 1))
    for state in solution:
        for i in range(0, 16, 4):
            print(state[i:i+4])
        print()
else:
    print("No solution found or the puzzle is unsolvable.")
