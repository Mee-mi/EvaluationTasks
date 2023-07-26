from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route('/square', methods=['GET', 'POST'])
def square_number():
    if request.method == 'POST':
        try:
            number = int(request.form['number'])
            result = number ** 2
            return render_template('index.html', prediction=result)
        except Exception as e:
            # Handle any errors and return an error response
            return jsonify({'error': str(e)}), 500
    else:
        # Display the form
        return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)

