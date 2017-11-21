from random import randint

#====================ROBOT SETTINGS================
GEN_SIZE = 9 #Genome size
FUNC_NUM = 6 #<= 6 for now
wallhitweight = 1
mdweight = 100
stepweight = 1
#==================================================

class maze():
    def __init__(self,default_maze):
        self.map = []
        if default_maze == 0:
            self.map.append(['#', '#', '#', '#', '#', '#', '#'])
            self.map.append(['s', ' ', '#', ' ', ' ', ' ', '#'])
            self.map.append(['#', ' ', '#', ' ', '#', ' ', 'e'])
            self.map.append(['#', ' ', ' ', ' ', ' ', ' ', '#'])
            self.map.append(['#', '#', '#', '#', '#', '#', '#'])
        elif default_maze == 1:
            self.map.append(['#', '#', '#', '#', '#', '#', '#'])
            self.map.append(['s', ' ', '#', ' ', ' ', ' ', '#'])
            self.map.append(['#', ' ', '#', ' ', '#', ' ', 'e'])
            self.map.append(['#', ' ', '#', ' ', '#', ' ', '#'])
            self.map.append(['#', ' ', '#', ' ', '#', ' ', '#'])
            self.map.append(['#', ' ', '#', ' ', '#', ' ', '#'])
            self.map.append(['#', ' ', '#', ' ', '#', ' ', '#'])
            self.map.append(['#', ' ', ' ', ' ', '#', ' ', '#'])
            self.map.append(['#', '#', '#', '#', '#', '#', '#'])
        elif default_maze == 2:
            self.map.append(['#', '#', '#', '#', '#', '#', '#'])
            self.map.append(['s', ' ', ' ', ' ', '#', ' ', '#'])
            self.map.append(['#', '#', '#', ' ', '#', ' ', 'e'])
            self.map.append(['#', ' ', ' ', ' ', '#', ' ', '#'])
            self.map.append(['#', ' ', ' ', ' ', '#', ' ', '#'])
            self.map.append(['#', ' ', '#', '#', '#', ' ', '#'])
            self.map.append(['#', ' ', ' ', ' ', '#', ' ', '#'])
            self.map.append(['#', '#', '#', ' ', '#', ' ', '#'])
            self.map.append(['#', ' ', ' ', ' ', '#', ' ', '#'])
            self.map.append(['#', ' ', '#', '#', '#', ' ', '#'])
            self.map.append(['#', ' ', ' ', ' ', '#', ' ', '#'])
            self.map.append(['#', '#', '#', ' ', '#', ' ', '#'])
            self.map.append(['#', ' ', ' ', ' ', ' ', ' ', '#'])
            self.map.append(['#', '#', '#', '#', '#', '#', '#'])

        self.starting_point = [1, 0]  # x katakorifo y orizontio
        self.finishing_point = [2, 6]
        self.threshold = (self.starting_point[0] - self.finishing_point[0]) / 2 #Calculating threshold

    def printmaze(self,robopos):

        for it in range(len(self.map)):    #For x pos
            for it2 in range(len(self.map[it])): #For y pos
                if robopos == [it,it2]:
                    print("R",end="  ")  #Print the robot
                else:
                    print(self.map[it][it2], " ", end="")
            print("\n", end="")




        return

    def get_threshold(self):  #Getter for threshold
        return self.threshold



class robot:
    def __init__(self,maze): #Initialization requires a valid map
        self.maze = maze
        self.cur_pos = maze.starting_point #that has a starting point
        self.end_pos = maze.finishing_point #And an ending point
        self.steps = 0
        self.collisions = 0
        self.maze = maze.map
        self.last_bad_move = None #Documenting last bad move
        self.terminals = ["U","D","F","B"] #Basic terminals
        self.threshold = maze.get_threshold   #Getting threshold from maze
        self.genome = [] #Dynamic Genome vessel
        self.available_functions = FUNC_NUM #Number of available functions
        self.fitness = 100000 #Robot's individual fitness


        #Initial genome creation====================
        for it in range(0, GEN_SIZE): #Generating the robot's genome
            self.genome.append(randint(1,self.available_functions))
        self.genome_length = len(self.genome)
        #Each robot has a random first move that will be part of the robot's genome
        self.first_dir = randint(1,self.available_functions) #Leaf node of the robot's genome tree
        #Robots behavior for correcting it's path if it's given a "bad move"
        self.behavior = randint(1,3)

        #Weights to be passed into robots for evaluating the total population results
        self.w1 = wallhitweight
        self.w2 = mdweight
        self.w3 = stepweight
    #Sub_Functions ===================
        #Move function essential for the rest
    def move(self,choice): #Μove function
        self.steps += 1

        if self.cur_pos[1] == self.end_pos[1]-1 and self.cur_pos[0] == self.end_pos[0]-1:
            self.cur_pos[0] += 1
            self.cur_pos[1] += 1
            self.steps += 1
            return True
        elif self.cur_pos[1] == self.end_pos[1]-1 and self.cur_pos[0] == self.end_pos[0]+1:
            self.cur_pos[0] -= 1
            self.cur_pos[1] += 1
            self.steps += 1
            return True
        if self.cur_pos[1] == self.end_pos[1]-1 and self.cur_pos[0] == self.end_pos[0]:
            self.cur_pos[1] += 1
            self.steps += 1
            return True
        elif choice == "U" and self.maze[self.cur_pos[0]-1][self.cur_pos[1]] != "#":
            self.cur_pos[0] += -1
            self.steps += 1
        elif choice == "D" and self.maze[self.cur_pos[0]+1][self.cur_pos[1]] != "#":
            self.cur_pos[0] += 1
            self.steps += 1
        elif choice == "F" and self.maze[self.cur_pos[0]][self.cur_pos[1]+1] != "#":
            self.cur_pos[1] += 1
            self.steps += 1
        elif choice == "B" and self.maze[self.cur_pos[0]][ self.cur_pos[1]-1] != "#":
            self.cur_pos[1] += -1
            self.steps += 1
        else: #If there is a wall to the direction that the robot is trying to go
            self.steps += 1
            self.collisions += 1 #Update wallhits
            self.last_bad_move = choice #Make the choice made the last bad move for later use
            #print("WE HIT A WALL COMMANDER")
            return False
        return True

        #Reverse_direction function reversing the direction given
    def change_direction(self,lbm):
        if self.behavior == 1: #Reverse Direction
            if lbm == "U":
                return "D"
            elif lbm == "D":
                return "U"
            elif lbm == "F":
                return "B"
            elif lbm == "B":
                return "F"
        if self.behavior == 2: #Turn right
            if lbm == "U":
                return "F"
            elif lbm == "D":
                return "B"
            elif lbm == "F":
                return "D"
            elif lbm == "B":
                return "U"
        if self.behavior == 3: #Turn left
            if lbm == "U":
                return "B"
            elif lbm == "D":
                return "F"
            elif lbm == "F":
                return "U"
            elif lbm == "B":
                return "D"
        #Executing the robot's genome

    #Manhattan Distance Calculator
    def get_manhattan_distance(self):
        return abs(self.cur_pos[0]-self.end_pos[0]) + abs(self.cur_pos[1]-self.end_pos[1])

    #Fitness calculator
    def calculate_fitness(self):
        self.fitness = mdweight * self.get_manhattan_distance() + wallhitweight * self.collisions\
                       + stepweight*self.steps
        #(self.fitness)
        return

    #Genome executioner
    def execute_genome(self):
        next_dir = self.first_dir
        self.steps = 0
        self.collisions = 0
        self.cur_pos = [1, 0]  # that has a starting point
        self.end_pos = [2, 6]  # And an ending point

        for it in range(0,self.genome_length):
            next_dir,result = self.function_handler(next_dir,self.genome[it])

        self.calculate_fitness()
        return
        # Functions============
        # 1.
    def get_away_from_wall(self, dir):

        if dir == self.last_bad_move:  # If the last move was a bad move
            dir = self.change_direction(self.last_bad_move)  # Choose another
        if self.cur_pos == self.end_pos:  # Check if we have arrived
            return dir, True  # We have arrived
        state = self.move(dir)
        if state == False:  # If we hit a wall
            self.change_direction(dir)

            state = self.move(dir)
            if state == False:
                self.last_bad_move = dir
        return dir, False
        #2.
    def get_closer_x(self, dir):  # try to get closer regarding the x vertical axis

        if self.cur_pos == self.end_pos:  # Check if we have arrived
            return dir, True  # We have arrived
        if self.cur_pos[0] < self.end_pos[0]:
            dir = "D"
        elif self.cur_pos[0] > self.end_pos[0]:
            dir = "U"
        elif self.cur_pos[0] == self.end_pos[0]:  # If we dont want to move the x axis
            self.last_bad_move = dir
            return dir, False

        state = self.move(dir)  # Try to move
        if state == False:  # If we hit a wall
            self.last_bad_move = dir
        return dir, False  # Wallhit
        #3.
    def get_closer_y(self, dir):  # Try to get closer regarding the y horizontal axis

        if self.cur_pos == self.end_pos:  # Check if we have arrived
            return dir, True  # We have arrived

        if self.cur_pos[1] < self.end_pos[1]:
            dir = "F"
        elif self.cur_pos[1] > self.end_pos[1]:
            dir = "B"
        else:  # If we dont want to move the y axis
            self.last_bad_move = dir
            return dir, False

        state = self.move(dir)
        if state == False:  # If we hit a wall
            self.last_bad_move = dir
        return dir, False  # Wallhit
        #4.
    def while_not_hit_wall(self,dir):

        if dir == self.last_bad_move: #If the last move was a bad move
            dir = self.change_direction(self.last_bad_move) #Choose another


        while 1:  #While you don't hit a wall
            if self.cur_pos == self.end_pos: #Check if we have arrived
                return dir,True #We have arrived
            state = self.move(dir) #Try to move
            if state == False:  #If we hit a wall
                self.last_bad_move = dir
                return dir,False #Wallhit
        #5.
    def while_too_far_away_from_dest(self,dir):

        if dir == self.last_bad_move:  # If the last move was a bad move
            dir = self.change_direction(self.last_bad_move)  # Choose another

        while 1:
            if self.cur_pos == self.end_pos:  # Check if we have arrived
                return dir, True  # We have arrived
            if self.cur_pos[0] > self.threshold():
                if self.cur_pos[0] < self.end_pos[0]:
                    dir = "F"
                elif self.cur_pos[1]< self.end_pos[1]:
                    dir = "U"

                state = self.move(dir)
                if state == False:  # If we hit a wall
                    self.last_bad_move = dir
                    return dir, False  # Wallhit
        #6
    def simple_move(self,dir):
        if dir == self.last_bad_move:  # If the last move was a bad move
            dir = self.change_direction(self.last_bad_move)  # Choose another
        if self.cur_pos == self.end_pos:  # Check if we have arrived
            return dir, True  # We have arrived
        self.move(dir)

        return dir,False

    #Function Handler=======
    def function_handler(self,dir,choice): #Executioner
        # 1 = get_away_from_wall
        # 2 = get_closer_x
        # 3 = get_closer_y
        # 4 = while_not_hit_wall
        # 5 = while_too_far_away_from_dest
        # 6 = simple_move

        if choice == 1:
            #print ("ONE")
            return self.get_away_from_wall(dir)
        elif choice == 2:
           # print("TWO")
            return self.get_closer_x(dir)
        elif choice == 3:
           # print("THREE")
            return self.get_closer_y(dir)
        elif choice == 4:
           # print("FOUR")
            return self.while_not_hit_wall(dir)
        elif choice == 5:
           # print("FIVE")
            return self.while_too_far_away_from_dest(dir)
        elif choice == 6:
           # print("SIX")
            return self.simple_move(dir)
        else:
            print("Error, No such function with No: ", choice, " identifier")