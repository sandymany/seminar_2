import random
import time
import turtle
import serial
from threading import Thread
import signal
import sys

def signal_handler(sig, frame):
    for t in threads:
        print("Killing thread:\n", t.name())
        t.join()
    sys.exit(0)

# define ctrl+c signal handler (to join all threads):
signal.signal(signal.SIGINT, signal_handler)

# define constants
FRAME_RATE = 50  # Frames per second
TIME_FOR_1_FRAME = 1 / FRAME_RATE  # Seconds
CANNON_STEP = 10
LASER_LENGTH = 20
LASER_SPEED = 20
ALIEN_SPAWN_INTERVAL = 1.2  # Seconds
ALIEN_SPEED = 3.5

window = turtle.Screen()
window.tracer(0)
window.setup(0.5, 0.75)
window.bgcolor(0.2, 0.2, 0.2)
window.title("Turtle invader")

# initialize arduino object for serial data transfer:
arduino = serial.Serial(port='/dev/cu.usbmodem141301', baudrate=9600, timeout=.1)
threads = []

LEFT = -window.window_width() / 2
RIGHT = window.window_width() / 2
TOP = window.window_height() / 2
BOTTOM = -window.window_height() / 2
FLOOR_LEVEL = 0.9 * BOTTOM
GUTTER = 0.025 * window.window_width()

# Create laser cannon
turtle.register_shape("spider", shape="~/FER/8.semestar/seminar_2/code/scripts/spider.gif")
cannon = turtle.Turtle()
cannon.penup()
cannon.color(1, 1, 1)
cannon.shape("circle")
# cannon.shape("spider")
cannon.setposition(0, FLOOR_LEVEL)
cannon.cannon_movement = 0  # -1, 0 or 1 for left, stationary, right

# Create turtle for writing text
text = turtle.Turtle()
text.penup()
text.hideturtle()
text.setposition(LEFT * 0.8, TOP * 0.8)
text.color(1, 1, 1)

lasers = []
aliens = []

def draw_cannon():
    cannon.clear()
    cannon.turtlesize(1, 4)  # Base
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 10)
    cannon.turtlesize(1, 1.5)  # Next tier
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL + 20)
    cannon.turtlesize(0.8, 0.3)  # Tip of cannon
    cannon.stamp()
    cannon.sety(FLOOR_LEVEL)

def move_left():
    cannon.cannon_movement = -1

def move_right():
    cannon.cannon_movement = 1

def stop_cannon_movement():
    cannon.cannon_movement = 0

def create_laser():
    laser = turtle.Turtle()
    laser.penup()
    laser.color(1, 0, 0)
    laser.hideturtle()
    laser.setposition(cannon.xcor(), cannon.ycor())
    laser.setheading(90)
    # Move laser to just above cannon tip
    laser.forward(20)
    # Prepare to draw the laser
    laser.pendown()
    laser.pensize(5)

    lasers.append(laser)

def move_laser(laser):
    laser.clear()
    laser.forward(LASER_SPEED)
    # Draw the laser
    laser.forward(LASER_LENGTH)
    laser.forward(-LASER_LENGTH)

def create_alien():
    alien = turtle.Turtle()
    alien.penup()
    alien.turtlesize(1.5)
    alien.setposition(
        random.randint(
            int(LEFT + GUTTER),
            int(RIGHT - GUTTER),
        ),
        TOP,
    )
    alien.shape("turtle")
    alien.setheading(-90)
    alien.color(random.random(), random.random(), random.random())
    aliens.append(alien)

def remove_sprite(sprite, sprite_list):
    sprite.clear()
    sprite.hideturtle()
    window.update()
    sprite_list.remove(sprite)
    turtle.turtles().remove(sprite)

def get_new_cannon_coordinate():
    while 1:
        try :
            res = arduino.readline().decode().strip()
        except:
            continue
        if res == '':
            continue
        res = int(res)
        print(res)
        x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement
        sredina = 570
        tolerance = 20

        if not(res >= (sredina - tolerance) and res <= (sredina + tolerance)):
            # nije vise u sivoj zoni gdje se cannon ne smije micati. Sad se mice lijevo ili desno:
            if res < (sredina - tolerance):
                move_right()
            else:
                move_left()
        else:
            stop_cannon_movement()
    #print("IM DONE")


# Key bindings
window.onkeypress(move_left, "Left")
window.onkeypress(move_right, "Right")
window.onkeyrelease(stop_cannon_movement, "Left")
window.onkeyrelease(stop_cannon_movement, "Right")
window.onkeypress(create_laser, "space")
window.onkeypress(turtle.bye, "q")
window.listen()

draw_cannon()

# stvoriti zaseban thread za citanje podataka s Arduina zbog blokirajuce operacije!
thread = Thread(target = get_new_cannon_coordinate, name="1324") # args = (...) ako funkcija prima argumente.
threads.append(thread)
thread.start()

# Game loop
alien_timer = 0
game_timer = time.time()
score = 0
game_running = True

while game_running:
    timer_this_frame = time.time()

    time_elapsed = time.time() - game_timer
    text.clear()
    text.write(
        f"Time: {time_elapsed:5.1f}s\nScore: {score:5}",
        font=("Courier", 20, "bold"),
        )

    # Move cannon:
    new_x = cannon.xcor() + CANNON_STEP * cannon.cannon_movement # lijevo ili desno
    
    # update cannon position:
    if LEFT + GUTTER <= new_x <= RIGHT - GUTTER:
        cannon.setx(new_x)
        draw_cannon()

    # Move all lasers
    for laser in lasers.copy():
        move_laser(laser)
        # Remove laser if it goes off screen
        if laser.ycor() > TOP:
            remove_sprite(laser, lasers)
            break
        # Check for collision with aliens
        for alien in aliens.copy():
            if laser.distance(alien) < 20:
                remove_sprite(laser, lasers)
                remove_sprite(alien, aliens)
                score += 1
                break

    # Spawn new aliens when time interval elapsed
    if time.time() - alien_timer > ALIEN_SPAWN_INTERVAL:
        create_alien()
        alien_timer = time.time()

    # Move all aliens
    for alien in aliens:
        alien.forward(ALIEN_SPEED)
        # Check for game over
        if alien.ycor() < FLOOR_LEVEL:
            game_running = False
            break

    time_for_this_frame = time.time() - timer_this_frame
    if time_for_this_frame < TIME_FOR_1_FRAME:
        time.sleep(TIME_FOR_1_FRAME - time_for_this_frame)
    window.update()

splash_text = turtle.Turtle()
splash_text.hideturtle()
splash_text.color(1, 1, 1)
splash_text.write("GAME OVER", font=("Courier", 40, "bold"), align="center")
turtle.done()

for t in threads:
    print("Killing thread:", t.name)
    t.join()

exit(0)


