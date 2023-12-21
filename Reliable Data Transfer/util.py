# Please run receiver.py before main.py
# Constants for the packet format
 
# Function to create the checksum of the packet 
def create_checksum(packet_wo_checksum):
    """create the checksum of the packet (MUST-HAVE DO-NOT-CHANGE)
 
    Args:
      packet_wo_checksum: the packet byte data (including headers except for checksum field)
 
    Returns:
      the checksum in bytes
 
    """
    # Calculating the checksum using the UDP checksum algorithm
    checksum = 0
 
    # Iterating over the packet bytes in 2-byte chunks
    for i in range(0, len(packet_wo_checksum), 2):
        if i + 1 < len(packet_wo_checksum):
            
            # Extract the current 2-byte chunk
            chunk = packet_wo_checksum[i] + (packet_wo_checksum[i + 1] << 8)
 
            # Add the chunk to the checksum
            checksum += chunk
 
    # One's complement of the checksum
    checksum = (checksum & 0xFFFF) + (checksum >> 16)
    checksum = ~checksum & 0xFFFF
    
    # Convert checksum to bytes
    return checksum.to_bytes(2, 'little')
 
# Function to verify packet checksum
def verify_checksum(packet):
    """verify packet checksum (MUST-HAVE DO-NOT-CHANGE)
 
    Args:
      packet: the whole (including original checksum) packet byte data
 
    Returns:
      True if the packet checksum is the same as specified in the checksum field
      False otherwise
 
    """
    # Extract the original checksum from the packet
    original_checksum = packet[8:10]
 
    # Calculate the checksum of the packet without the original checksum field
    calculated_checksum = create_checksum(packet[:8] + b'\x00\x00' + packet[10:])
 
    # Compare the original checksum with the calculated checksum
    return original_checksum == calculated_checksum
 
# Function to create a packet
def make_packet(data_str, ack_num, seq_num):
    """Make a packet (MUST-HAVE DO-NOT-CHANGE)
 
    Args:
      data_str: the string of the data (to be put in the Data area)
      ack: an int tells if this packet is an ACK packet (1: ack, 0: non ack)
      seq_num: an int tells the sequence number, i.e., 0 or 1
 
    Returns:
      a created packet in bytes
 
    """
    # make sure your packet follows the required format!
 
    # Calculate the packet length
    packet_length = 16
 
    # creating 16 bit value comprising of length, ack_num and seq_num
    length = packet_length << 2
    length |= ack_num << 1
    length |= seq_num << 0
 
    # create packet_wo_checksum. Intialise checksum to 0
    # Bytes 1-8: Fixed identifier
    packet_wo_checksum = b"COMPNETW"  

    # Bytes 9-10: Placeholder for checksum
    packet_wo_checksum += b'\00\00'  

    # Bytes 11-12: Length field in network byte order
    packet_wo_checksum += length.to_bytes(2, 'big')
    
    if (type(data_str) == str):
      packet_wo_checksum += data_str.encode()
    else:
      packet_wo_checksum += data_str
    
    # Calculate checksum
    checksum = create_checksum(packet_wo_checksum)
 
    #Add calculated checksum to the packet to be sent
    # Packet format: HEADER + CHECKSUM + LENGTH + DATA
    packet = packet_wo_checksum[:8] + checksum + packet_wo_checksum[10:]
    
    # Return the created packet
    return packet
 
# Function to extract the sequence number from the packet
def extract_seq_num(packet):
    # Extract the sequence number from the packet using bit manipulation
    # just brute forced this with trial & error to the get the need result
    flags = (packet[10] << 8) + packet[10 + 1]
    
    # Extract the sequence number using bitwise AND
    seq_num = (flags & 0b0000001)

    # Return the extracted sequence number
    return seq_num
 
# Function to extract the ACK number from the packet
def extract_ack_num(packet):
    # extracting ack num from the the packet
    # just brute forced this with trial & error to the get the need result
    flags = (packet[10] << 8) + packet[10 + 1]
    
    # Extract the ACK number using bitwise AND and right shift
    ack_num = (flags & 0b0000010) >> 1
    
    # Return the extracted ACK number
    return ack_num
 
# Function to extract data from the packet
def extract_data(packet):
    # Extract the data from the packet by skipping the header
    # Decode the data from bytes to string
    data = packet[12:].decode()

    # Return the extracted data
    return data
 
###### These three functions will be automatically tested while grading. ######
###### Hence, your implementation should NOT make any changes to         ######
###### the above function names and args list.                           ######
###### You can have other helper functions if needed.                    ######
 