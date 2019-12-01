import time
from decimal import *
import platform
import os
#Metrics class

#scoring
#if we click a 0 with no adjacent zeros, that counts as a point

#if we click a location that has anything else, that counts as a point
'''
TTD in Game class
    place Metrics() constructor in proper method to start game
    
Scoring Gameplay
    Human Player
        Plays a certain square
            If the square is adjacent to a known zero, score does not increase.
            If the square is NOT adjacent to a known zero, score increases by one.
    
    Agent Player    
'''

class Metrics:
    def __init__(self):
        #start game timer
        self.start_time = time.time()
        #number of moves made
        self.moves = 0
        #contains the class name of the AI, if any; otherwise it's a human player
        self.agent = "Human Player"
        #gets host name of computer running simulation (for records purposes)
        self.host_pc = platform.node()
        #win or loss
        self.outcome = "Loss"
        #set decimal precision to 3 decimal places
        getcontext().prec = 3

    def elapsed_time(self):
        return Decimal(time.time()) - Decimal(self.start_time)

    def record_move(self):
        self.moves += 1

    #this records the name of the AI class being used in the game, or "Human Player" if human
    def register_agent(self, agent):
        if agent is not None:
            self.agent = str(agent.__class__).replace('<class \'', '').replace('\'>', '')

    def end(self, log=False):
        test_date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        game_length = str(self.elapsed_time())

        print("Game time (sec): " + str(game_length))
        print("Moves: " + str(self.moves))
        print(self.outcome)

        #appends the current date and time, game time in seconds, and number of moves to a csv log file, results.csv
        if log:
            f = None
            if not os.path.exists('metrics.csv'):
                f = open('metrics.csv', 'w+')
                f.write('Test Date and Time,Host PC,Agent Type,Length of Game (sec),Number of Moves,Outcome')
            f = open('metrics.csv', 'a')
            f.write("\n" + test_date_time + ',' + self.host_pc + ',' + self.agent + ',' + game_length + ',' + str(self.moves) +
                    ',' + self.outcome)


if __name__ == '__main__':
    m = Metrics()
    time.sleep(1)
    print(m.elapsed_time())
    m.record_move()

    time.sleep(1)
    m.end()