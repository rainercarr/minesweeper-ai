import time
#Metrics class

#scoring
#if we click a 0 with no adjacent zeros, that counts as a point

#if we click a location that has anything else, that counts as a point


class Metrics:
    def __init__(self):
        #start game timer
        self.start_time = time.time()
        self.moves = 0

    def elapsed_time(self):
        return time.time() - self.start_time

    def record_move(self):
        self.moves += 1

if __name__ == '__main__':
    m = Metrics()
    time.sleep(1)
    print(m.elapsed_time())