## Important imports ##
from flask import Flask, render_template

##neccesary code##
app = Flask(__name__)

## render 'homepage.html' when 127
@app.route("/")
def hello():
    return render_template('homepage.html')
 
## To run the Flask##
if __name__ == "__main__":
    app.run()