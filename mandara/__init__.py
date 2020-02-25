from flask import Flask

app = Flask(__name__)
#app.config.from_object('mandara.config')

import mandara.views
