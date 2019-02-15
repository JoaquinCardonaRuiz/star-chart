class Log:
    """Logging module for StarChart"""
    
    text = []

    @classmethod
    def add(cls,str):
        cls.text.append(str)
    
    @classmethod
    def print(cls):
        for str in cls.text:
            print(str)