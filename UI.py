# importing Tkinter and other modules 
from tkinter import *
from CFG import Grammer
from calculator import calculate

root = Tk() 

root.title('Calulator') 
root.geometry() 
e = Entry(root) 
e.grid(row=0,column=0,columnspan=6,pady=3) 
e.focus_set()

def equals(): 
    expression = e.get()
    text = expression.replace('x','*')
    result = calculate(text)
    e.delete(0,END) 
    e.insert(0,result) 

  
def clear_one(): 
    txt=e.get()[:-1] 
    e.delete(0,END) 
    e.insert(0,txt) 


# Creating Buttons 
Button(root,text='AC',width=5,height=3, 
        fg="red", bg="green", 
        command=lambda:e.delete(0,END)).grid(row=1, column=4) 

Button(root,text='C',width=5,height=3, 
        fg="red",bg="green", 
        command=lambda:clear_one()).grid(row=1, column=5) 

Button(root,text="(+)",width=5,height=3, 
        fg="red",bg="green", 
        command=lambda:e.insert(END, '(+)')).grid(row=2, column=4) 

Button(root,text="(-)",width=5,height=3, 
        fg="red",bg="green", 
        command=lambda:e.insert(END, '(-)')).grid(row=2, column=5)

Button(root,text="+",width=5,height=3, 
        fg="blue",bg="green", 
        command=lambda:e.insert(END, '+')).grid(row=3, column=4) 

Button(root,text="-",width=5,height=3, 
        fg="blue",bg="green", 
        command=lambda:e.insert(END, '-')).grid(row=3, column=5)

Button(root,text="=",width=11,height=3,
        fg="blue", bg="green",
        command=lambda:equals()).grid(row=4, column=4,columnspan=2) 

Button(root,text="÷",width=5,height=3, 
        fg="blue",bg="green", 
        command=lambda:e.insert(END, '/')).grid(row=1, column=3)

Button(root,text="x",width=5,height=3, 
        fg="blue",bg="green", 
        command=lambda:e.insert(END, 'x')).grid(row=2, column=3) 

Button(root,text="^",width=5,height=3, 
        fg="blue",bg="green", 
        command=lambda:e.insert(END, '^')).grid(row=3, column=3) 

Button(root,text=".",width=5,height=3, 
        fg="black",bg="green", 
        command=lambda:e.insert(END, '.')).grid(row=4, column=3) 

Button(root,text="0",width=17,height=3, 
        fg="black",bg="green", 
        command=lambda:e.insert(END, '0')).grid(row=4, column=0, columnspan=3) 

Button(root,text="1",width=5,height=3, 
        fg="black",bg="green", 
        command=lambda:e.insert(END, '1')).grid(row=3, column=0) 

Button(root,text="2",width=5,height=3, 
        fg="black",bg="green", 
        command=lambda:e.insert(END, '2')).grid(row=3, column=1) 

Button(root,text="3",width=5,height=3, 
        fg="black",bg="green", 
        command=lambda:e.insert(END, '3')).grid(row=3, column=2) 

Button(root,text="4",width=5,height=3, 
        fg="black",bg="green", 
        command=lambda:e.insert(END, '4')).grid(row=2, column=0) 

Button(root,text="5",width=5,height=3, 
        fg="black",bg="green", 
        command=lambda:e.insert(END, '5')).grid(row=2, column=1) 

Button(root,text="6",width=5,height=3, 
        fg="black",bg="green", 
        command=lambda:e.insert(END, '6')).grid(row=2, column=2) 

Button(root,text="7",width=5,height=3, 
        fg="black",bg="green", 
        command=lambda:e.insert(END, '7')).grid(row=1, column=0) 

Button(root,text="8",width=5,height=3, 
        fg="black",bg="green", 
        command=lambda:e.insert(END, '8')).grid(row=1, column=1) 

Button(root,text="9",width=5,height=3, 
        fg="black",bg="green", 
        command=lambda:e.insert(END, '9')).grid(row=1, column=2)

root.mainloop() 