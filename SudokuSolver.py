import copy
# Node class. Includes methods for the constructor, __eq__, __repr__ , and get_f
class Node:
    def __init__(self, s = [], g = None, h = None, p = None):
        self.lst = s
        self.g = g
        self.p = p
        self.h = h

    def __eq__(self, other):
        if(type(other) != Node):
            return False
        if (self.lst == other.lst):
            return True
        else:
            return False

    def __repr__(self):
        return repr(self.lst) + "\n"

    def get_f(self):
        if(self.g != None and self.h != None):
             return (self.g + self.h)
        else:
            return 0

# Loops through two board states and checks if the value at each index on both boards are equal. If they are not
# then calculate the absolute distance from the x and y coordinates and add that to the manhattan distance
def calculate_man_distance(lst1, lst2):
    man_distance = 0
    for i in range(4):
        for j in range (4):
            if (lst1[i][j] == lst2[i][j]):
                continue
            else:
                for x in range(4):
                    for y in range(4):
                        if(lst1[i][j] == lst2[x][y]):
                            man_distance += abs(x - i) + abs (y - j)
                            break
    return man_distance

# Opens the desired file, creates two Nodes for initial and goal states that includes a list of the state
def get_state_space(filename):
    inputFile = open(filename, "r")
    init_state = Node([], 0, None, None)
    goal_state = Node([], None, 0, None)
    for i in range(9):
        next_line = inputFile.readline()
        if 0 <= i <= 3:
            init_state.lst.append(next_line.strip().split(" "))
        elif i >= 5:
            goal_state.lst.append(next_line.strip().split(" "))
        else:
            continue
    init_state.h = calculate_man_distance(init_state.lst, goal_state.lst)
    state_space = [goal_state, init_state]
    return state_space

# Takes a list and returns the coordinates of Zero
def locate_zero(lst):
    row = -1
    col = -1
    for i in range(4):
        for j in range(4):
            if (lst[i][j] == '0'):
                row = i
                col = j
                return (row, col)

# Determines what possible moves can be made on a board
def find_moves(curr_state):
    moves_lst = []
    zero_coords = locate_zero(curr_state.lst)
    if (zero_coords[1] != 0 and zero_coords[1] != 3):
        moves_lst.append('L')
        moves_lst.append('R')
    elif (zero_coords[1] != 0):
        moves_lst.append('L')
    else:
        moves_lst.append('R')
    if(zero_coords[0] != 0 and zero_coords[0] != 3):
        moves_lst.append('U')
        moves_lst.append('D')
    elif(zero_coords[0] != 3):
        moves_lst.append('D')
    else:
        moves_lst.append('U')
    return moves_lst

# Takes the current state, and creates a child node after conducting the move give in the parameter. Returns None
# if the move creates a node that was already visited
def create_child(curr_state, move, goal_state, old_states):
    newlst = copy.deepcopy(curr_state.lst)
    zero_coords = locate_zero(curr_state.lst)
    if (move == 'U'):
        newlst[zero_coords[0]][zero_coords[1]], newlst[(zero_coords[0] - 1)][zero_coords[1]] = newlst[(zero_coords[0] - 1)][zero_coords[1]], newlst[zero_coords[0]][zero_coords[1]]
    elif (move == 'L'):
        newlst[zero_coords[0]][zero_coords[1]], newlst[zero_coords[0]][(zero_coords[1] - 1)] = newlst[zero_coords[0]][(zero_coords[1] - 1)], newlst[zero_coords[0]][zero_coords[1]]
    elif (move == 'D'):
        newlst[zero_coords[0]][zero_coords[1]], newlst[(zero_coords[0] + 1)][zero_coords[1]] = newlst[(zero_coords[0] + 1)][zero_coords[1]], newlst[zero_coords[0]][zero_coords[1]]
    else:
        newlst[zero_coords[0]][zero_coords[1]], newlst[zero_coords[0]][(zero_coords[1] + 1)] = newlst[zero_coords[0]][( zero_coords[1] + 1)], newlst[zero_coords[0]][zero_coords[1]]
    if newlst in old_states:
        return None
    h = calculate_man_distance(newlst, goal_state.lst)
    return Node(newlst, curr_state.g + 1, h, curr_state)

# Takes in an initial state and a goal state and returns a tuple containing the node equaling goal state that was
# found by the function, and the number of nodes created.
def solve(curr_state, goal_state):
    visited_list = []
    new_states = []
    new_states.append(curr_state)
    nodes_visited = 1
    # Continue looping until we find the goal node, or until there are no more unique states left
    while len(new_states) > 0:
        curr_node = new_states[0]
        curr_index = 0
        # Checks all f values and assigns current node to the node in the list with the smallest f value
        for index, item in enumerate(new_states):
            if item.get_f() < curr_node.get_f():
                curr_node = item
                curr_index = index
        moves_lst = find_moves(curr_node)
        # Get rid of node after expanding on it, and append it to visited nodes
        new_states.pop(curr_index)
        visited_list.append(curr_node)
        if curr_node == goal_state:
            return (curr_node, nodes_visited)
        # Create new nodes for each possible move the current node can take
        for i in range(len(moves_lst)):
            new_child = create_child(curr_node, moves_lst[i], goal_state, visited_list)
            if new_child != None:
                new_states.append(new_child)
                nodes_visited += 1

# Takes a node and its parent, and returns the move taken by the parent to reach the node
def move_taken(node, parent):
    node_zero = locate_zero(node.lst)
    parent_zero = locate_zero(parent.lst)
    if parent_zero[0] == node_zero[0]:
        if parent_zero[1] < node_zero[1]:
            return 'R'
        else:
            return 'L'
    else:
        if parent_zero[0] < node_zero[0]:
            return 'D'
        else:
            return 'U'

# Returns the sequence of moves and f values of all nodes along the solution path
def get_move_seq_and_f_vals(node):
    sequence = []
    f_vals = []
    while(node.p != None):
        sequence.insert(0, move_taken(node, node.p))
        f_vals.insert(0, node.get_f())
        node = node.p
    f_vals.insert(0, node.get_f())
    return (sequence, f_vals)


def main():
    filename = str(input("Enter the name of the input file: "))
    state_space = get_state_space(filename)
    i_state = state_space[1]
    g_state = state_space[0]
    solved_tup = solve(i_state, g_state)
    nodes_visited = solved_tup[1]
    solution_node = solved_tup[0]
    move_seq_and_f_vals = get_move_seq_and_f_vals(solution_node)
    outputfile = open("output.txt", "w")
    inputfile = open(filename, "r")
    for i in range(9):
        nextline = inputfile.readline()
        outputfile.write(nextline)
    outputfile.write("\n")
    outputfile.write(str(solution_node.g) + '\n')
    outputfile.write(str(nodes_visited) + '\n')
    s = ""
    s1 = ""
    for elem in move_seq_and_f_vals[0]:
        s += elem + " "
    outputfile.write(s + "\n")
    for elem in move_seq_and_f_vals[1]:
        s1 += str(elem) + " "
    outputfile.write(s1)


main()
