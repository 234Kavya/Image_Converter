from flask import Flask, render_template, request, send_file
from io import BytesIO
from PIL import Image, ImageFilter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'imageFile' not in request.files:
        return "No image uploaded", 400

    image_file = request.files['imageFile']
    output_format = request.form['outputFormat']
    resize_width = request.form.get('resizeWidth')
    resize_height = request.form.get('resizeHeight')
    filter_type = request.form.get('filter')

    if image_file.filename == '':
        return "No image selected", 400

    # Save the uploaded image temporarily
    temp_image_path = 'temp_image.' + image_file.filename.rsplit('.', 1)[1]
    image_file.save(temp_image_path)

    # Open the uploaded image
    img = Image.open(temp_image_path)

    # Resize image if dimensions are provided
    if resize_width and resize_height:
        img = img.resize((int(resize_width), int(resize_height)))

    # Apply filter if selected
    if filter_type == 'grayscale':
        img = img.convert('L')
    elif filter_type == 'blur':
        img = img.filter(ImageFilter.BLUR)
    elif filter_type == 'sharpen':
        img = img.filter(ImageFilter.SHARPEN)
    # Add other filter conditions here

    # Save the converted image to BytesIO buffer
    output_image = BytesIO()
    img.save(output_image, format=output_format)
    output_image.seek(0)

    # Provide the converted image for download
    return send_file(output_image, as_attachment=True, download_name=f"converted_image.{output_format}")

if __name__ == '__main__':
    app.run(debug=True)
