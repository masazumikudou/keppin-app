from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

from routes.shortage import bp as shortage_bp
from routes.view import bp as view_bp

app.register_blueprint(shortage_bp)
app.register_blueprint(view_bp)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8090))
    app.run(host='0.0.0.0', port=port, debug=True)
