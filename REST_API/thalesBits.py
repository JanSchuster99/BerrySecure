from RNGRaspPi import generateRandomNumber

import time
#script to generate the 7.2M bits in a binary file 
#the file will be saved with the current timestamp in this dir
def create_binary_file(binary_string):
    # Convert binary string to bytes
    binary_data = bytearray()
    for i in range(0, len(binary_string), 8):
        byte = binary_string[i:i + 8]
        decimal = int(byte, 2)
        binary_data.append(decimal)

    # Get the current timestamp
    timestamp = time.strftime("%Y%m%d%H%M%S")

    # Create the filename with the current timestamp
    filename = f"thalesBits{timestamp}.bin"

    # Save the binary data to a file
    with open(filename, "wb") as file:
        file.write(binary_data)

    print(f"Binary file '{filename}' created successfully.")


rstring = generateRandomNumber(7200000,1)
print("length of string:")
print(len(rstring))
create_binary_file(rstring)

