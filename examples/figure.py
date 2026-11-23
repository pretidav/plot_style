"""The figure of the README: python examples/figure.py  ->  figure.png (next to this file)"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import plot_style

plot_style.use()

x = np.linspace(0, 10, 200)
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x, np.cos(x), color=plot_style.ACCENT, label="COS")   # the colour cycle is ink, accent, grey, sand
ax.plot(x, np.sin(x), color=plot_style.INK, ls=plot_style.DASHED, label="SIN")
ax.set_xlabel("TIME")
ax.set_ylabel(r"AMPLITUDE  $f(t)$")
ax.set_title("[ OSCILLATOR ]")

plot_style.style_axes(ax)                # square corners of the box (a style file cannot set them)
plot_style.legend(ax, "upper right")     # square, opaque legend with a hard frame
plot_style.savefig(fig, Path(__file__).with_name("figure.png"))    # paper background, 150 dpi
