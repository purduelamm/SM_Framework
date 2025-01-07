#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 14 2024

@author: Yuseop Sim
@Contributor : Hojun Lee

Upload karel formatted file to robot controller using FTP protocol

"""
from ftplib import FTP
import os
import stat

class FTP_uploader():
    def __init__(self, host='192.168.1.100', port= 21, user = 'ROBOT', passwd = 'admin'):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
    def upload_ftp(self, filename, file_path):
        try:
            ftp = FTP(timeout=30) # Robot IP
            ftp.connect(host=self.host, port = self.port)
            ftp.login(user= self.user, passwd=self.passwd)
            ftp.encoding = "utf-8"
            ftp.cwd('/md:\/')
            #ftp.dir()
            filename = 'move_command.ls' 
            file_path = 'C:/Users/TAMS/Desktop/move_command.ls'
            os.chmod(file_path, 0o777)
            #perm = os.stat(file_path)
            #print(perm)
            #os.chmod(file_path, permissionFlag)
            if os.path.exists(file_path):
                with open(file_path, 'rb') as f:
                    retCode = ftp.storbinary(f"STOR %s" %filename, fp=f, blocksize = 1024*1024)
            ftp.quit()
        except Exception as e:
            print(e)

if __name__ == "__main__":
    ftp_uploader = FTP_uploader()
    ftp_uploader.upload_ftp('move_command.ls' , 'C:/Users/TAMS/Desktop/move_command.ls')

