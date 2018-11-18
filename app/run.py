from flask import Flask, jsonify, render_template
from models import user
from flask_debugtoolbar import DebugToolbarExtension
import sys
sys.stdout = sys.stderr = open('/tmp/flask_log.log','wt')

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '1234'
toolbar = DebugToolbarExtension(app)

@app.route('/')
def index():
    u = user.get_by_id(id=0)
    data = {
        'user': user.get_by_id(id=0)
    }
    u2 = user.get_by_id(id=0)
    return render_template("index.html", value=data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')