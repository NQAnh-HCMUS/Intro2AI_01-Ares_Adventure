############################
#     HÀM TÌM KIẾM CƠ BẢN  #
############################
import queue
from collections import deque

def validMove(state):
    moves = []
    directions = [('U', 0, -1), ('D', 0, 1), ('L', -1, 0), ('R', 1, 0)]
    for (m, dx, dy) in directions:
        if state.can_move(dx, dy) or state.can_push(dx, dy):
            moves.append(m)
    return moves

def BFSsolution(game):
    print("Processing BFS...")
    start_time = time.time()
    node_generated = 0
    init_state = copy.deepcopy(game)
    visited = set()
    visited.add(tuple(map(tuple, init_state.get_matrix())))
    q = deque()
    q.append(init_state)
    while q:
        if (time.time() - start_time) >= TIME_LIMITED:
            print("Time Out!")
            return ("TimeOut", node_generated)
        cur = q.popleft()
        if cur.is_completed():
            print("BFS found solution:", cur.pathSol)
            return (cur.pathSol, node_generated)
        for mv in validMove(cur):
            new_st = copy.deepcopy(cur)
            node_generated += 1
            if mv == 'U':
                new_st.move(0, -1, False)
            elif mv == 'D':
                new_st.move(0, 1, False)
            elif mv == 'L':
                new_st.move(-1, 0, False)
            elif mv == 'R':
                new_st.move(1, 0, False)
            new_st.pathSol += mv
            mkey = tuple(map(tuple, new_st.get_matrix()))
            if mkey not in visited:
                visited.add(mkey)
                q.append(new_st)
    print("No Solution!")
    return ("NoSol", node_generated)

def DFSsolution(game):
    print("Processing DFS...")
    start_time = time.time()
    node_generated = 0
    stack = [copy.deepcopy(game)]
    visited = set()
    visited.add(tuple(map(tuple, game.get_matrix())))
    
    while stack:
        if time.time() - start_time >= TIME_LIMITED:
            print("Time Out!")
            return ("TimeOut", node_generated)
        
        current_state = stack.pop()
        if current_state.is_completed():
            print("DFS found solution:", current_state.pathSol)
            return (current_state.pathSol, node_generated)
        
        for mv in validMove(current_state):
            new_state = copy.deepcopy(current_state)
            node_generated += 1
            if mv == 'U':
                new_state.move(0, -1, False)
            elif mv == 'D':
                new_state.move(0, 1, False)
            elif mv == 'L':
                new_state.move(-1, 0, False)
            elif mv == 'R':
                new_state.move(1, 0, False)
            new_state.pathSol += mv
            mkey = tuple(map(tuple, new_state.get_matrix()))
            if mkey not in visited:
                visited.add(mkey)
                stack.append(new_state)
    print("No Solution!")
    return ("NoSol", node_generated)

def UCSsolution(game):
    print("Processing UCS...")
    start_time = time.time()
    node_generated = 0
    init_state = copy.deepcopy(game)
    cost_so_far = { tuple(map(tuple, init_state.get_matrix())): 0 }
    frontier = queue.PriorityQueue()
    frontier.put((0, init_state))
    
    while not frontier.empty():
        if time.time() - start_time >= TIME_LIMITED:
            print("Time Out!")
            return ("TimeOut", node_generated)
        
        current_cost, current_state = frontier.get()
        if current_state.is_completed():
            print("UCS found solution:", current_state.pathSol)
            return (current_state.pathSol, node_generated)
        
        for mv in validMove(current_state):
            new_state = copy.deepcopy(current_state)
            node_generated += 1
            if mv == 'U':
                action_cost = new_state.move_with_cost(0, -1, False)
            elif mv == 'D':
                action_cost = new_state.move_with_cost(0, 1, False)
            elif mv == 'L':
                action_cost = new_state.move_with_cost(-1, 0, False)
            elif mv == 'R':
                action_cost = new_state.move_with_cost(1, 0, False)
            new_state.pathSol += mv
            new_key = tuple(map(tuple, new_state.get_matrix()))
            new_total = current_cost + action_cost
            old_cost = cost_so_far.get(new_key, float('inf'))
            if new_total < old_cost:
                cost_so_far[new_key] = new_total
                frontier.put((new_total, new_state))
    print("No Solution!")
    return ("NoSol", node_generated)

def GreedyBestFirstSolution(game):
    print("Processing Greedy Best-first Search...")
    start_time = time.time()
    node_generated = 0
    init_state = copy.deepcopy(game)
    frontier = queue.PriorityQueue()
    frontier.put((get_distance(init_state), init_state))
    visited = set()
    visited.add(tuple(map(tuple, init_state.get_matrix())))
    
    while not frontier.empty():
        if time.time() - start_time >= TIME_LIMITED:
            print("Time Out!")
            return ("TimeOut", node_generated)
        h, current_state = frontier.get()
        if current_state.is_completed():
            print("Greedy Best-first found solution:", current_state.pathSol)
            return (current_state.pathSol, node_generated)
        
        for mv in validMove(current_state):
            new_state = copy.deepcopy(current_state)
            node_generated += 1
            if mv == 'U':
                new_state.move(0, -1, False)
            elif mv == 'D':
                new_state.move(0, 1, False)
            elif mv == 'L':
                new_state.move(-1, 0, False)
            elif mv == 'R':
                new_state.move(1, 0, False)
            new_state.pathSol += mv
            mkey = tuple(map(tuple, new_state.get_matrix()))
            if mkey not in visited:
                visited.add(mkey)
                frontier.put((get_distance(new_state), new_state))
    print("No Solution!")
    return ("NoSol", node_generated)

def SwarmSolution(game):
    print("Processing Swarm Search...")
    start_time = time.time()
    node_generated = 0
    init_state = copy.deepcopy(game)
    g_value = { tuple(map(tuple, init_state.get_matrix())): 0 }
    
    def swarm_heuristic(state):
        return min(get_distance(state), worker_to_box(state))
    
    f_init = g_value[tuple(map(tuple, init_state.get_matrix()))] + swarm_heuristic(init_state)
    frontier = queue.PriorityQueue()
    frontier.put((f_init, init_state))
    visited = set()
    
    while not frontier.empty():
        if time.time() - start_time >= TIME_LIMITED:
            print("Time Out!")
            return ("TimeOut", node_generated)
        cur_f, cur_state = frontier.get()
        if cur_state.is_completed():
            print("Swarm Search found solution:", cur_state.pathSol)
            return (cur_state.pathSol, node_generated)
        mkey = tuple(map(tuple, cur_state.get_matrix()))
        visited.add(mkey)
        for mv in validMove(cur_state):
            new_state = copy.deepcopy(cur_state)
            node_generated += 1
            if mv == 'U':
                action_cost = new_state.move_with_cost(0, -1, False)
            elif mv == 'D':
                action_cost = new_state.move_with_cost(0, 1, False)
            elif mv == 'L':
                action_cost = new_state.move_with_cost(-1, 0, False)
            elif mv == 'R':
                action_cost = new_state.move_with_cost(1, 0, False)
            new_state.pathSol += mv
            new_key = tuple(map(tuple, new_state.get_matrix()))
            if new_key not in visited:
                g_new = g_value[mkey] + action_cost
                g_value[new_key] = g_new
                f_new = g_new + swarm_heuristic(new_state)
                frontier.put((f_new, new_state))
    print("No Solution!")
    return ("NoSol", node_generated)

def ConvergentSwarmSolution(game):
    print("Processing Convergent Swarm Search...")
    start_time = time.time()
    node_generated = 0
    init_state = copy.deepcopy(game)
    g_value = { tuple(map(tuple, init_state.get_matrix())): 0 }
    
    def convergent_heuristic(state):
        return (get_distance(state) + worker_to_box(state)) / 2.0
    
    f_init = g_value[tuple(map(tuple, init_state.get_matrix()))] + convergent_heuristic(init_state)
    frontier = queue.PriorityQueue()
    frontier.put((f_init, init_state))
    visited = set()
    
    while not frontier.empty():
        if time.time() - start_time >= TIME_LIMITED:
            print("Time Out!")
            return ("TimeOut", node_generated)
        cur_f, cur_state = frontier.get()
        if cur_state.is_completed():
            print("Convergent Swarm found solution:", cur_state.pathSol)
            return (cur_state.pathSol, node_generated)
        mkey = tuple(map(tuple, cur_state.get_matrix()))
        for mv in validMove(cur_state):
            new_state = copy.deepcopy(cur_state)
            node_generated += 1
            if mv == 'U':
                action_cost = new_state.move_with_cost(0, -1, False)
            elif mv == 'D':
                action_cost = new_state.move_with_cost(0, 1, False)
            elif mv == 'L':
                action_cost = new_state.move_with_cost(-1, 0, False)
            elif mv == 'R':
                action_cost = new_state.move_with_cost(1, 0, False)
            new_state.pathSol += mv
            new_key = tuple(map(tuple, new_state.get_matrix()))
            if new_key not in visited:
                g_new = g_value[mkey] + action_cost
                g_value[new_key] = g_new
                f_new = g_new + convergent_heuristic(new_state)
                frontier.put((f_new, new_state))
        visited.add(mkey)
    print("No Solution!")
    return ("NoSol", node_generated)


def DijkstraSolution(game):
    print("Processing Dijkstra...")
    start_time = time.time()
    node_generated = 0
    init_state = copy.deepcopy(game)
    cost_so_far = { tuple(map(tuple, init_state.get_matrix())): 0 }
    frontier = queue.PriorityQueue()
    frontier.put((0, init_state))
    while not frontier.empty():
        if (time.time() - start_time) >= TIME_LIMITED:
            print("Time Out!")
            return ("TimeOut", node_generated)
        cur_cost, cur_st = frontier.get()
        if cur_st.is_completed():
            print("Dijkstra found solution:", cur_st.pathSol)
            return (cur_st.pathSol, node_generated)
        for mv in validMove(cur_st):
            new_st = copy.deepcopy(cur_st)
            node_generated += 1
            if mv == 'U':
                action_cost = new_st.move_with_cost(0, -1, False)
            elif mv == 'D':
                action_cost = new_st.move_with_cost(0, 1, False)
            elif mv == 'L':
                action_cost = new_st.move_with_cost(-1, 0, False)
            elif mv == 'R':
                action_cost = new_st.move_with_cost(1, 0, False)
            new_st.pathSol += mv
            new_mkey = tuple(map(tuple, new_st.get_matrix()))
            new_total = cur_cost + action_cost
            old_val = cost_so_far.get(new_mkey, 999999)
            if new_total < old_val:
                cost_so_far[new_mkey] = new_total
                frontier.put((new_total, new_st))
    print("No Solution!")
    return ("NoSol", node_generated)

def AstarSolution(game):
    print("Processing A*...")
    start_time = time.time()
    node_generated = 0
    init_state = copy.deepcopy(game)
    g_value = { tuple(map(tuple, init_state.get_matrix())): 0 }
    def heuristic(st):
        return get_distance(st)
    f_init = heuristic(init_state)
    frontier = queue.PriorityQueue()
    frontier.put((f_init, init_state))
    while not frontier.empty():
        if (time.time() - start_time) >= TIME_LIMITED:
            print("Time Out!")
            return ("TimeOut", node_generated)
        cur_f, cur_st = frontier.get()
        if cur_st.is_completed():
            print("A* found solution:", cur_st.pathSol)
            return (cur_st.pathSol, node_generated)
        mkey = tuple(map(tuple, cur_st.get_matrix()))
        for mv in validMove(cur_st):
            new_st = copy.deepcopy(cur_st)
            node_generated += 1
            if mv == 'U':
                action_cost = new_st.move_with_cost(0, -1, False)
            elif mv == 'D':
                action_cost = new_st.move_with_cost(0, 1, False)
            elif mv == 'L':
                action_cost = new_st.move_with_cost(-1, 0, False)
            elif mv == 'R':
                action_cost = new_st.move_with_cost(1, 0, False)
            new_st.pathSol += mv
            new_mkey = tuple(map(tuple, new_st.get_matrix()))
            g_new = g_value[mkey] + action_cost
            old_val = g_value.get(new_mkey, 999999)
            if g_new < old_val:
                g_value[new_mkey] = g_new
                f_new = g_new + heuristic(new_st)
                frontier.put((f_new, new_st))
    print("No Solution!")
    return ("NoSol", node_generated)
