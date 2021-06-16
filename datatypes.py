class AnswerSet:
    def __init__(self, wealth, burden, ground, running_start, running_stop):
        self.wealth = wealth
        self.burden = burden
        self.ground = ground
        self.running_start = running_start
        self.running_stop = running_stop

    def __call__(self):
        return self.wealth, self.burden, self.ground, self.timeStamp
