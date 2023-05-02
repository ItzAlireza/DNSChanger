import sys,os,ctypes
import subprocess
import customtkinter as ctk
import tkinter as ttk
import json
import re

#File Opening
s = open('setting.json','r')

#VARIABLES
#----------
colors = {'dark':{'bg':'#323232','interfaceText':'#B5B5B5','activeText':'#E8E8E8','deactiveText':'#2B2B2B','deactiveButtonbg':'#41DC0B','activeButtonbg':'#707070'},
          'light':{'bg':'#DFDFDF','interfaceText':'#222222','activeText':'#2B2B2B','deactiveText':'#FFFFFF','deactiveButtonbg':'#33BF02','activeButtonbg':'#FFFFFF'}}
setting = json.loads(s.read())
dns = setting['dns']
colorMode = setting['app']['colorMode']

#FUNCTIONS
#---------

def adminCheck():#Checking if user is using Administrator or not
    try:
        is_admin = os.getuid() == 0
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if is_admin:
        pass
    else:
        ttk.messagebox.showerror(title='Error', message='Please run the app as administrator!')
        sys.exit()

def NIGathering():#Getting Connected network adapter
    list = []
    final = []
    r = subprocess.check_output('netsh interface show interface')

    #deletes first 2 lines
    r1 = str(r).split('\\n')[3:]
    for item in r1:
        list.append(item.split('   '))
    for item in list:

        #Checking for connected interface
        if item[2][2:] == "Connected":

            #returning the name of the connected interface
            return item[6].replace('\\r','')[2:]
        
def getConnectedDns(interface):#For getting the connected dns
    r = subprocess.check_output('netsh interface ip show config "'+interface+'"')
    r = str(r).split('\\n')
    for i in r:
        #finding the line of dns's
        if i[:38] == '    Statically Configured DNS Servers:':

            #Returning the primary and secondary dns's
            #List index to find dynamic dns ip's
            connectedDns = [r[r.index(i)].replace(' ','')[r[r.index(i)].replace(' ','').index(':')+1:-2],r[r.index(i)+1].replace(' ','')[:-2]]
            return connectedDns,list(dns.keys())[list(dns.values()).index(connectedDns)]
        elif i[:40] == '    DNS servers configured through DHCP:':
            return 'Automatic','Automatic'

def setDns(i,d):#For setting the dns
    if d == 'Automatic':
        os.system('netsh interface ip set dns name="'+i+'" dhcp')

    elif(type(d) == list and len(d) == 2):#Checking for d object to be a list with 2 items

        #Checking for ip address regex in dnslist
        if(bool(re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", d[0])) and bool(re.match(r"[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}", d[1]))):
            os.system('netsh interface ip set dns name="'+i+'" static '+d[0])
            os.system('netsh interface ip add dns name="'+i+'" '+d[1]+' index=2')
        else:
            ttk.messagebox.showerror(title='Data entry Error', message='The dns data is wrong! Please check dnslist formatting guide!')
            return False
    else:
        ttk.messagebox.showerror(title='Data entry Error', message='The dns data is wrong! Please check dnslist formatting guide!')
        return False
    
def buttonPressed(d,i):#Handling BtnPressed from DNSChanger.py 
    a = setDns(i,d) #Returns False if ip's are wrong
    if a == 0:
        return 0

def changePositions(a,b,colorMode):#Changes positions of active button and clicked button
    br = b.grid_info()['row']
    b.grid(row=2)
    a.grid(row=br)
    a.configure(fg_color=colors[colorMode]['activeButtonbg'],text_color=colors[colorMode]['activeText'],state='normal')
    b.configure(fg_color=colors[colorMode]['deactiveButtonbg'],text_color=colors[colorMode]['deactiveText'],state='disabled')

def colorModeInverse(a):
    if a == 'dark':
        return 'light'
    if a == 'light':
        return 'dark'