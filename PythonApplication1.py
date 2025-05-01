

import pygame
import os
from pygame.locals import*
from sys import exit
import astar_real

#directory path
directory_path= os.path.dirname(__file__)
screen= pygame.display.set_mode((500,500))#the frame size
pygame.display.set_caption("Maze Generator and Solver Application")#title of the frame
cursor_img=os.path.join(directory_path,"cursor.png") #"C:\\Users\\174896\\Desktop\\algoProject\\PythonApplication1\"
bg_img=os.path.join(directory_path,"bg.jpg")#"C:\\Users\\174896\\Desktop\\algoProject\\PythonApplication1\\bg.jpg"
pygame.font.init()
titleFont= pygame.font.Font(os.path.join(directory_path,"pixel_font.ttf"),13)#font for title: "C:\\Users\\174896\\Desktop\\algoProject\\PythonApplication1\\pixel_font.ttf"

title= titleFont.render(" Maze Generator and Solver Application",True,(255,255,255))

stroke_surface = titleFont.render(" Maze Generator and Solver Application",True,(0,0,0))

row_num_font= pygame.font.Font(os.path.join(directory_path,"pixel_font.ttf"),14)
row_num_txt= row_num_font.render("Enter number of rows: ",True,(255,255,255))
row_num_stroke= row_num_font.render("Enter number of rows: ",True,(0,0,0))

choose_mode_txt = row_num_font.render("choose the barrier's mode: ",True,((255,255,255)))
choose_mode_stroke= row_num_font.render("choose the barrier's mode: ",True,(0,0,0))

manual_txt = row_num_font.render("Manual",True,((255,255,255)))
manual_stroke= row_num_font.render("Manual",True,(0,0,0))

#dash_txt=row_num_font.render("-",True,((255,255,255)))
#dash_stroke= row_num_font.render("-",True,(0,0,0))

mazeGeneratorFlag=False

mode=-1#no mode for automatic-manual
algo_mode=-1#mode of algorithm
Automatic_txt = row_num_font.render("Automatic",True,((255,255,255)))
Automatic_stroke= row_num_font.render("Automatic",True,(0,0,0))

class pressed:
   def __init__(self,x_pos,y_pos,img,msg):
       self.x_pos=x_pos
       self.y_pos=y_pos
       self.img=img
       self.msg=msg
       self.rect= self.img.get_rect(center=(self.x_pos,self.y_pos))#rectangle around button
       self.msg_rendrer = row_txt_font.render(msg,True,(255,255,255))
       self.check=False
       self.msg_stroke=row_txt_font.render(msg,True,(0,0,0))

       #stroke =  row_txt_font.render(msg,True,(0,0,0))
       self.img_hover= pygame.transform.scale(img,(150,150))
       self.img_hover.set_alpha(150)

       self.img_normal= pygame.transform.scale(img,(100,100))
       self.img_normal.set_alpha(255)

   def updateItem(self,screen,cursor):
     
     
     if self.rect.colliderect(cursor):#collision between two rectangles
        self.img = self.img_hover
        screen.blit(self.img,(self.x_pos,self.y_pos))
        self.msg_rendrer = row_txt_font.render(self.msg,True,(255,0,0))
        self.check=True
            

        screen.blit(self.msg_stroke,(self.x_pos,self.y_pos+181))
        screen.blit(self.msg_stroke,(self.x_pos,self.y_pos+179))
        screen.blit(self.msg_stroke,(self.x_pos+1,self.y_pos+180))
        screen.blit(self.msg_stroke,(self.x_pos-1,self.y_pos+180))
        screen.blit(self.msg_rendrer,(self.x_pos,self.y_pos+180))

     else:
          self.img = self.img_normal
          screen.blit(self.img,(self.x_pos,self.y_pos))
          self.msg_rendrer = row_txt_font.render(self.msg,True,(255,255,255))
          self.check=False


          screen.blit(self.msg_stroke,(self.x_pos,self.y_pos+139))
          screen.blit(self.msg_stroke,(self.x_pos,self.y_pos+141))
          screen.blit(self.msg_stroke,(self.x_pos+1,self.y_pos+140))
          screen.blit(self.msg_stroke,(self.x_pos-1,self.y_pos+140))
          screen.blit(self.msg_rendrer,(self.x_pos,self.y_pos+140))


   def draw(self,screen):

       screen.blit(self.img,(self.x_pos,self.y_pos))
row_txt_font= pygame.font.Font(os.path.join(directory_path,"pixel_font.ttf"),10)
row_txt=""
row_txt_render= row_txt_font.render(row_txt,True,(0,0,0))    
pygame.init()



bg_img=pygame.image.load(bg_img).convert_alpha()#backgroud load
bg_img=pygame.transform.scale(bg_img,(500,500))#background scaling


mouse_cursor=pygame.image.load(cursor_img).convert_alpha()#loading curser image
mouse_cursor=pygame.transform.scale(mouse_cursor,(50,50))#scaling the cursor size
pygame.mouse.set_visible(False)
icon = pygame.image.load(os.path.join(directory_path,"icon.png")).convert_alpha()#"C:\\Users\\174896\\Desktop\\algoProject\\PythonApplication1\\icon.png"
pygame.display.set_icon(icon)



#button creating

#1)A*
A_star= pygame.image.load(os.path.join(directory_path,"A star.jpg")).convert_alpha()#"C:\\Users\\174896\\Desktop\\algoProject\\PythonApplication1\\A star.jpg"
A_star=pygame.transform.scale(A_star,(100,100))

#2)BFS
BFS_img= pygame.image.load(os.path.join(directory_path,"Bfs.jpg")).convert_alpha()#"C:\\Users\\174896\\Desktop\\algoProject\\PythonApplication1\\Bfs.jpg"
BFS_img=pygame.transform.scale(BFS_img,(100,100))

#2)DFS
DFS_img= pygame.image.load(os.path.join(directory_path, "Depth first.jpg")).convert_alpha()#"C:\\Users\\174896\\Desktop\\algoProject\\PythonApplication1\\Depth first.jpg"
DFS_img=pygame.transform.scale(DFS_img,(100,100))


#screen.fill((255,255,255))
A_star_button = pressed(50,200,A_star,"A* algorithm")
BFS_button = pressed(200,200,BFS_img,"BFS algorithm")
DFS_button = pressed(350,200,DFS_img,"DFS algorithm")



#Automatic-manual selector object
#automanual= mode(60,450,350,450,"Automatic","manual")
run= True
while run:
    for event in pygame.event.get():
        if event.type==QUIT:
            exit()
        elif event.type== pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                row_txt=""
                row_txt_render= row_txt_font.render(row_txt,True,(0,0,0)) 
            elif event.key == pygame.K_RIGHT:
                manual_txt= row_num_font.render("Manual",True,((255,0,0)))
                mode=1#manual
                Automatic_txt = row_num_font.render("Automatic",True,((255,255,255)))
            elif event.key == pygame.K_LEFT:
                manual_txt= row_num_font.render("Manual",True,((255,255,255)))
                Automatic_txt = row_num_font.render("Automatic",True,((255,0,0)))
                mode=0#automatic
            else:
                if len(row_txt)<2:
                    row_txt+= str(event.unicode)
                    row_txt_render= row_txt_font.render(row_txt,True,(0,0,0))    
        if pygame.mouse.get_pressed()[0] and A_star_button.check:
            try:
                if int(row_txt)>50 or int(row_txt)<10 or mode == -1:
                    raise("invalid number of rows")
                print(int(row_txt)," in A*")#here is our A* logic
                algo_mode=0#A*
                run=False
                mazeGeneratorFlag=True
            except:
                print("error")
        elif pygame.mouse.get_pressed()[0] and BFS_button.check:
              try:
                if int(row_txt)>50 or int(row_txt)<10 or mode == -1:
                    raise("invalid number of rows")
                print(int(row_txt)," in BFS")#here is our BFS logic
                algo_mode=1#BFS
                run=False
                mazeGeneratorFlag=True
              except:
                print("error")
        elif pygame.mouse.get_pressed()[0] and DFS_button.check:
             try:
                if int(row_txt)>50 or int(row_txt)<10 :
                    raise("invalid number of rows")
                print(int(row_txt)," in DFS")#here is our DFS logic
                algo_mode=2#DFS
                run=False
                mazeGeneratorFlag=True
             except:
                print("error")
    x,y = pygame.mouse.get_pos()
    x-= mouse_cursor.get_width()/2
    y-= mouse_cursor.get_height()/2

    mouse_rect=mouse_cursor.get_rect(topleft=(x-40,y-40))#to cover the whole cursor image

    screen.blit(bg_img,(0,0))

    #drawing text field

    #strokes for text box
    pygame.draw.rect(screen,(0,0,0),pygame.Rect(352,100,60,20))
    pygame.draw.rect(screen,(0,0,0),pygame.Rect(348,100,60,20))
    pygame.draw.rect(screen,(0,0,0),pygame.Rect(350,98,60,20))
    pygame.draw.rect(screen,(0,0,0),pygame.Rect(350,102,60,20))
    #the text field itself
    pygame.draw.rect(screen,(255,255,255),pygame.Rect(350,100,60,20))
   

   
    #strokes for "choose your row: "
    screen.blit(row_num_stroke,(12,100))
    screen.blit(row_num_stroke,(8,100))
    screen.blit(row_num_stroke,(10,98))
    screen.blit(row_num_stroke,(10,102))
    #drawing the text next to text field
    screen.blit(row_num_txt,(10,100))

    #Algorithms images bliting(using pressed class objects)
    BFS_button.updateItem(screen,mouse_rect)
    DFS_button.updateItem(screen,mouse_rect)
    A_star_button.updateItem(screen,mouse_rect)
    

    #strokes are 5 text messages above each other
    screen.blit(stroke_surface,(-1,20))
    screen.blit(stroke_surface,(3,20))
    screen.blit(stroke_surface,(1,18))
    screen.blit(stroke_surface,(1,22))

    #title
    screen.blit(title,(1,20))

    
    #strokes for text mode statement(order is important)
    screen.blit(choose_mode_stroke,(12,420))
    screen.blit(choose_mode_stroke,(8,420))
    screen.blit(choose_mode_stroke,(10,422))
    screen.blit(choose_mode_stroke,(10,418))
    #choose the mode text
    screen.blit(choose_mode_txt,(10,420))

    #screen.blit(BFS_img,(200,200))
    #screen.blit(DFS_img,(350,200))
    screen.blit(row_txt_render,(350,100))
    screen.blit(mouse_cursor,(x,y))
   
    #stroke of manual
    screen.blit(manual_stroke,(251,450))
    screen.blit(manual_stroke,(249,450))
    screen.blit(manual_stroke,(250,451))
    screen.blit(manual_stroke,(250,449))
   
     #manual
    screen.blit(manual_txt,(250,450))

    #stroke of automatic
    screen.blit(Automatic_stroke,(11,450))
    screen.blit(Automatic_stroke,(9,450))
    screen.blit(Automatic_stroke,(10,451))
    screen.blit(Automatic_stroke,(10,449))

     #automatic
    screen.blit(Automatic_txt,(10,450))


    pygame.display.update()
WIN= pygame.display.set_mode((600,600))
pygame.mouse.set_visible(True)
if mazeGeneratorFlag:
       row_txt_handled=(int(row_txt)//10)*10
       astar_real.main(WIN,600,row_txt_handled,algo_mode,mode)#add parameter of manual and automatic
   #32/10= 3*10=30

