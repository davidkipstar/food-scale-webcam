from flask import Flask, render_template
import os

app = Flask(__name__, template_folder = './templates')
app.config['UPLOAD_FOLDER'] = 'static'
pwd = os.getcwd()

@app.route('/')
@app.route('/index')
def show_index():
    full_filename = f"./static/img.jpg"
    return render_template("index.html", user_image = full_filename)
    
if __name__ == "__main__":
    app.run(debug=True)
