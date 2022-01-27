
import pygame, sys, time, random, json
from pygame.locals import *

pygame.init()
WIDTH, HEIGHT = 800, 600
surface=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
fps=100
ft=pygame.time.Clock()
pygame.display.set_caption('Ping Pong')

class App:
    def __init__(self, surface):
        self.surface = surface
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "background": (40, 51, 80),
            "paddle": (0, 249, 56),
            "ball": (255, 181, 0),
            "danger_bar": (249, 56, 0)
        }
        self.ball_pos = [WIDTH//2, HEIGHT//2]
        self.ball_direction = (random.choice([-1, 1]), random.choice([-1, 1]))
        self.ball_size = 30
        self.ball_speed = 1.5
        self.paddle_size = (150, 20)
        self.paddle_floating_height = 5
        self.paddle_pos = (WIDTH//2)-(self.paddle_size[0]//2)
        self.danger_bar_height = 3
        self.paddle_speed = 60
    def draw_paddle(self):
        pygame.draw.rect(self.surface, self.color["paddle"], (self.paddle_pos, HEIGHT-self.paddle_floating_height-self.paddle_size[1], self.paddle_size[0], self.paddle_size[1]))
    def draw_ball(self):
        pygame.draw.circle(self.surface, self.color["ball"], self.ball_pos, self.ball_size//2)
    def draw_danger_bar(self):
        pygame.draw.rect(self.surface, self.color["danger_bar"], (0, HEIGHT-self.danger_bar_height, WIDTH, self.danger_bar_height))
    def move_ball(self):
        self.ball_pos[0] += (self.ball_direction[0]*self.ball_speed)
        self.ball_pos[1] += (self.ball_direction[1]*self.ball_speed)
    def move_paddle(self, direction):
        self.paddle_pos += (self.paddle_speed*direction)
        if self.paddle_pos<=0:
            self.paddle_pos = 0
        elif self.paddle_pos>(WIDTH-self.paddle_size[0]):
            self.paddle_pos = WIDTH-self.paddle_size[0]
    def is_ball_collided_With_walls(self):
        pass
    def check_ball_collided(self):
        self.is_ball_collided_With_walls()
    def action(self):
        self.move_ball()
        self.check_ball_collided()
    def render(self):
        self.draw_ball()
        self.draw_danger_bar()
        self.draw_paddle()
    def run(self):
        play = True
        while play:
            self.surface.fill(self.color["background"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        play=False
                    elif event.key==K_RIGHT:
                        self.move_paddle(1)
                    elif event.key==K_LEFT:
                        self.move_paddle(-1)
            #--------------------------------------------------------------
            self.action()
            self.render()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)





if  __name__ == "__main__":
    app = App(surface)
    app.run()
