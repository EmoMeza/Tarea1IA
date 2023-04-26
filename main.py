import random
class Node:
    def __init__(self, name, heuristic_value):
        self.name = name
        self.heuristic_value = heuristic_value
        self.times_expanded = 0
        self.tuple = []

    def add_tuple(self, tuple):
        self.tuple.append(tuple)

    def increase_expanded(self):
        self.times_expanded += 1
    def get_random_tuple(self):
        #we get the number of tuples in the node
        num_tuples = len(self.tuple)
        #we get a random number between 0 and the number of tuples
        random_num = random.randint(0, num_tuples-1)
        return self.tuple[random_num][0], self.tuple[random_num][1]

    def get_name_tuple(self, index):
        return self.tuple[index][0]
        
    def print_node(self):
        print(self.name, self.heuristic_value, self.times_expanded, self.tuple)
    def erase_tuple(self, name):
        #if the first element of the tuple is the name we want to erase, we erase it
        for t in self.tuple:
            if t[0] == name:
                self.tuple.remove(t)
                break
    
def read_input():
    with open('input.txt') as f:
        nodes=[]
        lines = f.readlines()
        for line in lines:
            #check the first 5 characters of the line
            if line[0:5] == 'Init:':
                #get the second word of the line that is separated by 1 space
                initial_state = line.split()[1]
            elif line[0:5] == 'Goal:':
                goal_state = line.split()[1]
            #if theres 2 arguments, create a node with both arguments
            elif len(line.split()) == 2:
                name=line.split()[0]
                heuristic_value=int(line.split()[1])
                node = Node(name, heuristic_value)
                nodes.append(node)
            elif len(line.split()) == 3:
                #get the node that has the same name as the first argument
                for n in nodes:
                    if n.name == line.split()[0]:
                        node = n
                #get the node that has the same name as the second argument
                for n in nodes:
                    if n.name == line.split()[1]:
                        second_node = n
                #add the tuple to the node
                node.add_tuple((second_node, int(line.split()[2])))
        return initial_state, goal_state, nodes
    
def print_nodes(nodes):
    for n in nodes:
        print(n.name, n.heuristic_value, n.tuple)

def random_depth_search(nodes, initial_state, goal_state):
    rds=[]
    rds=nodes
    cost=0
    #get the node that has the same name as the initial state
    stack = [initial_state]
    while stack:
        #get a random node from the tuple of the last node in the stack
        current_node, travel_value = stack[-1].get_random_tuple()
        stack[-1].increase_expanded()
        #increase the cost with the travel value
        cost += travel_value
        #add it to the stack
        stack.append(current_node)
        #check if the last node in the stack is the goal state
        if stack[-1].name == goal_state:
            print("Goal state found")
            break
        if len(stack[-1].tuple) == 0:
            #remove the last node from the stack
            last_node_name = stack[-1].name
            stack.pop()
            for t in stack[-1].tuple:
                if t[0] == last_node_name:
                    cost -= t[1]
            stack[-1].erase_tuple(last_node_name)
            #decrease the cost with the value of the second element of the tuple that has as first element the last node
            
    #print the stack
    print("Path from initial state to goal state: ")
    for n in stack:
        print(n.name)
    print("Number of nodes expanded for each node: ")
    for n in rds:
        print(f'{n.name} Expanded: {n.times_expanded}')
    print(f'Total number of nodes expanded: {sum(n.times_expanded for n in nodes)}')
    print("Cost: ", cost)

def uniform_cost_search(nodes, initial_state, goal_state):
    #create a node called finish that has the name as "finish"
    finish = Node("finish", 0)
    queue = [(initial_state,0,finish)]
    best_route = []
    while queue:
        current_node, travel_value, parent_node = queue.pop(0)
        for n in best_route:
            if n[0].name == current_node.name:
                best_route.remove(n)
                break
        best_route.append((current_node, travel_value, parent_node))
        if current_node.name == goal_state:
            print("Goal state found")
            break
        current_node.increase_expanded()
        for n in current_node.tuple:
            acumulated_cost = travel_value + n[1]
            queue.append((n[0], acumulated_cost, current_node))
            for q in queue:
                if q[0].name == n[0].name and q[1] >= acumulated_cost:
                    queue.remove(q)
                    queue.append((n[0], acumulated_cost, current_node))
                    break
        queue.sort(key=lambda x: x[1])
    path=[]
    current_node = goal_state
    while True:
        for n in best_route:
            if n[0].name == current_node:
                path.append(n)
                current_node = n[2].name
        if current_node == "finish":
            break
    path.reverse()
    print("Path from initial state to goal state: ")
    for n in path:
        print(f'{n[0].name} Expanded: {n[0].times_expanded}')
    #check the total number of nodes expanded
    print(f'Total number of nodes expanded: {sum(n.times_expanded for n in nodes)}')
    print("Cost: ", path[-1][1])

# def Greedy_Best_First_Search(nodes, initial_state, goal_state):        

def main():
    nodes=[]
    initial_state, goal_state, nodes = read_input()
    for n in nodes:
        if n.name == initial_state:
            initial_state = n
    #get initial state and goal state nodes
    print("First Depth Search (random):")
    random_depth_search(nodes, initial_state, goal_state)
    print("Uniform Cost Search:")
    uniform_cost_search(nodes, initial_state, goal_state)

if __name__ == "__main__":
    main()