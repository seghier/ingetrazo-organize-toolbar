# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2026 Marco Sumari Tellez and IngeTrazo contributors.
"""Organize Toolbar plugin for IngeTrazo.

Self-contained plugin providing a dedicated toolbar and Extensions submenu for:
- Hide selection (Ctrl+H)
- Unhide Last
- Unhide All
- Reverse Faces
- Make Group (Ctrl+G)
- Explode Group (Ctrl+Shift+G)
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


_ICON_DISPATCH = {
    "hide": _draw_hide,
    "unhide_last": _draw_unhide_last,
    "unhide_all": _draw_unhide_all,
    "reverse_face": _draw_reverse_face,
    "group": _draw_group,
    "ungroup": _draw_ungroup,
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


# ---- Plugin Setup -----------------------------------------------------------

def setup(app) -> None:
    """Entry point called by IngeTrazo when loading extensions."""
    win = app.window

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

    tb.show()

    # Register all actions for theme refresh if supported
    if hasattr(win, "_icon_actions") and isinstance(win._icon_actions, list):
        for act, key in actions:
            win._icon_actions.append((act, key))

    # Add an "Organize" submenu to Extensions menu
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
    except Exception as e:
        log.warning("Could not add Organize submenu to Extensions: %s", e)
