import turtle
import sys
import time

# Set up the screen
screen = turtle.Screen()
screen.title("Pong Game")
screen.bgcolor("beige")
screen.setup(width=800, height=600)
screen.tracer(0)

# Constants
WINNING_SCORE = 5
MAX_BALL_SPEED = 8.0

# Create paddles and ball
# Left paddle
paddle_left = turtle.Turtle()
paddle_left.speed(0)
paddle_left.shape("square")
paddle_left.color("maroon")
paddle_left.shapesize(stretch_wid=5, stretch_len=1)
paddle_left.penup()
paddle_left.goto(-350, 0)

# Right paddle
paddle_right = turtle.Turtle()
paddle_right.speed(0)
paddle_right.shape("square")
paddle_right.color("maroon")
paddle_right.shapesize(stretch_wid=5, stretch_len=1)
paddle_right.penup()
paddle_right.goto(350, 0)

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("circle")
ball.color("black")
ball.penup()
ball.goto(0, 0)
ball.dx = 3.0
ball.dy = 3.0

# Score
score_left = 0
score_right = 0
score_display = turtle.Turtle()
score_display.speed(3)
score_display.color("maroon")
score_display.penup()
score_display.hideturtle()
score_display.goto(0, 260)
score_display.write("Player A: 0  Player B: 0", align="center", font=("Courier", 24, "normal"))

# Instructions display
instructions = turtle.Turtle()
instructions.speed(0)
instructions.color("purple")
instructions.penup()
instructions.hideturtle()
instructions.goto(0, -260)
instructions.write("W/S: Left Paddle | ↑/↓: Right Paddle | P: Pause | R: Reset | ESC: Exit", 
                  align="center", font=("Courier", 12, "normal"))

# Game over display
game_over_display = turtle.Turtle()
game_over_display.speed(0)
game_over_display.color("green")
game_over_display.penup()
game_over_display.hideturtle()

# Game state
game_paused = False

# Paddle movement functions
def paddle_left_up():
    y = paddle_left.ycor()
    if y < 250:
        paddle_left.sety(y + 20)

def paddle_left_down():
    y = paddle_left.ycor()
    if y > -250:
        paddle_left.sety(y - 20)

def paddle_right_up():
    y = paddle_right.ycor()
    if y < 250:
        paddle_right.sety(y + 20)

def paddle_right_down():
    y = paddle_right.ycor()
    if y > -250:
        paddle_right.sety(y - 20)

def exit_game():
    screen.bye()
    sys.exit()

def check_winner():
    if score_left >= WINNING_SCORE:
        game_over_display.goto(0, 0)
        game_over_display.write("Player A Wins!", align="center", font=("Courier", 36, "normal"))
        return True
    elif score_right >= WINNING_SCORE:
        game_over_display.goto(0, 0)
        game_over_display.write("Player B Wins!", align="center", font=("Courier", 36, "normal"))
        return True
    return False

def reset_game():
    global score_left, score_right, game_paused
    score_left = 0
    score_right = 0
    score_display.clear()
    score_display.write(f"Player A: {score_left}  Player B: {score_right}", align="center",
                       font=("Courier", 24, "normal"))
    game_over_display.clear()
    ball.goto(0, 0)
    ball.dx = 3.0
    ball.dy = 3.0
    game_paused = False

def toggle_pause():
    global game_paused
    game_paused = not game_paused

# Keyboard bindings
screen.listen()
screen.onkeypress(paddle_left_up, "w")
screen.onkeypress(paddle_left_down, "s")
screen.onkeypress(paddle_right_up, "Up")
screen.onkeypress(paddle_right_down, "Down")
screen.onkey(reset_game, "r")
screen.onkey(exit_game, "Escape")
screen.onkey(toggle_pause, "p")

# Main game loop
def update_game():
    global score_left, score_right, game_paused

    if not game_paused:
        # Move the ball
        ball.setx(ball.xcor() + ball.dx)
        ball.sety(ball.ycor() + ball.dy)

        # Border checking
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1

        # Scoring
        if ball.xcor() > 390:
            score_left += 1
            score_display.clear()
            score_display.write(f"Player A: {score_left}  Player B: {score_right}", align="center",
                              font=("Courier", 24, "normal"))
            if check_winner():
                game_paused = True
            ball.goto(0, 0)
            ball.dx *= -1

        if ball.xcor() < -390:
            score_right += 1
            score_display.clear()
            score_display.write(f"Player A: {score_left}  Player B: {score_right}", align="center",
                              font=("Courier", 24, "normal"))
            if check_winner():
                game_paused = True
            ball.goto(0, 0)
            ball.dx *= -1

        # Paddle collisions with speed limit
        if (ball.xcor() > 340 and ball.xcor() < 350) and (
                ball.ycor() < paddle_right.ycor() + 50 and ball.ycor() > paddle_right.ycor() - 50):
            ball.setx(340)
            ball.dx = max(min(ball.dx * -1.1, -MAX_BALL_SPEED), -MAX_BALL_SPEED)
            ball.dy = max(min(ball.dy * 1.1, MAX_BALL_SPEED), -MAX_BALL_SPEED)

        if (ball.xcor() < -340 and ball.xcor() > -350) and (
                ball.ycor() < paddle_left.ycor() + 50 and ball.ycor() > paddle_left.ycor() - 50):
            ball.setx(-340)
            ball.dx = max(min(ball.dx * -1.1, MAX_BALL_SPEED), -MAX_BALL_SPEED)
            ball.dy = max(min(ball.dy * 1.1, MAX_BALL_SPEED), -MAX_BALL_SPEED)

    screen.update()
    screen.ontimer(update_game, 16)

# Start the game
update_game()
turtle.done()