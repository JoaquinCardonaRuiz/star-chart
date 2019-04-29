import configparser

class Config():
    config = configparser.ConfigParser()
    chars = configparser.ConfigParser()
    try:
        config.read('config.ini')
        chars.read('chars.ini')
    except:
        print("init error")
        quit()