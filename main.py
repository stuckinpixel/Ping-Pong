
import pygame, sys, time, random, json
from pygame.locals import *

pygame.init()
WIDTH, HEIGHT = 600, 400
surface=pygame.display.set_mode((WIDTH, HEIGHT),0,32)
fps=100
ft=pygame.time.Clock()
pygame.display.set_caption('Ping Pong')

life_font = pygame.font.SysFont('Comic Sans MS', 30)

class Paddle_Set:
    def __init__(self):
        self.ball_pos = [WIDTH//2, HEIGHT//2]
        self.ball_direction = [random.choice([-1, 1]), random.choice([-1, 1])]
        self.ball_size = 30
        self.ball_speed = 1.5
        self.paddle_size = (100, 20)
        self.paddle_floating_height = 5
        self.paddle_pos = (WIDTH//2)-(self.paddle_size[0]//2)
        self.danger_bar_height = self.paddle_floating_height+self.paddle_size[1]-3
        self.paddle_speed = 4
        self.paddle_max_reach = 80
        self.paddle_target = None
    def move_ball(self):
        self.ball_pos[0] += (self.ball_direction[0]*self.ball_speed)
        self.ball_pos[1] += (self.ball_direction[1]*self.ball_speed)
    def set_paddle_target(self, direction):
        self.paddle_target = self.paddle_pos+(self.paddle_max_reach*direction)
    def move_paddle(self):
        if self.paddle_target is not None:
            direction = (self.paddle_target-self.paddle_pos)/abs(self.paddle_target-self.paddle_pos)
            diff = abs(self.paddle_target-self.paddle_pos)
            self.paddle_pos += (direction*min(self.paddle_speed, diff))
            if self.paddle_pos==self.paddle_target:
                self.paddle_target = None
            if self.paddle_pos<=0:
                self.paddle_pos = 0
            elif self.paddle_pos>(WIDTH-self.paddle_size[0]):
                self.paddle_pos = WIDTH-self.paddle_size[0]
    def is_ball_collided_With_walls(self):
        ball_radius = self.ball_size//2
        if not (ball_radius)<self.ball_pos[0]<(WIDTH-ball_radius):
            self.ball_direction[0] *= (-1)
        if not (ball_radius)<self.ball_pos[1]<(HEIGHT-ball_radius-self.danger_bar_height):
            self.ball_direction[1] *= (-1)
    def is_collided_with_danger_bar(self):
        ball_radius = self.ball_size//2
        if self.ball_pos[1]>=(HEIGHT-ball_radius-self.danger_bar_height):
            if not (self.paddle_pos)<self.ball_pos[0]<(self.paddle_pos+self.paddle_size[0]):
                return True
        return False
    def check_ball_collided(self):
        self.is_ball_collided_With_walls()
        return self.is_collided_with_danger_bar()


class App:
    def __init__(self, surface):
        self.surface = surface
        self.play = True
        self.mouse=pygame.mouse.get_pos()
        self.click=pygame.mouse.get_pressed()
        self.color = {
            "background": (40, 51, 80),
            "paddle": (0, 249, 56),
            "ball": (255, 181, 0),
            "danger_bar": (249, 56, 0),
            "life_line": (249, 30, 0)
        }
        self.paddle_set = Paddle_Set()
        self.life = 3
    def draw_paddle(self):
        pygame.draw.rect(self.surface, self.color["paddle"], (self.paddle_set.paddle_pos, HEIGHT-self.paddle_set.paddle_floating_height-self.paddle_set.paddle_size[1], self.paddle_set.paddle_size[0], self.paddle_set.paddle_size[1]))
    def draw_ball(self):
        pygame.draw.circle(self.surface, self.color["ball"], self.paddle_set.ball_pos, self.paddle_set.ball_size//2)
    def draw_danger_bar(self):
        pygame.draw.rect(self.surface, self.color["danger_bar"], (0, HEIGHT-self.paddle_set.danger_bar_height, WIDTH, self.paddle_set.danger_bar_height))
    def draw_lifes(self):
        text_value = life_font.render("Life : "+str(self.life), False, self.color["life_line"])
        self.surface.blit(text_value,(WIDTH-100,30))
    def action(self):
        self.paddle_set.move_ball()
        self.paddle_set.move_paddle()
        if self.paddle_set.check_ball_collided():
            self.life -= 1
            if self.life<=0:
                self.play = False
    def render(self):
        self.draw_ball()
        self.draw_danger_bar()
        self.draw_paddle()
        self.draw_lifes()
    def run(self):
        while self.play:
            self.surface.fill(self.color["background"])
            self.mouse=pygame.mouse.get_pos()
            self.click=pygame.mouse.get_pressed()
            for event in pygame.event.get():
                if event.type==QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type==KEYDOWN:
                    if event.key==K_TAB:
                        self.play=False
                    elif event.key==K_RIGHT:
                        self.paddle_set.set_paddle_target(1)
                    elif event.key==K_LEFT:
                        self.paddle_set.set_paddle_target(-1)
            #--------------------------------------------------------------
            self.action()
            self.render()
            # -------------------------------------------------------------
            pygame.display.update()
            ft.tick(fps)



if  __name__ == "__main__":
    app = App(surface)
    app.run()


