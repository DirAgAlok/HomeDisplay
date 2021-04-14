import pygame
from pygame.locals import *
 
import pygame
from pygame.locals import *
 
class CEvent:
    def __init__(self):
        pass
    def on_input_focus(self):
        pass
    def on_input_blur(self):
        pass
    def on_key_down(self, event):
        pass
    def on_key_up(self, event):
        pass
    def on_mouse_focus(self):
        pass
    def on_mouse_blur(self):
        pass
    def on_lbutton_up(self, event):
        pass
    def on_lbutton_down(self, event):
        pass
    def on_rbutton_up(self, event):
        pass
    def on_rbutton_down(self, event):
        pass
    def on_minimize(self):
        pass
    def on_restore(self):
        pass
    def on_resize(self,event):
        pass
    def on_expose(self):
        pass
    def on_exit(self):
        pass
    def on_event(self, event):
        pass
    def on_mouse_move(self, event):
        pass
 
if __name__ == "__main__" :
    event = CEvent()