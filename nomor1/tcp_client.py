import sys
import socket
import json
import logging
import ssl
import os
import threading
import random
import datetime

server_address = ('172.16.16.102', 12000)

def createsocket(destination_address='localhost',port=12000):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (destination_address, port)
        sock.connect(server_address)
        return sock
    except Exception as ee:
        logging.warning(f"error {str(ee)}")

def deserialisasi(s):
    return json.loads(s)
    

def send_command(command_str,is_secure=False):
    alamat_server = server_address[0]
    port_server = server_address[1]

    sock = createsocket(alamat_server,port_server)
    
    try:
        sock.sendall(command_str.encode())
      
        data_received="" 
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
      
        hasil = deserialisasi(data_received)
        return hasil
    except Exception as ee:
        logging.warning(f"error during data receiving {str(ee)}")
        return False
def getdatapemain(nomor=0,is_secure=False):
    cmd=f"getdatapemain {nomor}\r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    if (hasil):
        pass
    else:
        print("Failed to get response")
    print("==> Got data: " + str(hasil))
    return hasil
def lihatversi(is_secure=False):
    cmd=f"versi \r\n\r\n"
    hasil = send_command(cmd,is_secure=is_secure)
    return hasil
if __name__=='__main__':

    sample_threads = [1, 5, 10, 20]
    for i in sample_threads:
        threads = {}
        print("")
        print("Thread number " + str(i))

        start_datetime = datetime.datetime.now()

        request_sent = 0
        for x in range(i):
            print("Sending request number {} of {} requests".format(x+1, i))
            threads[x] = threading.Thread(target=getdatapemain, args=(random.randint(1, 4),False))
            threads[x].start()
            request_sent += 1

        for x in range(i):
            threads[x].join()

        finish_datetime = datetime.datetime.now()

        latency = (finish_datetime-start_datetime).total_seconds() / i

        print("Thread number " + str(i) + " finished. Average latency: {} seconds".format(latency))