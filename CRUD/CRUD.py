from flask import Flask, jsonify, request
import os

app = Flask(__name__)

# Sample data (can be replaced with a database)
books = [
    {"id": 1, "book_name": "book1", "author": "author1"},
    {"id": 2, "book_name": "book2", "author": "author2"}
]

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books), 200

# Get a specific book by ID
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return jsonify(book), 200
    return jsonify({'error': 'Book not found'}), 404

# Create a book
@app.route('/books', methods=['POST'])
def create_book():
    if not request.json or not 'title' in request.json or not 'author' in request.json:
        return jsonify({'error': 'Invalid input'}), 400

    new_book = {
        'id': len(books) + 1,
        'book_name': request.json['title'],
        'author': request.json['author']
    }
    books.append(new_book)
    return jsonify(new_book), 201

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    for book in books:
        if book['id'] == book_id:
            book['book_name'] = request.json.get('title', book['book_name'])
            book['author'] = request.json.get('author', book['author'])
            return jsonify(book), 200
    return jsonify({'error': 'Book not found'}), 404

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    for book in books:
        if book['id'] == book_id:
            books.remove(book)
            return jsonify({"data": "Book Deleted Successfully"}), 200
    return jsonify({'error': 'Book not found'}), 404

# Upload a book file
@app.route('/uploadbook', methods=['POST'])
def uploadbook():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    uploaded_file = request.files['file']
    if uploaded_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if not allowed_file(uploaded_file.filename):
        return jsonify({'error': 'Invalid file type'}), 400

    destination = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
    uploaded_file.save(destination)
    return jsonify({'data': 'File Uploaded Successfully'}), 200

def allowed_file(filename):
    ALLOWED_EXTS = {'png', 'jpg', 'jpeg'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTS

# Run the Flask App
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
