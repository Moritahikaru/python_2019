import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog as Filedialog
import tkinter.font as tkFont
import math
import matplotlib.pyplot as plt
import numpy as np
import csv
L=[]
n=0.000000001
u=0.000001
m=0.001
k=1000
def run():
    global L
    global n
    global u
    global m
    global k
    L=[]
    u0=5.0
    L1=23.6*u
    L2=23.6*u
    C1=108.0*n
    C2=108.0*n
    M=1.98*u
    R1=0.08
    R2=0.08
    RL=25.0
    data=v1.get()
    frfre=v2.get()
    lasfre=v3.get()
    if data.isdecimal()==True and frfre.isdecimal()==True and lasfre.isdecimal()==True:
        
        fldata=float(data)*0.001
        flfr=float(frfre)
        fllas=float(lasfre)
        freq=round(flfr,3)
        while freq <= fllas:
            omega=2*math.pi*freq*k
            u=energy_power(u0,L1,L2,C1,C2,M,R1,R2,RL,omega)
            print(str(freq)+" "+u)
            if freq+fldata > fllas and fllas > freq:
                freq=round(fllas,3)
            else:
                freq=round(freq+fldata,3)
    else:
        v1.set("")
        v2.set("")
        v3.set("")
        print("error!!")
        
def energy_power(u0,L1,L2,C1,C2,M,R1,R2,RL,o):
    C12=pow(C1,2)
    C22=pow(C2,2)
    L12=pow(L1,2)
    L22=pow(L2,2)
    M2=pow(M,2)
    M4=pow(M,4)
    R12=pow(R1,2)
    R22=pow(R2,2)
    RL2=pow(RL,2)
    o2=pow(o,2)
    o4=pow(o,4)
    o6=pow(o,6)
    o8=pow(o,8)
    x1=(u0**2*C12*o2)*(C22*M2*RL2*o4+C22*M2*R2*o4+C22*L22*R1*o4+C22*R1*RL2*o2+2*C22*R1*R2*RL*o2+C22*R1*R22*o2-2*C2*L2*R1*o2+R1)
    y=2*(C12*C22*M4*o8-2*C12*C22*L1*L2*M2*o8+C12*C22*L12*L22*o8+C12*C22*L12*RL2*o6+2*C12*C22*L12*R2*RL*o6+2*C12*C22*M2*R1*RL*o6+C12*C22*L12*R22*o6+2*C12*C22*M2*R1*R2*o6+C12*C22*L22*R12*o6+2*C1*C22*L2*M2*o6+2*C12*C2*L1*M2*o6-2*C1*C22*L1*L22*o6-2*C12*C2*L12*L2*o6+C12*C22*R12*RL*2*o4-2*C1*C22*L1*RL2*o4+2*C12*C22*R12*R2*RL*o4-4*C1*C22*L1*R2*RL*o4+C12*C22*R12*R22*o4-2*C1*C22*L1*R22*o4-2*C12*C2*L2*R12*o4-2*C1*C2*M2*o4+C22*L22*o4+4*C1*C2*L1*L2*o4+C12*L12*o4+C22*RL2*o2+2*C22*R2*RL*o2+C12*R22*o2+C12*R12*o2-2*C2*L2*o2-C1*L1*o2+1)
    x2=u0**2*C12*C22*M2*RL*o6
    p1=x1/y
    p2=x2/y
    nu=(C22*M2*RL*o4)/(C22*M2*RL2*o4+C22*M2*R2*o4+C22*L22*R1*o4+C22*R1*RL2*o2+2*C22*R1*R2*RL*o2+C22*R1*R22*o2-2*C2*L2*R1*o2+R1)
    return str(p1)+" "+str(p2)+" "+str(nu)

def save():
    pass
def plot():
    pass

root=tk.Tk()
v1=tk.StringVar()
v2=tk.StringVar()
v3=tk.StringVar()

font=tkFont.Font(size=13)
#entry
ent1=tk.Entry(root,font=font,textvariable=v1)
ent1.grid(row=0,column=1,columnspan=1)
ent2=tk.Entry(root,font=font,textvariable=v2)
ent2.grid(row=1,column=1,columnspan=1)
ent3=tk.Entry(root,font=font,textvariable=v3)
ent3.grid(row=2,column=1,columnspan=1)

#label
label1=tk.Label(root,font=font,text='increase_frequency')
label1.grid(row=0,column=0)
label1_Hz=tk.Label(root,font=font,text='Hz')
label1_Hz.grid(row=0,column=2)
label2=tk.Label(root,font=font,text='first_frequency')
label2.grid(row=1,column=0)
label2_Hz=tk.Label(root,font=font,text='kHz')
label2_Hz.grid(row=1,column=2)
label3=tk.Label(root,font=font,text='last_frequency')
label3.grid(row=2,column=0)
label3_Hz=tk.Label(root,font=font,text='kHz')
label3_Hz.grid(row=2,column=2)

#button
run_button=tk.Button(root,text='run',font=font,height=1,padx=10,command=run)
run_button.grid(row=3,column=0)
save_button=tk.Button(root,text='save',font=font,height=1,padx=10,command=save)
save_button.grid(row=3,column=1)
plot_button=tk.Button(root,text='plot',font=font,height=1,padx=10,command=plot)
plot_button.grid(row=3,column=2)
root.mainloop()
