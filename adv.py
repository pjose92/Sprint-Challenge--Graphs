from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

class Queue():
    def __init__(self):
        self.queue = []

    def enqueue(self, value):
        self.queue.append(value)

    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None

    def size(self):
        return len(self.queue)


class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

# start from room 0
player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
graph = {}
visited = []
currRoom = player.current_room
reverse_direction = {"n": "s", "s": "n", "w": "e", "e": "w"}

# add rooms to the graph 
def add_room(room, graph):
    graph[room.id] = {}
    for exit in room.get_exits():
        graph[room.id][exit] = "?"
        
# get unvisited rooms 
def get_unvisited_exits(room):
    room_id = room.id 
    unvisited_exits = []
    # add directions each room to graph
    exits = room.get_exits() #should return a lists of exists
    #loop through exits
    for exit in exits:
        if graph[room_id][exit] == "?":
            unvisited_exits.append(exit)
    return unvisited_exits

def create_graph_recursive(room, graph, visited):
    # check if the room is in the graph
    if room.id not in graph:
        add_room(room, graph)
        # append the visited room order to visited
        visited.append(room.id)
    # get unvisited exits
    unvisited_exits = get_unvisited_exits(room)
    if len(unvisited_exits) > 0:
        # loop through unvisited exits
        for exit in unvisited_exits:
            # get the new room of that direction
            new_room = room.get_room_in_direction(exit)
            # add the new room to graph if it's not in yet
            if new_room.id not in graph:
                add_room(new_room, graph)
                visited.append(new_room.id)
            # get the reverse exit
            reverse_exit = reverse_direction[exit]
            # update graph
            graph[room.id][exit] = new_room.id
            graph[new_room.id][reverse_exit] = room.id
            create_graph_recursive(new_room, graph, visited)
    if len(graph) == len(room_graph):
        return graph, visited

def bfs(starting_room, destination_room, graph):
    visited = set()
    #two queues, path to rooms and another for direction with movements
    room_queue = Queue()
    dir_queue = Queue()
    room_queue.enqueue([starting_room])
    dir_queue.enqueue([])
    
    #room queue determines bfs
    while room_queue.size() > 0:
        room_path = room_queue.dequeue()
        # take the next direction to travel in the queue
        dir_path = dir_queue.dequeue()
        last_room = room_path[-1]
        if last_room not in visited:
            visited.add(last_room)
            # we found our shortest path between 2 rooms
            if last_room == destination_room:
                return dir_path
            for direction in graph[last_room]:
                # add direction to both queues
                new_room_path = room_path + [graph[last_room][direction]]
                new_dir_path = dir_path + [direction]
                room_queue.enqueue(new_room_path)
                dir_queue.enqueue(new_dir_path)

room_graph, room_visited = create_graph_recursive(currRoom, graph, visited)

# for each room in the visited list
for i in range(len(room_visited) -1):
    #bfs to find shoertest path btween two rooms
    path = bfs(room_visited[i], room_visited[i+1], graph)
    #add path navigation between two rooms to traversal path
    traversal_path.extend(path)

# # print(f"hello im GRAPH: ", graph)
# print(f"Hello i am visited rooms: ", room_visited)
# print(f"Hello i am traversal path: ", traversal_path)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
