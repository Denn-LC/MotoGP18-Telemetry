import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Wedge, Rectangle
from matplotlib import patheffects as pe
from matplotlib.font_manager import FontProperties
from motogp_dashboard import config

def _get_font_props(size):
    # Accepts custom font, else uses default fallback
    if config.FONT_PATH and isinstance(config.FONT_PATH, str) and len(config.FONT_PATH.strip()) > 0:
        try:
            return FontProperties(fname = config.FONT_PATH, size = size, weight = config.FONT_WEIGHT)
        except Exception:
            pass
    return FontProperties(family = config.FONT_FALLBACK, size = size, weight = config.FONT_WEIGHT)

def stroke_effect():
    # Text stroke effect for better visibility
    rgba_black = (0.0, 0.0, 0.0, float(config.STROKE_ALPHA))
    return [pe.withStroke(linewidth = float(config.STROKE_W), foreground = rgba_black)]

def init_plot(x, y):
    # Basic figure and track underlay
    fig, ax = plt.subplots(figsize = config.TRACK_SIZE)
    fig.subplots_adjust(bottom = config.SUBPLOT_BOTTOM)

    # Track underlay line
    ax.plot(
        x, y,
        color = config.TRACK_COLOR,
        zorder = 0,
        linewidth = getattr(config, "TRACK_LINEWIDTH", 1.2),
        alpha = getattr(config, "TRACK_ALPHA", 0.25)
    )

    # Bike position marker
    dot, = ax.plot([], [], 'o', color = config.DOT_COLOR, markersize = 10, zorder = 2)

    # Clean canvas
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.tick_params(left = False, bottom = False, labelleft = False, labelbottom = False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.axis('equal'); ax.grid(False)
    ax.set_title("MotoGP18 Lap Simulation")

    return fig, ax, dot

def setup_underlay(df, x, y, use_underlay):
    if use_underlay and ('lapIndex' in df.columns):
        base_mask = (df['lapIndex'] == 1)
        if base_mask.any():
            x_base = x[base_mask]
            y_base = y[base_mask]
            fig, ax, dot = init_plot(x_base, y_base)
            for ln in list(ax.lines):
                if ln is not dot:
                    ln.set_linewidth(getattr(config, "TRACK_LINEWIDTH", 1.2))
                    ln.set_color(getattr(config, "TRACK_COLOR", (0.20, 0.20, 0.20)))
                    ln.set_alpha(getattr(config, "TRACK_ALPHA", 0.25))
            return fig, ax, dot


def build_hud(fig):

    hud_ax = fig.add_axes(config.HUD_BOX_POS)
    hud_ax.set_facecolor((1, 1, 1, 0))
    hud_ax.axis('off')

    # Lean arc area
    lean_ax = fig.add_axes([
        config.HUD_BOX_POS[0] + config.LEAN_AX_REL[0] * config.HUD_BOX_POS[2],
        config.HUD_BOX_POS[1] + config.LEAN_AX_REL[1] * config.HUD_BOX_POS[3],
        config.LEAN_AX_REL[2] * config.HUD_BOX_POS[2],
        config.LEAN_AX_REL[3] * config.HUD_BOX_POS[3]
    ])
    lean_ax.set_xlim(-1.0 - float(config.LEAN_X_PAD), 1.0 + float(config.LEAN_X_PAD))
    lean_ax.set_ylim(-0.2 - float(config.LEAN_Y_PAD), 1.2 + float(config.LEAN_Y_PAD))
    lean_ax.axis('off')

    R_arc    = float(config.LEAN_ARC_RADIUS)
    w_fill   = float(config.LEAN_FILL_WIDTH)
    edge_pad = float(config.LEAN_EDGE_PAD_DEG)

    # Grey outline arc
    arc_bg = Arc(
        (0, 0), width = 2 * R_arc, height = 2 * R_arc,
        theta1 = 0.0 + edge_pad, theta2 = 180.0 - edge_pad,
        linewidth = config.LEAN_ARC_LINEWIDTH,
        color = config.LEAN_RING_BG, zorder = 3
    )
    arc_bg.set_clip_on(False)
    lean_ax.add_patch(arc_bg)

    # Alignment for fill wedges
    R_fill = R_arc + w_fill / 2.0

    left_fill  = Wedge(center = (0, 0), r = R_fill,
                       theta1 = 90, theta2 = 90, width = w_fill,
                       facecolor = config.LEAN_FILL_COLOR, edgecolor = None, zorder = 2)
    right_fill = Wedge(center = (0, 0), r = R_fill,
                       theta1 = 90, theta2 = 90, width = w_fill,
                       facecolor = config.LEAN_FILL_COLOR, edgecolor = None, zorder = 2)
    left_fill.set_clip_on(False)
    right_fill.set_clip_on(False)
    lean_ax.add_patch(left_fill); lean_ax.add_patch(right_fill)

    # Lean ang readout 
    lean_text = lean_ax.text(
        0.0, 0.22, '',
        ha = 'center', va = 'center',
        fontproperties = _get_font_props(config.FONT_SIZE_LEAN),
        color = config.TEXT_COLOR, weight = config.FONT_WEIGHT, zorder = 4,
        path_effects = stroke_effect()
    )

    # Bars area
    bars_ax = fig.add_axes([
        config.HUD_BOX_POS[0] + config.BARS_AX_REL[0] * config.HUD_BOX_POS[2],
        config.HUD_BOX_POS[1] + config.BARS_AX_REL[1] * config.HUD_BOX_POS[3],
        config.BARS_AX_REL[2] * config.HUD_BOX_POS[2],
        config.BARS_AX_REL[3] * config.HUD_BOX_POS[3]
    ])
    bars_ax.set_xlim(0, 1); bars_ax.set_ylim(0, 1); bars_ax.axis('off')

    gap_frac  = 0.04
    half_frac = 0.5
    left_x0   = 0.0
    left_x1   = half_frac - gap_frac * 0.5
    right_x0  = half_frac + gap_frac * 0.5
    right_x1  = 1.0

    bar_h = 0.52
    bar_y = 0.5 - bar_h / 2

    # Grey outlines behind the bars
    bg_left  = Rectangle((left_x0,  bar_y),  left_x1 - left_x0,  bar_h, facecolor = (0.90, 0.90, 0.90), edgecolor = None, zorder = 0)
    bg_right = Rectangle((right_x0, bar_y),  right_x1 - right_x0, bar_h, facecolor = (0.90, 0.90, 0.90), edgecolor = None, zorder = 0)
    bars_ax.add_patch(bg_left); bars_ax.add_patch(bg_right)

    # Brake + Throttle bars
    brk_rect = Rectangle((left_x1,  bar_y), 0.0, bar_h, facecolor = config.BRAKE_COLOR,    edgecolor = None, zorder = 1)
    thr_rect = Rectangle((right_x0, bar_y), 0.0, bar_h, facecolor = config.THROTTLE_COLOR, edgecolor = None, zorder = 1)
    bars_ax.add_patch(brk_rect); bars_ax.add_patch(thr_rect)

    # Speed and gear
    speed_text = hud_ax.text(
        *config.SPEED_POS_REL, '', transform = hud_ax.transAxes,
        ha = 'center', va = 'center',
        fontproperties = _get_font_props(config.FONT_SIZE_SPEED),
        color = config.TEXT_COLOR, weight = config.FONT_WEIGHT,
        path_effects = stroke_effect()
    )
    gear_text  = hud_ax.text(
        *config.GEAR_POS_REL,  '', transform = hud_ax.transAxes,
        ha = 'center', va = 'center',
        fontproperties = _get_font_props(config.FONT_SIZE_GEAR),
        color = config.TEXT_COLOR, weight = config.FONT_WEIGHT,
        path_effects = stroke_effect()
    )

    # Meta labels: Lap (left), Time (right)
    lap_text = hud_ax.text(
        *config.LAP_POS_REL, '', transform = hud_ax.transAxes,
        ha = 'left', va = 'center',
        fontproperties = _get_font_props(config.FONT_SIZE_META),
        color = config.TEXT_COLOR, weight = config.FONT_WEIGHT,
        path_effects = stroke_effect()
    )
    laptime_text = hud_ax.text(
        *config.LAPTIME_POS_REL, '', transform = hud_ax.transAxes,
        ha = 'right', va = 'center',
        fontproperties = _get_font_props(config.FONT_SIZE_META),
        color = config.TEXT_COLOR, weight = config.FONT_WEIGHT,
        path_effects = stroke_effect()
    )

    bars_geo = {
        'left_edge'   : left_x1,
        'left_min'    : left_x0,
        'right_edge'  : right_x0,
        'right_max'   : right_x1,
        'bar_y'       : bar_y,
        'bar_h'       : bar_h,
        'edge_pad_deg': float(config.LEAN_EDGE_PAD_DEG)
    }

    return (
        left_fill, right_fill, lean_text,
        brk_rect, thr_rect, speed_text, gear_text,
        lap_text, laptime_text,
        bars_geo
    )

def hud(fig, ax):
    return build_hud(fig)
