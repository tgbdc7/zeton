import sys, os

sys.path.append(os.getcwd())

import zeton

app = zeton.create_app()

if __name__ == '__main__':
    # if you want test on computer use this command
    port = os.environ.get('PORT', 5000)
    app.run(host= '0.0.0.0', port=port, debug=True)

    # # If you want test on mobile use this command
    # # also you must use your local ip in your browser
    # # Only one statment app.run is allowed
    # app.run(host='0.0.0.0', port=80, debug=True)
#comment