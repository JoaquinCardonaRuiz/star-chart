class Log:
    def __init__(self):
        self.text = []

    def add(self,str):
        self.text.append(str)
        print(str)
    
    def print(self):
        for str in self.text:
            print(str)