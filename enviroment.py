import operator
import sys
import classes
from bisect import bisect
import random
from random import randint

# =============ENVIROMENT SETTINGS========================
POP_SIZE = 100
fitness_threshold = 0.89  # Pososto epitixias twn robot
fitness_score_improvement = False  # Prospatheia veltiwsis tou fitness
improvement_tries = 10  # Arithmos prospatheiwn gia tin veltiwsi tou fitness
SELECTION_NUM = 2  # Two individuals selected per pop gen
crossover_rate = 0.1
mutation_rate = 0.5
NUM_OF_GENERATIONS = 1000
# ========================================================





class enviroment():
    def __init__(self, maze, robot):  # passing one robot to get the genomesize etc
        self.population = []  # Type robot
        self.genome_size = robot.genome_length
        self.robot_func_num = robot.available_functions
        self.maze = maze
        self.probabilities = []  # Probabilities regarding crossover to the next gen
        self.bestpop = []
        self.w1 = robot.w1  # wallhitweight
        self.w2 = robot.w2  # Manhattan distance weight
        self.w3 = robot.w3  # Stepweight

    # Generation handling and execution
    def execute_gen(self):

        gen = 0
        median_fitness = 0

        best_fitness = sys.maxsize  # Setting max size for median_fitness
        end = False  # Setting the end of the Generation execution
        success = 0  # Success of the experiment
        tries = 0 #Number of times to try and improve the fitness
        if fitness_score_improvement == True:
            print("Fitness score improvement selected:",
                  "\n",improvement_tries,"Executions of the experiment will occur, each one ending\n",
                  "when the fitness_threshold is above","{0:.0f}%".format(fitness_threshold * 100),
                  "in order to find the best possible fitness\n")

        while end == False:  # If there is no score improvement or it's at the end
            gen = 0
            self.population = []
            # For every individual
            for it in range(0, POP_SIZE):
                # Creating a map and appending it into the robot
                mazespawn = classes.maze(1)
                spawn = classes.robot(mazespawn)
                self.population.append(spawn)


            # For every generation
            for i in range(0, NUM_OF_GENERATIONS):
                if len(self.population) > POP_SIZE:
                    print("Size error",len(self.population))



                if fitness_score_improvement == False:
                    print("Generation No:", i, end='')
                for it in range(0, len(self.population)):
                    # print(self.population[it].cur_pos)
                    self.population[it].execute_genome()
                    # Setting the probabilities to a fo

                # To dict periexei ta probabilities kai tin thesi twn elements
                dict, self.fitness = self.selection(self.population)

                # Next generation creation
                self.population = self.next_gen(dict)
                count = 0

                for it in range(0, len(self.population)):
                    if self.population[it].cur_pos == [2, 6]:
                        count += 1
                print(' Percentage',round((count / len(self.population)),1 )* 100, ' %')
                if count / len(self.population) > fitness_threshold:
                    gen = i
                    success = - 1
                    break
            #Execution complete =================
            #Counting the median fitness=========
            sumfit = 0
            count = 0
            for robot in self.population:
                if robot.cur_pos == [2, 6]:
                    count += 1
                    sumfit += robot.fitness
            median_fitness = sumfit / count
            #Taking the best population
            if median_fitness < best_fitness:
                best_fitness = median_fitness  # Setting the best fitness we have found
                self.bestpop = self.population  # Saving the best pop
                best_gen = gen

            else:
                tries += 1


            #Printing the results of each generation
            if gen != 0 :
                print("Iteration number ", tries + 1, " done in: ",gen," Generations.\n Current Best fitness : ", best_fitness)
            else :
                print("Iteration number ", tries + 1," failed to produce a sample of ","{0:.0f}%".format(fitness_threshold * 100), " success rate",
                 "\n Current Best Fitness: ", best_fitness)
            #===========================================

            #Checking if the experiment is over
            if tries + 1 == improvement_tries or fitness_score_improvement == False : #An exoun teleiwsei oi prospathies
                end = True
        #Potential Fitness Improvement Complete
        if success == - 1:
            print("\nSimulation Complete in Generation:", best_gen, " with more than",
                  "{0:.0f}%".format(fitness_threshold * 100), " success rate ",
                  "and ", classes.GEN_SIZE, " number of moves with", "Median fitness: ", best_fitness)
            self.print_results(self.bestpop)
        else:
            print("\n\nSimulation Complete, but did not reach the desired limit of ",
                  "{0:.0f}%".format(fitness_threshold * 100), " success rate\n")

        return
        # =========================================

    def selection(self, population):  # Selection process. Calculating probabilities of passing into next gen etc
        # ================================Selection
        fitness = []
        for it in range(0, len(self.population)):
            fitness.append(population[it].fitness)
        maxv = max(fitness)  # Getting the max value
        for it in range(0, len(fitness)):
            fitness[it] = maxv - fitness[it] + 1  # Making the score better = higher

        # Normalizing

        self.probabilities = [1 - (float(i) / sum(fitness)) for i in fitness]

        dict = []
        for it in range(0, len(self.probabilities)):  # Printing the probabilities
            dict.append([it, self.probabilities[it], fitness[it]])

        dict.sort(key=operator.itemgetter(1))

        return dict, fitness

    def next_gen(self, dict):
        newpop = []
        # Splitting the dict
        probs = []
        positions = []
        for probability in (i[1] for i in dict):
            probs.append(probability)
        for pos in (i[0] for i in dict):
            positions.append(pos)

        candidate = self.get_one(probs, positions)
        newpop.append(self.population[candidate])
        while len(newpop) < POP_SIZE:
            if len(newpop) == POP_SIZE:
                return newpop

            candidate = self.get_one(probs, positions)
            newpop.append(self.population[candidate])

            if random.random() < crossover_rate:
                maze1 = classes.maze(1)
                cain = classes.robot(maze1)
                maze2 = classes.maze(1)
                abel = classes.robot(maze2)
                cain.genome, abel.genome = self.crossover(newpop[-1].genome, newpop[-2].genome)
                cain.behavior = newpop[-1].behavior
                cain.first_dir = newpop[-1].first_dir
                abel.behavior = newpop[-1].behavior
                abel.first_dir = newpop[-1].first_dir
                if len(newpop) < POP_SIZE:
                    cain.genome = self.mutate(cain.genome)

                    newpop.append(cain)
                    # print(newpop[-1].genome)
                if len(newpop) < POP_SIZE:
                    abel.genome = self.mutate(abel.genome)
                    newpop.append(abel)

        return newpop

    def get_one(self, probs, positions):
        pick = self.roulette(probs)

        return positions[pick]

    def roulette(self, score):
        index = 0
        totalFitness = 0.0
        randf = random.random()
        for i in range(len(score)):  # for each chromosome's fitness score
            totalFitness += score[i]  # add each chromosome's fitness score to cumalative fitness

            if totalFitness > randf:  # in the event of cumalative fitness becoming greater than r, return index of that chromo
                return i

    def crossover(self, adams_genome, eves_genome):  # Crossover between two robots
        r = random.randint(0, len(adams_genome))
        return adams_genome[:r] + eves_genome[r:], eves_genome[:r] + adams_genome[r:]

    def mutate(self, genome):  # Mutator
        mutated_genome = []
        # Mutating one function with the next
        for i in genome:
            if random.random() < mutation_rate:
                if i == 1:
                    mutated_genome.append(2)
                elif i == 2:
                    mutated_genome.append(3)
                elif i == 3:
                    mutated_genome.append(4)
                elif i == 4:
                    mutated_genome.append(5)
                elif i == 5:
                    mutated_genome.append(6)
                elif i == 6:
                    mutated_genome.append(1)
            else:
                mutated_genome.append(i)
        return mutated_genome

    def next_genn(self, dict):
        newpop = []  # The new improved population
        # Selecting x number of individuals based on probability
        probs = []  # List of probabilities

        for probability in (i[1] for i in dict):
            probs.append(probability)

        positions = []
        for pos in (i[0] for i in dict):
            positions.append(pos)

        while len(newpop) < POP_SIZE:  # For each generation

            if len(newpop) < POP_SIZE:
                val = self.get_one(probs, positions)
                print(val)
                newpop.append(self.population[val])

            # Probability to do crossover
            if random.random() < crossover_rate:
                # Generate two new robots
                maze1 = classes.maze(1)
                cain = classes.robot(maze1)
                maze2 = classes.maze(1)
                abel = classes.robot(maze2)
                # Do the crossover
                cain.genome, abel.genome = self.crossover(newpop[-1].genome, newpop[-2].genome)
                # Try to mutate and append them in the population
                if len(newpop) < POP_SIZE:
                    cain.genome = self.mutate(cain.genome)
                    newpop.append(cain)

                if len(newpop) < POP_SIZE:
                    abel.genome = self.mutate(abel.genome)
                    newpop.append(abel)

        return newpop

    def print_results(self, population):
        txt = open("Results.txt", "w")
        final_perc = 0
        count = 1
        flag = 0
        print("===================================================")
        print("============Printing the Resulting Map=============\n")

        for robot in population:
            if robot.cur_pos == [2, 6]:
                if flag == 0:
                    self.maze.printmaze(robot.cur_pos)
                    flag = 1
                final_perc += 1


        final_perc = final_perc / len(population) #Calculating the Final Success Rate
        txt.write("==================================================\n")
        txt.write("===================Results========================\n")
        print("Genome Legend: \n",
              "1 = get_away_from_wall \n",
              "2 = get_closer_x \n",
              "3 = get_closer_y \n",
              "4 = while_not_hit_wall \n",
              "5 = while_too_far_away_from_destination \n",
              "6 = simple_move", file=txt)



        for robot in population:
            if robot.cur_pos == [2, 6]:
                print("__________________________________________________\n", "Successfull genome:\n",file = txt)
                for gen in robot.genome:
                    if gen == 1:
                        print("< get_away_from_wall >\n",file=txt)
                    elif gen == 2:
                        print("< get_closer_x >\n", file=txt)
                    elif gen == 3:
                        print("< get_closer_y >\n", file=txt)
                    elif gen == 4:
                        print("< while_not_hit_wall >\n", file=txt)
                    elif gen == 5:
                        print("< while_too_far_away_from_destination >\n", file=txt)
                    elif gen == 6:
                        print("< simple_move >\n", file=txt)

            break

        print("__________________________________________________", file=txt)
        print("Final success percentage:", "{0:.0f}%".format(final_perc * 100), file=txt)

        txt.write("\n__________________________________________________\n")
        txt.write("Successful Robots:\n__________________________________________________\n")
        for robot in population:
            if robot.cur_pos == [2, 6]:
                print("Robot No: ", count, " Pos :", robot.cur_pos, " Fitness: ", robot.fitness,
                      " ", robot.genome, file=txt)
                count += 1




        txt.close()
        return
