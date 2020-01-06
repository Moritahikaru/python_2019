import time
import serial
import csv
import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.font as tkFont
import tkinter.ttk as ttk
import sqlite3

root=tk.Tk()


x=0
y=0
L=[]
line=0
var=0

def maindef():
    global x
    global y
    global L
    global ser
    global line
    if x==0 and y==0:
        pass
    elif x==1 and y==0:
        x=0
    elif x==0 and y==1:
        #データ受け取り、append
        X=ser.ser
        line = X.readline().decode('ascii').rstrip()
        var=tk.StringVar()
        var.set(line)
        voltage_exit=tk.Entry(root,font=font,textvariable=var) #受け取ったデータをGUIに表示する
        voltage_exit.grid(row=2,column=1)
        print(line) #Python Shellで表示
        L.append(line) #.csvで保存するためにリスト[L]に計測データを追加


    elif x==1 and y==1:
        #データを送らない、後始末
        X=ser.ser
        X.write('b'.encode('ascii')) # arduinoへ終了の合図を送る。
        X.flush() # バッファ内の待ちデータを送りきる。
        print("--stop--")
        time.sleep(1) # 安全のため
        L.append("stop")
        x=0
        y=0
    root.after(10,maindef)

class Ser:
    def __init__(self):
        self.ser=None

    def start_connect(self):
        comport='COM3' # arduino ideで調べてから
        tushinsokudo=57600 # arduinoのプログラムと一致させる。
        timeout=5 # エラーになったときのために。とりあえず１０秒で戻ってくる。
        self.ser = serial.Serial(comport,tushinsokudo,timeout=timeout)
        time.sleep(2) # 1にするとダメ！短いほうがよい。各自試す。

    def send_com(self):
        global x
        global y
        ser=self.ser
        data=v.get() # vの文字列は、v.get()で取り出す。 下部send_entry内のTextvariableでデータ入力
        if data.isdecimal()==True:
                ser.write('a'.encode('ascii')) # arduinoへ開始の合図を送る。
                ser.write(data.encode('ascii'))
                ser.flush() # バッファ内の待ちデータを送りきる。
                print("send: "+data)
                y=1#周波数データ送信完了
#               time.sleep(1) # send直後にreceiveしようとすると、timeoutになるので
        else:
                print("error")
                v.set("")

    def stop_com(self):
        global x
        x=1

    def connect(self):
        self.start_connect()
        send_button.configure(state=tk.NORMAL)
        stop_button.configure(state=tk.NORMAL)
        send_entry.configure(state=tk.NORMAL)
        saveas_button.configure(state=tk.NORMAL)
        connect_button.configure(state=tk.DISABLED)

def saveas():
    global L
    filename=tkFileDialog.asksaveasfilename(defaultextension=".csv",filetypes=[("csv","*.csv*")])
    #kakikomi_csv(filename,L)
    with open(filename,'w') as fout:
        fout.write("\n".join(L))




font=tkFont.Font(size=24)
ser=Ser()
v=tk.StringVar() # tk.TK()の後に書く。



root.title('Function Generator')
#GUI画面
#1段目
connect_button=tk.Button(root,text='connect',font=font,height=2,padx=20,command=ser.connect)
connect_button.grid(row=0,column=0)
send_button=tk.Button(root,text='send',font=font,height=2,padx=20,command=ser.send_com)
send_button.grid(row=0,column=1)
send_button.configure(state=tk.DISABLED)
stop_button=tk.Button(root,text='stop',font=font,height=2,padx=20,command=ser.stop_com)
stop_button.grid(row=0,column=2)
stop_button.configure(state=tk.DISABLED)
saveas_button=tk.Button(root,text='save',font=font,height=2,padx=20,command=saveas)
saveas_button.grid(row=0,column=3)
saveas_button.configure(state=tk.DISABLED)

#2段目
label1=tk.Label(root,font=font,text='Enter Frequency')
label1.grid(row=1,column=0,sticky=(tk.W + tk.E + tk.N + tk.S))
send_entry=tk.Entry(root,font=font,textvariable=v)
send_entry.grid(row=1,column=1,sticky=(tk.W + tk.E + tk.N + tk.S))
send_entry.configure(state=tk.DISABLED)
label_Hz=tk.Label(root,font=font,text='Hz')
label_Hz.grid(row=1,column=2)

#3段目
label2=tk.Label(root,font=font,text='Receive Data')
label2.grid(row=2,column=0)
label_W=tk.Label(root,font=font,text='W')
label_W.grid(row=2,column=2)


root.after(100,maindef)
root.mainloop()
