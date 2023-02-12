from flask import Flask, render_template, request , jsonify
import cv2
import skimage.io 
from ClassOOP import Processing
from Functions import*
import json

app = Flask(__name__,template_folder="templates")

image1_object =Processing('image1.jpg')
image2_object =Processing('image2.jpg')

#............ To get uploaded images from Front-End and return FFT images..............

@app.route('/', methods=['POST','GET'])
def home():
    if request.method == "POST":
        global image1_object
        global image2_object

        file= request.files['image'].read()   
        default_value = '0'
        name = request.form.get('name', default_value)   
        write_file_to_image(file)  
        img = skimage.io.imread("image.jpg")

        if name==str(1):
            cv2.imwrite('image1.jpg', img)  
            image1_object =Processing('image1.jpg',400,750,60)
            Mag_img1,Phase_img1= savefigures(image1_object.magnitude_spectrum,"mag1.jpg",image1_object.phase_spectrum,"phase1.jpg")
            return jsonify({'status':str(Mag_img1),'status2':str(Phase_img1)})

        elif name==str(2):
            cv2.imwrite('image2.jpg', img)
            image2_object =Processing('image2.jpg',400,750,400)
            Mag_img2,Phase_img2=savefigures(image2_object.magnitude_spectrum,"mag2.jpg",image2_object.phase_spectrum,"phase2.jpg")
            return jsonify({'status':str(Mag_img2),'status2':str(Phase_img2)})
    
    return render_template('index.html')

#............ To get coordinates from Front-End and return Reconstruct image..............

@app.route('/coordinates', methods=['POST','GET'])
def coordinates():
    if request.method == "POST":
        global image1_object
        global image2_object
        if  request.get_json()!= None:
            output = request.get_json()
            co = json.loads(output)
            image1_object.reconstruct(image2_object,co['Mag_rectangle_x: ' ]
            ,co['Mag_rectangle_y: '],co['Mag_rectangle_width: ' ],co['Mag_rectangle_height: '],
            co['Phase_rectangle_x: '],co['Phase_rectangle_y: '],co['Phase_rectangle_width: '],co[ 'Phase_rectangle_height: ' ],co['inverse: '])
            print(co)
            rec=save_output(image1_object.img_output)
            return jsonify({'status':str(rec)})
        
    return render_template('index.html')


if __name__ == '__main__':
   app.run(debug=True)