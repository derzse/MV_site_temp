from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')  # Assumes you have an about.html template

@app.route('/privacy')
def privacy():
    return render_template('privacy.html')  # Assumes you have a privacy.html template


if __name__ == '__main__':
    app.run(debug=True)
