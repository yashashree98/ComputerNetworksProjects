# Please run receiver.py before main.py

# Import the socket module for network communication
from socket import *
# Import the util module, which presumably contains utility functions
import util
# Import the make_packet function from the util module 
from util import make_packet
 
 
class Sender:

    def __init__(self):
        """
        Your constructor should not expect any argument passed in,
        as an object will be initialized as follows:
        sender = Sender()
       
        Please check the main.py for a reference of how your function will be called.
        """
        # Initialize the Sender class
        self.data = None

        # Get the receiver's IP address using a function from the util module
        self.receiver_ip = 'localhost'
        
        # Get the receiver's port number using a function from the util module
        self.receiver_port = 10100 + (4193376 % 500)
        
        # Initialize the packet number to 1
        self.pkt_num = 1
        
        # Initialize the sequence number to 0
        self.seq_num = 0
 
    def rdt_send(self, app_msg_str):
        """realibly send a message to the receiver (MUST-HAVE DO-NOT-CHANGE)
 
      Args:
        app_msg_str: the message string (to be put in the data field of the packet)
 
      """
        # Store the application message string
        self.data = app_msg_str

        # Create a UDP socket for sending data
        sender_socket = socket(AF_INET, SOCK_DGRAM)

        # Set a timeout value for simulating timeout later
        sender_socket.settimeout(2)

        # Check type of the message to be sent
        if (type(app_msg_str) == str):
            print("original message string: " + app_msg_str)
        else:
            print("original message string: " + app_msg_str.decode())
        
        # Use the make_packet function from util.py to create a packet
        pkt = make_packet(app_msg_str, 0, self.seq_num)
        
        print("packet created: " + str(pkt))
        
        # Call the udt_send function to send the packet
        self.udt_send(pkt, sender_socket)
        
        # Close the socket
        sender_socket.close()
 
    def udt_send(self, packet, sender_socket):
        """realibly send a message to the receiver 
 
      Args:
        self: passing self as an argument
        packet: the created packet
        sender_socket: to connect to the socket
 
      """
        repeat = True

        # Send the packet to the receiver
        sender_socket.sendto(packet, (self.receiver_ip, self.receiver_port))
        
        print("packet num." + str(self.pkt_num) + " is successfully sent to the receiver.")
        
        # Using while here for simulating timeout and corruption
        # Having while loop prevents the msg numbers to skip forward
        while repeat:
            try:
                # Receive a packet and its source address
                recv_packet, addr = sender_socket.recvfrom(1000)
                self.pkt_num += 1

                #Verify checksum value
                if util.verify_checksum(recv_packet):
                    #recv_ack_num = util.extract_ack_num(recv_packet)
                    recv_ack_num = (packet[10] << 8) + packet[10 + 1] & 0b0000010 >> 1
 
                    # received ack is equal to the seq of the sent message
                    # Check if the received ACK is equal to the sequence number of the sent message
                    if recv_ack_num == self.seq_num:
                        print("packet is received correctly: seq. num " + str(self.seq_num) + " = "+
                            "ACK num " + str(recv_ack_num) + ". all done!" + "\n\n")
                        
                        #Flip the seq number value
                        self.seq_num = (self.seq_num + 1) % 2
                        
                        # Break out of while loop for msg to move forward
                        repeat = False
 
                    else:
                        # The received ACK is not equal to the sent sequence number
                        print("receiver acked previous pkt, resend!" + "\n\n")
                        
                        #Check the type of the data to be string
                        if (type(self.data) == str):
                            print("[ACK-Previous retransmission]: " + self.data)
                        else:
                            print("[ACK-Previous retransmission]: " + self.data.decode())
                        
                        #send the data back to the receiver
                        sender_socket.sendto(packet, (self.receiver_ip, self.receiver_port))
                        
                        print("packet num." + str(self.pkt_num) + " is successfully sent to the receiver.")
 
            except timeout:
                # In case of a timeout, resend the packet
                print("socket timeout! Resend!" + "\n\n")

                #Check the type of the data to be string
                if (type(self.data) == str):
                    print("[timeout retransmission]: " + self.data)
                else:
                    print("[timeout retransmission]: " + self.data.decode())
                
                #send the data back to the receiver
                sender_socket.sendto(packet, (self.receiver_ip, self.receiver_port))
                
                #Increment packet number
                self.pkt_num += 1
                
                print("packet num." + str(self.pkt_num) + " is successfully sent to the receiver.")
 
    ####### Your Sender class in sender.py MUST have the rdt_send(app_msg_str)  #######
    ####### function, which will be called by an application to                 #######
    ####### send a message. DO NOT change the function name.                    #######
    ####### You can have other functions if needed.                             #######