from flask import Flask, render_template, request, url_for

# configuration
DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/shortener', methods=['GET', 'POST'])
def shortener():
    short_url = 'Here will be you short url'
    if request.method == 'POST':
        full_url = request.form['full_url']
        if full_url != "":
            short_url = convert_url(full_url) 
    return render_template('shortener.html', short_url=short_url)

def convert_url(full_url):
    """
    Returns shortened url
    """
    return "Wow, nice short url"
            
        
    

if __name__ == '__main__':
    app.run()
