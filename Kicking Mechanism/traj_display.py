"""File to display the trajectory of the ball after kick."""

import pygame
import pygame_gui as pg
import math

pygame.init()

# Intitialising the dimensions
WIDTH, HEIGHT = 1400, 700

# Making the window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ERA')

# Making the UI buttons / input manager
UImanager = pg.UIManager((WIDTH, HEIGHT))

# The FPS management element
CLOCK = pygame.time.Clock()

# Creating the UI elements
rect = pygame.Rect((320, 90), (200, 60))
GO_button = pg.elements.UIButton(
    relative_rect=rect,
    text='GO',
    manager=UImanager)


rect = pygame.Rect((600, 15), (200, 60))
ANGLE_input = pg.elements.UITextEntryLine(
    relative_rect=rect,
    manager=UImanager,
)

rect = pygame.Rect((320, 15), (200, 60))
FORCE_input = pg.elements.UITextEntryLine(
    relative_rect=rect,
    manager=UImanager,
)


class Ball(pygame.Surface):
    """Class to hold the ball object."""
    SCALER = 0.2
    GRAV = 9.8*(SCALER**2)
    time_delta = 1
    HIT_VEL = 50 * SCALER

    def __init__(self, radius, mass, x=100, y=500):
        """Initialise the ball object with """
        self.r = radius
        self.m = mass
        self.x = x
        self.y = y
        self.angle = 0
        self.vel_x = 0
        self.vel_y = 0

    def display_ball(self):
        """Display the ball on the screen."""
        pygame.draw.circle(WIN,
                           pygame.color.Color(0, 0, 0),
                           (self.x, self.y),
                           self.r)

    def set_angle(self, angle):
        """Update the angle of impact for the ball."""
        self.angle = angle

    def hit_ball(self):
        """Initiate the hit."""
        self.vel_x = self.HIT_VEL * math.cos(math.pi*self.angle/180)
        self.vel_y = -1 * self.HIT_VEL * math.sin(math.pi*self.angle/180)
        print(self.vel_x, self.vel_y)

    def update_pos(self):
        """Update the pos wrt time-delta."""
        self.x += self.vel_x*self.time_delta
        self.y += self.vel_y*self.time_delta

        if self.vel_y != 0:
            self.vel_y += self.GRAV*self.time_delta
            print(self.vel_y)

        if self.y > 500:
            self.vel_x = 0
            self.vel_y = 0


# Test Ball
ball = Ball(30, 0.41)


def redraw_window():
    """Construct all the elements on the screen."""
    WIN.fill(pygame.Color(127, 67, 50, 200))
    ball.display_ball()


def run_window():
    run = True
    FPS = 60

    while run:

        time_del = CLOCK.tick(FPS)/1000

        # update the ball position
        ball.update_pos()

        # Handling the events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            UImanager.process_events(event)

            if event.type == pygame.USEREVENT:
                if event.user_type == pg.UI_BUTTON_PRESSED:
                    if event.ui_element == GO_button:
                        text = ANGLE_input.get_text()
                        angle = int(text)

                        text = FORCE_input.get_text()
                        force = int(text)

                        ball.HIT_VEL = force*ball.SCALER*ball.time_delta/ball.m
                        ball.set_angle(angle)
                        ball.hit_ball()

        # Drawing the stuff on the screen
        redraw_window()

        # UI Stuff
        UImanager.update(time_del)
        UImanager.draw_ui(WIN)

        # Updating the Display
        pygame.display.update()


run_window()
