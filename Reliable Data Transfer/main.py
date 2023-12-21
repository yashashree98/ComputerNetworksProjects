# Import the Sender class from the sender module
from sender import Sender

# Create an instance of the Sender class
sender = Sender() 

# Loop from 1 to 10 (inclusive)
for i in range(1, 10):
    # Send a message using the rdt_send method of the Sender class
    sender.rdt_send('msg' + str(i))