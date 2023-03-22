# -*- coding: utf-8 -*-
"""
Created on Thu Nov 17 12:25:03 2022

@author: 113423
"""
import subprocess
import os
import sys

passwordfile=open("password.txt",'w')

passwordfile.write("here are your passwords")
passwordfile.close()

wififiles=[]
wifiname=[]
wifipwd=[]

command=subprocess.run(["netsh", "wlan", "export", "profile", "key=clear"], capture_output= True).stdout.decode()

path=os.getcwd()

for filename in os.listdir(path):
    if filename.startswith("Wi-Fi") and filename.endswith(".xml"):
        wififiles.append(filename)
        for i in wififiles:
            with open(i, 'r') as f:
                for line in f.readlines():
                    if 'name' in line:
                        stripped=line.strip()
                        front = stripped[6:]
                        back= front[:-7]
                        wifiname.append(back)
                        
                    if 'keyMaterial' in line:
                        stripped= line.strip()
                        front=stripped[13:]
                        back=front[:-14]
                        wifipwd.append(back)
                        for x, y in zip(wifiname,wifipwd):
                           sys.stdout=open("passwords.txt","a")
                           print("ssid: "+x,"pwd: "+y,sep='\n')
                           sys.stdout.close()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
