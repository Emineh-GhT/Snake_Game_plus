
import random
import math
import arcade


W = 700
H = 550
SPEED = 1


#-------------------------------------------------- snake --------------------------------------------------

class Snake(arcade.Sprite):

    def __init__(self, width, height):
        arcade.Sprite.__init__(self)
        self.color = arcade.color.PURPLE
        self.speed = SPEED
        self.width = 25
        self.height = 25
        self.center_x = width//2
        self.center_y = height//2
        self.change_x = 0
        self.change_y = 0
        self.score = 0
        self.snakebody_list = []

    def draw(self):
        arcade.draw_rectangle_filled(self.center_x,self.center_y,25,25,self.color)
        for i in self.snakebody_list:
            arcade.draw_rectangle_filled(i[0],i[1],25,25,self.color)
           
    def move(self):
        for i in range(len(self.snakebody_list)-1, 0, -1):
            self.snakebody_list[i][0] = self.snakebody_list[i-1][0]
            self.snakebody_list[i][1] = self.snakebody_list[i-1][1]
                
        self.center_x += self.speed * self.change_x
        self.center_y += self.speed * self.change_y
        
        if self.snakebody_list:
            self.snakebody_list[0][0] += self.speed * self.change_x
            self.snakebody_list[0][1] += self.speed * self.change_y

    def eat(self):
        self.snakebody_list.append([self.center_x,self.center_y])
        self.score += 1   



#-------------------------------------------------- apple --------------------------------------------------

class Apple(arcade.Sprite):
    def __init__(self, width, height):
        super().__init__("pic/apple.png")
        self.width = 50
        self.height = 50
        self.center_x = random.randint(0, width) //2
        self.center_y = random.randint(0, height) //2


#-------------------------------------------------- poop --------------------------------------------------

class Poop(arcade.Sprite):
    def __init__(self, width, height):
        super().__init__("pic/poop.png")
        self.width = 60
        self.height = 50
        self.center_x = random.randint(0, width) //2
        self.center_y = random.randint(0, height) //2


#-------------------------------------------------- pear --------------------------------------------------

class Pear(arcade.Sprite):
    def __init__(self, width, height):
        super().__init__("pic/pear.png")
        self.width = 50
        self.height = 50
        self.center_x = random.randint(0, width) //2
        self.center_y = random.randint(0, height)  //2



#-------------------------------------------------- Snake Game  --------------------------------------------------

class Snake_Game (arcade.Window):
    def __init__(self):
        arcade.Window.__init__(self, W,H, "Snake Game ")
        self.snake = Snake(W,H)
        self.apple = Apple(W,H)
        self.pear = Pear(W,H)
        self.poop = Poop(W,H)
        self.background = arcade.load_texture("pic/background.jpg")
    def on_draw(self):
        arcade.start_render()
        arcade.draw_texture_rectangle(350, 275, W,H, self.background)
        if self.snake.score > -1 :
            self.apple.draw()
            self.snake.draw()
            self.pear.draw()
            self.poop.draw()
            arcade.draw_text(f"Score: {self.snake.score}",0 ,520 ,arcade.color.MAGENTA, 25)
        else:
            arcade.draw_text("Game  Over!", 160, 250, arcade.color.RED, width=H, font_size = 70, align="center") 
    def on_update(self, delta_time: float):
        A=0
        B=0
        if math.sqrt((self.snake.center_x-self.apple.center_x)**2+(self.snake.center_y-self.apple.center_y)**2)<\
            math.sqrt((self.snake.center_x-self.pear.center_x)**2+(self.snake.center_y-self.pear.center_y)**2):
            A=self.apple.center_x
            B=self.apple.center_y
        else :
            A=self.pear.center_x   
            B=self.pear.center_y
        FR=True
        FL=True
        FT=True
        FB=True
        if self.snake.center_x<self.poop.center_x and self.snake.center_y==self.poop.center_y:
            FR=False
        if self.snake.center_x>self.poop.center_x and self.snake.center_y==self.poop.center_y:
            FL=False
        if self.snake.center_x==self.poop.center_x and self.snake.center_y<self.poop.center_y:
            FT=False
        if self.snake.center_x==self.poop.center_x and self.snake.center_y>self.poop.center_y:
            FB=False
        if  FL and self.snake.center_x > A:
            self.snake.change_x = -1
            self.snake.change_y = 0
            self.snake.move()
        elif FR and  self.snake.center_x < A:
            self.snake.change_x = 1
            self.snake.change_y = 0
            self.snake.move()
        elif FT and self.snake.center_y < B:
            self.snake.change_y = 1
            self.snake.change_x = 0
            self.snake.move()
        elif FB and self.snake.center_y > B:
            self.snake.change_y = -1
            self.snake.change_x = 0
            self.snake.move()
        if arcade.check_for_collision(self.snake,self.apple):
            self.apple = Apple(W,H)
            self.snake.eat()
        if arcade.check_for_collision(self.snake,self.pear):
            self.pear = Pear(W,H)    
            self.snake.eat()
            self.snake.eat()
        if arcade.check_for_collision(self.snake,self.poop):
            self.poop = Poop(W,H)  
            self.snake.score-=1
            if(self.snake.score>0):
               self.snake.snakebody_list.pop(-1)
        if (self.snake.center_x < 0) or (self.snake.center_x > W) or (self.snake.center_y < 0) or (self.snake.center_y > H) : 
            self.snake.score = -1   
        arcade.draw_text(f"Score: {self.snake.score}",570 ,50 ,arcade.color.MAGENTA ,25)



Snake_Game  = Snake_Game ()
arcade.run()