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

    # resize to 84...
    base_width = 88
    wpercent = (base_width / float(img_raw.size[0]))
    hsize = int((float(img_raw.size[1]) * float(wpercent)))
    img_adj = img_raw.resize((base_width, hsize), Image.Resampling.LANCZOS)
    img_adj = np.asarray(img_adj)

    # is currently an ndarray, should make it a bytearray?
    # let's give it as an ndarray (each item can be bitized)
    # 85, 102, 119, 136, 68 #intro header 
    # [1d, 76, 30] [27, 88, 49] (or 52)
    header_list = [27, 88, 52, int(base_width/8), int(hsize)]
    header_list = np.array(header_list)
 
    #resize_img = Image.fromarray(img_adj)
    #resize_img.show()
    img_flat = np.reshape(img_adj, (1,-1))
    img_flat = img_flat.flatten()
    img_flat = 255*np.array(img_flat)
    img_out = np.append(header_list,img_flat)
    return img_out

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

ser.reset_output_buffer
for i in range(len(term_bytes)):
    to_ser = bytearray(hex(term_bytes[i]),'utf-8')
    ser.write(to_ser)
ser.write(bytearray('\n', 'utf-8'))
out = ''
time.sleep(0.5)
while ser.inWaiting() > 0:
    out += ser.read(1)
if out != '':
    print(">>") + out
ser.close()
exit()