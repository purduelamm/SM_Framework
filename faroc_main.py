#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Mar 13 2024

@author: Yuseop Sim
@Contributor : Hojun Lee

Using Faroc & mySQL, upload machine data to MySQL local database

"""

from faroc import FaRoC_Mover
from uploader import UPLOADER
from opc_server import OPC_server
import time
import time
import struct

 
robot = FaRoC_Mover(socket_timeout = 60, debug_mode = 0)    # can read and write data and move the robot.
mydb = UPLOADER()
opc = OPC_server()
mydb.db_connection()
opc.db_connection()
opc.opc_connection()

robot.connect()
robot.status()

# %% JOINT move in joint space
code, msg, data = robot.set_pos_reg(1, "joint",
                             vals=[-109, 0.0, 0.0, 0.0, 0.0, 0.0])
#print(f"Set PR[1] (joint): {data[1] if code==0 else msg}")
code, msg, data = robot.set_pos_reg(2, "joint",
                             vals=[-109, -16, -40, 0, 35.0, 0])
#print(f"Set PR[2] (joint): {data[1] if code==0 else msg}")
code, msg, data = robot.set_pos_reg(3, "joint",
                             vals=[-109, 47, -40.0, 0.0, 35.0, 0])
 #print(f"Set PR[3] (joint): {data[1] if code==0 else msg}")
code, msg, data = robot.set_pos_reg(4, "joint",
                            vals=[-109, -16, -40.0, 0.0, 35.0, 0])
#print(f"Set PR[3] (joint): {data[1] if code==0 else msg}")
code, msg, data = robot.set_pos_reg(5, "joint",
                            vals=[-109.0, 0, 0, 0.0, 0.0, 0])
 #print(f"Set PR[3] (joint): {data[1] if code==0 else msg}")
time.sleep(0.1)
robot.run_task("move_command")
#robot.run_task("dispensenorth")

while(True):
      try:
            code, msg, data = robot.get_curjpos(6)
            correct_byte_data_list = [round(struct.unpack('>f',struct.pack('<f', byte_data))[0],3) for byte_data in data]
            #print(f'Current joints: {correct_byte_data_list if code==0 else msg}')
            mydb.upload_data("jpos", correct_byte_data_list)

            # get robot position
            code, msg, data = robot.get_curpos()
            correct_byte_data_list = [round(struct.unpack('>f',struct.pack('<f', byte_data))[0],3) for byte_data in data[1:7]]
            #print(f'Current Pose: {correct_byte_data_list if code==0 else msg}')
            mydb.upload_data("pos", correct_byte_data_list)

            #%% get robot current energy consumption in watt 
            code, msg, data = robot.get_ins_power()
            byte_data=struct.pack('<f', data[0])

            cdab_bytes = bytes([byte_data[2], byte_data[3], byte_data[0], byte_data[1]])
            correct_byte_data = round(struct.unpack('>f', cdab_bytes)[0], 3)
            correct_byte_data = round(struct.unpack('>f', byte_data)[0],3)
            #print(correct_byte_data)
            #print(f'Energy consumption in watt: {correct_byte_data if code==0 else msg}')
            mydb.upload_data("power", correct_byte_data)

            opc.set_value()

            time.sleep(0.1)
      except Exception as e:
            print(e)
      #finally:
            #%% disconnect 
            #code, msg = robot.disconnect()




