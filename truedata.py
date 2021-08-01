from truedata_ws.websocket.TD import TD
import sys
import pandas as pd
import time
import key

td_id=key.td_id
td_pass=key.td_pass

td_obj = TD(td_id, td_pass,live_port=None)
#
#td_obj_live = TD(td_id, td_pass,historical_port=None)
# This connects you to the default real time port which is 8082 & the REST History feed.
# If you have been authourised on another live port please enter another parameter
# Example
# td_obj = TD('<enter_your_login_id>', '<enter_your_password>', live_port=8084)