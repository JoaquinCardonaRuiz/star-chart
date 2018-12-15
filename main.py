from logic import Logic
import time

try:
    while True:
        time.sleep(0.005)
        if Logic.check_screen_size():
            Logic.draw_state()
            key = Logic.get_input()
            Logic.handle_input(key)
        else:
            Logic.pause("Window must be at least 150x38")
        Logic.refresh()
except:
    raise
finally:    
    Logic.end()
