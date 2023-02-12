import numpy as np
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import io 
import base64 

def write_file_to_image(file):
    npimg = np.fromstring(file, np.uint8)
    img = cv2.imdecode(npimg,cv2.IMREAD_COLOR)
    img = Image.fromarray(img.astype("uint8"))
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read())
    with open("image.jpg", "wb") as fh:
        fh.write(base64.decodebytes(img_base64)) 

def savefigures(magnitude_spectrum,mag_name,phase_spectrum,phase_name):
    fig =plt.figure(figsize=(15, 20))
    plt.imshow(magnitude_spectrum, cmap='gray')
    plt.savefig(mag_name)
    plt.imshow(phase_spectrum, cmap='gray')
    plt.savefig(phase_name)    
    Mag_img= Image.open(mag_name)
    Phase_img= Image.open(phase_name) 
    data = io.BytesIO()
    Mag_img.save(data, "JPEG")
    data2 = io.BytesIO()
    Phase_img.save(data2, "JPEG")
    Magnitude_Image = base64.b64encode(data.getvalue())
    Phase_Image=base64.b64encode(data2.getvalue())
    return Magnitude_Image,Phase_Image  

def save_output(img_output):
    plt.imsave("reconstruct_img.jpg", img_output)
    gray_img = cv2.imread("reconstruct_img.jpg", cv2.IMREAD_GRAYSCALE) 
    color_img = cv2.cvtColor(gray_img, cv2.COLOR_GRAY2RGB) 
    plt.imsave("reconstruct_img.jpg", color_img)
    Reconstruct_img= Image.open("reconstruct_img.jpg")
    data3 = io.BytesIO()
    Reconstruct_img.save(data3, "JPEG")
    Reconstruct_Image=base64.b64encode(data3.getvalue())
    return Reconstruct_Image
