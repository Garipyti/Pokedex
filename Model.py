import pandas as pd
from abc import ABC, abstractmethod
from tkinter import *
from tkinter import ttk
root=Tk()
cStringVar=StringVar(root,'sensclassement')
classementC=Radiobutton(root, variable=cStringVar, value="C" )
classementC.place(x=350,y=100)
labelclassementC=Label(root,text='croissant')
labelclassementC.place(x=400,y=100)
classementD=Radiobutton(root,variable=cStringVar,value="D")
classementD.place(x=350,y=120)
labelclassementD=Label(root,text='décroissant')
labelclassementD.place(x=400,y=120)





