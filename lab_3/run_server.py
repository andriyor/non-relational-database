from lab_3.app import app

from lab_3.views import tr_app

app.register_blueprint(tr_app)

if __name__ == '__main__':
    app.run(port=3035, debug=True)
