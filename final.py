# -*- coding: utf-8 -*-
"""
Created on Sat Dec 25 02:29:59 2021

@author: Tim
"""


import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
from numpy.fft import fft


def main():
    def selectExcelfile():
        sfname = filedialog.askopenfilename()
        print(sfname)
        text1.insert(tk.INSERT,sfname)
        return sfname
    
    

    def doProcess():
        data=pd.read_csv(selectExcelfile())
        data.columns=['time','amp']
        f = Figure(figsize=(15, 15), dpi=50)
        a = f.add_subplot(211)
        b = f.add_subplot(212)

        t = data['time']
        s = data['amp']
        t1=np.array(t)
        print(t1)
        s1=np.array(s)
        L = len(t)
        fs =256
        freq= np.arange(0, round(0.5 * L)+1)
        freq = fs * freq / L
        amp_fft=fft(s1)
        abs_amp_fft = abs(amp_fft/L)
        P1 = abs_amp_fft[0:round(0.5 * L + 1)]
        P1[1:round(0.5 * L)] = 2 * P1[1:round(0.5 * L)]
        a.plot(t, s)
        a.set_title('Origin signal')
        b.plot(freq,P1)
        b.set_title('FFT signal')
        canvas = FigureCanvasTkAgg(f, master=root)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)

        def processing():
            f_xDC = freq[1:len(freq[0:800])+1]
            P1_xDC = abs_amp_fft[1:len(freq[0:800])+1]
            max_index = np.argsort(P1_xDC)
            
            return f_xDC,P1_xDC,max_index
        def processing_print():
            f_xDC=processing()[0]
            P1_xDC=processing()[1]
            max_index=processing()[2]
            print('The DC component:', freq[0] ,'Hz')
            print(f'The 1st major component: {f_xDC[max_index[-1]]} Hz, magnitude = {P1_xDC[max_index[-1]]}')
            print(f'The 2nd major component: {f_xDC[max_index[-2]]} Hz, magnitude = {P1_xDC[max_index[-2]]}')
            print(f'The 3rd major component: {f_xDC[max_index[-3]]} Hz, magnitude = {P1_xDC[max_index[-3]]}')
            print(f'The 4th major component: {f_xDC[max_index[-4]]} Hz, magnitude = {P1_xDC[max_index[-4]]}')
            
             
        def lockin_amp():
            # Set reference
            index_ref = 1
            f_ref = processing()[0][processing()[2][-index_ref]]
            
            # Lock-in
            y_ref_sin = np.sin(2 * np.pi * f_ref * t1)
            y_ref_cos = np.cos(2 * np.pi * f_ref * t1)
            I_sin = np.trapz(s * y_ref_sin, x = t1) / (t1[-1])
            I_cos = np.trapz(s * y_ref_cos, x = t1) / (t1[-1])
            magnitude = 2 * np.sqrt(I_sin * I_sin + I_cos * I_cos)
            phase = np.arctan2(I_cos, I_sin)
            phase_deg = round(phase * 180 / np.pi)
            y_lockin = magnitude * np.sin(2 * np.pi * f_ref * t1 + phase)
            y_residual = s - y_lockin
            
            return y_lockin,y_residual,f_ref,magnitude,phase,phase_deg
        
        def lockin_amp_print():
            f_ref=lockin_amp()[2]
            magnitude=lockin_amp()[3]
            phase=lockin_amp()[4]
            phase_deg=lockin_amp()[5]
            print(f"Frequency = {f_ref} Hz")
            print(f"Magnitude = {magnitude} arb'U")
            print(f"Phase = {phase} rad = {phase_deg} deg")
        
        def lockin():
            roots=tk.Tk()
            roots.title('Python GUI Learning')
            roots.geometry('500x300+570+200')
                
                
            f1 = Figure(figsize=(15, 15), dpi=45)
            c = f1.add_subplot(211)
            d = f1.add_subplot(212)
            c.plot(t, lockin_amp()[0])
            c.set_title('Lock_in signal')
            d.plot(t, lockin_amp()[1])
            d.set_title('Residual Signal')
            canvas = FigureCanvasTkAgg(f1, master=roots)
            canvas.draw()
            canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=1)
            roots.mainloop()
        def save_csv():

            y_lockin_data=[]
            y_lockin_data=np.vstack((t,lockin_amp()[0]))
            y_lockin_data=np.transpose(y_lockin_data)
            pandas_y_lockin=pd.DataFrame(y_lockin_data)
            pandas_y_lockin.to_csv(r'C:\Users\Tim\OneDrive - NTUMEMS.NET\NTU_python程式設計\final_project\outputlockin.csv',header= False,index= False)
            
        button1 = tk.Button(root, text = "Print frequency", command = processing_print)
        button1.configure(width = 14, activebackground = "#33B5E5")
        button1.place(x=310,y=5)
        button4 = tk.Button(root, text = "Quit", command = _quit)
        button4.configure(width = 8, activebackground = "#33B5E5")
        button4.place(x=420,y=5)
        button5 = tk.Button(root, text = "Lock_in", command = lockin_amp_print)
        button5.configure(width = 8, activebackground = "#33B5E5")
        button5.place(x=10,y=5)
        button6 = tk.Button(root, text = "Lock_in_plot", command = lockin)
        button6.configure(width = 16, activebackground = "#33B5E5")
        button6.place(x=100,y=5)
        button7 = tk.Button(root, text = "save_csv", command = save_csv)
        button7.configure(width = 8, activebackground = "#33B5E5")
        button7.place(x=425,y=271)

        
    def _quit():
        root.quit()
        root.destroy()
        
    
    
    root=tk.Tk()

    
    root.title('Python GUI Learning')
   
    root.geometry('500x300+570+200')


    label1=tk.Label(root,text='請選擇文件:')
    text1=tk.Entry(root,bg='white',width=45)

    button2=tk.Button(root,text='處理',width=8,command=doProcess)
    button3=tk.Button(root,text='離開',width=8,command=_quit)

    label1.pack()
    text1.pack()

    button2.pack()
    button3.pack() 

    label1.place(x=30,y=30)
    text1.place(x=100,y=30)
    
    button2.place(x=160,y=80)
    button3.place(x=260,y=80)
 
    root.mainloop() 


 
if __name__=="__main__":
    main()
    
