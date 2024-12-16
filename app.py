from flask import Flask, request, render_template
from calc_parameters import *

app = Flask(__name__)

@app.route('/')
def upload_page():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400
    
    file = request.files['file']

    if file.filename == '':
        return "No selected file", 400

    if file:
        try:
            img = decode_image(file)
            brightness = check_brightness(img, 50, 200)
            resolution = check_resolution(img)
            blurriness = check_blurriness(img, 50, 150)
            vibrancy = check_vibrancy(img, 30, 150)

            return render_template('index.html', brightness=brightness, resolution=resolution, 
                                   blurriness=blurriness, vibrancy=vibrancy)
        
        except Exception as e:
            return f"Error processing the file: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)
