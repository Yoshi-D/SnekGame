from tkinter import *
import random
#acreate checkered tile
GAME_BREADTH=700
GAME_HEIGHT=700
SPEED=90
SPACE_SIZE=50
SNAKE_SIZE=3
SNAKE_COLOUR="#2a52be"
FOOD_COLOUR="#FF3030"

class Snake:
    def __init__(self):
        self.body_size=SNAKE_SIZE
        self.coordinates=[]
        self.squares=[]

        for i in range(0,SNAKE_SIZE):
            self.coordinates.append([0,0])
        for x,y in self.coordinates:
            square=canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOUR)
            self.squares.append(square)
class Food:
    def __init__(self):
        x=random.randint(0,int(GAME_BREADTH/SPACE_SIZE)-1)*SPACE_SIZE
        y=random.randint(0,int(GAME_HEIGHT/SPACE_SIZE)-1)*SPACE_SIZE
        while [x, y] in snake.coordinates:
            x = random.randint(0, int(GAME_BREADTH / SPACE_SIZE) - 1) * SPACE_SIZE
            y = random.randint(0, int(GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates=[x,y]
        canvas.create_oval(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=FOOD_COLOUR,tag="food")


def next_turn(snake,food):
    x,y=snake.coordinates[0]

    if dir=="up":
        y-=SPACE_SIZE
    elif dir=="down":
        y+=SPACE_SIZE
    elif dir=="left":
        x-=SPACE_SIZE
    elif dir=="right":
        x+=SPACE_SIZE

    snake.coordinates.insert(0,(x,y))
    square=canvas.create_rectangle(x,y,x+SPACE_SIZE,y+SPACE_SIZE,fill=SNAKE_COLOUR)
    snake.squares.insert(0,square)

    if x==food.coordinates[0] and y==food.coordinates[1]:
        global score
        score+=1
        label.config(text="SCORE:{}".format(score))
        canvas.delete("food")
        food=Food()
    else:
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collision(snake):
        game_over()
    else:
        root.after(SPEED,next_turn,snake,food)

def change_dir(new_dir):
    global dir

    if new_dir=='left':
        if dir!='right':
            dir=new_dir
    elif new_dir=='right':
        if dir!='left':
            dir=new_dir
    elif new_dir=='up':
        if dir!='down':
            dir=new_dir
    elif new_dir=='down':
        if dir!='up':
            dir=new_dir

def check_collision(snake):
    x,y=snake.coordinates[0]

    if x<0 or x>=GAME_BREADTH:
        return True
    elif y<0 or y>=GAME_HEIGHT:
        return True
    for body_part in snake.coordinates[1:]:
        if x==body_part[0] and y==body_part[1]:
            return True
    return False

def checkered_tiles():
    colour = True
    for x in range(0, 701, 50):
        for y in range(0, 701, 50):
            if colour == True:
                canvas.create_rectangle(x, y, x + 50, y + 50, fill='#65DA65')
                colour = not colour
            else:
                canvas.create_rectangle(x, y, x + 50, y + 50, fill='#32CD32')
                colour = not colour


def restart():

    global snake,food,score,dir,restart_button
    canvas.delete(ALL)
    checkered_tiles()
    snake=Snake()
    food=Food()
    score=0
    dir='right'
    label.config(text="SCORE:{}".format(score))
    next_turn(snake,food)
    restart_button.destroy()
def game_over():
    #add high score and users score here
    global restart_button,score
    canvas.delete(ALL)
    file=open('score.txt','r+')
    prev_high_score=file.read()

    if int(prev_high_score)<=score:
        file.seek(0)
        file.write(str(score))
        label2.config(text="HIGH SCORE:{}".format(score))
        canvas.create_text(canvas.winfo_width() / 2, (canvas.winfo_height() - 300) / 2, font=('Verdana', 40),
                           text="YOU BEAT THE HIGH SCORE!",
                           fill="#00FF00")
        canvas.create_text(canvas.winfo_width() / 2, (canvas.winfo_height()-100) / 2, font=('Verdana', 40), text="NEW HIGH SCORE:{}".format(score),
                           fill="#00FF00")
    else:
        canvas.create_text(canvas.winfo_width() / 2, (canvas.winfo_height() - 300) / 2, font=('Verdana', 50),
                           text="HIGH SCORE:{}".format(prev_high_score),
                           fill="#FF0000")
        canvas.create_text(canvas.winfo_width() / 2, (canvas.winfo_height() - 100) / 2, font=('Verdana', 50),
                           text="YOUR SCORE:{}".format(score),
                           fill="#00FF00")
    file.close()
    canvas.create_text(canvas.winfo_width()/2,(canvas.winfo_height()-550)/2,font=('Verdana',50),text="GAME OVER",fill="#FF0000")
    restart_button=Button(root,text="Restart",command=restart,font=('Verdana',35),bg='#FFFFFF',fg="#000000")
    restart_button.place(x=(canvas.winfo_width()-150)/2,y=(canvas.winfo_height()+200)/2)

def easy():
    global SPEED,easy_button
    SPEED = 120
    restart()
    easy_button.destroy()
    medium_button.destroy()
    hard_button.destroy()
def medium():
    global SPEED,medium_button
    SPEED = 80
    restart()
    easy_button.destroy()
    medium_button.destroy()
    hard_button.destroy()
def hard():
    global SPEED,hard_button
    SPEED = 50
    restart()
    easy_button.destroy()
    medium_button.destroy()
    hard_button.destroy()

root=Tk()
root.title("Snek game")
root.resizable(False,False)

score=0
#dir='right'

label=Label(root,text="SCORE:{}".format(score),font=('Verdana',30))
label.place(x=250,y=10)
label.pack()

file=open('score.txt','r')
prev_high_score=int(file.read())
label2=Label(root,text="HIGH SCORE:{}".format(prev_high_score),font=('Verdana',30))
label2.place(x=0,y=0)
file.close()
canvas=Canvas(root,bg="#000000",height=GAME_HEIGHT,width=GAME_HEIGHT)

#checkered_tiles()
canvas.pack()
root.bind('<Left>', lambda event: change_dir('left'))
root.bind('<Right>', lambda event: change_dir('right'))
root.bind('<Down>', lambda event: change_dir('down'))
root.bind('<Up>', lambda event: change_dir('up'))
restart_button=Button()

easy_button=Button(root,text="Easy",command=easy,font=('Verdana',35),bg='#FFFFFF',fg="#FFC247")
medium_button=Button(root,text="Medium",command=medium,font=('Verdana',35),bg='#FFFFFF',fg="#DF7E20")
hard_button=Button(root,text="Hard",command=hard,font=('Verdana',35),bg='#FFFFFF',fg="#FF0000")

easy_button.place(x=130,y=350)
medium_button.place(x=260,y=350)
hard_button.place(x=440,y=350)

'''
snake=Snake()
food=Food()
restart_button=Button()
next_turn(snake,food)'''
root.mainloop()