import os
from app import app, server

debug = (os.getenv('DEBUG', 'False') == 'True')
port = os.getenv('PORT', '7777')

if __name__ == "__main__":
    print "User service starting..."
    server.initialize_redis()
    app.run(host='0.0.0.0', port=int(port), debug=debug)
