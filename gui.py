from tkinter import *
import colorsys
from groups import *
import time
from random import randint


master = Tk()

WIDTH = 720
HEIGHT = 720

G = dihedral(5000)

t0 = time.time_ns()
A = ordersDepr(G)
t1 = time.time_ns()
B = orders(G)
t2 = time.time_ns()

print("O(n^2):",(t1-t0)/1e9,"s")
print("O(nlog(n)):",(t2-t1)/1e9,"s")

canvas = Canvas(master, width=WIDTH, height=HEIGHT)

canvas.pack()
img = PhotoImage(width=len(G), height=len(G))
canvas.create_rectangle(0,0,WIDTH,HEIGHT,fill="white")

def drawCayleyTable():
    global finalimg
    colors = list()
    if len(G) == 1:
        colors = ["#ff0000"]
    else: 
        for k in range(len(G)):
            col = colorsys.hsv_to_rgb(0.75*k/(len(G)-1),1,1)
            hexcol = "#"+"%02X" % int(col[0]*255)+"%02X" % int(col[1]*255)+"%02X" % int(col[2]*255)
            colors.append(hexcol)
            
    for i in range(len(G)):
        img.put(" ".join([colors[G[i][j]] for j in range(len(G))]), [i,0])

    finalimg = img.zoom(WIDTH//len(G),HEIGHT//len(G))
    canvas.create_image(WIDTH//2,HEIGHT//2, image = finalimg, state="normal")
    canvas.update()
    
def drawCayleyGraph():
    points = [(randint(WIDTH*1//10,WIDTH*9//10),randint(HEIGHT*1//10,HEIGHT*9//10)) for g in range(len(G))]
    gens = [1,3]
    gencol = ["#ff0000","#0000ff"]

    for p in points:
        canvas.create_oval(p[0]-5,p[1]-5,p[0]+5,p[1]+5,fill="green")

    for p in range(len(points)):
        for gen in range(len(gens)):
            product = G[p][gens[gen]]
            canvas.create_line(points[p][0],points[p][1],points[product][0],points[product][1], arrow=LAST, fill=gencol[gen])
    
    canvas.update()
    
##G = groups.falseWitness(17407) 17425

##drawCayleyTable()
##drawCayleyGraph()






def write():
    img.write("FW17407.png", format="png")
