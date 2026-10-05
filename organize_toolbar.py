# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""Organize & Styles Toolbar plugin for IngeTrazo.

Self-contained plugin providing dedicated toolbars and Extensions submenu for:
- Organize toolbar:
  - Hide selection (Ctrl+H)
  - Unhide Last
  - Unhide All
  - Reverse Faces
  - Make Group (Ctrl+G)
  - Explode Group (Ctrl+Shift+G)
- Styles toolbar:
  - Default (Shaded with Textures)
  - Architectural (Clean white presentation)
  - Shaded (Face colors without textures)
  - Hidden line (Opaque white faces)
  - Monochrome (Two-tone front/back)
  - Wireframe (Edges only)
  - X-ray (Translucent see-through)
"""
from __future__ import annotations

import logging
from PySide6.QtCore import QPointF, QRectF, QSize, Qt
from PySide6.QtGui import (
    QAction,
    QColor,
    QGuiApplication,
    QIcon,
    QPainter,
    QPainterPath,
    QPen,
    QPixmap,
    QPolygonF,
)

log = logging.getLogger("ingetrazo.plugins")


def _tr(text: str) -> str:
    try:
        from core.i18n import tr
        return tr(text)
    except Exception:
        return text


# ---- Vector Icon Generator (Self-Contained) --------------------------------

def _accent() -> QColor:
    try:
        from views.icons import _ACCENT
        return QColor(_ACCENT)
    except Exception:
        return QColor(243, 115, 41)  # IngeTrazo vibrant orange


def _ink() -> QColor:
    try:
        from views.icons import _ink as vi_ink
        return vi_ink()
    except Exception:
        pass
    try:
        app = QGuiApplication.instance()
        if app is not None:
            c = app.palette().windowText().color()
            return QColor(c.red(), c.green(), c.blue())
    except Exception:
        pass
    return QColor(236, 239, 241)


def _rpen(color: QColor, width: float, style: Qt.PenStyle = Qt.SolidLine) -> QPen:
    pen = QPen(color, width, style)
    pen.setCapStyle(Qt.RoundCap)
    pen.setJoinStyle(Qt.RoundJoin)
    return pen


def _dot(p: QPainter, x: float, y: float, r: float, color: QColor) -> None:
    p.setPen(Qt.NoPen)
    p.setBrush(color)
    p.drawEllipse(QPointF(x, y), r, r)


def _draw_hide(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setPen(_rpen(ink, 2.8))
    p.setBrush(Qt.NoBrush)
    eye = QPainterPath()
    eye.moveTo(8, 24)
    eye.quadTo(24, 11, 40, 24)
    eye.quadTo(24, 37, 8, 24)
    p.drawPath(eye)
    _dot(p, 24, 24, 4.5, ink)
    p.setPen(_rpen(acc, 3.4))
    p.drawLine(QPointF(11, 37), QPointF(37, 11))
    p.restore()


def _draw_unhide_last(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setPen(_rpen(ink, 2.8))
    p.setBrush(Qt.NoBrush)
    eye = QPainterPath()
    eye.moveTo(7, 27)
    eye.quadTo(24, 16, 41, 27)
    eye.quadTo(24, 38, 7, 27)
    p.drawPath(eye)
    _dot(p, 24, 27, 4.0, ink)
    p.setPen(_rpen(acc, 2.6))
    p.drawArc(QRectF(22, 5, 18, 14), 10 * 16, 190 * 16)
    p.setPen(Qt.NoPen)
    p.setBrush(acc)
    p.drawPolygon(QPolygonF([
        QPointF(22, 12),
        QPointF(28, 9),
        QPointF(26, 15)
    ]))
    p.restore()


def _draw_unhide_all(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setPen(_rpen(ink, 2.8))
    p.setBrush(Qt.NoBrush)
    eye = QPainterPath()
    eye.moveTo(8, 24)
    eye.quadTo(24, 11, 40, 24)
    eye.quadTo(24, 37, 8, 24)
    p.drawPath(eye)
    p.drawEllipse(QPointF(24, 24), 6.5, 6.5)
    _dot(p, 24, 24, 3.8, acc)
    p.setPen(_rpen(acc, 2.4))
    p.drawLine(QPointF(24, 4), QPointF(24, 8))
    p.drawLine(QPointF(14, 7), QPointF(17, 10))
    p.drawLine(QPointF(34, 7), QPointF(31, 10))
    p.restore()


def _draw_reverse_face(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    quad = QPolygonF([QPointF(10, 24), QPointF(24, 32), QPointF(38, 24), QPointF(24, 16)])
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(acc.red(), acc.green(), acc.blue(), 70))
    p.drawPolygon(quad)
    p.setPen(_rpen(ink, 2.4))
    p.setBrush(Qt.NoBrush)
    p.drawPolygon(quad)
    p.setPen(_rpen(acc, 2.6))
    p.drawArc(QRectF(13, 7, 22, 18), 30 * 16, 140 * 16)
    p.setPen(Qt.NoPen)
    p.setBrush(acc)
    p.drawPolygon(QPolygonF([QPointF(14, 14), QPointF(19, 10), QPointF(18, 17)]))
    p.setPen(_rpen(ink, 2.6))
    p.setBrush(Qt.NoBrush)
    p.drawArc(QRectF(13, 23, 22, 18), 210 * 16, 140 * 16)
    p.setPen(Qt.NoPen)
    p.setBrush(ink)
    p.drawPolygon(QPolygonF([QPointF(34, 34), QPointF(29, 38), QPointF(30, 31)]))
    p.restore()


def _draw_group(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setPen(_rpen(ink, 2.0))
    p.setBrush(QColor(ink.red(), ink.green(), ink.blue(), 40))
    p.drawRoundedRect(QRectF(12, 15, 11, 11), 1.5, 1.5)
    p.drawRoundedRect(QRectF(25, 23, 11, 11), 1.5, 1.5)
    dash = QPen(acc, 2.4, Qt.DashLine)
    dash.setCapStyle(Qt.RoundCap)
    p.setPen(dash)
    p.setBrush(Qt.NoBrush)
    p.drawRect(QRectF(7, 10, 34, 28))
    for cx, cy in ((7, 10), (41, 10), (7, 38), (41, 38)):
        _dot(p, cx, cy, 2.0, acc)
    p.restore()


def _draw_ungroup(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setPen(_rpen(ink, 2.0))
    p.setBrush(QColor(ink.red(), ink.green(), ink.blue(), 40))
    p.drawRoundedRect(QRectF(12, 15, 11, 11), 1.5, 1.5)
    p.drawRoundedRect(QRectF(25, 23, 11, 11), 1.5, 1.5)
    p.setPen(_rpen(acc, 2.4))
    p.setBrush(Qt.NoBrush)
    p.drawLine(QPointF(6, 16), QPointF(6, 9))
    p.drawLine(QPointF(6, 9), QPointF(13, 9))
    p.drawLine(QPointF(35, 9), QPointF(42, 9))
    p.drawLine(QPointF(42, 9), QPointF(42, 16))
    p.drawLine(QPointF(6, 32), QPointF(6, 39))
    p.drawLine(QPointF(6, 39), QPointF(13, 39))
    p.drawLine(QPointF(35, 39), QPointF(42, 39))
    p.drawLine(QPointF(42, 39), QPointF(42, 32))
    p.restore()


# ---- Isometric Style Cube Geometry -------------------------------------------
_CUBE_TOP = QPolygonF([QPointF(24, 7), QPointF(39, 15), QPointF(24, 23), QPointF(9, 15)])
_CUBE_LEFT = QPolygonF([QPointF(9, 15), QPointF(24, 23), QPointF(24, 39), QPointF(9, 31)])
_CUBE_RIGHT = QPolygonF([QPointF(24, 23), QPointF(39, 15), QPointF(39, 31), QPointF(24, 39)])


def _draw_style_default(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(225, 230, 235))
    p.drawPolygon(_CUBE_TOP)
    p.setBrush(QColor(170, 185, 200))
    p.drawPolygon(_CUBE_LEFT)
    p.setBrush(QColor(120, 140, 160))
    p.drawPolygon(_CUBE_RIGHT)
    p.setPen(_rpen(QColor(50, 65, 80, 180), 1.3))
    p.drawLine(QPointF(9, 20), QPointF(24, 28))
    p.drawLine(QPointF(9, 25.5), QPointF(24, 33.5))
    p.drawLine(QPointF(14, 17.8), QPointF(14, 22.8))
    p.drawLine(QPointF(19, 25.5), QPointF(19, 30.8))
    p.drawLine(QPointF(14, 28.2), QPointF(14, 33.5))
    p.setPen(_rpen(QColor(130, 140, 150, 150), 1.2))
    p.drawLine(QPointF(14, 12.3), QPointF(29, 20.3))
    p.drawLine(QPointF(19, 9.7), QPointF(34, 17.7))
    p.setPen(Qt.NoPen)
    p.setBrush(acc)
    p.drawRoundedRect(QRectF(30, 24, 6, 6), 1.5, 1.5)
    p.setPen(_rpen(ink, 2.2))
    p.setBrush(Qt.NoBrush)
    p.drawPolygon(_CUBE_TOP)
    p.drawPolygon(_CUBE_LEFT)
    p.drawPolygon(_CUBE_RIGHT)
    p.restore()


def _draw_style_architectural(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(252, 252, 254))
    p.drawPolygon(_CUBE_TOP)
    p.setBrush(QColor(235, 238, 242))
    p.drawPolygon(_CUBE_LEFT)
    p.setBrush(QColor(210, 218, 226))
    p.drawPolygon(_CUBE_RIGHT)
    p.setPen(_rpen(ink, 2.2))
    p.setBrush(Qt.NoBrush)
    p.drawPolygon(_CUBE_TOP)
    p.drawPolygon(_CUBE_LEFT)
    p.drawPolygon(_CUBE_RIGHT)
    p.setPen(_rpen(acc, 2.2))
    p.drawLine(QPointF(5, 43), QPointF(43, 43))
    p.drawLine(QPointF(7, 40), QPointF(10, 46))
    p.drawLine(QPointF(38, 40), QPointF(41, 46))
    p.restore()


def _draw_style_shaded(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(215, 230, 250))
    p.drawPolygon(_CUBE_TOP)
    p.setBrush(QColor(140, 175, 220))
    p.drawPolygon(_CUBE_LEFT)
    p.setBrush(QColor(80, 115, 165))
    p.drawPolygon(_CUBE_RIGHT)
    p.setPen(_rpen(ink, 2.2))
    p.setBrush(Qt.NoBrush)
    p.drawPolygon(_CUBE_TOP)
    p.drawPolygon(_CUBE_LEFT)
    p.drawPolygon(_CUBE_RIGHT)
    p.restore()


def _draw_style_hidden_line(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(255, 255, 255))
    p.drawPolygon(_CUBE_TOP)
    p.drawPolygon(_CUBE_LEFT)
    p.drawPolygon(_CUBE_RIGHT)
    p.setPen(_rpen(ink, 2.4))
    p.setBrush(Qt.NoBrush)
    p.drawPolygon(_CUBE_TOP)
    p.drawPolygon(_CUBE_LEFT)
    p.drawPolygon(_CUBE_RIGHT)
    p.restore()


def _draw_style_monochrome(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(240, 240, 245))
    p.drawPolygon(_CUBE_TOP)
    p.drawPolygon(_CUBE_LEFT)
    p.setBrush(QColor(155, 175, 195))
    p.drawPolygon(_CUBE_RIGHT)
    p.setPen(_rpen(acc, 2.0))
    p.drawLine(QPointF(28, 30), QPointF(35, 25))
    p.drawLine(QPointF(35, 25), QPointF(31, 24))
    p.setPen(_rpen(ink, 2.2))
    p.setBrush(Qt.NoBrush)
    p.drawPolygon(_CUBE_TOP)
    p.drawPolygon(_CUBE_LEFT)
    p.drawPolygon(_CUBE_RIGHT)
    p.restore()


def _draw_style_wireframe(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setBrush(Qt.NoBrush)
    p.setPen(_rpen(QColor(ink.red(), ink.green(), ink.blue(), 120), 1.8, Qt.DashLine))
    p.drawLine(QPointF(9, 31), QPointF(24, 23))
    p.drawLine(QPointF(39, 31), QPointF(24, 23))
    p.drawLine(QPointF(24, 7), QPointF(24, 23))
    p.setPen(_rpen(ink, 2.4))
    hex_pts = QPolygonF([
        QPointF(24, 7), QPointF(39, 15), QPointF(39, 31),
        QPointF(24, 39), QPointF(9, 31), QPointF(9, 15)
    ])
    p.drawPolygon(hex_pts)
    p.drawLine(QPointF(24, 23), QPointF(24, 39))
    p.drawLine(QPointF(24, 23), QPointF(9, 15))
    p.drawLine(QPointF(24, 23), QPointF(39, 15))
    p.setPen(Qt.NoPen)
    p.setBrush(acc)
    for pt in (QPointF(24, 7), QPointF(39, 15), QPointF(39, 31), QPointF(24, 39), QPointF(9, 31), QPointF(9, 15)):
        p.drawEllipse(pt, 2.2, 2.2)
    p.restore()


def _draw_style_xray(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    p.setPen(Qt.NoPen)
    p.setBrush(QColor(90, 170, 245, 75))
    p.drawPolygon(_CUBE_TOP)
    p.drawPolygon(_CUBE_LEFT)
    p.drawPolygon(_CUBE_RIGHT)
    p.setPen(_rpen(acc, 2.2, Qt.DashLine))
    p.drawLine(QPointF(9, 31), QPointF(24, 23))
    p.drawLine(QPointF(39, 31), QPointF(24, 23))
    p.drawLine(QPointF(24, 7), QPointF(24, 23))
    p.setPen(_rpen(ink, 2.2))
    p.setBrush(Qt.NoBrush)
    p.drawPolygon(_CUBE_TOP)
    p.drawPolygon(_CUBE_LEFT)
    p.drawPolygon(_CUBE_RIGHT)
    p.restore()


def _draw_axes(p: QPainter, ink: QColor, acc: QColor) -> None:
    p.save()
    o = QPointF(19, 28)
    # Negative dotted axes
    p.setPen(_rpen(QColor(120, 130, 145, 140), 1.6, Qt.DotLine))
    p.drawLine(o, QPointF(19, 42))   # -Z
    p.drawLine(o, QPointF(7, 21))    # -X
    p.drawLine(o, QPointF(7, 35))    # -Y

    # Z Axis (Blue / Cyan) - Vertical
    c_z = QColor(60, 145, 255)
    p.setPen(_rpen(c_z, 2.8))
    p.drawLine(o, QPointF(19, 8))
    p.setPen(Qt.NoPen)
    p.setBrush(c_z)
    p.drawPolygon(QPolygonF([QPointF(19, 5), QPointF(16, 11), QPointF(22, 11)]))

    # X Axis (Red / Coral) - Front-Left
    c_x = QColor(245, 65, 75)
    p.setPen(_rpen(c_x, 2.8))
    p.drawLine(o, QPointF(35, 38))
    p.setBrush(c_x)
    p.drawPolygon(QPolygonF([QPointF(38, 40), QPointF(32, 36), QPointF(35, 32)]))

    # Y Axis (Green / Lime) - Front-Right
    c_y = QColor(45, 200, 105)
    p.setPen(_rpen(c_y, 2.8))
    p.drawLine(o, QPointF(40, 20))
    p.setBrush(c_y)
    p.drawPolygon(QPolygonF([QPointF(43, 18), QPointF(36, 18), QPointF(38, 24)]))

    # Origin sphere
    p.setPen(Qt.NoPen)
    p.setBrush(acc)
    p.drawEllipse(o, 3.2, 3.2)
    p.setBrush(ink)
    p.drawEllipse(o, 1.6, 1.6)
    p.restore()


_ICON_DISPATCH = {
    "hide": _draw_hide,
    "unhide_last": _draw_unhide_last,
    "unhide_all": _draw_unhide_all,
    "reverse_face": _draw_reverse_face,
    "group": _draw_group,
    "ungroup": _draw_ungroup,
    "axes": _draw_axes,
    "style_default": _draw_style_default,
    "style_architectural": _draw_style_architectural,
    "style_shaded": _draw_style_shaded,
    "style_hidden_line": _draw_style_hidden_line,
    "style_monochrome": _draw_style_monochrome,
    "style_wireframe": _draw_style_wireframe,
    "style_xray": _draw_style_xray,
}


def _make_icon(key: str) -> QIcon:
    """Generate high-DPI crisp vector icon (loads disk asset if available)."""
    try:
        import os
        base_dir = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(base_dir, "assets", f"icon_{key}.png")
        if os.path.exists(path):
            return QIcon(path)
    except Exception:
        pass

    fn = _ICON_DISPATCH.get(key)
    if fn is None:
        try:
            from views.icons import tool_icon
            return tool_icon(key)
        except Exception:
            return QIcon()
    
    pm = QPixmap(48, 48)
    pm.fill(Qt.transparent)
    p = QPainter(pm)
    p.setRenderHint(QPainter.Antialiasing, True)
    fn(p, _ink(), _accent())
    p.end()
    return QIcon(pm)


# ---- Action Handlers (Defensive) -------------------------------------------

_SESSION_HIDDEN_HISTORY: list[list] = []


def _is_entity_hidden(e) -> bool:
    try:
        from core.history import _is_hidden
        return _is_hidden(e)
    except Exception:
        pass
    if getattr(e, "hidden", False):
        return True
    attrs = getattr(e, "attrs", None)
    if isinstance(attrs, dict) and attrs.get("hidden"):
        return True
    return False


def _iter_hide_commands(cmd):
    # Support CompoundCommand (e.g. from Eraser tool or batch operations)
    sub_cmds = getattr(cmd, "commands", None)
    if sub_cmds and isinstance(sub_cmds, (list, tuple)):
        for sc in sub_cmds:
            yield from _iter_hide_commands(sc)
    else:
        name = cmd.__class__.__name__
        if name in ("HideCommand", "HideEdgesCommand") or hasattr(cmd, "_entities"):
            hides = getattr(cmd, "hides", None)
            if hides is None:
                hides = getattr(cmd, "_hidden", False)
            if hides:
                yield cmd


def _on_hide_impl(win) -> None:
    vp = getattr(win, "viewport", None)
    sel = list(vp.scene.selection) if (vp and getattr(vp, "scene", None)) else []
    fn = getattr(win, "_on_hide", None)
    if callable(fn):
        fn()
    hidden_now = [e for e in sel if _is_entity_hidden(e)]
    if hidden_now:
        _SESSION_HIDDEN_HISTORY.append(hidden_now)


def _on_unhide_last_impl(win) -> None:
    """Robust Unhide Last that restores faces, edges, groups, and compound commands."""
    vp = getattr(win, "viewport", None)
    if vp is None:
        return
    history = getattr(vp, "history", None)
    if history is None:
        return

    from core.history import HideCommand

    # 1. Inspect undo_stack backwards
    undo_stack = getattr(history, "undo_stack", [])
    for cmd in reversed(undo_stack):
        for h_cmd in _iter_hide_commands(cmd):
            entities = getattr(h_cmd, "entities", None)
            if entities is None:
                entities = getattr(h_cmd, "_entities", [])
            still = [e for e in entities if _is_entity_hidden(e)]
            if still:
                history.execute(HideCommand(still, hidden=False))
                vp.update()
                sb = win.statusBar() if hasattr(win, "statusBar") else None
                if sb:
                    sb.showMessage(_tr(f"Unhid {len(still)} entities."), 3000)
                return

    # 2. Check session fallback
    while _SESSION_HIDDEN_HISTORY:
        last_batch = _SESSION_HIDDEN_HISTORY.pop()
        still = [e for e in last_batch if _is_entity_hidden(e)]
        if still:
            history.execute(HideCommand(still, hidden=False))
            vp.update()
            sb = win.statusBar() if hasattr(win, "statusBar") else None
            if sb:
                sb.showMessage(_tr(f"Unhid {len(still)} entities."), 3000)
            return

    sb = win.statusBar() if hasattr(win, "statusBar") else None
    if sb:
        sb.showMessage(_tr("Nothing to unhide."), 3000)


def _safe_call(win, attr_name: str) -> None:
    fn = getattr(win, attr_name, None)
    if callable(fn):
        fn()


def _toggle_axes(win, visible: bool) -> None:
    """Toggle XYZ drawing axes visibility in the 3D viewport."""
    try:
        import views.viewport as vv
        vv._SHOW_AXES = bool(visible)
        vp = getattr(win, "viewport", None)
        if vp is not None:
            vp.update()
        sb = win.statusBar() if hasattr(win, "statusBar") else None
        if sb:
            msg = _tr("Axes visible.") if visible else _tr("Axes hidden.")
            sb.showMessage(msg, 2000)
    except Exception as e:
        log.warning("Could not toggle axes: %s", e)


def _apply_style_by_name(win, name: str) -> None:
    """Activate a display style preset by name, updating viewport and menus."""
    try:
        from core.style import style_by_name
        preset = style_by_name(name)
        if preset is None:
            return
        if hasattr(win, "_apply_display_style") and callable(win._apply_display_style):
            win._apply_display_style(preset)
        else:
            scene = getattr(win, "scene", None) or getattr(getattr(win, "viewport", None), "scene", None)
            if scene is not None:
                scene.display_style = preset.copy()
            if hasattr(win, "viewport"):
                win.viewport.update()
    except Exception as e:
        log.warning("Could not apply style %s: %s", name, e)


# ---- Plugin Setup -----------------------------------------------------------

def setup(app) -> None:
    """Entry point called by IngeTrazo when loading extensions."""
    win = app.window

    # Intercept viewport axes rendering so Axes button can toggle them live
    try:
        import views.viewport as vv
        if not hasattr(vv, "_ORIG_AXES_VERTICES"):
            vv._ORIG_AXES_VERTICES = vv._axes_vertices
            vv._SHOW_AXES = True

            def _patched_axes_vertices(spacing: float, pos_len: float = 1.0e5):
                if not getattr(vv, "_SHOW_AXES", True):
                    from array import array
                    return array("f"), {"x": (0, 0), "y": (0, 0), "z": (0, 0)}
                return vv._ORIG_AXES_VERTICES(spacing, pos_len)

            vv._axes_vertices = _patched_axes_vertices
    except Exception as e:
        log.warning("Could not patch axes vertices: %s", e)

    # Also register our icon renderers with views.icons._DRAW if present
    try:
        import views.icons as vi
        if hasattr(vi, "_DRAW"):
            for k, fn in _ICON_DISPATCH.items():
                if k not in vi._DRAW:
                    vi._DRAW[k] = lambda p, ink, _f=fn: _f(p, ink, _accent())
    except Exception:
        pass

    # Patch win._on_unhide_last so Edit menu and shortcuts also benefit
    try:
        win._on_unhide_last = lambda: _on_unhide_last_impl(win)
    except Exception:
        pass

    # 1. Create or retrieve the Organize toolbar
    from PySide6.QtWidgets import QToolBar
    if hasattr(win, "_new_toolbar") and callable(win._new_toolbar):
        tb = win._new_toolbar(_tr("Organize"), "organize")
    else:
        tb = QToolBar(_tr("Organize"), win)
        tb.setObjectName("organize")
        tb.setMovable(True)
        tb.setFloatable(True)
        try:
            from views.icons import toolbar_icon_px
            px = toolbar_icon_px()
        except Exception:
            px = 24
        tb.setIconSize(QSize(px, px))
        tb.setToolButtonStyle(Qt.ToolButtonIconOnly)
        win.addToolBar(Qt.TopToolBarArea, tb)

    if hasattr(win, "toolbars") and isinstance(win.toolbars, dict):
        win.toolbars["organize"] = tb

    actions = []

    # Hide
    act_hide = QAction(_make_icon("hide"), _tr("Hide"), win)
    act_hide.setToolTip(f"{_tr('Hide')}  (Ctrl+H)")
    act_hide.setStatusTip(_tr("Stop showing the selected objects, faces and edges; they stay in the document until unhidden."))
    act_hide.triggered.connect(lambda: _on_hide_impl(win))
    tb.addAction(act_hide)
    actions.append((act_hide, "hide"))

    # Unhide Last
    act_unhide_last = QAction(_make_icon("unhide_last"), _tr("Unhide Last"), win)
    act_unhide_last.setToolTip(_tr("Unhide Last"))
    act_unhide_last.setStatusTip(_tr("Show again what the last hiding put away."))
    act_unhide_last.triggered.connect(lambda: _on_unhide_last_impl(win))
    tb.addAction(act_unhide_last)
    actions.append((act_unhide_last, "unhide_last"))

    # Unhide All
    act_unhide_all = QAction(_make_icon("unhide_all"), _tr("Unhide All"), win)
    act_unhide_all.setToolTip(_tr("Unhide All"))
    act_unhide_all.setStatusTip(_tr("Show again everything that is hidden."))
    act_unhide_all.triggered.connect(lambda: _safe_call(win, "_on_unhide_all"))
    tb.addAction(act_unhide_all)
    actions.append((act_unhide_all, "unhide_all"))

    tb.addSeparator()

    # Reverse Faces
    act_rev = QAction(_make_icon("reverse_face"), _tr("Reverse Faces"), win)
    act_rev.setToolTip(_tr("Reverse Faces"))
    act_rev.setStatusTip(_tr("Swap the front and back sides of the selected faces."))
    act_rev.triggered.connect(lambda: _safe_call(win, "_on_reverse_faces"))
    tb.addAction(act_rev)
    actions.append((act_rev, "reverse_face"))

    tb.addSeparator()

    # Make Group
    act_grp = QAction(_make_icon("group"), _tr("Make Group"), win)
    act_grp.setToolTip(f"{_tr('Make Group')}  (Ctrl+G)")
    act_grp.setStatusTip(_tr("Wrap the selection in a group that moves as one and keeps apart from the geometry around it."))
    act_grp.triggered.connect(lambda: _safe_call(win, "_on_make_group"))
    tb.addAction(act_grp)
    actions.append((act_grp, "group"))

    # Explode Group
    act_ungrp = QAction(_make_icon("ungroup"), _tr("Explode Group"), win)
    act_ungrp.setToolTip(f"{_tr('Explode Group')}  (Ctrl+Shift+G)")
    act_ungrp.setStatusTip(_tr("Break the selected groups apart, back into the geometry around them."))
    act_ungrp.triggered.connect(lambda: _safe_call(win, "_on_explode_group"))
    tb.addAction(act_ungrp)
    actions.append((act_ungrp, "ungroup"))

    tb.addSeparator()

    # Toggle Axes
    act_axes = QAction(_make_icon("axes"), _tr("Axes"), win)
    act_axes.setToolTip(f"{_tr('Axes')}  ({_tr('Show / Hide Axes')})")
    act_axes.setStatusTip(_tr("Show or hide the red, green and blue coordinate axes in the viewport."))
    act_axes.setCheckable(True)
    act_axes.setChecked(True)
    act_axes.toggled.connect(lambda on: _toggle_axes(win, on))
    tb.addAction(act_axes)
    actions.append((act_axes, "axes"))

    tb.show()

    # 2. Create or retrieve the Styles toolbar
    if hasattr(win, "_new_toolbar") and callable(win._new_toolbar):
        styles_tb = win._new_toolbar(_tr("Styles"), "styles_toolbar")
    else:
        styles_tb = QToolBar(_tr("Styles"), win)
        styles_tb.setObjectName("styles_toolbar")
        styles_tb.setMovable(True)
        styles_tb.setFloatable(True)
        try:
            from views.icons import toolbar_icon_px
            px = toolbar_icon_px()
        except Exception:
            px = 24
        styles_tb.setIconSize(QSize(px, px))
        styles_tb.setToolButtonStyle(Qt.ToolButtonIconOnly)
        win.addToolBar(Qt.TopToolBarArea, styles_tb)

    if hasattr(win, "toolbars") and isinstance(win.toolbars, dict):
        win.toolbars["styles_toolbar"] = styles_tb

    from PySide6.QtGui import QActionGroup
    style_group = QActionGroup(win)
    try:
        style_group.setExclusionPolicy(QActionGroup.ExclusionPolicy.ExclusiveOptional)
    except Exception:
        style_group.setExclusive(True)

    style_actions: dict[str, QAction] = {}
    style_defs = [
        ("Default", "style_default", _tr("Default"), _tr("Default (Shaded with Textures)"),
         _tr("Faces with their materials and textures, under the sky.")),
        ("Architectural", "style_architectural", _tr("Architectural"), _tr("Architectural"),
         _tr("Faces with their materials on a plain white background, without the sky.")),
        ("Shaded", "style_shaded", _tr("Shaded"), _tr("Shaded"),
         _tr("Faces in their colours, without textures.")),
        ("Hidden line", "style_hidden_line", _tr("Hidden Line"), _tr("Hidden line"),
         _tr("White faces that hide what lies behind them — a clean line drawing.")),
        ("Monochrome", "style_monochrome", _tr("Monochrome"), _tr("Monochrome"),
         _tr("Every face in the front or back colour, without materials.")),
        ("Wireframe", "style_wireframe", _tr("Wireframe"), _tr("Wireframe"),
         _tr("Only the edges: the faces are not drawn.")),
        ("X-ray", "style_xray", _tr("X-ray"), _tr("X-ray  (Alt+X)"),
         _tr("See-through faces, so the edges behind them show.")),
    ]

    for name, key, label, tip, status_tip in style_defs:
        act = QAction(_make_icon(key), label, win)
        act.setToolTip(tip)
        act.setStatusTip(status_tip)
        act.setCheckable(True)
        style_group.addAction(act)
        act.triggered.connect(lambda _c=False, n=name: _apply_style_by_name(win, n))
        styles_tb.addAction(act)
        style_actions[name] = act
        actions.append((act, key))

    def _sync_style_toolbar_buttons() -> None:
        try:
            vp = getattr(win, "viewport", None)
            scene = getattr(vp, "scene", None)
            cur_style = getattr(scene, "display_style", None)
            cur_name = getattr(cur_style, "name", None)
            for n, a in style_actions.items():
                a.blockSignals(True)
                a.setChecked(n == cur_name)
                a.blockSignals(False)
        except Exception:
            pass

    orig_sync = getattr(win, "_sync_style_menu", None)
    if callable(orig_sync):
        def _hooked_sync():
            orig_sync()
            _sync_style_toolbar_buttons()
        win._sync_style_menu = _hooked_sync

    vp = getattr(win, "viewport", None)
    if hasattr(vp, "sceneVersionChanged"):
        try:
            vp.sceneVersionChanged.connect(lambda _v: _sync_style_toolbar_buttons())
        except Exception:
            pass

    _sync_style_toolbar_buttons()
    styles_tb.show()

    # Register all actions for theme refresh if supported
    if hasattr(win, "_icon_actions") and isinstance(win._icon_actions, list):
        for act, key in actions:
            win._icon_actions.append((act, key))

    # 3. Add an "Organize" submenu to Extensions menu
    try:
        ext_menu = app.add_menu(_tr("Organize"))
        if ext_menu is not None:
            for act, _k in actions[:3]:
                ext_menu.addAction(act)
            ext_menu.addSeparator()
            ext_menu.addAction(act_rev)
            ext_menu.addSeparator()
            ext_menu.addAction(act_grp)
            ext_menu.addAction(act_ungrp)
            ext_menu.addSeparator()
            ext_menu.addAction(act_axes)
            ext_menu.addSeparator()
            styles_submenu = ext_menu.addMenu(_tr("Styles"))
            for name, _key, _label, _tip, _stip in style_defs:
                styles_submenu.addAction(style_actions[name])
    except Exception as e:
        log.warning("Could not add Organize submenu to Extensions: %s", e)
