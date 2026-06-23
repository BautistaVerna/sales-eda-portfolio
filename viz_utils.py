"""
viz_utils.py
Shared styling and helper functions for all project visualisations.
"""

from pathlib import Path
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


# ── Palette ────────────────────────────────────────────────────────────────────
PALETTE = {
    "primary":    "#2563EB",   # blue-600
    "secondary":  "#7C3AED",   # violet-600
    "accent":     "#059669",   # emerald-600
    "warning":    "#D97706",   # amber-600
    "danger":     "#DC2626",   # red-600
    "neutral":    "#6B7280",   # gray-500
    "light_bg":   "#F8FAFC",   # near-white background
    "grid":       "#E2E8F0",   # grid lines
}

# Sequential palette for heatmaps / choropleths (5 shades of primary blue)
BLUES = ["#DBEAFE", "#93C5FD", "#3B82F6", "#1D4ED8", "#1E3A8A"]

# Categorical palette (distinct colours for category charts)
CAT_PALETTE = [
    "#2563EB", "#7C3AED", "#059669", "#D97706", "#DC2626",
    "#0891B2", "#65A30D", "#9333EA", "#EA580C", "#0F766E",
]

FONT_FAMILY = "DejaVu Sans"   # ships with matplotlib, always available


def set_style() -> None:
    """
    Apply a consistent, minimal visual style to every subsequent plot.
    Call once at the top of a notebook (after imports).
    """
    mpl.rcParams.update({
        # Figure
        "figure.facecolor":     PALETTE["light_bg"],
        "figure.dpi":           120,
        "figure.titlesize":     16,
        "figure.titleweight":   "bold",

        # Axes
        "axes.facecolor":       PALETTE["light_bg"],
        "axes.edgecolor":       PALETTE["grid"],
        "axes.spines.top":      False,
        "axes.spines.right":    False,
        "axes.labelsize":       11,
        "axes.labelcolor":      "#1E293B",
        "axes.titlesize":       13,
        "axes.titleweight":     "bold",
        "axes.titlepad":        12,
        "axes.prop_cycle":      mpl.cycler(color=CAT_PALETTE),

        # Grid
        "axes.grid":            True,
        "grid.color":           PALETTE["grid"],
        "grid.linewidth":       0.7,
        "grid.linestyle":       "--",

        # Ticks
        "xtick.labelsize":      9,
        "ytick.labelsize":      9,
        "xtick.color":          "#475569",
        "ytick.color":          "#475569",

        # Legend
        "legend.frameon":       False,
        "legend.fontsize":      9,

        # Font
        "font.family":          FONT_FAMILY,

        # Lines
        "lines.linewidth":      2.0,
        "patch.linewidth":      0.5,
    })


def save_fig(fig: plt.Figure, filename: str, output_dir: str | Path = "outputs/figures") -> Path:
    """
    Save a matplotlib figure to outputs/figures/ at high resolution.

    Parameters
    ----------
    fig      : the Figure object to save
    filename : filename without extension (e.g. "01_sales_trend")
    output_dir : where to save; created if missing

    Returns
    -------
    Path to the saved file.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path = output_dir / f"{filename}.png"
    fig.savefig(out_path, dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    print(f"Saved → {out_path}")
    return out_path


def add_value_labels(
    ax: plt.Axes,
    fmt: str = "{:.1f}",
    padding: float = 3,
    fontsize: int = 8,
    color: str = "#1E293B",
    horizontal: bool = False,
) -> None:
    """
    Annotate each bar in a bar chart with its height value.

    Parameters
    ----------
    ax         : Axes with bar patches
    fmt        : format string, e.g. "{:,.0f}" for integers with thousands sep
    padding    : points between bar tip and label
    fontsize   : label font size
    color      : label color
    horizontal : set True for horizontal bar charts (barh)
    """
    for patch in ax.patches:
        if horizontal:
            value = patch.get_width()
            x = value + padding * 0.01 * (ax.get_xlim()[1] - ax.get_xlim()[0])
            y = patch.get_y() + patch.get_height() / 2
            ha, va = "left", "center"
        else:
            value = patch.get_height()
            x = patch.get_x() + patch.get_width() / 2
            y = value + padding
            ha, va = "center", "bottom"

        if value == 0:
            continue

        ax.annotate(
            fmt.format(value),
            xy=(x, y),
            ha=ha, va=va,
            fontsize=fontsize,
            color=color,
        )


def format_currency_axis(ax: plt.Axes, axis: str = "y") -> None:
    """Format an axis with R$ thousands abbreviation (Brazilian Real)."""
    def _fmt(x, _):
        if x >= 1_000_000:
            return f"R${x/1_000_000:.1f}M"
        if x >= 1_000:
            return f"R${x/1_000:.0f}K"
        return f"R${x:.0f}"

    target = ax.yaxis if axis == "y" else ax.xaxis
    target.set_major_formatter(mticker.FuncFormatter(_fmt))
