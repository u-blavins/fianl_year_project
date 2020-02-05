from flask import Flask
from blueprints.infrastructure_provisioner import provisioner


app = Flask(__name__)
app.debug = True

app.register_blueprint(provisioner)

@app.route('/')
def index():
    return "Infrastructure Provisioner"

if __name__ == '__main__':
    app.run(port=8080)