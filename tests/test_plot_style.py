import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pytest

import plot_style


@pytest.fixture(autouse=True)
def reset():
    yield
    plt.close("all")
    matplotlib.rcdefaults()


def test_style_file_is_installed_and_loads():
    plot_style.use()
    assert matplotlib.rcParams["axes.linewidth"] == 3
    assert matplotlib.colors.to_hex(matplotlib.rcParams["figure.facecolor"]) == plot_style.PAPER
    assert matplotlib.rcParams["axes.grid"] is True
    assert matplotlib.rcParams["xtick.direction"] == "in"
    assert matplotlib.rcParams["font.family"][0] == "Space Mono"


def test_use_by_name():
    plt.style.use("plot_style.brutalist")
    assert matplotlib.rcParams["axes.linewidth"] == 3


def test_context_restores_rcparams():
    before = matplotlib.rcParams["axes.linewidth"]
    with plot_style.context():
        assert matplotlib.rcParams["axes.linewidth"] == 3
    assert matplotlib.rcParams["axes.linewidth"] == before


def test_grid_linestyle_is_dotted():
    with plot_style.context():
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1])
        fig.canvas.draw()
        assert matplotlib.rcParams["grid.linestyle"] == plot_style.DOTTED
        assert ax.xaxis.get_gridlines()[0]._unscaled_dash_pattern == plot_style.DOTTED
        assert ax.xaxis.get_gridlines()[0].get_linewidth() == 0.5


def test_style_axes_box():
    with plot_style.context():
        fig, ax = plt.subplots()
        plot_style.style_axes(ax)
    for sp in ax.spines.values():
        assert sp.get_visible() and sp.get_linewidth() == 3 and sp.get_capstyle() == "projecting"
    assert matplotlib.colors.to_hex(ax.get_facecolor()) == plot_style.PAPER


def test_legend_and_savefig(tmp_path):
    fig = plot_style.new_figure((4, 3))
    ax = fig.add_subplot()
    ax.plot([0, 1], [0, 1], label="A")
    leg = plot_style.legend(ax)
    assert leg.get_frame().get_linewidth() == 2
    assert leg.get_frame().get_boxstyle().__class__.__name__ == "Square"
    out = tmp_path / "f.png"
    plot_style.savefig(fig, out)
    assert out.stat().st_size > 1000


def test_colormaps_registered():
    assert matplotlib.colormaps["brutalist_div"](0.0) == matplotlib.colors.to_rgba(plot_style.INK)
    assert matplotlib.colormaps["brutalist_div"](1.0) == matplotlib.colors.to_rgba(plot_style.ACCENT)
    assert matplotlib.colormaps["brutalist_seq"](0.0) == matplotlib.colors.to_rgba(plot_style.PAPER)


def test_bundled_font_is_registered():
    from pathlib import Path

    fonts = Path(str(plot_style.FONTS_DIR))
    files = sorted(p.name for p in fonts.glob("*.ttf"))
    assert files == ["SpaceMono-Bold.ttf", "SpaceMono-BoldItalic.ttf", "SpaceMono-Italic.ttf", "SpaceMono-Regular.ttf"]
    registered = {Path(f.fname).name for f in matplotlib.font_manager.fontManager.ttflist
                  if Path(f.fname).parent == fonts}
    assert registered == set(files)
    assert (fonts / "OFL.txt").exists()
    plot_style.use()
    found = Path(matplotlib.font_manager.findfont("Space Mono", fallback_to_default=False))
    assert found.name.startswith("SpaceMono") or "Space Mono" in found.name
