import time
import serial
import csv
import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.font as tkFont

x=0
y=0
L=[]
fre='0'
laf='0'
data='0'
ep=0.0
var=0

def maindef():
    global x
    global y
    global L
    global ser
    global fre
    global data
    global laf
    global ep
    X=ser.ser
    if x==0 and y==0:
        pass
    elif x==1 and y==0:
        x=0
    elif x==0 and y==1:
        #データ受け取り、appen
        var=tk.StringVar()
        var.set(fre)
        voltage_exit=tk.Entry(root,font=font,textvariable=var) #受け取ったデータをGUIに表示する
        voltage_exit.grid(row=4,column=1)
        line = X.readline().decode('ascii').rstrip()
        ep = line
        print(fre+" "+line)
        
        L.append(line)
        fre=str(int(fre) + int(data))
        if int(fre) > int(laf):
            x=1
            root.after(10,maindef)
        else:
            pass
        
        X.write('a'.encode('ascii')) # arduinoへ開始の合図を送る。 
        X.write(fre.encode('ascii'))
        X.flush() # バッファ内の待ちデータを送りきる。
        time.sleep(1)
    elif x==1 and y==1:
        #データを送らない、後始末
        X.write('b'.encode('ascii')) # arduinoへ終了の合図を送る。
        X.flush() # バッファ内の待ちデータを送りきる。
        
        print("--stop--")
        time.sleep(1) # 安全のため
        L.append("stop")
        x=0
        y=0
    if x==0 and y==1:
        root.after(8000,maindef)
    else:
        root.after(10,maindef)

class Ser:
    def __init__(self):
        self.ser=None
        
    def start_connect(self):
        comport1='COM3' # arduino ideで調べてから。
        tushinsokudo=57600 # arduinoのプログラムと一致させる。
        timeout=5 # エラーになったときのために。とりあえず１０秒で戻ってくる。
        self.ser = serial.Serial(comport,tushinsokudo,timeout=timeout)
        time.sleep(2) # 1にするとダメ！短いほうがよい。各自試す。
        
    def send_com(self):
        global x
        global y
        global data
        global fre
        global laf
        #global var
        ser=self.ser
        data=v.get() # vの文字列は、v.get()で取り出す。 下部send_entry内のTextvariableでデータ入力
        fre=u.get()
        laf=s.get()
        if data.isdecimal()==True and fre.isdecimal()==True and laf.isdecimal()==True:
                ser.write('a'.encode('ascii')) # arduinoへ開始の合図を送る。 
                ser.write(fre.encode('ascii'))
                ser.flush() # バッファ内の待ちデータを送りきる。
                print("send: "+data)
                time.sleep(10) # send直後にreceiveしようとすると、timeoutになるので
                y=1#周波数データ送信完了
        else:
                print("error")
                v.set("")
    def Re_send(self):
        global data
        global fre
        ser=self.ser
        #fre=str(int(fre) + int(data))
        #ser.write('a'.encode('ascii')) # arduinoへ開始の合図を送る。 
        #ser.write(fre.encode('ascii'))
        #ser.flush() # バッファ内の待ちデータを送りきる。
        #time.sleep(1)
        
    def stop_com(self):
        global x
        x=1

    def connect(self):
        self.start_connect()
        send_button.configure(state=tk.NORMAL)
        stop_button.configure(state=tk.NORMAL)
        send_entry.configure(state=tk.NORMAL)
        defalt_entry.configure(state=tk.NORMAL)
        saveas_button.configure(state=tk.NORMAL)
        max_entry.configure(state=tk.NORMAL)
        connect_button.configure(state=tk.DISABLED)

def saveas():
    global L
    filename=tkFileDialog.asksaveasfilename(defaultextension=".csv",filetypes=[("csv","*.csv*")])
    #kakikomi_csv(filename,L)
    with open(filename,'w') as fout:
        fout.write("\n".join(L))
        
root=tk.Tk()
font=tkFont.Font(size=24)
ser1=Ser() #
ser2=
v=tk.StringVar() # tk.TK()の後に書く。
u=tk.StringVar()
s=tk.StringVar()
connect_button=tk.Button(root,text='connect',font=font,height=2,padx=20,command=ser.connect)
connect_button.grid(row=0,column=0)
send_button=tk.Button(root,text='send',font=font,height=2,padx=20,command=ser.send_com)
send_button.grid(row=0,column=1)
send_button.configure(state=tk.DISABLED)
stop_button=tk.Button(root,text='stop',font=font,height=2,padx=20,command=ser.stop_com)
stop_button.grid(row=0,column=2)
stop_button.configure(state=tk.DISABLED)
#entry
send_entry=tk.Entry(root,font=font,textvariable=v)
send_entry.grid(row=1,column=1,columnspan=2)
send_entry.configure(state=tk.DISABLED)
defalt_entry=tk.Entry(root,font=font,textvariable=u)
defalt_entry.grid(row=2,column=1,columnspan=2)
defalt_entry.configure(state=tk.DISABLED)
max_entry=tk.Entry(root,font=font,textvariable=s)
max_entry.grid(row=3,column=1,columnspan=2)
max_entry.configure(state=tk.DISABLED)

#label
label1=tk.Label(root,font=font,text='enter_division')
label1.grid(row=1,column=0)
label1_Hz=tk.Label(root,font=font,text='Hz')
label1_Hz.grid(row=1,column=3)
label2=tk.Label(root,font=font,text='first_frequency')
label2.grid(row=2,column=0)
label2_Hz=tk.Label(root,font=font,text='Hz')
label2_Hz.grid(row=2,column=3)
label3=tk.Label(root,font=font,text='last_frequency')
label3.grid(row=3,column=0)
label3_Hz=tk.Label(root,font=font,text='Hz')
label3_Hz.grid(row=3,column=3)
label4_Hz=tk.Label(root,font=font,text='Hz')
label4_Hz.grid(row=4,column=2)

saveas_button=tk.Button(root,text='save',font=font,height=2,padx=20,command=saveas)
saveas_button.grid(row=0,column=3)
saveas_button.configure(state=tk.DISABLED)

root.after(10,maindef)
root.mainloop()   
