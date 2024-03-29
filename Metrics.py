import time
from decimal import *
import platform
import os

class Metrics:
    def __init__(self):
        # contains the class name of the AI, if any; otherwise it's a human player
        self.agent = "Human Player"
        # board length
        self.board_length = 0
        # bombs on board
        self.board_bombs = 0
        #gets host name of computer running simulation (for records purposes)
        self.host_pc = platform.node()
        #number of moves made
        self.moves = 0
        #win or loss
        self.outcome = "Loss"
        #start game timer
        self.start_time = time.time()
        #number of successful moves made
        self.successful_moves = 0

        #set decimal precision to 3 decimal places
        getcontext().prec = 3

    def elapsed_time(self):
        return Decimal(time.time()) - Decimal(self.start_time)

    def end(self, log=False):
        #end game timer
        game_length = str(self.elapsed_time())

        #record time test was run
        test_date_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


        print("Game time (sec): " + str(game_length))
        print("Moves: " + str(self.moves))
        print("Successful moves: ", self.successful_moves)
        print(self.outcome)

        #appends the current date and time, game time in seconds, and number of moves to a csv log file, results.csv
        if log:
            f = None
            #if log file not present
            if not os.path.exists('metrics.csv'):
                f = open('metrics.csv', 'w+')
                f.write('Test Date and Time,Host PC,Agent Type,Length of Game (sec),Board Size,Bombs,Number of Moves,Successful Moves,Outcome')

            #write log entry to file
            f = open('metrics.csv', 'a')
            log_entry = "\n" + test_date_time + ',' + self.host_pc + ',' + self.agent + ',' + game_length + ',' + str(self.board_length) + ',' + str(self.board_bombs) + ',' + str(self.moves) + ',' + str(self.successful_moves) + ',' + self.outcome
            f.write(log_entry)
            f.close()

    def record_move(self):
        self.moves += 1

    def record_successful_move(self):
        self.successful_moves += 1

    #this records the name of the AI class being used in the game, or "Human Player" if human
    def register_agent(self, agent):
        if agent is not None:
            self.agent = str(agent.__class__).replace('<class \'', '').replace('\'>', '')

if __name__ == '__main__':
    m = Metrics()
    #other test code here if needed