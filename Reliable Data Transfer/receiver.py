# Please run receiver.py before main.py

# Import necessary modules and functions 
from socket import *

# Import the sleep function from the time module
from time import sleep

# Import the util module, which presumably contains utility functions
import util

port = 10100 + (4193376 % 500)
host = 'localhost'
# Create an empty file called "received_pkt.txt" or clear its contents if it already exists
open("received_pkt.txt","w").close()

# Define the function to receive packets and perform reliable data transfer 
def rdt_receive(receiver_socket):
    """receive the message from the sender and process the received packet
 
      Args:
        receiver_socket: the message string (to be put in the data field of the packet)
 
      """
    # Initialize the expected sequence number to 0
    expected_seq_num = 0

    # Initialize the packet number to 0
    pkt_num = 0
   
    # The receiver runs indefinitely
    while True:

        #Receive packet from sender
        packet, addr = receiver_socket.recvfrom(1000)
        
        # Increment the packet number
        pkt_num += 1
        print("packet num." + str(pkt_num) + " received: " + str(packet))
        
        # Write the received packet to the "received_pkt.txt" file
        with open("received_pkt.txt","a") as file :
            file.write(f"{str(packet)}\n")
        
        # Extract the sequence number from the received packet
        #seq_num = util.extract_seq_num(packet) 
        seq_num = (packet[10] << 8) + packet[10 + 1] & 0b0000001

        # Simulate packet loss by delaying and triggering a timeout event on the sender side
        if pkt_num % 6 == 0:
            print("simulating packet loss: sleep a while to trigger timeout event on the send side...")
            
            # Simulate a timeout by sleeping for 2 seconds
            sleep(2)  
            print("all done for this packet!" + "\n\n")
 
        # Simulate packet corruption by sending the wrong ACK
        elif pkt_num % 3 == 0:
            print("simulating packet bit errors/corrupted: ACK the previous packet!")
            
            # Create an ACK packet with the wrong ACK number
            ack_packet = util.make_packet('', 1 - seq_num, 0)
            
            # Send the ACK packet to the sender
            receiver_socket.sendto(ack_packet, addr)
            print("all done for this packet!" + "\n\n")

        # If the received packet's sequence number matches the expected sequence number
        elif seq_num == expected_seq_num:

            # Process the packet and get the data
            # Extract the data from the received packet
            #data = util.extract_data(packet)
            data = packet[12:].decode()
            print("packet is expected, message string delivered: " + data)
 
            # Create and send ACK
            print("packet is delivered, now creating and sending the ACK packet...")
            
            # Create an ACK packet with the correct ACK number
            ack_packet = util.make_packet('', seq_num, 0)

            # Send the ACK packet to the sender
            receiver_socket.sendto(ack_packet, addr)
            print("all done for this packet!" + "\n\n")
 
            # Change the expected sequence number from 0 to 1 or from 1 to 0
            expected_seq_num = 1 - expected_seq_num
 
        elif seq_num < expected_seq_num:
            # Received a duplicate packet, send ACK again
            ack_packet = util.make_packet('', seq_num, 0)

            # Create an ACK packet with the received sequence number
            # Send the ACK packet to the sender
            receiver_socket.sendto(ack_packet, addr)
            print("Sent duplicate ACK for sequence number " + str(seq_num) + "\n\n")
 
        # If the received packet's sequence number is greater than the expected sequence number
        else:
            # Received an out-of-order packet, discard it and do not send ACK
            print("Discarded packet with sequence number" + str(seq_num) + "\n\n")
 
# Main function 
def main():
    """
      main function which calls the rdt_receiver()
    """
    # Set up the receiver's socket
    receiver_sock = socket(AF_INET, SOCK_DGRAM)
    receiver_sock.bind((host, port))
 
    # Receive packets using the rdt_receive function
    rdt_receive(receiver_sock)
 
    # Close the socket
    receiver_sock.close()
 
 
if __name__ == '__main__':
    main()
 