from flask import Flask, render_template, request,redirect,url_for,flash,session
app = Flask(__name__)
@app.route('/')
def index():
 return render_template('index.html')

app.run(host='localhost',port=8080, debug=True)

