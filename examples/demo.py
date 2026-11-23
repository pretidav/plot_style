"""Demo: python examples/demo.py  ->  demo.png"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import TwoSlopeNorm

import plot_style
from plot_style import ACCENT, INK

plot_style.use()
x = np.linspace(0, 10, 200)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.6))
ax1.plot(x, np.exp(-x / 4) * np.cos(2 * x), color=ACCENT, lw=2.4, label="DAMPED")
ax1.plot(x, np.exp(-x / 4), color=INK, ls=plot_style.DASHED, label="ENVELOPE")
ax1.plot(x[::10], np.exp(-x[::10] / 4) * np.cos(2 * x[::10]), "s", color=INK, label="SAMPLES")
ax1.set_xlabel("TIME")
ax1.set_ylabel(r"AMPLITUDE  $e^{-t/4}\cos 2t$")
ax1.set_title("[ OSCILLATOR ]")
plot_style.legend(ax1, "upper right")

g = np.linspace(-2, 2, 120)
z = np.outer(np.sin(g * 2), np.cos(g * 2)) + 0.2 * g
m = ax2.pcolormesh(g, g, z, cmap=plot_style.CMAP_DIVERGING, norm=TwoSlopeNorm(0), shading="nearest")
ax2.set_title("[ DIVERGING MAP ]")
fig.colorbar(m, ax=ax2)

for ax in (ax1, ax2):
    plot_style.style_axes(ax, grid=ax is ax1)
fig.tight_layout()
plot_style.savefig(fig, "demo.png")
