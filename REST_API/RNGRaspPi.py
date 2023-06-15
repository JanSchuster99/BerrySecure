import pyaudio
import struct
import subprocess

def generateRandomNumber(length, amount):
    # Check if microphone is connected: return empty string if not 
    process = subprocess.Popen('arecord -l', shell=True, stdout=subprocess.PIPE)
    output = process.stdout.read().decode('utf8')
    if not output.__contains__('USB Audio'):
        return ""
    
    # Create an instance of the PyAudio class
    p = pyaudio.PyAudio()

    # Open a stream to record audio from the default input device
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True, frames_per_buffer=512)

    # Discard the first 2 seconds worth of audio samples because it contains patterns
    for i in range(0, int(44100 / 512 * 2)):
        stream.read(512, exception_on_overflow=False)

    # Initialize the LSB string
    lsb_string = ""

    # Loop until the desired string length is reached
    while len(lsb_string) < length*amount:
        # Read a buffer of audio samples from the stream
        buffer = stream.read(512, exception_on_overflow=False)

        # Convert the buffer to a list of integers
        samples = list(struct.unpack('h'*512, buffer))

        # Extract the least significant bit from each sample and add it to the LSB string
        for sample in samples:
            lsb_string += str(sample % 2)

    # Close the audio stream and PyAudio instance
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Cut the string to desired length
    lsb_string = lsb_string[:length*amount]
    return lsb_string

def encode_in_hex(length,lsb_string):
    # Split the string to desired length and write each string to a list
    stringList = [lsb_string[i:i+length] for i in range(0, len(lsb_string), length)]
    # Write leading 0s to the string if it is not divisible by 4
    for i, string in enumerate(stringList):
        if len(string) % 4 != 0:
            stringList[i] = '0'*(4 - len(string) % 4) + string
    hex_list = []
    # Calculate length of the hex number for the result list
    lengthOfHex = len(stringList[0])/4
    # Convert binary strings to hex strings
    for binary_str in stringList:
        decimal_num = int(binary_str, 2)
        hex_str = hex(decimal_num)[2:].upper()
        hex_list.append(hex_str)
    # Add leading 0s to the hex strings
    for i, string in enumerate(hex_list):
        if(not len(string) == int(lengthOfHex)):
            hex_list[i] = "0"*(int(lengthOfHex)-len(string))+string

    # Split the hexadecimal string into substrings of the desired length
    return hex_list


