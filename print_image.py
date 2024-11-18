import time
import serial
from PIL import Image
import numpy as np


def LoadImage():
    # image must be in monochrome bitmap
	# format: 1B 58 31 0B 30 + image data
    # where = 1B 58 31 = image format
	# 0B 30 = width x height (tes.bmp: 84x48 pixel)
	# 0B = image width/8 -> 84/8 = 11 (in decimal) -> 0B (in hex)
	# 30 = image height = 48 (in decimal) -> 30 in hexa
	# see: http://bluebamboo.helpserve.com/index.php?/Knowledgebase/Article/View/48
    # 0x55 ,  0x66 ,  0x77 ,  0x88 ,  0x44 ,  0x1B ,  0x58 ,  0x31
    # converting from hex to bytes screws it up...
    img_raw = Image.open('relaxin.png')
    # convert to monochrome bitmap
    img_raw = img_raw.convert('1')
    #img_raw = np.asarray(img_raw)
    # resize to 84...
    base_width = 88
    wpercent = (base_width / float(img_raw.size[0]))
    hsize = int((float(img_raw.size[1]) * float(wpercent)))
    img_adj = img_raw.resize((base_width, hsize), Image.Resampling.LANCZOS)
    img_adj = np.asarray(img_adj)
    # is currently an ndarray, should make it a bytearray?
    # header_list = ['55', '66', '77', '88', '44', '1b', '58', '31', str(int(base_width/8)), str(int(hsize))]
    header_list =  ['1b', 'X', '1', hex(int(base_width/8)), hex(int(hsize))]
    #header_str = '\x1b\x58\x31'
    # imgsize = bytearray(int(base_width/8)) # fix this
    # imgsize += bytearray(hsize)
    header = bytearray(b'')
    for i in range(len(header_list)):
        header += bytearray(header_list[i], 'utf-8')
    resize_img = Image.fromarray(img_adj)
    resize_img.show()
    img_flat = np.reshape(img_adj, (1,-1))
    img_flat = img_flat.flatten()
    #img_byte = bytearray(img_flat)
    img_out = header
    for i in range(len(img_flat)):
        if img_flat[i] == True:
            img_out += b'\x00'
        else:
            img_out += b'\xFF'
    return img_out

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM3',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.EIGHTBITS
)

ser.isOpen()
print("Serial Open")

# end command: \n
term_bytes = LoadImage()
ret_byte = bytearray('\n', 'utf-8')
term_bytes += ret_byte
ser.reset_output_buffer
ser.write(term_bytes)
out = ''
time.sleep(0.5)
while ser.inWaiting() > 0:
    out += ser.read(1)
if out != '':
    print(">>") + out
ser.close()
exit()