from flask import Flask, request, jsonify, render_template
import hashlib

app = Flask(__name__)

@app.route('/img', methods=['GET', 'POST'])
def calculate_md5():
    if request.method == 'POST':
        try:
            if 'img' not in request.files:  # Corrected the field name here
                return jsonify({'error': 'No image file provided.'}), 400

            image = request.files['img']  # Corrected the field name here

            # Read the image bytes and calculate the MD5 hash
            im_bytes = image.read()
            im_hash = hashlib.md5(im_bytes).hexdigest()

            return render_template('index2.html', md5_hash=im_hash)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
            
    else:
        return render_template('index2.html')

if __name__ == '__main__':
    # Run the Flask app on localhost (127.0.0.1) and port 6000
    app.run(port=6000, debug=True)
