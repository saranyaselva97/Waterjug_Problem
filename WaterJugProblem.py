import collections

def main():
    start_node = [[0, 0]]
    jugs = get_jugs()
    target_capacity = get_target(jugs)
    check_dict = {}
    search(start_node, jugs, target_capacity, check_dict)

def get_index(node):
    return pow(4, node[0]) * pow(3, node[1])

#Get volume of the jugs
def get_jugs():
    
    jugs = []
    temp = int(input("Enter first jug volume: "))
    while temp < 1:
            temp = int(input("Enter a valid amount (>1): "))       
    jugs.append(temp)
    
    temp = int(input("Enter second jug volume: "))
    while temp < 1:
            temp = int(input("Enter a valid amount (>1): "))     
    jugs.append(temp)
    
    return jugs
    
#**Desired water capacity
def get_target(jugs):
  
    max_capacity = max(jugs[0], jugs[1])
    s = "Desired water capacity : ".format(max_capacity)
    target_capacity = int(input(s))
    while target_capacity < 1 or target_capacity > max_capacity:
        target_capacity = int(input("Enter a valid amount (1 - {0}): ".format(max_capacity)))
        
    return target_capacity

##########
#Check the jugs reached to Target capacity
def is_target(path, target_capacity):
    return path[-1][0] == target_capacity or path[-1][1] == target_capacity

def been_there(node, check_dict):
    print(" {0} is a before visited state ".format(node))
    return check_dict.get(get_index(node), False)

def next_transitions(jugs, path, check_dict):
   
    print("Search next state/ position")
    result = []
    next_nodes = []
    node = []
    
    a_max = jugs[0]
    b_max = jugs[1]
    
    # Start state Jug 01
    a = path[-1][0]  
    # Start state Jug 02
    b = path[-1][1]  

    # 1. Fill 4l/ First jug
    node.append(a_max)
    node.append(b)
    if not been_there(node, check_dict):
        next_nodes.append(node)
    node = []

    # 2. Fill 3l/ Second jug
    node.append(a)
    node.append(b_max)
    if not been_there(node, check_dict):
        next_nodes.append(node)
    node = []

    # 3. 3l to 4l / 2nd jug to 1st jug
    node.append(min(a_max, a + b))
    node.append(b - (node[0] - a))  # b - ( a' - a)
    if not been_there(node, check_dict):
        next_nodes.append(node)
    node = []

    # 4. 4l to 3l / 1st jug to 2nd jug
    node.append(min(a + b, b_max))
    node.insert(0, a - (node[0] - b))
    if not been_there(node, check_dict):
        next_nodes.append(node)
    node = []

    # 5. Empty 4l/ 1st jug
    node.append(0)
    node.append(b)
    if not been_there(node, check_dict):
        next_nodes.append(node)
    node = []

    # 6. Empty 3l/ 2nd jug
    node.append(a)
    node.append(0)
    if not been_there(node, check_dict):
        next_nodes.append(node)


    # Neighbour paths
    for i in range(0, len(next_nodes)):
        temp = list(path)
        temp.append(next_nodes[i])
        result.append(temp)

    if len(next_nodes) == 0:
        print("No unvisited nodes\n\nTurn back")
    else:
        print("Possible states: ")
        for nnode in next_nodes:
            print(nnode)

    return result


def transition(old, new, jugs):
    
    a = old[0]
    b = old[1]
    a_prime = new[0]
    b_prime = new[1]
    a_max = jugs[0]
    b_max = jugs[1]

    if a > a_prime:
        if b == b_prime:
            return "Clear {0}-liter jug:\t\t".format(a_max)
        else:
            return "Pour {0}-liter jug into {1}-liter jug:\t".format(a_max, b_max)
    else:
        if b > b_prime:
            if a == a_prime:
                return "Clear {0}-liter jug:\t\t".format(b_max)
            else:
                return "Pour {0}-liter jug into {1}-liter jug:\t".format(b_max, a_max)
        else:
            if a == a_prime:
                return "Fill {0}-liter jug:\t\t".format(b_max)
            else:
                return "Fill {0}-liter jug:\t\t".format(a_max)


def print_path(path, jugs):
  
    print("Start State :", path[0])
    for i in  range(0, len(path) - 1):
        print(i+1,":", transition(path[i], path[i+1], jugs), path[i+1])




##########

def search(start_node, jugs, target_capacity, check_dict):
    
    target = []
    accomplished = False
    
    q = collections.deque()
    q.appendleft(start_node)
    
    while len(q) != 0:
        path = q.popleft()
        check_dict[get_index(path[-1])] = True
        if len(path) >= 2:
            print(transition(path[-2], path[-1], jugs), path[-1])
        if is_target(path, target_capacity):
            accomplished = True
            target = path
            break

        next_moves = next_transitions(jugs, path, check_dict)
        for i in next_moves:
                q.append(i)

    if accomplished:
        print("\nReached to the Target capacity : Sequence")
        print_path(target, jugs)
    else:
        print("Can't find a solution.")


if __name__ == '__main__':
    main()
