import classes
import enviroment
from builtins import print
import random
import os




def brain():
    print("Brain starting")
    mymaze = classes.maze(2)
    Adam = classes.robot(mymaze)
    #Adam.execute_genome()
    #mymaze.printmaze(Adam.cur_pos)

    e = enviroment.enviroment(mymaze,Adam)

    e.execute_gen()

    #mymaze.printmaze(Roberta.cur_pos)

    return

brain()