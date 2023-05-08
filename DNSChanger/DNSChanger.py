try:
    from ctypes import windll, byref, sizeof, c_int 
except:
    pass
import tkinter as tk
import os
from tkinter import ttk
import customtkinter as ctk
from functions import *
from functools import partial

#Functions
def changeTitleBarColor(color):
    try:
        HWND = windll.user32.GetParent(window.winfo_id())
        windll.dwmapi.DwmSetWindowAttribute(HWND,35,byref(c_int(color)),sizeof(c_int))
    except:
        pass

def btnPressed(NDns,d,i):#DNS Button pressed Event
    global buttons
    if setDns(i.get(),d) == 0:
        return 0
    connectedDnsName.set(getConnectedDns(i.get())[1])
    buttonGrid(buttons,dns,connectedDnsName)

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
    labelTwo.configure(text_color=colors[colorMode]['interfaceText'],fg_color=colors[colorMode]['activeButtonbg'])
    window.configure(fg_color=colors[colorMode]['bg'])
    modeSwitch.configure(text_color=colors[colorModeInvert(colorMode)]['activeText'],text=colorModeInvert(colorMode).upper()+' MODE',fg_color=colors[colorModeInvert(colorMode)]['activeButtonbg'])
    for i in buttons:
        if i == connectedDnsName.get():
            buttons[i].configure(fg_color=colors[colorMode]['deactiveButtonbg'],text_color=colors[colorMode]['deactiveText'])
        else:
            buttons[i].configure(fg_color=colors[colorMode]['activeButtonbg'],text_color=colors[colorMode]['activeText'])

def buttonGrid(buttons,dns,connectedDns):#Rearranging all buttons
    counter = 3
    for i in dns:
        if i == connectedDns.get():#Checking for connected dns button
            buttons[i].grid(row=2,column=1,columnspan=2,sticky='wens',padx=20,pady=5)
            buttons[i].configure(fg_color=colors[colorMode]['deactiveButtonbg'],text_color=colors[colorMode]['deactiveText'],state='disabled')
        else:#other buttons
            buttons[i].grid(row=counter,column=1,columnspan=2,sticky='wens',padx=20,pady=5)
            buttons[i].configure(fg_color=colors[colorMode]['activeButtonbg'],text_color=colors[colorMode]['activeText'],state='normal')
            counter +=1

def interfaceSelectedChange(a):#Event for changing the network adapter
    global connectedDns,dns,connectedDnsName,buttons,interface
    interface.set(a)
    connectedDns = getConnectedDns(a)#Functions.py
    connectedDnsName.set(connectedDns[1])#Setting current dns in tkinter var cause of re-usability
    buttonGrid(buttons,dns,connectedDnsName)

#---------
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

# **UI Elements and Variables**
#Variables
buttons = {}
interface = ctk.StringVar()
connectedDnsName = ctk.StringVar()
interfaces = getInterface()#Functions.py
#UI
upperLabelFont = ctk.CTkFont(family="Vazir", size=20,weight='normal')
buttonsFont = ctk.CTkFont(family="Vazir", size=24,weight='bold')
modeSwitchFont = ctk.CTkFont(family="Vazir", size=15,weight='normal')
labelOne = ctk.CTkLabel(window,text='Network Adapter : ',font=(upperLabelFont),text_color=colors[colorMode]['interfaceText'])
labelTwo = ctk.CTkComboBox(window,values=interfaces,font=(ctk.CTkFont(family="Vazir", size=17,weight='bold')),fg_color=colors[colorMode]['activeButtonbg'],text_color=colors[colorMode]['interfaceText'],command=interfaceSelectedChange)
modeSwitch = ctk.CTkButton(window,text_color=colors[colorModeInvert(colorMode)]['activeText'],text=colorModeInvert(colorMode).upper()+' MODE',command=changeColorMode,font=modeSwitchFont,fg_color=colors[colorModeInvert(colorMode)]['activeButtonbg'])
for i in dns:#Creating all buttons
    buttons[i] = ctk.CTkButton(window,text=i,font=buttonsFont,corner_radius=20,fg_color=colors[colorMode]['activeButtonbg'],text_color=colors[colorMode]['activeText'],command=partial(btnPressed,i,dns[i],interface))
#Positioning using grid
interfaceSelectedChange(labelTwo.get())#Calling once for getting dns for selected interface and button positioning using grid
labelOne.grid(column=1,row=0,pady=20)
labelTwo.grid(column=2,row=0,pady=20)
modeSwitch.grid(column=1,columnspan=2,row=1)

window.mainloop()