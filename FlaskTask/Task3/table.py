from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

@app.route("/")
def getTableNumber():
    return render_template("index3.html")

@app.route('/table', methods=['GET', 'POST'])

def generate_table():
 if request.method == 'POST':
    tableNumber = int(request.form["number"])

    return render_template('index3.html' , num = tableNumber)

if __name__ == '__main__':
    # Run the Flask app on localhost (127.0.0.1) and port 5000
    app.run(debug=True)
