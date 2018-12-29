class Log:
    """Logging module for StarChart"""

    def __init__(self):
        self.text = []

    def add(self,str):
        self.text.append(str)
    
    def print(self):
        for str in self.text:
            print(str)