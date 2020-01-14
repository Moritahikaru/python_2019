import time
import serial
import csv
import tkinter as tk
import tkinter.filedialog as tkFileDialog
import tkinter.font as tkFont
import matplotlib.pyplot as plt

x=0
y=0
L=[] #dataを保存
fre=0 #測定範囲の最小値
laf=0 #1目盛りの周波数
data=0 #測定範囲の最大値
ser1=0 #送電側のシリアル通信
ser2=0 #受電側のシリアル通信
kHzL=[]
senL=[]
reaL=[]
peff=[]

def maindef():
    global x
    global y
    global L
    global ser
    global fre
    global data
    global laf
    global ser1 
    global ser2 
    
   
    if x==0 and y==0:
        pass
    elif x==1 and y==0:
        x=0
    elif x==0 and y==1:
        #データ受け取り、次の周波数を入力
        line1 = ser1.readline().decode('ascii').rstrip()
        line2 = ser2.readline().decode('ascii').rstrip()
        line3 = str(round(float(line2) / float(line1),3))
        print(fre+" "+line1+" "+line2+" "+line3)
        L.append(fre+" "+line1+" "+line2+" "+line3)
        if int(fre)+int(data) > int(laf) and int(laf) > int(fre):
            fre=str(laf)
        else:
            fre=str(int(fre) + int(data))
        
        if int(fre) > int(laf):
            stop_data()
            x=1
            
        else:
            resend_freq(fre)
    elif x==1 and y==1:
        #データを送らない、後始末
        x=0
        y=0
        send_button.configure(state=tk.NORMAL)
        stop_button.configure(state=tk.NORMAL)
        send_entry.configure(state=tk.NORMAL)
        defalt_entry.configure(state=tk.NORMAL)
        saveas_button.configure(state=tk.NORMAL)
        max_entry.configure(state=tk.NORMAL)
    #測定するとき以外は0.01秒で返す．
    if x==0 and y==1:
        root.after(10000,maindef)
    else:
        root.after(10,maindef)

class Ser:
    def __init__(self):
        self.ser=None
        
    def start_connect(self):
        global ser1
        global ser2
        comport1='COM3' # arduino ideで調べてから。送電側
        comport2='COM4' #受電側必ずcomportは送電側受電側異なるものを使用
        tushinsokudo=57600 # arduinoのプログラムと一致させる。
        timeout=5# エラーになったときのために。とりあえず5秒で戻ってくる。
        ser1=self.ser
        ser2=self.ser
        ser1 = serial.Serial(comport1,tushinsokudo,timeout=timeout)
        ser2 = serial.Serial(comport2,tushinsokudo,timeout=timeout)
        time.sleep(2) # 1にするとダメ！短いほうがよい。各自試す。
        
    def send_com(self):
        global x
        global y
        global data
        global fre
        global laf
        global ser1
        global ser2
        global L
        global kHz
        # v,u,sの文字列は、
        #ぞれぞれv.get(),u.get(),s.get()で取り出す。
        #下部send_entry内のTextvariableでデータ入力
        data=v.get()
        fre=u.get() 
        laf=s.get()
        kHz.clear()
        if data.isdecimal()==True and fre.isdecimal()==True and laf.isdecimal()==True:
                resend_freq(fre)
                print("send incease_fre:"+data+" first_fre:"+fre+" last_fre:"+laf)
                print("frequency transmission_ep receiving_ep power_efficiency")
                L.append("increase_frequency:"+data+" first_frequency:"+fre+" last_frequency:"+laf)
                L.append("frequency transmission_ep receiving_ep power_efficiency")
                time.sleep(8)
                y=1#周波数データ送信完了
        else:
                print("error")
                v.set("")        
    def stop_com(self):
        global x
        stop_data()
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
    
    with open(filename,'w') as fout:
        fout.write("\n".join(L))
#周波数をclock_genelaterに送る
def resend_freq(a):
    global ser1
    global ser2
    ser1.write('a'.encode('ascii')) # arduinoへ開始の合図を送る。
    ser2.write('a'.encode('ascii'))
    ser1.write(a.encode('ascii'))
    ser1.flush() # バッファ内の待ちデータを送りきる。
    ser2.flush()
#ストップするときの関数
def stop_data():
    global ser1
    global ser2
    global fre
    #記録時間が10秒と長いため
    #root.afterがelif x=1 and y=1:にいくまでボタンやエントリーをストップ
    send_button.configure(state=tk.DISABLED)
    stop_button.configure(state=tk.DISABLED)
    send_entry.configure(state=tk.DISABLED)
    defalt_entry.configure(state=tk.DISABLED)
    saveas_button.configure(state=tk.DISABLED)
    max_entry.configure(state=tk.DISABLED)
    
    ser1.write('b'.encode('ascii')) # arduinoへ終了の合図を送る。
    ser2.write('b'.encode('ascii'))
    ser1.flush() # バッファ内の待ちデータを送りきる。
    ser2.flush()
    print("--stop--")
    time.sleep(1) # 安全のため
    L.append("stop")
    fre='0'
        
    
    
root=tk.Tk()
font=tkFont.Font(size=24)
ser=Ser() 
v=tk.StringVar() # tk.TK()の後に書く。
u=tk.StringVar()
s=tk.StringVar()
#ボタン入力
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
label1=tk.Label(root,font=font,text='increase_frequency')
label1.grid(row=1,column=0)
label1_Hz=tk.Label(root,font=font,text='kHz')
label1_Hz.grid(row=1,column=3)
label2=tk.Label(root,font=font,text='first_frequency')
label2.grid(row=2,column=0)
label2_Hz=tk.Label(root,font=font,text='kHz')
label2_Hz.grid(row=2,column=3)
label3=tk.Label(root,font=font,text='last_frequency')
label3.grid(row=3,column=0)
label3_Hz=tk.Label(root,font=font,text='kHz')
label3_Hz.grid(row=3,column=3)

#セーブボタン
saveas_button=tk.Button(root,text='save',font=font,height=2,padx=20,command=saveas)
saveas_button.grid(row=0,column=3)
saveas_button.configure(state=tk.DISABLED)

root.after(10,maindef)
root.mainloop()   
