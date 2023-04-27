import random
class Node
    def __init__(self, name, heuristic_value):
        self.name = name
        self.heuristic_value = heuristic_value
        self.times_expanded = 0
        self.tuple = []

    # a function to add a tuple to the node
    def add_tuple(self, tuple):
        self.tuple.append(tuple)

    # a function to increase the times_expanded variable by one
    def increase_expanded(self):
        self.times_expanded += 1

    # a function to get a random tuple from the node
    def get_random_tuple(self):
        # get the number of tuples in the node
        num_tuples = len(self.tuple)
        # get a random number between 0 and the number of tuples
        random_num = random.randint(0, num_tuples-1)
        # return the first and second element of the tuple
        return self.tuple[random_num][0], self.tuple[random_num][1]

    # a function to get the name of a tuple from the node
    def get_name_tuple(self, index):
        return self.tuple[index][0]

    # a function to get the heuristic value of the node
    def get_heuristic_value():
        return self.heuristic_value
        
    # a function to print the node
    def print_node(self):
        print(self.name, self.heuristic_value, self.times_expanded, self.tuple)

    # a function to erase a tuple from the node
    def erase_tuple(self, name):
        # if the first element of the tuple is the name we want to erase, we erase it
        for t in self.tuple:
            if t[0].name == name:
                self.tuple.remove(t)
                break
    
# a function to read the input from a file
def read_input():
    # open the file
    with open('input.txt') as f:
        nodes=[]
        lines = f.readlines()
        for line in lines:
            # check the first 5 characters of the line
            if line[0:5] == 'Init:':
                # get the second word of the line that is separated by 1 space
                initial_state = line.split()[1]
            elif line[0:5] == 'Goal:':
                goal_state = line.split()[1]
            # if there are 2 arguments, create a node with both arguments
            elif len(line.split()) == 2:
                name=line.split()[0]
                heuristic_value=int(line.split()[1])
                node = Node(name, heuristic_value)
                nodes.append(node)
            elif len(line.split()) == 3:
                # get the node that has the same name as the first argument
                for n in nodes:
                    if n.name == line.split()[0]:
                        node = n
                # get the node that has the same name as the second argument
                for n in nodes:
                    if n.name == line.split()[1]:
                        second_node = n
                # add the tuple to the node
                node.add_tuple((second_node, int(line.split()[2])))
        # get the node that has the same name as the initial state
        for n in nodes:
            if n.name == initial_state:
                initial_state = n
        # return the initial state, goal state, and the list of nodes
        return initial_state, goal_state, nodes
    
# a function to print the nodes
def print_nodes(nodes):
    for n in nodes:
        print(n.name, n.heuristic_value, n.tuple)

def first_depth_search(nodes, initial_state, goal_state):
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


# Define a function called uniform_cost_search that takes in three arguments: nodes, initial_state, and goal_state.
def uniform_cost_search(nodes, initial_state, goal_state):
    # Create a node called finish that has the name as "finish"
    finish = Node("finish", 0)
    # Create a queue and add the initial state, its travel value, and the finish node as a tuple to the queue.
    queue = [(initial_state,0,finish)]
    # Create an empty list called best_route
    best_route = []
    # Loop while the queue is not empty
    while queue:
        # Pop the first tuple in the queue and set the current node, travel value, and parent node to their respective values.
        current_node, travel_value, parent_node = queue.pop(0)
        # Check if the current node is already in the best_route list
        for n in best_route:
            if n[0].name == current_node.name:
                # Remove the current node from best_route if it is already in the list.
                best_route.remove(n)
                break
        # Add the current node, its travel value, and its parent node as a tuple to the best_route list.
        best_route.append((current_node, travel_value, parent_node))
        # Check if the current node is the goal state
        if current_node.name == goal_state:
            # If the current node is the goal state, print "Goal state found" and break out of the while loop.
            print("Goal state found")
            break
        # Increase the number of times the current node has been expanded.
        current_node.increase_expanded()
        # Loop through each tuple in the current node's tuple list
        for n in current_node.tuple:
            # Calculate the accumulated cost for the current node and its neighbor node
            accumulated_cost = travel_value + n[1]
            # Append the neighbor node, its accumulated cost, and the current node to the queue
            queue.append((n[0], accumulated_cost, current_node))
            # Check if the neighbor node is already in the queue and if it has a higher accumulated cost.
            for q in queue:
                if q[0].name == n[0].name and q[1] >= accumulated_cost:
                    # If the neighbor node is already in the queue and has a higher accumulated cost, remove it from the queue and append it with its new cost and current node.
                    queue.remove(q)
                    queue.append((n[0], accumulated_cost, current_node))
                    break
        # Sort the queue based on the accumulated cost of each node.
        queue.sort(key=lambda x: x[1])
    # Create an empty list called path.
    path=[]
    # Set the current node to the goal state.
    current_node = goal_state
    # Loop while True
    while True:
        # Loop through each tuple in the best_route list
        for n in best_route:
            if n[0].name == current_node:
                # If the name of the current node matches the name of a node in the best_route list, append the tuple to the path list and set the current node to the parent node's name.
                path.append(n)
                current_node = n[2].name
        # Check if the current node is "finish"
        if current_node == "finish":
            # If the current node is "finish", break out of the while loop.
            break
    # Reverse the order of the path list.
    path.reverse()
    # Print "Path from initial state to goal state:"
    for n in path:
        print(f'{n[0].name}')
    nodes_expanded=[]
    for n in nodes:
        #check if the node name is in the nodes_expanded list
        if n.name in nodes_expanded:
            #increase the times expanded of the node that has the same name as the node in the nodes_expanded list
            for n2 in nodes:
                if n2.name == n.name:
                    n2.increase_expanded()
        else:
            #if the node name is not in the nodes_expanded list, add it
            nodes_expanded.append(n.name)
    #print the number of nodes expanded for each node
    print("Number of nodes expanded for each node: ")
    for n in nodes:
        print(f'{n.name} Expanded: {n.times_expanded}')

    #check the total number of nodes expanded
    print(f'Total number of nodes expanded: {sum(n.times_expanded for n in nodes)}')
    print("Cost: ", path[-1][1])

def Greedy_Best_First_Search(nodes, initial_state, goal_state):
    # Initialize cost and stack with initial state
    cost=0
    stack=[initial_state]
    
    # Loop until stack is empty
    while stack:
        # Get node with smallest heuristic value and update variables
        current_node = get_smallest_node_by_heuristic_value(stack[-1])
        heuristic_value = current_node.heuristic_value
        stack[-1].increase_expanded()
        cost += heuristic_value
        stack.append(current_node)
        
        # Check if goal state is reached and break if true
        if stack[-1].name == goal_state:
            print("Goal state found")
            break
        
        # Check if current node has no neighbors and backtrack if true
        if len(stack[-1].tuple)==0:
            last_node_name=stack[-1].name
            stack.pop()
            for tp in stack[-1].tuple:
                if tp[0].name == last_node_name:
                    cost -= tp[0].heuristic_value
                    stack[-1].erase_tuple(last_node_name)
                    print(stack[-1].tuple)
                    break
    #print the stack
    print("Path from initial state to goal state: ")
    for n in stack:
        print(f'{n.name}')
    print("Number of nodes expanded for each node: ")
    for n in nodes:
        print(f'{n.name} Expanded: {n.times_expanded}')
    print(f'Total number of nodes expanded: {sum(n.times_expanded for n in nodes)}')
    print("Cost: ", cost)
    
    # while stack:

def get_heuristic(node):
    return node[0].heuristic_value

def get_smallest_node_by_heuristic_value(node):
    tuples=[]
    for i in range(len(node.tuple)):
        tuples.append(node.tuple[i])  
    smallest_node= min(tuples,key=get_heuristic)
    return smallest_node[0]

#Define a function named A_star_search that takes in three parameters - nodes, initial_state, and goal_state.
def A_star_search(nodes, initial_state, goal_state):
    #Create a node called finish that has the name as "finish"
    finish = Node("finish", 0)
    #Create a list called queue with a tuple containing initial_state, 0, and finish as its elements.
    queue = [(initial_state,0,finish)]
    #Create an empty list called best_route.
    best_route = []
    #Start a while loop that runs as long as queue is not empty.
    while queue:
        #Pop the first element of queue and assign the values to current_node, travel_value, and parent_node respectively.
        current_node, travel_value, parent_node = queue.pop(0)
        #Start a loop that goes through all the elements in best_route.
        for n in best_route:
            #If the name of the node at index 0 of n is the same as the name of the current_node, remove that element from best_route.
            if n[0].name == current_node.name:
                best_route.remove(n)
                break
        #Append a tuple of current_node, travel_value, and parent_node to best_route.
        best_route.append((current_node, travel_value, parent_node))
        #If the name of the current_node is the same as the goal_state, print "Goal state found" and break out of the loop.
        if current_node.name == goal_state:
            print("Goal state found")
            break
        #Increase the expanded counter of current_node by 1.
        current_node.increase_expanded()
        #Start a loop that goes through all the elements in the tuple attribute of current_node.
        for n in current_node.tuple:
            #Calculate the accumulated cost using the formula provided and assign it to acumulated_cost.
            acumulated_cost = travel_value + n[1] + n[0].heuristic_value-current_node.heuristic_value
            #Append a tuple of n[0], acumulated_cost, and current_node to queue.
            queue.append((n[0], acumulated_cost, current_node))
            #Start a loop that goes through all the elements in queue.
            for q in queue:
                #If the name of the node at index 0 of q is the same as the name of n[0] and the value at index 1 of q is greater than or equal to acumulated_cost,
                if q[0].name == n[0].name and q[1] >= acumulated_cost:
                    #remove that element from queue and append a tuple of n[0], acumulated_cost, and current_node to queue.
                    queue.remove(q)
                    queue.append((n[0], acumulated_cost, current_node))
                break
        #Sort queue by the second element of each tuple in ascending order.
        queue.sort(key=lambda x: x[1])

    #print the answer
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
    acumulated_heuristic_value = 0
    for n in path:
        print(f'{n[0].name}')
        acumulated_heuristic_value += n[0].heuristic_value
    print("Number of nodes expanded for each node: ")
    for n in nodes:
        print(f'{n.name} Expanded: {n.times_expanded}')
    #check the total number of nodes expanded
    print(f'Total number of nodes expanded: {sum(n.times_expanded for n in nodes)}')
    print("Cost: ", path[-1][1]+10)


def main():
    nodes=[]
    initial_state, goal_state, nodes = read_input()
    print("First Depth Search (random):")
    first_depth_search(nodes, initial_state, goal_state)
    initial_state, goal_state, nodes = read_input()

    print("\nUniform Cost Search:")
    uniform_cost_search(nodes, initial_state, goal_state)
    initial_state, goal_state, nodes = read_input()

    print("\nGreedy:")
    Greedy_Best_First_Search(nodes, initial_state, goal_state)
    initial_state, goal_state, nodes = read_input()

    print("\nA* Search:")
    A_star_search(nodes, initial_state, goal_state)
if __name__ == "__main__":
    main()