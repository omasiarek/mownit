import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Slider, TextInput, Select
from bokeh.plotting import figure


DEFAULT_VALUE = 0

# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt


# Set up widgets
# Total population, N.
N = TextInput(title="Populacja")
# Initial number of infected and recovered individuals, I0 and R0.
I0 = TextInput(title="Ilość początkowa przypadków")
R0 = TextInput(title="Ilość ozdrowiałych przypadków")
# Contact rate, beta, and mean recovery rate, gamma, (in 1/days).
beta = Slider(title="Prawdopodobieństwo zakażenia", value = DEFAULT_VALUE, start=0, end=1, step=0.05)
gamma = Slider(title="Ilość dni do ozdrowienia", value=1, start=1, end=60, step=1)
# A grid of time points (in days)
t = TextInput(title="Okres epidemii")


source = ColumnDataSource(data=dict(t=[], S=[], I=[], R=[]))

def update_data(attrname, old, new):
  if (N.value=="" or I0.value=="" or R0.value=="" or beta.value=="" or gamma.value=="" or t.value==""):
    return
  Nx = int(N.value)
  I0x = int(I0.value)
  R0x = int(R0.value)
  betax = float(beta.value)
  gammax = 1.0/float(gamma.value)
  tx = np.linspace(0, int(t.value), int(t.value))
  # Initial conditions vector
  S0 = Nx - I0x - R0x
  y0 = S0, I0x, R0x
  # Integrate the SIR equations over the time grid, t.
  ret = odeint(deriv, y0, tx, args=(Nx, betax, gammax))
  S, I, R = ret.T
  source.data = dict(t=tx, S=S, I=I, R=R)

N.on_change('value', update_data)
I0.on_change('value', update_data)
R0.on_change('value', update_data)
beta.on_change('value_throttled', update_data)
gamma.on_change('value_throttled', update_data)
t.on_change('value', update_data)


plot = figure(plot_height=800, plot_width=800, title="Epidemia",
              tools="crosshair,pan,reset,save,wheel_zoom")

plot.line('t', 'S', source=source, line_color="blue", legend_label="Podatni na wirusa")
plot.line('t', 'I', source=source, line_color="red", legend_label="Zainfekowani")
plot.line('t', 'R', source=source, line_color="green", legend_label="Ozdrowiali")
plot.xaxis.axis_label = "Dzień"
plot.yaxis.axis_label = "Populacja"

inputs = column(N, I0, R0, beta, gamma, t)

curdoc().add_root(row(inputs, plot, width=1500))
curdoc().title = "Epidemic"
