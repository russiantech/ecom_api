import sys
import time
from datetime import datetime

from flask import g
from flask_jwt_extended import current_user

from apis.ecommerce_api.factory import db, app

start_time = 0


# TODO: not working, what did I wrong ??
@app.before_request
def before_req():
    global start_time
    g.user = current_user
    # start_time = time.clock()
    start_time = time.perf_counter() 


@app.after_request
def after_req(response):
    # end_time = time.clock()
    end_time = time.perf_counter() 
    elapsed = (end_time - start_time) * 1000
    sys.stdout.write('Request took %d milliseconds\n' % elapsed)
    return response
