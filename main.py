"""
   _____ _              _____ _                _   
  / ____| |            / ____| |              | |  
 | (___ | |_ __ _ _ __| |    | |__   __ _ _ __| |_ 
  \___ \| __/ _` | '__| |    | '_ \ / _` | '__| __|
  ____) | || (_| | |  | |____| | | | (_| | |  | |_ 
 |_____/ \__\__,_|_|   \_____|_| |_|\__,_|_|   \__|


 A 4X CLI game set in a randomnly generated Solar System.
"""

from logic import Logic
import time

try:
    while True:
        #TODO: move most of this to Logic
        #time.sleep(0.005)
        Logic.update_screen_size()
        Logic.draw_state()
        key = Logic.get_input()
        Logic.handle_input(key)
        Logic.refresh()
except:
    raise
finally:    
    Logic.end()
