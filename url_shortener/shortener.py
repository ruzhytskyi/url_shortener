from flask import Flask, render_template, request, url_for

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/shortener', methods=['GET', 'POST'])
def shortener():
    if request.method == 'GET':
        return render_template('shortener.html')
    

if __name__ == '__main__':
    app.run()
