import sys, os

sys.path.append(os.getcwd())

import zeton

app = zeton.create_app()

if __name__ == '__main__':
    # if you want test on computer use this command
    app.run(debug=True)

    # # If you want test on mobile use this command
    # # also you must use your local ip in your browser
    # # Only one statment app.run is allowed
    # app.run(host='0.0.0.0', port=80, debug=True)
