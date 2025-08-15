from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def home():
    return {"status": "ok", "message": "Simple server running", "port": os.environ.get('PORT', 5000)}

@app.route('/api/health')
def health():
    return {"status": "healthy", "message": "Simple health check", "timestamp": "2025-08-15"}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"🚀 Starting server on port {port}")
    print(f"🌍 Server will be available on port {port}")
    app.run(host='0.0.0.0', port=port, debug=False)
