import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Wedge, Rectangle, PathPatch
from matplotlib import patheffects as pe
from matplotlib.font_manager import FontProperties
from matplotlib.path import Path
from motogp_dashboard import config

def get_font(size):
    if config.FONT_PATH and isinstance(config.FONT_PATH, str) and len(config.FONT_PATH.strip()) > 0:
        try:
            return FontProperties(fname = config.FONT_PATH, size = size, weight = config.FONT_WEIGHT)
        except Exception:
            pass
    return FontProperties(family = config.FONT_FALLBACK, size = size, weight = config.FONT_WEIGHT)

def stroke_effect():
    rgba_black = (0.0, 0.0, 0.0, float(config.STROKE_ALPHA))
    return [pe.withStroke(linewidth = float(config.STROKE_W), foreground = rgba_black)]

def init_plot(x, y):
    fig, ax = plt.subplots(figsize = config.TRACK_SIZE)
    fig.subplots_adjust(bottom = config.SUBPLOT_BOTTOM)

    ax.plot(
        x, y,
        color = config.TRACK_COLOR,
        zorder = 0,
        linewidth = config.TRACK_LINEWIDTH,
        alpha = config.TRACK_ALPHA
    )

    dot, = ax.plot([], [], 'o', color = config.DOT_COLOR, markersize = 10, zorder = 2)

    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.tick_params(left = False, bottom = False, labelleft = False, labelbottom = False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.axis('equal'); ax.grid(False)
    ax.set_title("MotoGP18 Lap Simulation - Denn-LC")

    return fig, ax, dot

def setup_underlay(df, x, y, use_underlay):
    if not use_underlay:
        return None

    base_mask = (df['lapIndex'] == 1)
    x_base = x[base_mask]
    y_base = y[base_mask]

    fig, ax, dot = init_plot(x_base, y_base)

    for ln in list(ax.lines):
        if ln is not dot:
            ln.set_linewidth(config.TRACK_LINEWIDTH)
            ln.set_color(config.TRACK_COLOR)
            ln.set_alpha(config.TRACK_ALPHA)

    return fig, ax, dot

# Simple rounded HUD background
def hud_shape(width = 1.0, height = 1.0, r_frac = 0.08):
    w = float(width); h = float(height)
    r = float(r_frac) * min(w, h)
    r = max(0.0, min(r, 0.5 * min(w, h)))
    if r == 0.0:
        verts = [(0,0),(w,0),(w,h),(0,h),(0,0)]
        codes = [Path.MOVETO,Path.LINETO,Path.LINETO,Path.LINETO,Path.CLOSEPOLY]
        return Path(verts, codes)

    k = config.BEZIER_KAPPA
    cx = r * k; cy = r * k

    x0, y0 = 0.0, 0.0
    x1, y1 = w,   h

    verts = [
        (x0 + r, y0),                       # M
        (x1 - r, y0),                       # L
        (x1 - r + cx, y0), (x1, y0 + r - cy), (x1, y0 + r),          # C br
        (x1, y1 - r),                       # L
        (x1, y1 - r + cy), (x1 - r + cx, y1), (x1 - r, y1),          # C tr
        (x0 + r, y1),                       # L
        (x0 + r - cx, y1), (x0, y1 - r + cy), (x0, y1 - r),          # C tl
        (x0, y0 + r),                       # L
        (x0, y0 + r - cy), (x0 + r - cx, y0), (x0 + r, y0),          # C bl
        (x0 + r, y0)                        # Z
    ]
    codes = [
        Path.MOVETO,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.CLOSEPOLY
    ]
    return Path(verts, codes)

def hud_background(fig):
    if not getattr(config, "HUD_BG", True):
        return

    # Start from the main HUD box and a little
    x, y, w, h = config.HUD_BOX_POS
    inset_x = float(config.HUD_BG_INSET_X) * w
    inset_y = float(config.HUD_BG_INSET_Y) * h
    x0 = x + inset_x
    y0 = y + inset_y
    w0 = max(0.0, w - 2 * inset_x)
    h0 = max(0.0, h - 2 * inset_y)

    bg_ax = fig.add_axes([x0, y0, w0, h0], zorder = 0.05)
    bg_ax.set_axis_off()

    r_frac = float(getattr(config, "HUD_BG_ROUND_FRAC", 0.08))
    r_frac = max(0.0, min(0.5, r_frac))

    path = hud_shape(1.0, 1.0, r_frac = r_frac)
    r, g, b = config.HUD_BG_COLOR
    face_rgba = (r, g, b, float(config.HUD_BG_ALPHA))

    panel = PathPatch(
        path,
        facecolor = face_rgba,
        edgecolor = None,
        transform = bg_ax.transAxes,
        zorder = 0.06,
        clip_on = False
    )
    bg_ax.add_patch(panel)

def build_hud(fig):

    hud_background(fig)

    hud_ax = fig.add_axes(config.HUD_BOX_POS, zorder = 0.30)
    hud_ax.set_facecolor((1, 1, 1, 0))
    hud_ax.axis('off')

    # Lean arc area
    lean_ax = fig.add_axes([
        config.HUD_BOX_POS[0] + config.LEAN_AX_REL[0] * config.HUD_BOX_POS[2],
        config.HUD_BOX_POS[1] + config.LEAN_AX_REL[1] * config.HUD_BOX_POS[3],
        config.LEAN_AX_REL[2] * config.HUD_BOX_POS[2],
        config.LEAN_AX_REL[3] * config.HUD_BOX_POS[3]
    ], zorder = 0.35)
    lean_ax.set_xlim(-1.0 - float(config.LEAN_X_PAD), 1.0 + float(config.LEAN_X_PAD))
    lean_ax.set_ylim(-0.2 - float(config.LEAN_Y_PAD), 1.2 + float(config.LEAN_Y_PAD))
    lean_ax.axis('off')

    R_arc = float(config.LEAN_ARC_RADIUS)
    w_fill = float(config.LEAN_FILL_WIDTH)
    edge_pad = float(config.LEAN_EDGE_PAD_DEG)

    arc_bg = Arc(
        (0, 0), width = 2 * R_arc, height = 2 * R_arc,
        theta1 = 0.0 + edge_pad, theta2 = 180.0 - edge_pad,
        linewidth = config.LEAN_ARC_LINEWIDTH,
        color = config.LEAN_RING_BG, zorder = 3
    )
    arc_bg.set_clip_on(False)
    lean_ax.add_patch(arc_bg)

    R_fill = R_arc + w_fill / 2.0

    left_fill = Wedge(center = (0, 0), r = R_fill,
                       theta1 = 90, theta2 = 90, width = w_fill,
                       facecolor = config.LEAN_FILL_COLOR, edgecolor = None, zorder = 2)
    right_fill = Wedge(center = (0, 0), r = R_fill,
                       theta1 = 90, theta2 = 90, width = w_fill,
                       facecolor = config.LEAN_FILL_COLOR, edgecolor = None, zorder = 2)
    left_fill.set_clip_on(False)
    right_fill.set_clip_on(False)
    lean_ax.add_patch(left_fill); lean_ax.add_patch(right_fill)

    lean_text = lean_ax.text(
        0.0, 0.22, '',
        ha = 'center', va = 'center',
        fontproperties = get_font(config.FONT_SIZE_LEAN),
        color = config.TEXT_COLOR, weight = config.FONT_WEIGHT, zorder = 4,
        path_effects = stroke_effect()
    )

    # Bars area
    bars_ax = fig.add_axes([
        config.HUD_BOX_POS[0] + config.BARS_AX_REL[0] * config.HUD_BOX_POS[2],
        config.HUD_BOX_POS[1] + config.BARS_AX_REL[1] * config.HUD_BOX_POS[3],
        config.BARS_AX_REL[2] * config.HUD_BOX_POS[2],
        config.BARS_AX_REL[3] * config.HUD_BOX_POS[3]
    ], zorder = 0.35)
    bars_ax.set_xlim(0, 1); bars_ax.set_ylim(0, 1); bars_ax.axis('off')

    # Grey outlines
    bg_left = Rectangle((config.LEFT_X0,  config.BAR_Y),  config.LEFT_DIFF,  config.BAR_H, facecolor = (0.90, 0.90, 0.90), edgecolor = None, zorder = 0)
    bg_right = Rectangle((config.RIGHT_X0, config.BAR_Y),  config.RIGHT_DIFF, config.BAR_H, facecolor = (0.90, 0.90, 0.90), edgecolor = None, zorder = 0)
    bars_ax.add_patch(bg_left); bars_ax.add_patch(bg_right)

    # Bars
    brk_rect = Rectangle((config.LEFT_X0,  config.BAR_Y), 0.0, config.BAR_H, facecolor = config.BRAKE_COLOR,    edgecolor = None, zorder = 1)
    thr_rect = Rectangle((config.RIGHT_X0, config.BAR_Y), 0.0, config.BAR_H, facecolor = config.THROTTLE_COLOR, edgecolor = None, zorder = 1)
    bars_ax.add_patch(brk_rect); bars_ax.add_patch(thr_rect)

    # Text overlays
    speed_text = hud_ax.text(
        *config.SPEED_POS_REL, '', transform = hud_ax.transAxes,
        ha = 'center', va = 'center',
        fontproperties = get_font(config.FONT_SIZE_SPEED),
        color = config.TEXT_COLOR, weight = config.FONT_WEIGHT,
        path_effects = stroke_effect()
    )
    gear_text = hud_ax.text(
        *config.GEAR_POS_REL,  '', transform = hud_ax.transAxes,
        ha = 'center', va = 'center',
        fontproperties = get_font(config.FONT_SIZE_GEAR),
        color = config.TEXT_COLOR, weight = config.FONT_WEIGHT,
        path_effects = stroke_effect()
    )

    lap_text = hud_ax.text(
        *config.LAP_POS_REL, '', transform = hud_ax.transAxes,
        ha = 'left', va = 'center',
        fontproperties = get_font(config.FONT_SIZE_META),
        color = config.TEXT_COLOR, weight = config.FONT_WEIGHT,
        path_effects = stroke_effect()
    )
    laptime_text = hud_ax.text(
        *config.LAPTIME_POS_REL, '', transform = hud_ax.transAxes,
        ha = 'right', va = 'center',
        fontproperties = get_font(config.FONT_SIZE_META),
        color = config.TEXT_COLOR, weight = config.FONT_WEIGHT,
        path_effects = stroke_effect()
    )

    bars_geo = {
        'left_edge' : config.LEFT_X1,
        'left_min' : config.LEFT_X0,
        'right_edge' : config.RIGHT_X0,
        'right_max' : config.RIGHT_X1,
        'bar_y' : config.BAR_Y,
        'bar_h' : config.BAR_H,
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
