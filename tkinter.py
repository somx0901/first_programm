from tkinter import *
from tkinter import ttk #чтобы кнопки и другие элементы были более красивые
###tkinter._test()
##root=Tk()
##canv=Canvas(root,width=400,height=400,bg='lightblue',cursor="pencil")
##canv.pack()
##button_find_comport=Button()
##button_find_comport['text']="Com-port"
##text=Text(root,width=30,height=10,font="Verdana 12",wrap=WORD)
##text.insert(INSERT,"hfgggbfgf",'a')
##canv.create_window(50,15,window=button_find_comport) # чтобы кнопка была внутри canvas
##canv.create_window(250,100,window=text) # чтобы кнопка была внутри canvas
##canv.pack()
##root.mainloop()


def callback():
    print("press")

root=Tk()
Label(root,text="АЛКОТЕКТОР ЮПИТЕР BLUETOOTH").pack()
button=ttk.Button(root,text="alcotector")
##button_old=Button(root,text="alcotector")
##button_old.pack()

button.config(command=callback)
button.pack()

root.mainloop()
