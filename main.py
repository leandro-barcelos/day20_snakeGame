import sys
from turtle import Screen, Turtle
from time import sleep
from random import randint

screen = Screen()
screen.setup(width=600, height=600)
screen.bgpic('bg_image.png')
screen.title("Snake Game")
screen.tracer(0)


class Snake:
    # Starts with a 3 squares long body
    def __init__(self, food_):
        self.starting_position = [(0, 0), (-20, 0), (-40, 0)]
        self.segments = []
        self.food_ = food_

    # Creating the snake initial body
    def create_snake_body(self):
        for position in self.starting_position:
            s = Turtle('square')
            s.color("green")
            s.pu()
            s.goto(position)
            self.segments.append(s)

    # Adds a body segment
    def create_segment(self):
        new_s = Turtle('square')
        new_s.color("green")
        new_s.pu()
        new_s.goto(self.segments[len(self.segments) - 1].pos())
        self.segments.append(new_s)

    # Movement functions
    def move_up(self):
        for seg in self.segments:
            seg.seth(90)

    def move_down(self):
        for seg in self.segments:
            seg.seth(270)

    def move_left(self):
        for seg in self.segments:
            seg.seth(180)

    def move_right(self):
        for seg in self.segments:
            seg.seth(0)

    def movement(self):
        screen.listen()
        screen.onkeypress(self.move_up, "Up")
        screen.onkeypress(self.move_down, "Down")
        screen.onkeypress(self.move_left, "Left")
        screen.onkeypress(self.move_right, "Right")

    # Detects if a food was consumed and create a new body segment
    def eat_food(self):
        if collision(self.segments[0], self.food_.food):
            self.create_segment()
            self.food_.spawn()
            return True

    # Detects if the snake hit its on tale
    def hit_tale(self):
        for _ in range(3, len(self.segments)):
            if collision(self.segments[0], self.segments[_]):
                return True

    # Detects if the snake hit the border
    def hit_border(self):
        out_down_up = self.segments[0].xcor() >= 300 or self.segments[0].xcor() <= -300
        out_left_right = self.segments[0].ycor() >= 300 or self.segments[0].ycor() <= -300
        if out_down_up or out_left_right:
            return True

    # Ends game and prints score if any of the two function above return True
    def lost(self, score_class):
        if self.hit_border() or self.hit_tale():
            print(f"You lost!\nScore: {score_class.score}")
            sys.exit()


class Food:
    def __init__(self):
        self.food = Turtle('square')
        self.food.color('red')
        self.food.pu()
        self.spawn()

    # Spawns a fruit in a random location
    def spawn(self):
        self.food.goto(rand_cord())


class Scoreboard:

    def __init__(self, score):
        self.writer = Turtle()
        self.writer.hideturtle()
        self.writer.pu()
        self.writer.pencolor('black')
        self.score = score

    # Write on screen how many foods the snake consumed
    def write(self):
        self.writer.goto(0, 250)
        self.writer.clear()
        self.writer.write(f"Score: {self.score}", align='center', font=('Pixeboy', 20, 'normal'))


# Generates a random coordinate tuple
def rand_cord():
    rand_x = int(randint(-280, 280) / 20) * 20
    rand_y = int(randint(-280, 280) / 20) * 20
    cord = (rand_x, rand_y)
    return cord


# Checks collision
def collision(a, b):
    return abs(a.xcor() - b.xcor()) < 10 and abs(a.ycor() - b.ycor()) < 10


game_is_on = True

points = Food()
player = Snake(points)
player.create_snake_body()
player.movement()
score_ = 0
player_score = Scoreboard(score_)
player_score.write()
sleep(2)
while game_is_on:
    screen.update()
    player.lost(player_score)
    sleep(0.1)
    player_score.write()
    player_score.write()
    if player.eat_food():
        player_score.score += 1
    for i in range(len(player.segments) - 1, -1, -1):
        if i == 0:
            player.segments[i].fd(20)
        else:
            player.segments[i].goto(player.segments[i - 1].pos())

screen.exitonclick()
