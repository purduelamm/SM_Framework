#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mar 13 2024

@author: Yuseop Sim
@Contributor : Hojun Lee

Using mySQL, upload machine data to MySQL local database

"""
import pymysql
from datetime import datetime

class UPLOADER():
    def __init__(self, mysql_db_ip = "localhost", mysql_port = 3306, mysql_user = "root", mysql_password = "lamm1101!", mysql_DB="lamm2024", mysql_table = "`crx-10ia/l`"):
        self.mysql_db_ip = mysql_db_ip
        self.mysql_port=mysql_port
        self.mysql_user=mysql_user
        self.mysql_password=mysql_password
        self.mysql_table=mysql_table
        self.mysql_DB=mysql_DB

    def db_connection(self):
        try:
            self.db_instance=pymysql.connect(host=self.mysql_db_ip, user=self.mysql_user, password=self.mysql_password, db=self.mysql_DB, port=self.mysql_port)
            self.cursor = self.db_instance.cursor()
            time_zone = "set time_zone = \"+0:00\";"
            self.cursor.execute(time_zone)
            self.db_instance.commit()
        except Exception as e:
            print(f"Error connecting to MYSQL database {e}")
    def upload_data(self, category, text):
        try:
            self.timestamp = str(datetime.now())
            #print(self.timestamp)
            if(category=="pos"):
                self.data_category = "pos"
            elif(category=="jpos"):
                self.data_category = "jpos"
            elif(category=="power"):
                self.data_category = "power"
            else:
                self.data_category = "None"
            
            query = "INSERT INTO "+self.mysql_table+" (timestamp, category, value) VALUE('"+ str(self.timestamp) +"','"+ self.data_category +"','"+ str(text) + "');"
            #print(query)
            self.cursor.execute(query)
            self.db_instance.commit()
        except Exception as e:
            print(f"query has a issue {e}")