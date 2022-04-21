import pygame
import math
import time
pygame.init()
WIN_HEIGHT = 900
WIN_WIDTH =1500
n=9
show_steps=1
size=int(WIN_HEIGHT/n)
font = pygame.font.SysFont("comicsansms", size)
time_font = pygame.font.SysFont("comicsansms", (size//2))

red=(255,0,0)
white=(255,255,255)

class grid:
    def __init__(self,n):
        self.n=n
        self.table=[]
        
    def print(self):
        for i in self.table:
            print(i)
    
    def draw(self,win):
        j=0
        for i in range(0,WIN_HEIGHT+size,size):
            if j%3==0:
                pygame.draw.line(win, (255,255,255), (0,i-2), (WIN_HEIGHT,i-2))
                pygame.draw.line(win, (255,255,255), (0,i+2), (WIN_HEIGHT,i+2))
                pygame.draw.line(win, (255,255,255), (i-2,0), (i-2,WIN_HEIGHT))
                pygame.draw.line(win, (255,255,255), (i+2,0), (i+2,WIN_HEIGHT))


            pygame.draw.line(win, (255,255,255), (0,i), (WIN_HEIGHT,i))
            pygame.draw.line(win, (255,255,255), (i,0), (i,WIN_HEIGHT))
            j+=1
    


class number:
    def __init__(self,value,pos):
        self.value=value
        self.pos=pos
        self.is_default=0
        self.is_current=0

    def draw(self,win):

        x=(self.pos[0]-1)*size
        y=(self.pos[1]-1)*size
        if self.is_current:
            pygame.draw.rect(win, (0,255,0), [x,y,size,size])
        if self.value!=0:
            if self.is_default:
                color=red
            else:
                color=white
            text=font.render(str(self.value), True, color)
            win.blit(text,(x+(size/4),y+(size/4)))


def display(win,sudoku_grid,sudoku,times):

    win.fill((0,0,0))
    for lines in sudoku:
        for number in lines:
            number.draw(win)
    sudoku_grid.draw(win)
    for i,time_taken in enumerate(times):
        text=time_font.render('Problem '+str(i+1)+': '+str(time_taken), True, red)
        win.blit(text,(1000,WIN_HEIGHT/len(times)*i))
    
    pygame.display.update()





def create_sudoku(name):
    numbers=[]
    with open(name,'r') as problem:
        line="1"
        j=0
        while(line):
            j+=1
            line=problem.readline()
            i=0
            temp=[]
            for value in line.split():
                i+=1
                num=number(int(value), (i,j))
                if num.value!=0:
                    num.is_default=1
                temp.append(num)
            numbers.append(temp)
    
    return numbers




def is_possible(sudoku,value,pos):
    for i in range(n):
        if  sudoku[i][pos[1]].value==value:
            return False
        elif sudoku[pos[0]][i].value==value:
            return False
        k=int(n/math.sqrt(n))
        x1=(k*((pos[0])//k))+(i%k)
        y1=(k*((pos[1])//k))+(i//k)
        if sudoku[x1][y1].value==value:
            return False
    return True



def solve_sudoku(sudoku,pos,win,sudoku_grid,times):
    if pos[0]==n and pos[1]>=n-1:
        sudoku[pos[0]-1][pos[1]].is_current=0
        return True
    

    if pos[0]>8:
        pos=(0,pos[1]+1)
    if sudoku[pos[0]][pos[1]].is_default:
        return solve_sudoku(sudoku,(pos[0]+1,pos[1]), win, sudoku_grid,times)
    sudoku[pos[0]][pos[1]].is_current=1
    if show_steps:
        display(win, sudoku_grid, sudoku,times)
    for i in range(0,n+1):
        if is_possible(sudoku, i, pos):
                sudoku[pos[0]][pos[1]].value=i
                sudoku[pos[0]][pos[1]].is_current=0
                if solve_sudoku(sudoku,(pos[0]+1,pos[1]), win, sudoku_grid,times):
                    return True
                sudoku[pos[0]][pos[1]].is_current=0
                sudoku[pos[0]][pos[1]].value=0
    sudoku[pos[0]][pos[1]].is_current=0
    
    return False               
    

def main():
    global n
    sudoku_grid=grid(n)
    win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT));
    names=['problem1.txt','problem2.txt']
    sudokus=[]
    times=[]
    for name in names:
        sudokus.append(create_sudoku(name))
    start=1
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run=False    
                pygame.quit()
                quit()
        if start==1:
            time.sleep(10)
            for sudoku in sudokus:
                display(win, sudoku_grid, sudoku,times)
                start_time=time.time()
                solve_sudoku(sudoku, (0,0),win,sudoku_grid,times)
                time_taken=time.time()-start_time
                print(time_taken)
                times.append(time_taken)
                display(win, sudoku_grid, sudoku,times)
                time.sleep(2)
            start=0
main()
