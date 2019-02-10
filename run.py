import sys, os

sys.path.append(os.getcwd())

import zeton

app = zeton.create_app()
app.run()
