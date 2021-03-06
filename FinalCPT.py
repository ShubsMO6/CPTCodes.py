import sys
import pygame

SCREEN_SIZE = 810, 600

# Game object dimensions
BRICK_WIDTH = 90
BRICK_HEIGHT = 30
PADDLE_WIDTH = 80
PADDLE_HEIGHT = 12
BALL_DIAMETER = 16
BALL_RADIUS = 8

MAX_PADDLE_X = SCREEN_SIZE[0] - PADDLE_WIDTH
MAX_BALL_X = SCREEN_SIZE[0] - BALL_DIAMETER
MAX_BALL_Y = SCREEN_SIZE[1] - BALL_DIAMETER

# Paddle Y coordinate
PADDLE_Y = SCREEN_SIZE[1] - PADDLE_HEIGHT - 10

# Color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (255, 255, 255)
BRICK_COLOR = (165, 42, 42)

# State constants
STATE_BALL_IN_PADDLE = 0
STATE_PLAYING = 1
STATE_WON = 2
STATE_GAME_OVER = 3


class Bricka:

    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()

        self.screen = pygame.display.set_mode(SCREEN_SIZE) #Setting up screen
        pygame.display.set_caption("Brick Breaker by Jonathan and Shab")

        self.clock = pygame.time.Clock()

        if pygame.font:
            self.font = pygame.font.Font(None, 30)
        else:
            self.font = None

        pygame.mixer.music.load('GameMusic.mp3')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-3)

        self.init_game()

    def init_game(self): #The lives of the user while playing
        self.lives = 3
        self.score = 0
        self.state = STATE_BALL_IN_PADDLE
#creating the paddle and ball (below)
        self.paddle = pygame.Rect(300, PADDLE_Y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.ball = pygame.Rect(300, PADDLE_Y - BALL_DIAMETER, BALL_DIAMETER, BALL_DIAMETER)

        self.ball_vel = [5, -5]

        self.create_bricks()

        self.counter = 0

    def create_bricks(self): #Creating the bricks, x amount of bricks by y amount of bricks
        y_ofs = 10
        self.bricks = []
        for i in range(6):
            x_ofs = 10
            for j in range(10):
                self.bricks.append(pygame.Rect(x_ofs, y_ofs, BRICK_WIDTH, BRICK_HEIGHT))
                x_ofs += BRICK_WIDTH + 10
            y_ofs += BRICK_HEIGHT + 10

    def draw_bricks(self):
        for brick in self.bricks:
            pygame.draw.rect(self.screen, BRICK_COLOR, brick)

    def check_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]: #Paddle movement by right arrow key
            self.paddle.left -= 20
            if self.paddle.left < 0:
                self.paddle.left = 0

        if keys[pygame.K_RIGHT]: #Paddle Movement by left arrow key
            self.paddle.left += 20
            if self.paddle.left > MAX_PADDLE_X:
                self.paddle.left = MAX_PADDLE_X

        if keys[pygame.K_SPACE] and self.state == STATE_BALL_IN_PADDLE: #Begins the start of the game when the spacebar is pressed; music also plays
            self.ball_vel = [10, -10]
            self.state = STATE_PLAYING
            pygame.mixer.music.load('GameMusic.mp3')
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-3)
        elif keys[pygame.K_RETURN] and (self.state == STATE_GAME_OVER or self.state == STATE_WON):
            self.init_game()

    def move_ball(self):
        self.ball.left += self.ball_vel[0]
        self.ball.top += self.ball_vel[1]

        if self.ball.left <= 0: #Ball movement
            self.ball.left = 0
            self.ball_vel[0] = -self.ball_vel[0]
        elif self.ball.left >= MAX_BALL_X:
            self.ball.left = MAX_BALL_X
            self.ball_vel[0] = -self.ball_vel[0]

        if self.ball.top < 0: #Balls limitations and movement
            self.ball.top = 0
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top >= MAX_BALL_Y:
            self.ball.top = MAX_BALL_Y
            self.ball_vel[1] = -self.ball_vel[1]

    def handle_collisions(self):
        for brick in self.bricks:
            if self.ball.colliderect(brick):
                self.score += 3
                self.ball_vel[1] = -self.ball_vel[1]
                self.bricks.remove(brick)
                self.counter = self.counter + 1
                if self.counter > 5 == 0: #create the different speeds for the ball, as more bricks are destroyed (from velocity 10 to 15 to 20)
                    self.ball_vel = [10,-10]
                if self.counter > 10 == 0:
                    self.ball_vel = [15,-15]
                if self.counter > 20 == 0:
                    self.ball_vel = [20,-20]
                break

        if len(self.bricks) == 0:
            self.state = STATE_WON #When the number of bricks is 0, it will proceed to the winning state

        if self.ball.colliderect(self.paddle): #Describes what is to happen when the ball collides with an object
            self.ball.top = PADDLE_Y - BALL_DIAMETER
            self.ball_vel[1] = -self.ball_vel[1]
        elif self.ball.top > self.paddle.top:
            self.lives -= 1
            if self.lives > 0:
                self.state = STATE_BALL_IN_PADDLE
            else:
                pygame.mixer.music.load('GameOver.mp3') #Plays the game music
                pygame.mixer.music.set_volume(0.05)
                pygame.mixer.music.play(1)
                self.state = STATE_GAME_OVER

    def show_message(self, message):
        if self.font:
            size = self.font.size(message)
            font_surface = self.font.render(message, False, WHITE)
            x = (SCREEN_SIZE[0] - size[0]) / 2
            y = (SCREEN_SIZE[1] - size[1]) / 2
            self.screen.blit(font_surface, (x, y))

    def score_calc(self): #calculates and reports the score onto the screen
        f = open('score.txt', 'r')
        self.highscore = f.readline() # Accesses the high-score file and evaluates to see if the current score is greater than the highscore, if it is, it replaces the last highscore
        if int(self.score) > int(self.highscore):
            self.highscore = self.score
            f = open('score.txt', 'w')
            f.write(str(self.highscore))

        if self.font:
            if int(self.score) == int(self.highscore) and self.state == STATE_GAME_OVER:
                f = open('score.txt', 'r')
                self.score = f.readline() #scans the highscore file to read the now achieved high-score
                font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives) + "    YOU GOT A HIGH-SCORE! ", False, WHITE)
                self.screen.blit(font_surface, (205, 5))
            else:
                font_surface = self.font.render("SCORE: " + str(self.score) + " LIVES: " + str(self.lives), False, WHITE)
                self.screen.blit(font_surface, (205, 5))

    def run(self):
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: #for any event that would result in closing the game, it quits the program
                    pygame.display.quit()

            self.clock.tick(50)
            self.screen.fill(BLACK)
            self.check_input()

            if self.state == STATE_PLAYING:
                self.move_ball()
                self.handle_collisions()
            elif self.state == STATE_BALL_IN_PADDLE:
                self.ball.left = self.paddle.left + self.paddle.width / 2 #paddle movement when ball is not in air yet
                self.ball.top = self.paddle.top - self.ball.height
                self.show_message("PRESS SPACE TO LAUNCH THE BALL, USE ARROW KEYS TO MOVE AROUND") #alerting user of events that start the game
            elif self.state == STATE_GAME_OVER:
                self.show_message("GAME OVER. PRESS ENTER TO PLAY AGAIN")
            elif self.state == STATE_WON:
                self.show_message("YOU WON! PRESS ENTER TO PLAY AGAIN")

            self.draw_bricks()

            # Draw paddle
            pygame.draw.rect(self.screen, BLUE, self.paddle)

            # Draw ball
            pygame.draw.circle(self.screen, WHITE, (self.ball.left + BALL_RADIUS, self.ball.top + BALL_RADIUS),
                               BALL_RADIUS)

            self.score_calc()

            pygame.display.flip()


if __name__ == "__main__": #running the program
    Bricka().run()
