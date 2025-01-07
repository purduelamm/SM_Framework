"""
Created on Mar 21 2024

@author: Yuseop Sim
@Contributor : Hojun Lee

Using Faroc & mySQL, upload machine data to CESMII

"""

# OPC dependent
import pymysql
import time
import sys
sys.path.insert(0, "..")
from opcua import ua, Server

class OPC_server():
    def __init__(self, mysql_db_ip = "127.0.0.1", mysql_port = 3306, mysql_user = "root", mysql_password = "lamm1101!", mysql_DB="lamm2024", mysql_table = "`crx-10ia/l`"):
        self.mysql_db_ip = mysql_db_ip
        self.mysql_port=mysql_port
        self.mysql_user=mysql_user
        self.mysql_password=mysql_password
        self.mysql_table=mysql_table
        self.mysql_DB=mysql_DB
        self.robot_logger = "None"

        self.endpoint_url = "opc.tcp://127.0.0.1:62548/DataAccessServer"
        self.bposid=-1
        self.bjposid=-1
        self.bpowid=-1
        self.pre_time=999
        self.now_time=999
    
    def db_connection(self):
        try:
            self.db_instance=pymysql.connect(host=self.mysql_db_ip, user=self.mysql_user, password=self.mysql_password, db=self.mysql_DB, port=self.mysql_port)
            self.cursor = self.db_instance.cursor()
            time_zone = "set time_zone = \"+0:00\";"
            self.cursor.execute(time_zone)
            self.db_instance.commit()

        except Exception as e:
            print(f"Error connecting to MYSQL database {e}")

    def opc_connection(self):
        self.server = Server()
        self.server.set_endpoint(self.endpoint_url)
        self.idx = self.server.register_namespace("http://examples.freeopcua.github.io")
        # get Objects node, this is where we should put our nodes
        self.objects = self.server.get_objects_node()

        # populating our address space
        myobj = self.objects.add_object(self.idx, "BCI_robot_gate")

        # Pay attention to the variant type
        self.j1pos = myobj.add_variable(self.idx, "j1pos", 0.0, ua.VariantType.Float)
        self.j2pos = myobj.add_variable(self.idx, "j2pos", 0.0, ua.VariantType.Float)
        self.j3pos = myobj.add_variable(self.idx, "j3pos", 0.0, ua.VariantType.Float)
        self.j4pos = myobj.add_variable(self.idx, "j4pos", 0.0, ua.VariantType.Float)
        self.j5pos = myobj.add_variable(self.idx, "j5pos", 0.0, ua.VariantType.Float)
        self.j6pos = myobj.add_variable(self.idx, "j6pos", 0.0, ua.VariantType.Float)

        self.expos = myobj.add_variable(self.idx, "expos", 0.0, ua.VariantType.Float)
        self.eypos = myobj.add_variable(self.idx, "eypos", 0.0, ua.VariantType.Float)
        self.ezpos = myobj.add_variable(self.idx, "ezpos", 0.0, ua.VariantType.Float)
        self.exrot = myobj.add_variable(self.idx, "exrot", 0.0, ua.VariantType.Float)
        self.eyrot = myobj.add_variable(self.idx, "eyrot", 0.0, ua.VariantType.Float)
        self.ezrot = myobj.add_variable(self.idx, "ezrot", 0.0, ua.VariantType.Float)

        self.power = myobj.add_variable(self.idx, "power", 0.0, ua.VariantType.Float)

        # myvar = myobj.add_variable(idx, "MyVariable", 6.7, ua.VariantType.Double)
        # myvar = myobj.add_variable(idx, "MyVariable", 6, ua.VariantType.Int32)

        self.j1pos.set_writable()  # Set MyVariable to be writable by clients
        self.j2pos.set_writable()  # Set MyVariable to be writable by clients
        self.j3pos.set_writable()  # Set MyVariable to be writable by clients
        self.j4pos.set_writable()  # Set MyVariable to be writable by clients
        self.j5pos.set_writable()  # Set MyVariable to be writable by clients
        self.j6pos.set_writable()  # Set MyVariable to be writable by clients

        self.expos.set_writable()  # Set MyVariable to be writable by clients
        self.eypos.set_writable()  # Set MyVariable to be writable by clients
        self.ezpos.set_writable()  # Set MyVariable to be writable by clients
        self.exrot.set_writable()  # Set MyVariable to be writable by clients
        self.eyrot.set_writable()  # Set MyVariable to be writable by clients
        self.ezrot.set_writable()  # Set MyVariable to be writable by clients

        self.power.set_writable()

        # starting!
        self.server.start()

    def download_db(self):
        try:
            query = "(SELECT * FROM "+str(self.mysql_table)+" WHERE category='pos' ORDER BY timestamp DESC LIMIT 1) UNION "+ \
            "(SELECT * FROM "+str(self.mysql_table)+" WHERE category='jpos' ORDER BY timestamp DESC LIMIT 1) UNION "+ \
            "(SELECT * FROM "+str(self.mysql_table)+" WHERE category='power' ORDER BY timestamp DESC LIMIT 1)"
            
            self.cursor.execute(query)
            results = self.cursor.fetchall()
            #print(results)
            #print(results)
            return results
        except Exception as e:
            print(f"query has a issue {e}")
            return None

    def set_value(self):
        if(self.now_time>3): #Ensure 1Hz loop
            #query from server
            self.db_connection()
            result = self.download_db()
            if(result!=None):
                #print(result)
                self.posid = result[0][0]
                self.jposid = result[1][0]
                self.powid = result[2][0]
                
                if(self.posid!=self.bposid):
                    temp_pos = result[0][3]
                    numbers = temp_pos[1:-1].split(',')
                    pos = [float(num) for num in numbers]
                    #print(pos)
                    self.expos.set_value(pos[0])
                    self.eypos.set_value(pos[1]) 
                    self.ezpos.set_value(pos[2])
                    self.exrot.set_value(pos[3]) 
                    self.eyrot.set_value(pos[4])
                    self.ezrot.set_value(pos[5]) 
                if(self.jposid!=self.bjposid):
                    temp_pos = result[1][3]
                    numbers = temp_pos[1:-1].split(',')
                    pos = [float(num) for num in numbers]
                    print(pos)
                    self.j1pos.set_value(pos[0]) 
                    self.j2pos.set_value(pos[1]) 
                    self.j3pos.set_value(pos[2]) 
                    self.j4pos.set_value(pos[3]) 
                    self.j5pos.set_value(pos[4]) 
                    self.j6pos.set_value(pos[5])
                if(self.powid!=self.bpowid):
                    #print(float(result[2][3]))
                    self.power.set_value(float(result[2][3]))
                self.bposid = self.posid
                self.bjposid = self.jposid
                self.bpowid = self.powid
            self.pre_time = time.time()
            self.now_time = 0
        else:
            self.now_time = time.time()-self.pre_time