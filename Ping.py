from socket import *
import os
import sys
import struct
import time
import select
import threading
import signal

ICMP_ECHO_REQUEST = 8

def checksum(source_string):
    csum = 0
    countTo = (len(source_string) // 2) * 2
    count = 0
    
    while count < countTo:
        thisVal = source_string[count + 1] * 256 + source_string[count]
        csum = csum + thisVal
        csum = csum & 0xffffffff
        count = count + 2
        
    if countTo < len(source_string):
        csum = csum + source_string[len(source_string) - 1]
        csum = csum & 0xffffffff
        
    csum = (csum >> 16) + (csum & 0xffff)
    csum = csum + (csum >> 16)
    answer = ~csum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def receiveOnePing(mySocket, ID, timeout, destAddr):
    timeLeft = timeout
    while True:
        startedSelect = time.time()
        whatReady = select.select([mySocket], [], [], timeLeft)
        howLongInSelect = (time.time() - startedSelect)
        
        if whatReady[0] == []:
            return "Request timed out."
        
        timeReceived = time.time()
        recPacket, addr = mySocket.recvfrom(1024)
        
        icmpHeader = recPacket[20:28]
        type, code, checksum, packetID, sequence = struct.unpack("bbHHh", icmpHeader)
        
        if packetID == ID:
            bytesInDouble = struct.calcsize("d")
            timeSent = struct.unpack("d", recPacket[28:28 + bytesInDouble])[0]
            return timeReceived - timeSent
        
        timeLeft = timeLeft - howLongInSelect
        if timeLeft <= 0:
            return "Request timed out."

def signout(sig, frame):
    
    print("\nProgram Exit..")
    sys.exit(0)

def sendOnePing(mySocket, destAddr, ID):
    myChecksum = 0
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    data = struct.pack("d", time.time())
    
    myChecksum = checksum(header + data)

    myChecksum = htons(myChecksum)
    
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, myChecksum, ID, 1)
    packet = header + data
    
    mySocket.sendto(packet, (destAddr, 1))

def doOnePing(destAddr, timeout):
    icmp = getprotobyname("icmp")
    mySocket = socket(AF_INET, SOCK_RAW, icmp)
    
    myID = os.getpid() & 0xFFFF
    sendOnePing(mySocket, destAddr, myID)
    delay = receiveOnePing(mySocket, myID, timeout, destAddr)
    
    mySocket.close()
    return delay

def ping(host, timeout=1):
    dest = gethostbyname(host)
    print("Pinging " + dest + " using Python:")
    print("")
    
    while True:
        delay = doOnePing(dest, timeout)
        print("Ping " + host)
        print(f"Reply from {dest}: time = {delay*1000:.0f} ms\n " if isinstance(delay, float) else delay)
        time.sleep(1)
        
# def tcp_ping(host, port, timeout=1):
#     while True:
#         try:
#             with socket(AF_INET, SOCK_STREAM) as sock:
#                 sock.settimeout(timeout)
#                 start_time = time.time()
#                 sock.connect((host, port))
#                 end_time = time.time()
#                 print("Ping " + host)
#                 print(f"Reply from {host}:{port} - time = {(end_time - start_time) * 1000:.4f} ms\n\n")
#         except (TimeoutError, OSError):
#             print(f"Request to {host}:{port} timed out.")
#         time.sleep(1)

# tcp_loop = threading.Thread(target=tcp_ping, args=("192.168.5.83", 8082))

signal.signal(signal.SIGINT,signout)
ping_loop = threading.Thread(target=ping, args=("google.com",))

# tcp_loop.start()
ping_loop.start()

# tcp_loop.join()
ping_loop.join()
