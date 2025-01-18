from flask import Flask, request, jsonify, send_file ,render_template
from PIL import Image, ImageFilter
import os
from datetime import datetime

app = Flask(__name__)

# Configuration for file uploads

UPLOAD_FOLDER = './static/uploads'
FILTERED_FOLDER = './filtered_images'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(FILTERED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['FILTERED_FOLDER'] = FILTERED_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and allowed_file(file.filename):
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + '_' + file.filename
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return jsonify({'message': 'File uploaded successfully', 'filepath': filepath}), 200

    return jsonify({'error': 'Invalid file format'}), 400


@app.route('/filter', methods=['POST'])
def apply_filter():
    data = request.json
    if not data or 'filepath' not in data or 'filter' not in data:
        return jsonify({'error': 'Invalid request data'}), 400

    filepath = data['filepath']
    filter_type = data['filter']

    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    try:
        img = Image.open(filepath)
        if filter_type == 'BLUR':
            img = img.filter(ImageFilter.BLUR)
        elif filter_type == 'CONTOUR':
            img = img.filter(ImageFilter.CONTOUR)
        elif filter_type == 'DETAIL':
            img = img.filter(ImageFilter.DETAIL)
        elif filter_type == 'EDGE_ENHANCE':
            img = img.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_type == 'SHARPEN':
            img = img.filter(ImageFilter.SHARPEN)
        else:
            return jsonify({'error': 'Unsupported filter type'}), 400

        filtered_filename = 'filtered_' + os.path.basename(filepath)
        filtered_filepath = os.path.join(app.config['FILTERED_FOLDER'], filtered_filename)
        img.save(filtered_filepath)

        return jsonify({'message': 'Filter applied successfully', 'filtered_filepath': filtered_filepath}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/download', methods=['GET'])
def download_filtered_image():
    filepath = request.args.get('filepath')
    if not filepath or not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404

    return send_file(filepath, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
