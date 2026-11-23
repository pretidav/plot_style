"""Retro / digital-brutalist matplotlib style.

Monospace font, hard black box, inward ticks, dotted grid, one accent colour.

    import matplotlib.pyplot as plt
    import plot_style

    plot_style.use()                 # or: plt.style.use("plot_style.brutalist")
    fig, ax = plt.subplots()
    ax.plot(x, y)
    plot_style.style_axes(ax)        # optional: square corners of the box
    plot_style.savefig(fig, "figure.png")

The font (Space Mono, SIL Open Font License) comes with the package and is registered in matplotlib when the
package is imported. Almost everything else is in ``brutalist.mplstyle``. The functions only do what a style file cannot: the square
corners of the box, the width of the frame of the legend, and a few helpers.
"""
from importlib import resources

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap

__version__ = "0.1.0"

PAPER, INK, ACCENT, GREY, SAND = "#f2efe6", "#000000", "#ff3b00", "#6b6b6b", "#c9b9a0"
DASHED = (0, (4, 3))  # linestyles used for reference lines and for the boundaries
DOTTED = (0, (1, 3))

#: directory of the fonts that come with the package: Space Mono, regular, bold, italic, bold italic (OFL)
FONTS_DIR = resources.files(__package__) / "fonts"
for _font in sorted(FONTS_DIR.iterdir()):  # registered at import, so the style works without installing the font
    if _font.name.endswith(".ttf"):
        font_manager.fontManager.addfont(str(_font))

#: path of the style file, to be used with ``plt.style.use(plot_style.STYLE_PATH)``
STYLE_PATH = str(resources.files(__package__) / "brutalist.mplstyle")

#: diverging map INK - PAPER - ACCENT (centred on zero with ``TwoSlopeNorm``) and sequential map PAPER - INK
CMAP_DIVERGING = LinearSegmentedColormap.from_list("brutalist_div", [INK, PAPER, ACCENT])
CMAP_SEQUENTIAL = LinearSegmentedColormap.from_list("brutalist_seq", [PAPER, INK])
for _cmap in (CMAP_DIVERGING, CMAP_SEQUENTIAL):
    try:
        mpl.colormaps.register(_cmap)
    except ValueError:  # already registered (module reloaded)
        pass


def use():
    """Apply the style to every figure created from now on."""
    plt.style.use(STYLE_PATH)


def context():
    """The style for a block only: ``with plot_style.context(): ...``."""
    return plt.style.context(STYLE_PATH)


def style_axes(ax, grid=True):
    """Finish the axes: closed box with square corners, hard ticks, dotted grid (``grid=False`` to remove it).

    It is also enough to call this on axes created without ``use()``, but then the font and the sizes are the
    defaults of matplotlib: call ``use()`` or ``context()`` first.
    """
    ax.set_facecolor(PAPER)
    if grid:
        ax.grid(True, which="major", color=INK, lw=0.5, ls=DOTTED)
    else:
        ax.grid(False)
    ax.set_axisbelow(True)
    ax.tick_params(direction="in", length=6, width=2, color=INK)
    for sp in ax.spines.values():
        sp.set_visible(True)
        sp.set_linewidth(3)
        sp.set_color(INK)
        sp.set_capstyle("projecting")  # square corners
    return ax


def style_legend(leg):
    """Hard frame for a legend."""
    leg.get_frame().set_linewidth(2)
    return leg


def legend(ax, loc="best", **kw):
    """``ax.legend`` with the style: square frame, opaque paper background, hard border."""
    kw = {"fancybox": False, "framealpha": 1, "edgecolor": INK, "facecolor": PAPER, "borderpad": 0.8,
          "fontsize": 8, **kw}
    return style_legend(ax.legend(loc=loc, **kw))


def new_figure(figsize=(8, 5)):
    """A figure with the style applied (what the figures of the blog use)."""
    use()
    return plt.figure(figsize=figsize, facecolor=PAPER)


def savefig(fig, path, dpi=150, **kw):
    """Save with the paper background, so that the figure does not come out transparent or white."""
    fig.savefig(path, dpi=dpi, facecolor=PAPER, **kw)
