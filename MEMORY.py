# implementation of card game - Memory

import simplegui
import random

list = range(0,8)
list1 = range(0,8)
list.extend(list1)
exposed = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
moves = 0
c1 = 0
c2 = 1
state = 0



# helper function to initialize globals
def new_game():
    global exposed,list,moves
    exposed = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False]
    random.shuffle(list)
    moves = 0

     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global exposed,moves,c1,c2,state,list
    
    if 0 <= pos[1] <= 99 and exposed[(pos[0] // 50)] == False:
        
        if state == 0:
            state = 1
            c1 = pos[0] // 50
            exposed[(pos[0] // 50)] = True
        elif state == 1:
            state = 2
            c2 = pos[0] // 50
            exposed[(pos[0] // 50)] = True
            moves += 1
        elif state == 2:
            state = 1
            if list[c1] != list[c2]:
                exposed[c1] = False
                exposed[c2] = False
            c1 = pos[0] // 50
            exposed[pos[0] // 50] = True    
                        
    
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global exposed
    label.set_text("Moves = " + str(moves))
    
    for num in range(len(exposed)):
           
            if exposed[num] == True:
                
             canvas.draw_text(str(list[num]),(num * 52,60),42,"White")
             
                
            elif exposed[num] == False:
          
             canvas.draw_polygon([[num * 50,0],[(num+1)*50,0],[(num + 1)* 50,100],[num * 50,100]],3,"Red","Green")
             
         
         
# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", new_game)
label = frame.add_label("Moves = 0")

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()

