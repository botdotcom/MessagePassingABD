import grpc
import time
import datetime
import string
import random
from concurrent import futures
import sqlite3
import registerdb as rdb 

# importing generated classes
import abd_pb2
import abd_pb2_grpc

# database connectivity path
path = 'reg_db.sqlite'

class ABDServicer(abd_pb2_grpc.ABDServiceServicer):
    server_port = 0

    def __init__(self, port=2222):
        self.server_port = port # set a user-defined port number from the commmand-line; default is 2222

    def read1(self, read1_req, context):
        print("Received read request 1: {}".format(read1_req))
        conn = rdb.dbconnect()
        print("Connected to database")
        register = read1_req.register
        row = rdb.reader(conn, register)
        print(row)
        timestamp = row[1]
        value = row[2]
        # print("{}, {}".format(timestamp, value))
        response = abd_pb2.Read1Response(timestamp=timestamp, value=value)
        # response = abd_pb2.Read1Response(timestamp=datetime.datetime.now(), value="Hi......")
        rdb.dbclose(conn)
        print("Database disconnected")
        return response

    def read2(self, read2_req, context):
        print("Received read request 2: {}".format(read2_req))
        conn = rdb.dbconnect()
        print("Connected to database")
        register = read2_req.register
        row = rdb.reader(conn, register)
        timestamp = row[1]
        value = row[2]
        response = abd_pb2.AckResponse()
        rdb.dbclose(conn)
        print("Database disconnected")
        return response

    def write(self, write_req, context):
        print("Received write request: {}".format(write_req))
        register = write_req.register
        timestamp = write_req.timestamp
        value = write_req.value
        conn = rdb.dbconnect()
        print("Connected to database")
        rdb.writer(conn=conn, register=register, timestamp=timestamp, value=value)
        rdb.dbclose(conn)
        print("Database disconnected")
        response = abd_pb2.AckResponse()
        return response

    def name(self, name_req, context):
        print("Received name request: {}".format(name_req))
        response = abd_pb2.NameResponse()
        response.name = "USCS-Mac262-Shamli"
        return response

    def start_server(self):
        server = grpc.server(futures.ThreadPoolExecutor())
        abd_pb2_grpc.add_ABDServiceServicer_to_server(ABDServicer(2222), server)
        server.add_insecure_port("[::]:{}".format(self.server_port))

        # start the server
        print("Starting the ABD server...")
        server.start()
        time.sleep(3)   # random delay
        print("ABD server now running... Listening at port {}...".format(self.server_port))

        # stop the server
        try:
            while True:
                time.sleep(datetime.timedelta(days=1).total_seconds())  # keep server live till key press
        except KeyboardInterrupt:
            print("Stopping the ABD server...")
            server.stop(None)
            print("ABD server stopped...")

# use
port = input("Enter the port number you want to open for server: ")
current_server = ABDServicer(int(port))
current_server.start_server()