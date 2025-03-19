class Colours:
    def __init__(self):
        self.end = '\033[0m'

    def gre(self, s):
        return '\033[92m' + str(s) + self.end

    def red(self, s):
        return '\033[91m' + str(s) + self.end

    def yel(self, s):
        return '\033[93m' + str(s) + self.end

    def mag(self, s):
        return '\033[95m' + str(s) + self.end

    def err(self):
        return self.red('Error: ') + self.end
