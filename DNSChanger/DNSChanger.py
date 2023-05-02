try:
    from ctypes import windll, byref, sizeof, c_int 
except:
    pass
import tkinter as tk
import os
import customtkinter as ctk
from functions import *
from functools import partial

#Functions
#---------
def changeTitleBarColor(color):
    try:
        HWND = windll.user32.GetParent(window.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(HWND,35,byref(c_int(color)),sizeof(c_int))
    except:
        pass

def btnPressed(NDns,d,i):
    a = buttonPressed(d,i)#Functions.py
    if a == False:
        return 0
    changePositions(buttons[connectedDnsName.get()],buttons[NDns],colorMode)#Functions.py
    connectedDnsName.set(getConnectedDns(i)[1])#Setting current dns to new dns

def changeColorMode():
    global colorMode, labelOne, labelTwo, buttons, window, modeSwitch, setting
    if colorMode == 'dark':
        colorMode = 'light'
    else:
        colorMode = 'dark'
    setting['app']['colorMode'] = colorMode
    with open('setting.json','w') as f:
        json.dump(setting, f)
    changeTitleBarColor(int('0x00'+colors[colorMode]['bg'][1:],16))
    labelOne.configure(text_color=colors[colorMode]['interfaceText'])
    labelTwo.configure(text_color=colors[colorMode]['interfaceText'])
    window.configure(fg_color=colors[colorMode]['bg'])
    modeSwitch.configure(text_color=colors[colorModeInverse(colorMode)]['activeText'],text=colorModeInverse(colorMode).upper()+' MODE',fg_color=colors[colorModeInverse(colorMode)]['activeButtonbg'])
    for i in buttons:
        if i == connectedDnsName.get():
            buttons[i].configure(fg_color=colors[colorMode]['deactiveButtonbg'],text_color=colors[colorMode]['deactiveText'])
        else:
            buttons[i].configure(fg_color=colors[colorMode]['activeButtonbg'],text_color=colors[colorMode]['activeText'])
            
adminCheck()#functions.py
# *Window Setup**

window = ctk.CTk(fg_color=colors[colorMode]['bg'])
window.title('DNS Changer')
window.geometry(setting['app']['geometry'])
window.resizable(False,True)
window.iconbitmap("icon.ico")

window.columnconfigure(0, weight=2)
window.columnconfigure(1, weight=2)
window.columnconfigure(2, weight=2)
window.columnconfigure(3, weight=2)

changeTitleBarColor(int('0x00'+colors[colorMode]['bg'][1:],16))#To change the color of titleBar [Only Windows]


# **Variables**
buttons = {}
upperLabelFont = ctk.CTkFont(family="Vazir", size=20,weight='normal')
buttonsFont = ctk.CTkFont(family="Vazir", size=24,weight='bold')
modeSwitchFont = ctk.CTkFont(family="Vazir", size=15,weight='normal')

interface = ctk.StringVar()
interface.set(NIGathering())#Functions.py

connectedDnsName = ctk.StringVar()
connectedDns = getConnectedDns(interface.get())#Functions.py
connectedDnsName.set(connectedDns[1])#Setting current dns in tkinter var cause of re-usability

#Bringing current dns above all
index = list(dns).index(connectedDns[1])
tups = list(dns.items())
tups[0],tups[index] = tups[index],tups[0]
dns = dict(tups)

labelOne = ctk.CTkLabel(window,text='Network Adapter : ',font=(upperLabelFont),text_color=colors[colorMode]['interfaceText'])
labelTwo = ctk.CTkLabel(window,text='',font=(upperLabelFont),textvariable=interface,text_color=colors[colorMode]['interfaceText'])

modeSwitch = ctk.CTkButton(window,text_color=colors[colorModeInverse(colorMode)]['activeText'],text=colorModeInverse(colorMode).upper()+' MODE',command=changeColorMode,font=modeSwitchFont,fg_color=colors[colorModeInverse(colorMode)]['activeButtonbg'])

counter = 2 #For indexing buttons in buttons[]
for i in dns:
    if i == connectedDnsName.get():#Checking for connected dns button
        buttons[i] = ctk.CTkButton(window,text=i,font=buttonsFont,corner_radius=20,fg_color=colors[colorMode]['deactiveButtonbg'],text_color=colors[colorMode]['deactiveText'],state='disabled',command=partial(btnPressed,i,dns[i],interface.get()))
        buttons[i].grid(row=counter,column=1,columnspan=2,sticky='wens',padx=20,pady=5)
        counter +=1
    else:
        #Other buttons
        buttons[i] = ctk.CTkButton(window,text=i,font=buttonsFont,corner_radius=20,fg_color=colors[colorMode]['activeButtonbg'],text_color=colors[colorMode]['activeText'],command=partial(btnPressed,i,dns[i],interface.get()))
        buttons[i].grid(row=counter,column=1,columnspan=2,sticky='wens',padx=20,pady=5)
        counter +=1
labelOne.grid(column=1,row=0,pady=20)
labelTwo.grid(column=2,row=0,pady=20)
modeSwitch.grid(column=1,columnspan=2,row=1)
window.mainloop()