import configparser

class Config():
    config = configparser.ConfigParser()
    try:
        config.read('config.ini')
    except:
        print("init error")
        quit()