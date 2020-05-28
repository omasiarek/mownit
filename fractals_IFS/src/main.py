''' Present an interactive IFS explorer.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve main.py
at your command prompt.
Then navigate to the URL http://localhost:5006/main in your browser.
'''

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput, Select
from bokeh.plotting import figure
from ifs import ifs_points, mat_by_type

DEFAULT_ITERS = 10000
DEFAULT_COLOR = "#000000"

x, y = ifs_points(DEFAULT_ITERS, mat_by_type["paproc"])

source = ColumnDataSource(data=dict(x=x, y=y, color=[DEFAULT_COLOR for _ in x]))

# Set up plot
plot = figure(plot_height=800, plot_width=800, title="IFS",
              tools="crosshair,pan,reset,save,wheel_zoom")

plot.scatter('x', 'y', source=source, radius=0.001, fill_color='color', line_color=None)
plot.xgrid.visible = False
plot.ygrid.visible = False

obj_map = {
    "Paproc": "paproc",
    "Drzewo": "drzewo",
    "Lisc klonu": "klon",
    "Spirala": "spirala",
    "Drzewo symetryczne": "drzewoSymetryczne",
    "Lisc": "lisc",
    "Sniezynka": "sniezynka",
    "Smok": "smok",
    "Galazka": "galazka"
}

col_map = {
    "Czarny": "#000000",
    "Zolty": "#ffff00",
    "Zielony": "#00cc00",
    "Niebieski": "#0066ff",
    "Czerwony": "#cc0000",
    "Pomaranczowy": "#ff9900",
    "Szary": "#669999",
    "Fioletowy": "#993399"
}


# Set up widgets
obj = Select(title="Obiekt", options=sorted(obj_map.keys()), value="Paproc")
iterations = Slider(title="Ilosc iteracji", value=DEFAULT_ITERS, start=10000, end=1000000, step=DEFAULT_ITERS)
col = Select(title ="Kolor", options=sorted(col_map.keys()), value="Czarny")

def update_data():
    iters = int(iterations.value)
    color = col_map[col.value]
    object_type = obj_map[obj.value]
    mat = mat_by_type[object_type]

    # Generate the new curve
    x, y = ifs_points(iters, mat)

    source.data = dict(x=x, y=y, color=[color for _ in x])

# Set up callbacks

def handle_object_change(attrname, old, new):
    iterations.value = DEFAULT_ITERS
    update_data()

def handle_color_change(attrname, old, new):
    update_data()

def handle_iterations_change(attrname, old, new):
    update_data()

obj.on_change('value', handle_object_change)
col.on_change('value', handle_color_change)
iterations.on_change('value_throttled', handle_iterations_change)



# Set up layouts and add to document
inputs = column(obj, iterations, col)

curdoc().add_root(row(inputs, plot, width=1500))
curdoc().title = "Fractals"
