""" To view this example, first start a Bokeh server:

    bokeh serve --allow-websocket-origin=localhost:8000

And then load the example into the Bokeh server by
running the script:

    python animated.py

in this directory. Finally, start a simple web server
by running:

    python -m SimpleHTTPServer  (python 2)

or

    python -m http.server  (python 3)

in this directory. Navigate to

    http://localhost:8000/animated.html

"""
from __future__ import print_function

from numpy import pi, cos, sin, linspace, roll

from bokeh.client import push_session
from bokeh.embed import autoload_server
from bokeh.plotting import figure, curdoc
import datetime

from random import randint
init_temp=25
init_target=50

# figure() function auto-adds the figure to curdoc()
p = figure()
r = p.multi_line(xs=[0, 0], ys=[[init_temp], [init_target]],color=['red','green'])

session = push_session(curdoc())

html = """
<html>
  <head></head>
  <body>
    %s
  </body>
</html>
""" % autoload_server(p, session_id=session.id)

with open("animated.html", "w+") as f:
    f.write(html)

print(__doc__)

ds = r.data_source

def update():
    temp_line = ds.data["ys"][0]
    temp_line.append(randint(20,30))
    target_line = ds.data["ys"][1]
    target_line.append(randint(40,50))
    ds.data.update(ys=[temp_line, target_line])
    ds.data.update(xs=[range(0,len(temp_line)), range(0,len(temp_line))])

curdoc().add_periodic_callback(update, 1000)

session.loop_until_closed() # run forever
