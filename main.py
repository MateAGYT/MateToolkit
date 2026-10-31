#!/usr/bin/env python3
#  __  __       _          _    ____
# |  \/  | __ _| |_ ___   / \  / ___|
# | |\/| |/ _` | __/ _ \ / _ \| |  _
# | |  | | (_| | ||  __// ___ \ |_| |
# |_|  |_|\__,_|\__\___/_/   \_\____|
#
# (c) Copyright 2026 - MateAG
# All rights reserved. Any copy without
# consent of this code will be reported.
# 

import os
import re
import sys
import ssl
import json
import math
import time
import uuid
import socket
import random
import string
import shutil
import base64
import binascii
import traceback
import datetime
import difflib
import zipfile
import tarfile
import hashlib
import secrets
import binascii
import datetime
import ipaddress
import subprocess
import threading
import urllib.request
import urllib.parse
import urllib.error
import concurrent.futures

import requests

from PyQt6.QtCore import (
    Qt, QTimer, QUrl, QEasingCurve, QPropertyAnimation, QVariantAnimation, QThread,
    QPointF, QEvent, pyqtSignal
)
from PyQt6.QtGui import (
    QColor, QFont, QIcon, QPixmap, QPainter, QPen, QRadialGradient, QDesktopServices
)
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QTextEdit, QPlainTextEdit,
    QLineEdit, QComboBox, QSpinBox, QProgressBar, QGraphicsOpacityEffect,
    QScrollArea, QCheckBox, QFileDialog, QSplitter
)


class P:
    BG = "#080808"
    RAIL = "#0b0b0b"
    PANEL = "#0d0d0d"
    PANEL_2 = "#121212"
    PANEL_3 = "#181818"
    HOVER = "#1f1f1f"
    BORDER = "#1c1c1c"
    BORDER_HI = "#2e2e2e"
    TEXT = "#f2f2f2"
    MUTED = "#8f8f8f"
    DIM = "#616161"

    WHITE = "#f1f1f1"
    ACCENT = "#e4e4e4"

    MEDIA = "#e6b8d2"
    NETWORK = "#a6d8e2"
    RECON = "#bfc4ea"
    WEB = "#e8cfa4"
    DATA = "#aedbc0"
    UTILS = "#cfcfcf"
    START = "#e6e6e6"
    GREEN = "#aedbc0"

    OK = "#9fd8b4"
    WARN = "#e2c894"
    ERR = "#e79b98"
    DARK = "#0d0d0d"

    CAT = {
        "START": START,
        "MEDIA": MEDIA,
        "NETWORK": NETWORK,
        "RECON": RECON,
        "WEB": WEB,
        "DATA": DATA,
        "UTILITIES": UTILS,
    }

    LEVELS = {
        "text": "#d6d6d6", "info": "#808080", "dim": "#5e5e5e",
        "ok": "#9fd8b4", "warn": "#e2c894", "err": "#e79b98",
        "accent": "#e4e4e4", "out": "#e9e9e9",
    }


def mix(a, b, t):
    t = max(0.0, min(1.0, t))
    a = a if isinstance(a, QColor) else QColor(a)
    b = b if isinstance(b, QColor) else QColor(b)
    return QColor(
        int(a.red() + (b.red() - a.red()) * t),
        int(a.green() + (b.green() - a.green()) * t),
        int(a.blue() + (b.blue() - a.blue()) * t),
    )


def tint(color, factor):
    return mix(P.BG, color, factor).name()


def lift(color, factor):
    return mix(color, QColor("#ffffff"), factor).name()


def grad(top, bottom):
    return ("qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 {}, stop:1 {})"
            .format(top, bottom))


def human_size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return "{:.1f} {}".format(n, unit) if unit != "B" else "{} B".format(n)
        n /= 1024.0

def round_to(value, step=1, mode="nearest"):
    if not step:
        step = 1
    steps = value / step
    if mode == "up":
        steps = math.ceil(steps)
    elif mode == "down":
        steps = math.floor(steps)
    else:
        steps = round(steps)
    return steps * step


def round_str(value, digits=2, step=None, mode="nearest"):
    if step:
        value = round_to(value, step, mode)
    text = ("{:." + str(max(0, digits)) + "f}").format(value)
    if "." in text:
        text = text.rstrip("0").rstrip(".")
    return text or "0"

def resolve_binary(name):
    local = os.path.join(os.getcwd(), "bin_{}".format(name))
    if os.path.isdir(local):
        for root, _dirs, files in os.walk(local):
            for f in files:
                if f.lower() in ("{}.exe".format(name), name):
                    return os.path.join(root, f)
    return shutil.which(name)


def ua():
    return {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) MultiToolkit"}


def normalise(url):
    url = url.strip()
    if url and not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url


def _rng(base, chars):
    return {c: chr(base + i) for i, c in enumerate(chars)}


def _mix(*parts):
    out = {}
    for part in parts:
        out.update(part)
    return out


UPPER = string.ascii_uppercase
LOWER = string.ascii_lowercase
DIGITS = string.digits

SCRIPT_GAP_U = {"B": "\u212c", "E": "\u2130", "F": "\u2131", "H": "\u210b",
                "I": "\u2110", "L": "\u2112", "M": "\u2133", "R": "\u211b"}
SCRIPT_GAP_L = {"e": "\u212f", "g": "\u210a", "o": "\u2134"}
DOUBLE_GAP_U = {"C": "\u2102", "H": "\u210d", "N": "\u2115", "P": "\u2119",
                "Q": "\u211a", "R": "\u211d", "Z": "\u2124"}

STYLES = {
    "bold": _mix(_rng(0x1D400, UPPER), _rng(0x1D41A, LOWER), _rng(0x1D7CE, DIGITS)),
    "italic": _mix(_rng(0x1D434, UPPER), _rng(0x1D44E, LOWER), {"h": "\u210e"}),
    "bold italic": _mix(_rng(0x1D468, UPPER), _rng(0x1D482, LOWER)),
    "script": _mix(_rng(0x1D49C, UPPER), _rng(0x1D4B6, LOWER),
                   SCRIPT_GAP_U, SCRIPT_GAP_L),
    "bold script": _mix(_rng(0x1D4D0, UPPER), _rng(0x1D4EA, LOWER)),
    "double struck": _mix(_rng(0x1D538, UPPER), _rng(0x1D552, LOWER),
                          _rng(0x1D7D8, DIGITS), DOUBLE_GAP_U),
    "monospace": _mix(_rng(0x1D670, UPPER), _rng(0x1D68A, LOWER), _rng(0x1D7F6, DIGITS)),
    "sans bold": _mix(_rng(0x1D5A0, UPPER), _rng(0x1D5BA, LOWER), _rng(0x1D7E2, DIGITS)),
    "circled": _mix(_rng(0x24B6, UPPER), _rng(0x24D0, LOWER),
                    dict(zip("1234567890", "\u2460\u2461\u2462\u2463\u2464\u2465"
                                            "\u2466\u2467\u2468\u24ea"))),
    "parenthesized": _mix(_rng(0x249C, LOWER),
                          dict(zip("123456789", "\u2474\u2475\u2476\u2477"
                                                "\u2478\u2479\u247a\u247b\u247c"))),
    "fullwidth": _mix(_rng(0xFF21, UPPER), _rng(0xFF41, LOWER),
                      _rng(0xFF10, DIGITS), {" ": "\u3000"}),
    "small caps": dict(zip("abcdefghijklmnopqrstuvwxyz",
                           "\u1d00\u0299\u1d04\u1d05\u1d07\ua730\u0262\u029c\u026a\u1d0a"
                           "\u1d0b\u029f\u1d0d\u0274\u1d0f\u1d18Q\u0280\ua731\u1d1b\u1d1c"
                           "\u1d20\u1d21x\u028f\u1d22")),
    "upside down": dict(zip("abcdefghijklmnopqrstuvwxyz0123456789",
                            "\u0250q\u0254p\u01dd\u025f\u0183\u025e\u1d09\u027e\u029e"
                            "l\u026fupoq\u0279s\u0287n\u028c\u028dx\u028ez"
                            "0\u0196\u1405\u0190\u3123\u03db9\u312586")),
}

ZALGO = ["\u0300", "\u0301", "\u0302", "\u0303", "\u0308", "\u030a", "\u0311",
         "\u0313", "\u0334", "\u0335", "\u0336", "\u035c", "\u0361"]

MORSE = dict(zip(UPPER, [".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....",
                         "..", ".---", "-.-", ".-..", "--", "-.", "---", ".--.",
                         "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-",
                         "-.--", "--.."]))
MORSE.update(dict(zip(DIGITS, ["-----", ".----", "..---", "...--", "....-",
                               ".....", "-....", "--...", "---..", "----."])))
MORSE_REV = {v: k for k, v in MORSE.items()}

VERSION = "1.0"


class Tween(QVariantAnimation):
    def __init__(self, parent, start, end, apply, duration=160):
        super().__init__(parent)
        self.setStartValue(0.0)
        self.setEndValue(1.0)
        self.setDuration(duration)
        self.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._a = QColor(start)
        self._b = QColor(end)
        self._apply = apply
        self.valueChanged.connect(lambda v: self._apply(mix(self._a, self._b, float(v))))


class HoverBorder:
    def _hover_init(self, base, hot, duration=150):
        self._hb = QColor(base)
        self._hh = QColor(hot)
        self._hd = duration
        self._ht = None
        self._hpaint(0.0)

    def _hpaint(self, ratio):
        self.setStyleSheet(self._hsheet(mix(self._hb, self._hh, ratio).name()))

    def _hfade(self, target):
        anim = QVariantAnimation(self)
        anim.setStartValue(0.0)
        anim.setEndValue(float(target))
        anim.setDuration(self._hd)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.valueChanged.connect(lambda v: self._hpaint(float(v)))
        anim.start()
        self._ht = anim

    def enterEvent(self, event):
        if self.isEnabled():
            self._hfade(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hfade(0.0)
        super().leaveEvent(event)


class HoverLine(HoverBorder, QLineEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hover_init(P.BORDER, P.BORDER_HI)

    def _hsheet(self, color):
        return ("QLineEdit {{ background-color: {}; color: {}; border: 1px solid {};"
                " border-radius: 14px; padding: 0 14px; }}"
                "QLineEdit:focus {{ border-color: {}; }}".format(P.BG, P.TEXT, color, P.BORDER_HI))


class HoverCombo(HoverBorder, QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hover_init(P.BORDER, P.BORDER_HI)

    def _hsheet(self, color):
        return ("QComboBox {{ background-color: {}; color: {}; border: 1px solid {};"
                " border-radius: 14px; padding: 0 14px; }}"
                "QComboBox::drop-down {{ border: none; width: 20px; }}"
                "QComboBox QAbstractItemView {{ background-color: {}; color: {};"
                " border: 1px solid {}; border-radius: 12px; selection-background-color: {};"
                " outline: none; }}".format(
                    P.BG, P.TEXT, color, P.PANEL_2, P.TEXT, P.BORDER, P.PANEL_3))


class HoverSpin(HoverBorder, QSpinBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hover_init(P.BORDER, P.BORDER_HI)

    def _hsheet(self, color):
        return ("QSpinBox {{ background-color: {}; color: {}; border: 1px solid {};"
                " border-radius: 14px; padding: 0 14px; }}"
                "QSpinBox::up-button, QSpinBox::down-button {{ width: 16px; border: none; }}".format(
                    P.BG, P.TEXT, color))


class HoverText(HoverBorder, QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self._hover_init(P.BORDER, P.BORDER_HI)

    def _hsheet(self, color):
        return ("QPlainTextEdit {{ background-color: {}; color: {}; border: 1px solid {};"
                " border-radius: 14px; padding: 8px; }}".format(P.BG, P.TEXT, color))


class HoverFrame(QFrame):
    def __init__(self, accent=P.WHITE, radius=18, parent=None):
        super().__init__(parent)
        self._hf = QColor(accent)
        self._hr = radius
        self._hv = 0.0
        self._ha = None
        self._hpaint()

    def _hpaint(self):
        bg = mix(P.PANEL, self._hf, 0.05 * self._hv).name()
        bd = mix(QColor(P.BORDER), self._hf, 0.42 * self._hv).name()
        self.setStyleSheet(
            "QFrame {{ background-color: {}; border: 1px solid {}; border-radius: {}px; }}".format(
                bg, bd, self._hr))

    def _hfade(self, target):
        anim = QVariantAnimation(self)
        anim.setStartValue(self._hv)
        anim.setEndValue(float(target))
        anim.setDuration(180)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.valueChanged.connect(self._hstep)
        anim.start()
        self._ha = anim

    def _hstep(self, value):
        self._hv = float(value)
        self._hpaint()

    def enterEvent(self, event):
        self._hfade(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._hfade(0.0)
        super().leaveEvent(event)


class RootWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("Root")
        self.setMouseTracking(True)
        self._x = 0.5
        self._y = 0.25

    def set_pointer(self, point):
        self._x = point.x() / max(1, self.width())
        self._y = point.y() / max(1, self.height())
        self.update()

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.fillRect(self.rect(), QColor(P.BG))
        p.setPen(QPen(QColor(255, 255, 255, 10), 1))
        step = 64
        for x in range(0, self.width(), step):
            p.drawLine(x, 0, x, self.height())
        for y in range(0, self.height(), step):
            p.drawLine(0, y, self.width(), y)
        cx = self._x * self.width()
        cy = self._y * self.height()
        glow = QRadialGradient(QPointF(cx, cy), 340)
        glow.setColorAt(0.0, QColor(255, 255, 255, 24))
        glow.setColorAt(0.55, QColor(255, 255, 255, 8))
        glow.setColorAt(1.0, QColor(255, 255, 255, 0))
        p.setBrush(glow)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(QPointF(cx, cy), 340, 340)


class LogoMark(QWidget):
    def __init__(self, size=26, parent=None):
        super().__init__(parent)
        self.setFixedSize(size, size)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._angle = 205
        self._glow = 0.0
        self._t = QTimer(self)
        self._t.timeout.connect(self._spin)
        self._t.start(40)

    def _spin(self):
        self._angle = (self._angle + 4) % 360
        if self._glow > 0.0:
            self._glow = max(0.0, self._glow - 0.05)
        self.update()

    def enterEvent(self, event):
        self._glow = 1.0
        super().enterEvent(event)

    def mousePressEvent(self, event):
        self._glow = 1.0
        self._angle = (self._angle + 90) % 360
        super().mousePressEvent(event)

    def paintEvent(self, _e):
        s = self.width()
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        if self._glow > 0:
            halo = QColor(255, 255, 255)
            halo.setAlpha(int(60 * self._glow))
            p.setBrush(halo)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(self.rect().adjusted(-1, -1, 1, 1), s * 0.32, s * 0.32)
        p.setBrush(QColor(P.PANEL_3))
        p.setPen(QPen(QColor(mix(QColor(P.BORDER_HI), QColor(P.WHITE), self._glow)), 1))
        p.drawRoundedRect(self.rect().adjusted(0, 0, -1, -1), s * 0.30, s * 0.30)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(P.BORDER_HI), 1.2))
        p.drawEllipse(int(s * 0.14), int(s * 0.14), int(s * 0.72), int(s * 0.72))
        p.setPen(QPen(QColor(P.WHITE), max(1.6, s * 0.07),
                      Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawArc(int(s * 0.10), int(s * 0.18), int(s * 0.80), int(s * 0.64),
                  int(self._angle * 16), int(135 * 16))
        p.setPen(QColor(P.TEXT))
        p.setFont(QFont("Consolas", max(6, int(s * 0.28)), QFont.Weight.Bold))
        p.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "MT")


def build_icon():
    icon = QIcon()
    for size in (16, 20, 24, 32, 40, 48, 64, 128, 256):
        pm = QPixmap(size, size)
        pm.fill(Qt.GlobalColor.transparent)
        p = QPainter(pm)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        p.setBrush(QColor(P.BG))
        p.setPen(QPen(QColor(P.BORDER_HI), max(1.0, size * 0.02)))
        p.drawRoundedRect(pm.rect().adjusted(1, 1, -1, -1), size * 0.28, size * 0.28)
        p.setBrush(Qt.BrushStyle.NoBrush)
        p.setPen(QPen(QColor(P.BORDER_HI), max(1.0, size * 0.045)))
        p.drawEllipse(int(size * 0.13), int(size * 0.13), int(size * 0.74), int(size * 0.74))
        p.setPen(QPen(QColor(P.WHITE), max(1.5, size * 0.08),
                      Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        p.drawArc(int(size * 0.09), int(size * 0.18), int(size * 0.82), int(size * 0.62),
                  205 * 16, 130 * 16)
        p.setPen(QColor(P.TEXT))
        p.setFont(QFont("Consolas", max(5, int(size * 0.28)), QFont.Weight.Bold))
        p.drawText(pm.rect(), Qt.AlignmentFlag.AlignCenter, "MT")
        p.end()
        icon.addPixmap(pm)
    return icon


class PillButton(QPushButton):
    def __init__(self, text, accent=P.WHITE, filled=False, height=32, radius=999, parent=None):
        super().__init__(text, parent)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFixedHeight(height)
        self._r = radius
        self._filled = filled
        self._accent = QColor(accent)
        self._bg = QColor(accent if filled else P.PANEL_2)
        self._fg = QColor(P.DARK if filled else P.MUTED)
        self._bd = QColor(accent if filled else P.BORDER)
        self._t = []
        self.setFont(QFont("Segoe UI", 8, QFont.Weight.DemiBold))
        self._apply()

    def _apply(self):
        surface = grad(lift(self._bg, 0.10), self._bg.name()) if self._filled else self._bg.name()
        self.setStyleSheet(
            "QPushButton {{ background: {bg}; color: {fg}; border: 1px solid {bd};"
            " border-radius: {r}px; padding: 0 16px; }}"
            "QPushButton:disabled {{ background: {off}; color: #565656;"
            " border-color: {bd2}; }}".format(
                bg=surface, fg=self._fg.name(), bd=self._bd.name(), r=self._r,
                off=P.PANEL_3, bd2=P.BORDER))

    def _go(self, bg, fg, bd, dur=150):
        self._t = [
            Tween(self, self._bg, bg, self._set_bg, dur),
            Tween(self, self._fg, fg, self._set_fg, dur),
            Tween(self, self._bd, bd, self._set_bd, dur),
        ]
        for t in self._t:
            t.start()

    def _set_bg(self, c):
        self._bg = c
        self._apply()

    def _set_fg(self, c):
        self._fg = c
        self._apply()

    def _set_bd(self, c):
        self._bd = c
        self._apply()

    def _hover_style(self):
        if self._filled:
            c = QColor(lift(self._accent, 0.18))
            self._go(c, QColor(P.DARK), c)
        else:
            self._go(QColor(P.HOVER), QColor(P.TEXT), QColor(P.BORDER_HI))

    def enterEvent(self, e):
        if self.isEnabled():
            self._hover_style()
        super().enterEvent(e)

    def leaveEvent(self, e):
        if self._filled:
            self._go(QColor(self._accent), QColor(P.DARK), QColor(self._accent), 190)
        else:
            self._go(QColor(P.PANEL_2), QColor(P.MUTED), QColor(P.BORDER), 190)
        super().leaveEvent(e)

    def mousePressEvent(self, e):
        if self.isEnabled():
            c = QColor(tint(self._accent, 0.72))
            self._go(c, QColor(P.DARK if self._filled else P.TEXT), c, 90)
        super().mousePressEvent(e)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        if self.underMouse():
            self._hover_style()
        else:
            self.leaveEvent(e)


class PulseDot(QWidget):
    def __init__(self, color=P.WHITE, size=10, parent=None):
        super().__init__(parent)
        self._c = QColor(color)
        self._p = 0.35
        self._d = 1
        self._k = 0.0
        self.setFixedSize(size, size)
        self._t = QTimer(self)
        self._t.timeout.connect(self._tick)
        self._t.start(50)

    def set_color(self, color):
        self._c = QColor(color)
        self._k = 1.0
        self.update()

    def _tick(self):
        self._p += 0.05 * self._d
        if self._p >= 1.0:
            self._p, self._d = 1.0, -1
        elif self._p <= 0.3:
            self._p, self._d = 0.3, 1
        if self._k > 0:
            self._k = max(0.0, self._k - 0.06)
        self.update()

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        halo = QColor(self._c)
        halo.setAlpha(int((40 + 60 * self._p) * (1.0 + self._k * 1.6)))
        p.setBrush(halo)
        p.setPen(Qt.PenStyle.NoPen)
        p.drawEllipse(self.rect())
        c = QColor(self._c)
        c.setAlpha(int(120 + 135 * self._p))
        p.setBrush(c)
        p.drawEllipse(self.rect().adjusted(2, 2, -2, -2))


class Badge(QLabel):
    def __init__(self, text, fg=P.MUTED, bg=P.PANEL_3, parent=None):
        super().__init__(text, parent)
        self.setFixedHeight(20)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFont(QFont("Segoe UI", 8))
        self._fg = fg
        self._bg = bg
        self._v = 0.0
        self._a = None
        self._paint()

    def set_state(self, text, fg, bg):
        self.setText(text)
        self._fg = fg
        self._bg = bg
        self._paint()

    def _paint(self):
        fg = mix(self._fg, QColor(P.WHITE), 0.35 * self._v).name()
        bd = mix(QColor(tint(self._fg, 0.35)), QColor(self._fg), 0.6 * self._v).name()
        bg = mix(QColor(self._bg), QColor(tint(self._fg, 0.4)), 0.7 * self._v).name()
        self.setStyleSheet(
            "QLabel {{ color: {f}; background-color: {b}; border: 1px solid {bd};"
            " border-radius: 10px; padding: 0 10px; }}".format(f=fg, b=bg, bd=bd))

    def _fade(self, target):
        anim = QVariantAnimation(self)
        anim.setStartValue(self._v)
        anim.setEndValue(float(target))
        anim.setDuration(170)
        anim.valueChanged.connect(self._step)
        anim.start()
        self._a = anim

    def _step(self, value):
        self._v = float(value)
        self._paint()

    def enterEvent(self, event):
        self._fade(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._fade(0.0)
        super().leaveEvent(event)


class NavItem(QWidget):
    def __init__(self, glyph, text, accent=P.WHITE, parent=None):
        super().__init__(parent)
        self._hover = 0.0
        self._press = 0.0
        self._active = False
        self._accent = QColor(accent)
        self._t = None
        self.setFixedHeight(34)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(12, 0, 10, 0)
        lay.setSpacing(10)
        self.icon = QLabel(glyph)
        self.icon.setFont(QFont("Segoe UI Symbol", 11))
        self.icon.setFixedWidth(14)
        self.icon.setStyleSheet("color: {}; background: transparent; border: none;".format(P.DIM))
        self.label = QLabel(text)
        self.label.setFont(QFont("Segoe UI", 9))
        self.label.setStyleSheet("color: {}; background: transparent; border: none;".format(P.MUTED))
        lay.addWidget(self.icon)
        lay.addWidget(self.label, 1)

    def set_active(self, state):
        self._active = state
        self.label.setStyleSheet(
            "color: {}; background: transparent; border: none;".format(P.TEXT if state else P.MUTED))
        self.icon.setStyleSheet(
            "color: {}; background: transparent; border: none;".format(
                self._accent.name() if state else P.DIM))
        self.label.setFont(QFont("Segoe UI", 9, QFont.Weight.DemiBold if state else QFont.Weight.Normal))
        self.update()

    def press_fx(self):
        anim = QVariantAnimation(self)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setDuration(340)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)

        def step(v):
            self._press = float(v)
            self.update()

        anim.valueChanged.connect(step)
        anim.start()

    def enterEvent(self, e):
        self._anim(1.0)
        super().enterEvent(e)

    def leaveEvent(self, e):
        self._anim(0.0)
        super().leaveEvent(e)

    def _anim(self, target):
        anim = QVariantAnimation(self)
        anim.setStartValue(self._hover)
        anim.setEndValue(target)
        anim.setDuration(140)

        def step(v):
            self._hover = float(v)
            self.update()

        anim.valueChanged.connect(step)
        anim.start()
        self._t = anim

    def paintEvent(self, _e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)
        r = self.rect().adjusted(0, 1, -1, -1)
        if self._active:
            p.setBrush(QColor(P.PANEL_3))
            p.setPen(QPen(QColor(P.BORDER_HI), 1))
            p.drawRoundedRect(r, 10, 10)
            p.setBrush(self._accent)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(1, 10, 3, self.height() - 20, 2, 2)
        elif self._hover > 0.01:
            c = QColor(P.HOVER)
            c.setAlpha(int(255 * self._hover))
            p.setBrush(c)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(r, 10, 10)
            p.setBrush(self._accent)
            p.setOpacity(0.5 * self._hover)
            p.drawRoundedRect(1, 10, 3, self.height() - 20, 2, 2)
        if self._press > 0.01:
            flash = QColor(self._accent)
            flash.setAlpha(int(70 * self._press))
            p.setOpacity(1.0)
            p.setBrush(flash)
            p.setPen(Qt.PenStyle.NoPen)
            p.drawRoundedRect(r, 10, 10)

    def mousePressEvent(self, e):
        pass


class Toast(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
        lay = QHBoxLayout(self)
        lay.setContentsMargins(16, 10, 16, 10)
        self.label = QLabel("")
        self.label.setFont(QFont("Segoe UI", 9))
        lay.addWidget(self.label)
        self._fx = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._fx)
        self.hide()
        self._anim = None

    def show_message(self, text, level="ok"):
        fg = P.OK if level == "ok" else P.ERR if level == "err" else P.WARN
        self.setStyleSheet(
            "QFrame {{ background-color: {}; border: 1px solid {}; border-radius: 14px; }}".format(
                P.PANEL_2, tint(fg, 0.4)))
        self.label.setStyleSheet("color: {}; background: transparent; border: none;".format(fg))
        self.label.setText(text)
        self.adjustSize()
        self.resize(min(self.sizeHint().width() + 8, 460), self.sizeHint().height())
        self.show()
        self.raise_()
        self._place()
        grp = QVariantAnimation(self)
        grp.setStartValue(0.0)
        grp.setEndValue(1.0)
        grp.setDuration(170)
        grp.valueChanged.connect(lambda v: self._fx.setOpacity(float(v)))
        grp.start()
        self._anim = grp
        QTimer.singleShot(2600, self._out)

    def _place(self):
        p = self.parentWidget()
        if p:
            self.move(p.width() - self.width() - 26, p.height() - self.height() - 92)

    def _out(self):
        anim = QVariantAnimation(self)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setDuration(220)
        anim.valueChanged.connect(lambda v: self._fx.setOpacity(float(v)))
        anim.finished.connect(self.hide)
        anim.start()
        self._anim = anim


class HelpButton(QPushButton):
    def __init__(self, parent=None):
        super().__init__("?", parent)
        self.setFixedSize(18, 18)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setFont(QFont("Segoe UI", 8))
        self._on = False
        self._accent = P.WHITE
        self._v = 0.0
        self._flash = 0.0
        self._t = QTimer(self)
        self._t.timeout.connect(self._decay)
        self._t.start(40)
        self._paint()

    def _decay(self):
        if self._flash > 0.0:
            self._flash = max(0.0, self._flash - 0.08)
            self._paint()

    def set_accent(self, color):
        self._accent = color
        self._paint()

    def _paint(self):
        bg = self._accent if self._on else mix(QColor(P.PANEL_3), QColor(P.BORDER_HI), self._v).name()
        fg = P.DARK if self._on else mix(QColor(P.DIM), QColor(P.TEXT), self._v).name()
        bd = self._accent if self._on else mix(QColor(P.BORDER), QColor(P.BORDER_HI), self._v).name()
        if self._flash > 0.01:
            bg = mix(QColor(bg), QColor(self._accent), self._flash).name()
            bd = self._accent
            fg = P.DARK
        ring = 1 + int(round(3 * self._flash))
        self.setStyleSheet(
            "QPushButton {{ background-color: {bg}; color: {fg}; border: {ring}px solid {bd};"
            " border-radius: 9px; padding: 0; }}".format(bg=bg, fg=fg, bd=bd, ring=ring))

    def _fade(self, target):
        anim = QVariantAnimation(self)
        anim.setStartValue(self._v)
        anim.setEndValue(float(target))
        anim.setDuration(150)
        anim.valueChanged.connect(self._step)
        anim.start()

    def _step(self, value):
        self._v = float(value)
        self._paint()

    def enterEvent(self, event):
        self._fade(1.0)
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._fade(0.0)
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        self._flash = 1.0
        self._paint()
        super().mousePressEvent(event)

    def toggle(self):
        self._on = not self._on
        self._flash = 1.0
        self._paint()


class HelpStrip(QLabel):
    def __init__(self, text, accent=P.WHITE, parent=None):
        super().__init__(text, parent)
        self.setWordWrap(True)
        self.setVisible(False)
        self.setFont(QFont("Segoe UI", 9))
        self._fx = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._fx)
        self._fx.setOpacity(0.0)
        self._anim = None
        self._open = False
        self.setStyleSheet(
            "QLabel {{ color: {c}; background-color: {b}; border: none;"
            " border-left: 2px solid {a}; border-radius: 0 10px 10px 0; padding: 8px 12px; }}".format(
                c=P.MUTED, b=P.PANEL_2, a=tint(accent, 0.6)))

    def set_expanded(self, state):
        if state == self._open:
            return
        self._open = state
        if self._anim:
            self._anim.stop()
        anim = QVariantAnimation(self)
        anim.setDuration(210 if state else 160)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        if state:
            self.setVisible(True)
            self.setMaximumHeight(0)
            target = max(self.sizeHint().height(), 28)
            anim.setStartValue(0.0)
            anim.setEndValue(1.0)

            def step(v):
                v = float(v)
                self.setMaximumHeight(int(target * v))
                self._fx.setOpacity(v)

            anim.valueChanged.connect(step)
            anim.finished.connect(lambda: self.setMaximumHeight(16777215))
        else:
            height = max(self.height(), 1)
            anim.setStartValue(1.0)
            anim.setEndValue(0.0)

            def step(v):
                v = float(v)
                self.setMaximumHeight(int(height * v))
                self._fx.setOpacity(v)

            anim.valueChanged.connect(step)
            anim.finished.connect(self.hide)
        anim.start()
        self._anim = anim


class ConsoleView(QWidget):
    def __init__(self, accent=P.WHITE, parent=None):
        super().__init__(parent)
        self._accent = QColor(accent)
        self._folded = False
        lay = QVBoxLayout(self)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(4)
        head = QHBoxLayout()
        head.setContentsMargins(2, 0, 2, 0)
        head.setSpacing(4)
        self.title = QLabel("OUTPUT")
        self.title.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        self.title.setStyleSheet(
            "color: {}; background: transparent; border: none;".format(P.DIM))
        head.addWidget(self.title)
        head.addStretch()
        self.btn_stop = PillButton("STOP", accent=P.ERR, height=24)
        self.btn_stop.setEnabled(False)
        self.btn_fold = PillButton("FOLD", accent=accent, height=24)
        self.btn_copy = PillButton("COPY", accent=accent, height=24)
        self.btn_clear = PillButton("CLEAR", accent=accent, height=24)
        for b in (self.btn_stop, self.btn_fold, self.btn_copy, self.btn_clear):
            head.addWidget(b)
        self.view = QPlainTextEdit()
        self.view.setReadOnly(True)
        self.view.setFrameStyle(0)
        self.view.setMinimumHeight(160)
        self.view.setFont(QFont("Consolas", 9))
        self.view.setStyleSheet(
            "QPlainTextEdit {{ background-color: #050505; color: #cfcfcf;"
            " border: 1px solid {}; border-radius: 3px; padding: 8px;"
            " selection-background-color: {}; }}".format(
                P.BORDER, tint(accent, 0.35)))
        lay.addLayout(head)
        lay.addWidget(self.view, 1)
        self.btn_clear.clicked.connect(self.view.clear)
        self.btn_copy.clicked.connect(self._copy)
        self.btn_fold.clicked.connect(self.toggle_fold)

    def toggle_fold(self):
        self._folded = not self._folded
        self.view.setVisible(not self._folded)
        self.btn_fold.setText("UNFOLD" if self._folded else "FOLD")

    def set_accent(self, color):
        self._accent = QColor(color)

    def _copy(self):
        QApplication.clipboard().setText(self.view.toPlainText())

    def append(self, text, level="text"):
        color = self._accent.name() if level == "accent" else P.LEVELS.get(level, P.MUTED)
        esc = (text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
               .replace("\n", "<br>").replace(" ", "&nbsp;"))
        self.view.appendHtml('<span style="color:{};">{}</span>'.format(color, esc))
        bar = self.view.verticalScrollBar()
        bar.setValue(bar.maximum())


class Task(QThread):
    output = pyqtSignal(str, str)
    done = pyqtSignal(int)

    def __init__(self, command=None, fn=None):
        super().__init__()
        self.command = command
        self.fn = fn
        self.proc = None
        self._stop = False

    def stop(self):
        self._stop = True
        if self.proc and self.proc.poll() is None:
            try:
                subprocess.run(["taskkill", "/f", "/t", "/pid", str(self.proc.pid)],
                               capture_output=True)
            except Exception:
                self.proc.terminate()

    def should_stop(self):
        return self._stop

    def run(self):
        if self.fn:
            try:
                self.fn(lambda t, lv="out": self.output.emit(t, lv), self.should_stop)
                self.done.emit(0)
            except Exception as exc:
                self.output.emit("{}: {}\n".format(type(exc).__name__, exc), "err")
                self.done.emit(1)
            return
        try:
            self.proc = subprocess.Popen(self.command, stdout=subprocess.PIPE,
                                         stderr=subprocess.STDOUT, text=True,
                                         bufsize=1, errors="replace")
        except Exception as exc:
            self.output.emit("{}\n".format(exc), "err")
            self.done.emit(-1)
            return
        for line in self.proc.stdout:
            self.output.emit(line, "out")
            if self._stop:
                break
        self.proc.wait()
        self.done.emit(self.proc.returncode)


RECIPES = {
    "yt-dlp": ("pip", "yt-dlp"),
    "gallery-dl": ("pip", "gallery-dl"),
    "sqlmap": ("pip", "sqlmap"),
    "wafw00f": ("pip", "wafw00f"),
    "ffmpeg": ("zip", "https://github.com/BtbN/FFmpeg-Builds/releases/download/latest/"
                      "ffmpeg-master-latest-win64-gpl.zip", "bin_ffmpeg"),
    "nmap": ("zip", "https://nmap.org/dist/nmap-7.95-win32.zip", "bin_nmap"),
    "ffuf": ("zip", "https://github.com/ffuf/ffuf/releases/download/v2.1.0/"
                    "ffuf_2.1.0_windows_amd64.zip", "bin_ffuf"),
    "gobuster": ("zip", "https://github.com/OJ/gobuster/releases/download/v3.6.0/"
                        "gobuster_Windows_x86_64.zip", "bin_gobuster"),
    "feroxbuster": ("zip", "https://github.com/epi052/feroxbuster/releases/latest/download/"
                           "x86_64-windows-feroxbuster.exe.zip", "bin_feroxbuster"),
    "nuclei": ("zip", "https://github.com/projectdiscovery/nuclei/releases/download/v3.3.5/"
                      "nuclei_3.3.5_windows_amd64.zip", "bin_nuclei"),
    "subfinder": ("zip", "https://github.com/projectdiscovery/subfinder/releases/download/v2.6.6/"
                         "subfinder_2.6.6_windows_amd64.zip", "bin_subfinder"),
    "httpx": ("zip", "https://github.com/projectdiscovery/httpx/releases/download/v1.6.9/"
                     "httpx_1.6.9_windows_amd64.zip", "bin_httpx"),
    "trufflehog": ("zip", "https://github.com/trufflesecurity/trufflehog/releases/download/"
                          "v3.82.0/trufflehog_3.82.0_windows_amd64.zip", "bin_trufflehog"),
    "exiftool": ("zip", "https://exiftool.org/exiftool-12.76_64.zip", "bin_exiftool"),
}


class Installer(QThread):
    progress = pyqtSignal(int)
    log = pyqtSignal(str, str)
    done = pyqtSignal(bool, str)

    def __init__(self, key):
        super().__init__()
        self.key = key

    def _pip(self, package):
        self.log.emit("pip install {}\n".format(package), "dim")
        self.progress.emit(25)
        p = subprocess.Popen([sys.executable, "-m", "pip", "install", "--upgrade", package],
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in p.stdout:
            if line.strip():
                self.log.emit(line.strip() + "\n", "dim")
        p.wait()
        self.progress.emit(100)
        self.done.emit(p.returncode == 0,
                       "{} installed".format(package) if p.returncode == 0
                       else "pip failed for {}".format(package))

    def _fetch(self, url, path):
        self.log.emit("downloading {}\n".format(url), "dim")
        with requests.get(url, stream=True) as r:
            total = int(r.headers.get("content-length") or 0)
            got = 0
            with open(path, "wb") as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
                    got += len(chunk)
                    if total:
                        self.progress.emit(10 + int(75 * got / total))

    def _zip(self, url, folder):
        target = os.path.join(os.getcwd(), folder)
        os.makedirs(target, exist_ok=True)
        path = os.path.join(target, "_dl.zip")
        self._fetch(url, path)
        self.progress.emit(88)
        self.log.emit("extracting...\n", "dim")
        with zipfile.ZipFile(path) as z:
            z.extractall(target)
        os.remove(path)
        self.progress.emit(100)
        self.done.emit(True, "{} ready in {}".format(self.key, folder))

    def _tar(self, url, folder):
        target = os.path.join(os.getcwd(), folder)
        os.makedirs(target, exist_ok=True)
        path = os.path.join(target, "_dl.tar.gz")
        self._fetch(url, path)
        self.progress.emit(88)
        self.log.emit("extracting...\n", "dim")
        with tarfile.open(path) as t:
            t.extractall(target)
        os.remove(path)
        self.progress.emit(100)
        self.done.emit(True, "{} ready in {}".format(self.key, folder))

    def run(self):
        recipe = RECIPES.get(self.key)
        if not recipe:
            self.done.emit(False, "no recipe for {}".format(self.key))
            return
        try:
            if recipe[0] == "pip":
                self._pip(recipe[1])
            elif recipe[0] == "zip":
                self._zip(recipe[1], recipe[2])
            elif recipe[0] == "tar":
                self._tar(recipe[1], recipe[2])
            else:
                self.done.emit(False, recipe[1])
        except Exception as exc:
            self.done.emit(False, str(exc))


class ToolPage(QWidget):
    status = pyqtSignal(str, str, float)
    ACCENT = P.WHITE

    def __init__(self, tool_id, name, glyph, tagline, what, docs_html):
        super().__init__()
        self.tool_id = tool_id
        self.name = name
        self.accent = self.ACCENT
        self.task = None
        self.installer = None
        self._cb_wraps = {}

        root = QVBoxLayout(self)
        root.setContentsMargins(16, 10, 16, 8)
        root.setSpacing(8)

        head = QHBoxLayout()
        head.setSpacing(8)
        self.badge = HoverFrame(self.accent, 12)
        self.badge.setFixedSize(28, 28)
        bl = QHBoxLayout(self.badge)
        bl.setContentsMargins(0, 0, 0, 0)
        icon = QLabel(glyph)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        icon.setFont(QFont("Segoe UI Symbol", 11))
        icon.setStyleSheet("color: {}; background: transparent; border: none;".format(self.accent))
        bl.addWidget(icon)
        titles = QVBoxLayout()
        titles.setSpacing(1)
        title = QLabel(name)
        title.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        title.setStyleSheet("color: {}; background: transparent; border: none;".format(P.TEXT))
        sub = QLabel(tagline)
        sub.setFont(QFont("Segoe UI", 8))
        sub.setStyleSheet("color: {}; background: transparent; border: none;".format(P.DIM))
        titles.addWidget(title)
        titles.addWidget(sub)
        head.addWidget(self.badge, 0, Qt.AlignmentFlag.AlignTop)
        head.addLayout(titles)
        head.addStretch()
        self.btn_docs = PillButton("GUIDE", accent=self.accent, height=28)
        self.btn_docs.clicked.connect(self.toggle_docs)
        head.addWidget(self.btn_docs, 0, Qt.AlignmentFlag.AlignTop)
        root.addLayout(head)

        self.strip = HoverFrame(self.accent, 12)
        sl = QHBoxLayout(self.strip)
        sl.setContentsMargins(12, 8, 12, 8)
        text = QLabel(what)
        text.setWordWrap(True)
        text.setFont(QFont("Segoe UI", 9))
        text.setStyleSheet("color: {}; background: transparent; border: none;".format(P.MUTED))
        sl.addWidget(text)
        root.addWidget(self.strip)

        env = QHBoxLayout()
        env.setSpacing(6)
        self.dot = PulseDot(P.WARN, 8)
        self.env_label = QLabel("checking")
        self.env_label.setFont(QFont("Consolas", 8))
        self.env_label.setStyleSheet("color: {}; background: transparent; border: none;".format(P.WARN))
        self.bar = QProgressBar()
        self.bar.setFixedHeight(4)
        self.bar.setTextVisible(False)
        self.bar.setVisible(False)
        self.bar.setStyleSheet(
            "QProgressBar {{ border: none; background-color: {}; border-radius: 2px; }}"
            "QProgressBar::chunk {{ background-color: {}; border-radius: 2px; }}".format(
                P.PANEL_3, self.accent))
        self.btn_install = PillButton("INSTALL", accent=P.WHITE, filled=True, height=24)
        self.btn_install.setVisible(False)
        self.btn_install.clicked.connect(self.install)
        env.addWidget(self.dot)
        env.addWidget(self.env_label)
        env.addWidget(self.bar, 1)
        env.addWidget(self.btn_install)
        root.addLayout(env)

        self.stack = QStackedWidget()
        self.config = QWidget()
        self.docs = QTextEdit()
        self.docs.setReadOnly(True)
        self.docs.setFrameStyle(0)
        self.docs.setStyleSheet(
            "QTextEdit {{ background-color: {}; color: {}; border: 1px solid {};"
            " border-radius: 16px; padding: 20px; }}".format(P.PANEL, P.MUTED, P.BORDER))
        self.docs.setHtml(docs_html.replace("#b9a8ff", self.accent))
        self.stack.addWidget(self.config)
        self.stack.addWidget(self.docs)
        root.addWidget(self.stack, 1)

        cfg = QVBoxLayout(self.config)
        cfg.setContentsMargins(0, 0, 0, 0)
        cfg.setSpacing(8)

        split = QSplitter(Qt.Orientation.Vertical)
        split.setStyleSheet(
            "QSplitter::handle {{ background: transparent; height: 12px; }}"
            "QScrollArea {{ background: transparent; border: none; }}"
            "QScrollBar:vertical {{ background: transparent; width: 6px; }}"
            "QScrollBar::handle:vertical {{ background: #242424; border-radius: 3px; }}"
            "QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}")
        form_host = QWidget()
        form_host.setStyleSheet("background: transparent;")
        self.form = QVBoxLayout(form_host)
        self.form.setContentsMargins(2, 2, 8, 4)
        self.form.setSpacing(8)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameStyle(0)
        scroll.setWidget(form_host)
        self.form_scroll = scroll

        self.console = ConsoleView(self.accent)
        self.console.btn_stop.clicked.connect(self.stop)

        self.run_row = QHBoxLayout()
        self.run_row.setSpacing(10)
        cfg.addLayout(self.run_row)
        split.addWidget(scroll)
        split.addWidget(self.console)
        split.setSizes([200, 520])
        self.split = split
        cfg.addWidget(split, 1)

        QTimer.singleShot(60, self._safe_check)

    def _safe_check(self):
        try:
            self.check_env()
        except Exception:
            traceback.print_exc()

    def divider(self):
        line = QFrame()
        line.setFixedHeight(1)
        line.setStyleSheet("background-color: {}; border: none;".format(P.BORDER))
        self.form.addWidget(line)

    def group(self, text):
        cap = QLabel(text.upper())
        cap.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        cap.setStyleSheet(
            "color: {}; background: transparent; border: none; padding-top: 4px;".format(P.DIM))
        cap.setContentsMargins(0, 3, 0, 0)
        self.form.addWidget(cap)

    def toggle_docs(self):
        docs = self.stack.currentIndex() == 1
        self.stack.setCurrentIndex(0 if docs else 1)
        self.btn_docs.setText("BACK" if not docs else "GUIDE")

    def reveal(self):
        try:
            self._reveals = []
            delay = 0
            for index in range(self.form.count()):
                item = self.form.itemAt(index)
                holder = item.widget() if item is not None else None
                if holder is None:
                    continue
                old = holder.graphicsEffect()
                if old is not None:
                    holder.setGraphicsEffect(None)
                fx = QGraphicsOpacityEffect(holder)
                holder.setGraphicsEffect(fx)
                anim = QPropertyAnimation(fx, b"opacity", holder)
                anim.setDuration(230)
                anim.setStartValue(0.0)
                anim.setEndValue(1.0)
                anim.setEasingCurve(QEasingCurve.Type.OutCubic)
                QTimer.singleShot(delay, anim.start)
                self._reveals.append(anim)
                delay = min(delay + 16, 260)
        except Exception:
            traceback.print_exc()

    def check_env(self):
        self.env_label.setText("ready")

    def mark_ready(self, detail):
        self.dot.set_color(P.OK)
        self.env_label.setStyleSheet("color: {}; background: transparent; border: none;".format(P.OK))
        self.env_label.setText(detail)
        self.btn_install.setVisible(False)

    def mark_missing(self, detail, installable=True):
        self.dot.set_color(P.ERR)
        self.env_label.setStyleSheet("color: {}; background: transparent; border: none;".format(P.ERR))
        self.env_label.setText(detail)
        self.btn_install.setVisible(installable)

    def install(self):
        if self.tool_id not in RECIPES:
            self.console.append("[install] no automatic recipe, see the guide\n", "warn")
            return
        self.btn_install.setEnabled(False)
        self.bar.setVisible(True)
        self.bar.setValue(0)
        self.installer = Installer(self.tool_id)
        self.installer.progress.connect(self.bar.setValue)
        self.installer.log.connect(self.console.append)
        self.installer.done.connect(self._installed)
        self.installer.start()

    def _installed(self, ok, message):
        self.bar.setVisible(False)
        self.btn_install.setEnabled(True)
        self.console.append("[install] {}\n".format(message), "ok" if ok else "err")
        self.check_env()
        self.status.emit(message, "ok" if ok else "err", 1.0 if ok else 0.0)

    def run(self, command, label=None):
        self.console.append("\n$ {}\n{}\n".format(subprocess.list2cmdline(command), "-" * 54),
                            "accent")
        self._start(Task(command=command), label)

    def run_python(self, fn, label=None):
        self.console.append("\n> {}\n{}\n".format(label or "task", "-" * 54), "accent")
        self._start(Task(fn=fn), label)

    def _start(self, task, label):
        self.console.btn_stop.setEnabled(True)
        self.status.emit("running {}".format(label or self.name), "info", 0.35)
        task.output.connect(self.console.append)
        task.done.connect(self._done)
        self.task = task
        task.start()

    def _done(self, code):
        self.console.append("\n[done] exit {}\n".format(code), "ok" if code == 0 else "err")
        self.console.btn_stop.setEnabled(False)
        self.status.emit("finished" if code == 0 else "exited with {}".format(code),
                         "ok" if code == 0 else "err", 1.0 if code == 0 else 0.0)

    def stop(self):
        if self.task:
            self.task.stop()
            self.console.append("\n[cancelled]\n", "warn")
            self.console.btn_stop.setEnabled(False)
            self.status.emit("cancelled", "warn", 0.0)

    def labelled(self, text, help_text=None):
        wrap = QWidget()
        lay = QVBoxLayout(wrap)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(3)
        head = QHBoxLayout()
        head.setSpacing(5)
        cap = QLabel(text)
        cap.setFont(QFont("Segoe UI", 8))
        cap.setStyleSheet("color: {}; background: transparent; border: none;".format(P.MUTED))
        head.addWidget(cap)
        head.addStretch()
        strip = None
        if help_text:
            btn = HelpButton()
            btn.set_accent(self.accent)
            strip = HelpStrip(help_text, self.accent)
            btn.clicked.connect(lambda: (btn.toggle(), strip.set_expanded(btn._on)))
            head.addWidget(btn)
        lay.addLayout(head)
        self.form.addWidget(wrap)
        return lay, strip

    def text_field(self, label, placeholder="", help_text=None, value=""):
        lay, strip = self.labelled(label, help_text)
        entry = HoverLine(value)
        entry.setPlaceholderText(placeholder)
        entry.setFixedHeight(34)
        entry.setFont(QFont("Segoe UI", 9))
        lay.addWidget(entry)
        if strip:
            lay.addWidget(strip)
        return entry

    def text_area(self, label, placeholder="", help_text=None, height=100):
        lay, strip = self.labelled(label, help_text)
        area = HoverText()
        area.setPlaceholderText(placeholder)
        area.setFixedHeight(height)
        area.setFont(QFont("Consolas", 9))
        lay.addWidget(area)
        if strip:
            lay.addWidget(strip)
        return area

    def number_field(self, label, low, high, value, help_text=None):
        lay, strip = self.labelled(label, help_text)
        box = HoverSpin()
        box.setRange(low, high)
        box.setValue(value)
        box.setFixedHeight(34)
        box.setFont(QFont("Segoe UI", 9))
        lay.addWidget(box)
        if strip:
            lay.addWidget(strip)
        return box

    def path_field(self, label, mode="file", filt="", help_text=None, value=""):
        lay, strip = self.labelled(label, help_text)
        row = QHBoxLayout()
        row.setSpacing(8)
        entry = HoverLine(value)
        entry.setFixedHeight(34)
        entry.setFont(QFont("Segoe UI", 9))
        btn = PillButton("BROWSE", height=28)
        row.addWidget(entry, 1)
        row.addWidget(btn)

        def choose():
            if mode == "dir":
                path = QFileDialog.getExistingDirectory(self, "Choose folder")
            elif mode == "save":
                path, _ = QFileDialog.getSaveFileName(self, "Choose destination", filter=filt)
            else:
                path, _ = QFileDialog.getOpenFileName(self, "Choose file", filter=filt)
            if path:
                entry.setText(path)

        btn.clicked.connect(choose)
        lay.addLayout(row)
        if strip:
            lay.addWidget(strip)
        return entry

    def combo_field(self, label, items, help_text=None):
        lay, strip = self.labelled(label, help_text)
        box = HoverCombo()
        box.addItems(items)
        box.setFixedHeight(34)
        box.setFont(QFont("Segoe UI", 9))
        lay.addWidget(box)
        if strip:
            lay.addWidget(strip)
        return box

    def checkbox(self, label, help_text=None):
        wrap = QWidget()
        lay = QVBoxLayout(wrap)
        lay.setContentsMargins(0, 0, 0, 0)
        lay.setSpacing(6)
        row = QHBoxLayout()
        row.setSpacing(7)
        cb = QCheckBox(label)
        cb.setFont(QFont("Segoe UI", 9))
        cb.setCursor(Qt.CursorShape.PointingHandCursor)
        cb.setStyleSheet(
            "QCheckBox {{ color: {}; spacing: 8px; background: transparent; border: none; }}"
            "QCheckBox:hover {{ color: {}; }}"
            "QCheckBox::indicator {{ width: 14px; height: 14px; border-radius: 5px;"
            " border: 1px solid {}; background-color: {}; }}"
            "QCheckBox::indicator:hover {{ border-color: {}; }}"
            "QCheckBox::indicator:checked {{ background-color: {}; border-color: {}; }}".format(
                P.MUTED, P.TEXT, P.BORDER_HI, P.BG, P.TEXT, P.WHITE, P.WHITE))
        row.addWidget(cb)
        strip = None
        if help_text:
            btn = HelpButton()
            btn.set_accent(self.accent)
            strip = HelpStrip(help_text, self.accent)
            btn.clicked.connect(lambda: (btn.toggle(), strip.set_expanded(btn._on)))
            row.addWidget(btn)
        row.addStretch()
        lay.addLayout(row)
        if help_text:
            lay.addWidget(strip)
        self._cb_wraps[cb] = wrap
        self.form.addWidget(wrap)
        return cb

    def check_row(self, *items):
        row = QHBoxLayout()
        row.setSpacing(22)
        for cb in items:
            wrap = self._cb_wraps[cb]
            self.form.removeWidget(wrap)
            row.addWidget(wrap, 0, Qt.AlignmentFlag.AlignTop)
        row.addStretch()
        holder = QWidget()
        holder.setLayout(row)
        self.form.addWidget(holder)

    def action(self, text, handler, height=40):
        btn = PillButton(text, accent=P.WHITE, filled=True, height=height)
        btn.setFont(QFont("Segoe UI", 9, QFont.Weight.Bold))
        btn.clicked.connect(handler)
        self.run_row.addWidget(btn, 1)
        return btn


def doc(title, steps, notes=""):
    body = "".join("<p><b>{}</b> {}</p>".format(i + 1, s) for i, s in enumerate(steps))
    tail = "<h3>Notes</h3><p>{}</p>".format(notes) if notes else ""
    return "<h2 style='color:#b9a8ff'>{}</h2>{}{}".format(title, body, tail)


def T(i, l, ph="", h=""):
    return {"k": "text", "id": i, "label": l, "ph": ph, "help": h}


def A(i, l, ph="", h="", ht=110):
    return {"k": "area", "id": i, "label": l, "ph": ph, "help": h, "height": ht}


def N(i, l, lo, hi, v, h=""):
    return {"k": "num", "id": i, "label": l, "lo": lo, "hi": hi, "val": v, "help": h}


def C(i, l, items, h=""):
    return {"k": "combo", "id": i, "label": l, "items": items, "help": h}


def Pth(i, l, mode="file", filt="", h=""):
    return {"k": "path", "id": i, "label": l, "mode": mode, "filt": filt, "help": h}


def K(i, l, h="", on=False):
    return {"k": "check", "id": i, "label": l, "help": h, "on": on}


class DynamicPage(ToolPage):
    def __init__(self, spec):
        self.spec = spec
        self.ACCENT = P.CAT.get(spec["cat"], P.WHITE)
        super().__init__(spec["id"], spec["name"], spec["glyph"], spec["tagline"],
                         spec["what"], spec["docs"])
        self.widgets = {}
        for group_name, fields in spec["groups"]:
            self.group(group_name)
            checks = []
            for field in fields:
                widget = self._field(field)
                if widget is not None:
                    self.widgets[field["id"]] = widget
                    if field["k"] == "check":
                        checks.append(widget)
            if len(checks) > 1:
                self.check_row(*checks)
        self.action(spec.get("action", "RUN"), self.start)

    def _field(self, field):
        kind = field["k"]
        if kind == "text":
            return self.text_field(field["label"], field["ph"], field["help"])
        if kind == "area":
            return self.text_area(field["label"], field["ph"], field["help"], field["height"])
        if kind == "num":
            return self.number_field(field["label"], field["lo"], field["hi"], field["val"],
                                     field["help"])
        if kind == "combo":
            return self.combo_field(field["label"], field["items"], field["help"])
        if kind == "path":
            return self.path_field(field["label"], field["mode"], field["filt"], field["help"])
        if kind == "check":
            cb = self.checkbox(field["label"], field["help"])
            cb.setChecked(field["on"])
            return cb
        return None

    def check_env(self):
        binary = self.spec.get("binary")
        if not binary:
            self.mark_ready(self.spec.get("env", "built in"))
            return
        found = resolve_binary(binary)
        if found:
            self.mark_ready(found)
        else:
            self.mark_missing("{} not found".format(binary), bool(self.spec.get("install")))

    def _values(self):
        values = {}
        for fid, widget in self.widgets.items():
            if isinstance(widget, QCheckBox):
                values[fid] = widget.isChecked()
            elif isinstance(widget, QSpinBox):
                values[fid] = widget.value()
            elif isinstance(widget, QComboBox):
                values[fid] = widget.currentText()
            elif isinstance(widget, QPlainTextEdit):
                values[fid] = widget.toPlainText()
            else:
                values[fid] = widget.text().strip()
        return values

    def start(self):
        values = self._values()
        check = self.spec.get("validate")
        if check:
            message = check(values)
            if message:
                self.console.append("[error] {}\n".format(message), "err")
                return
        if self.spec.get("fn"):
            fn = self.spec["fn"]
            self.run_python(lambda emit, stop: fn(values, emit, stop), self.spec["name"])
            return
        command = self.spec["build"](values)
        if command:
            self.run(command, self.spec["name"])


def exe(name):
    return resolve_binary(name) or name


SPECS = []


def spec(**kw):
    SPECS.append(kw)


spec(id="gallerydl", cat="MEDIA", glyph="▤", name="gallery-dl", action="DOWNLOAD",
     tagline="download image galleries",
     binary="gallery-dl", install=True,
     what="Gallery downloader for image sites and posts. Point it at the set URL and pick a "
          "folder: every file is saved under its original name.",
     docs=doc("gallery-dl", ["Paste the gallery or post URL.",
                             "Pick the output folder.",
                             "Press DOWNLOAD."],
              "Sites that require a session need <code>--cookies-from-browser firefox</code>."),
     groups=[("source", [T("url", "Gallery URL", "https://site.com/post/123",
                           "Link to the full set.")]),
             ("output", [Pth("out", "Folder", "dir", "", "Where files are saved."),
                         C("mode", "Mode", ["Everything (images and video)", "Images only"],
                           "Images only skips clips.")])],
     validate=lambda v: "" if v["url"] else "the URL is empty",
     build=lambda v: [exe("gallery-dl"), "-D", v["out"] or ".",
                      "-f" if "Images only" in v["mode"] else "-G", v["url"]])

spec(id="magick", cat="MEDIA", glyph="◫", name="ImageMagick", action="PROCESS",
     tagline="convert and resize images",
     binary="magick", install=True,
     what="ImageMagick wrapper: resize, convert, strip metadata or build thumbnails in one step. "
          "It works on a copy, the original is untouched.",
     docs=doc("ImageMagick", ["Pick the input image.",
                              "Select the operation.",
                              "Type the output path and press PROCESS."],
              "Portable ImageMagick comes from imagemagick.org; the binary is called "
              "<code>magick</code>."),
     groups=[("input", [Pth("src", "Image", "file", "Images (*.png *.jpg *.webp *.gif *.tif)",
                            "File to transform.")]),
             ("operation", [C("op", "Operation",
                              ["Resize 50%", "Thumbnail 320px", "Convert to WebP",
                               "Convert to PNG", "Grayscale", "Strip metadata"],
                              "Each option uses a different operator.")]),
             ("output", [Pth("dst", "Output", "save", "", "Path with the new extension.")])],
     validate=lambda v: "" if v["src"] and v["dst"] else "input and output are both required",
     build=lambda v: [exe("magick"), v["src"]] + {
         "Resize 50%": ["-resize", "50%"],
         "Thumbnail 320px": ["-thumbnail", "320x320"],
         "Convert to WebP": ["-quality", "88"],
         "Convert to PNG": [],
         "Grayscale": ["-colorspace", "Gray"],
         "Strip metadata": ["-strip"],
     }[v["op"]] + [v["dst"]])

spec(id="mediainfo", cat="MEDIA", glyph="◱", name="MediaInfo", action="INSPECT",
     tagline="read containers and codecs",
     binary="mediainfo", install=True,
     what="Shows codecs, bitrate, resolution, tracks and real duration of a file. Useful to know "
          "what is inside before converting it.",
     docs=doc("MediaInfo", ["Pick the file.", "Press INSPECT."],
              "Download at mediaarea.net."),
     groups=[("file", [Pth("src", "File", "file", "Video (*.mp4 *.mkv *.avi *.webm *.mov)",
                           "Container to analyse.")])],
     validate=lambda v: "" if v["src"] else "pick a file",
     build=lambda v: [exe("mediainfo"), v["src"]])

spec(id="exiftool", cat="MEDIA", glyph="⌾", name="ExifTool", action="RUN",
     tagline="metadata of photos and documents",
     binary="exiftool", install=True,
     what="Reads all metadata from a file or wipes it. Removing GPS before publishing a photo is "
          "the usual job.",
     docs=doc("ExifTool", ["Pick the file.", "Choose read, clear GPS or clear everything.",
                           "Press RUN."],
              "It works in place: use <code>-o</code> to keep the original."),
     groups=[("file", [Pth("src", "File", "file", "", "Photo or document.")]),
             ("mode", [C("mode", "Mode", ["Read all", "Clear GPS", "Clear all"],
                         "Read does not modify anything.")])],
     validate=lambda v: "" if v["src"] else "pick a file",
     build=lambda v: [exe("exiftool")] + {
         "Read all": ["-a", "-G1"],
         "Clear GPS": ["-gps:all=", "-overwrite_original"],
         "Clear all": ["-all=", "-overwrite_original"],
     }[v["mode"]] + [v["src"]])

spec(id="sox", cat="MEDIA", glyph="♪", name="SoX", action="PROCESS",
     tagline="process audio from the command line",
     binary="sox", install=True,
     what="Normalises volume, trims silence or changes the format of an audio file. It is the "
          "audio swiss army knife for the console.",
     docs=doc("SoX", ["Pick the audio.", "Choose the effect.", "Type the output and press PROCESS."],
              "On Windows the binary ships in the official zip from sox.sourceforge.net."),
     groups=[("input", [Pth("src", "Audio", "file", "Audio (*.wav *.mp3 *.flac *.ogg *.m4a)",
                            "Source file.")]),
             ("effect", [C("op", "Effect", ["Normalise", "Trim silence", "Mono 16 kHz",
                                            "Convert to WAV"], "Changes the processing.")]),
             ("output", [Pth("dst", "Output", "save", "", "Destination path.")])],
     validate=lambda v: "" if v["src"] and v["dst"] else "input and output are both required",
     build=lambda v: [exe("sox"), v["src"], v["dst"]] + {
         "Normalise": ["norm"],
         "Trim silence": ["silence", "-l", "1", "0.1", "1%", "-1", "0.1", "1%"],
         "Mono 16 kHz": ["channels", "1", "rate", "16000"],
         "Convert to WAV": [],
     }[v["op"]])

spec(id="mkvmerge", cat="MEDIA", glyph="◧", name="MKVToolNix", action="MERGE",
     tagline="remux and strip tracks",
     binary="mkvmerge", install=True,
     what="Repackages a video into MKV without re-encoding, or drops unwanted subtitle and audio "
          "tracks. It is instant because the video is untouched.",
     docs=doc("MKVToolNix", ["Pick the file.", "Choose remux or strip subtitles.",
                             "Type the output and press MERGE."],
              "Install MKVToolNix from mkvtoolnix.download."),
     groups=[("input", [Pth("src", "File", "file", "Video (*.mp4 *.mkv *.avi *.mov)",
                            "Source.")]),
             ("operation", [C("op", "Operation", ["Remux to MKV", "Strip subtitles"],
                              "Remuxing does not re-encode.")]),
             ("output", [Pth("dst", "Output", "save", "", "Destination .mkv file.")])],
     validate=lambda v: "" if v["src"] and v["dst"] else "input and output are both required",
     build=lambda v: [exe("mkvmerge"), "-o", v["dst"]] +
                     (["--no-subtitles"] if "Strip" in v["op"] else []) + [v["src"]])

spec(id="sevenzip", cat="MEDIA", glyph="◨", name="7-Zip", action="RUN",
     tagline="list, test and extract archives",
     binary="7z", install=False,
     what="Opens archives other programs refuse: lists the contents, verifies integrity or "
          "extracts to a specific folder.",
     docs=doc("7-Zip", ["Pick the archive.", "Choose list, test or extract.",
                        "Set the folder if extracting and press RUN."],
              "Download from 7-zip.org. The console binary is <code>7z.exe</code>."),
     groups=[("file", [Pth("src", "Archive", "file", "Archives (*.zip *.7z *.rar *.tar *.gz)",
                           "File to open.")]),
             ("operation", [C("op", "Operation", ["List", "Test integrity", "Extract"],
                              "Extract needs a folder.")]),
             ("destination", [Pth("out", "Folder", "dir", "", "Only for extract.")])],
     validate=lambda v: "" if v["src"] else "pick a file",
     build=lambda v: [exe("7z")] + {
         "List": ["l"],
         "Test integrity": ["t"],
         "Extract": ["x", "-o" + (v["out"] or "."), "-y"],
     }[v["op"]] + [v["src"]])

spec(id="asciiart", cat="MEDIA", glyph="▚", name="Image to ASCII", action="RENDER",
     tagline="turn images into text",
     what="Converts an image into ASCII art by mapping brightness to characters. Everything in "
          "memory, no external dependencies.",
     docs=doc("Image to ASCII", ["Pick the image.", "Adjust the width.", "Press RENDER."],
              "Needs Pillow: it installs from the button if missing."),
     env="needs Pillow",
     groups=[("image", [Pth("src", "Image", "file", "Images (*.png *.jpg *.webp)",
                            "Source.")]),
             ("tuning", [N("width", "Width in characters", 20, 200, 90, "Wider means more detail."),
                         C("set", "Character set", ["Classic", "Blocks", "Simple"],
                           "Changes the visual density.")])],
     validate=lambda v: "" if v["src"] else "pick an image",
     fn=lambda v, emit, stop: _ascii_art(v, emit, stop))


def _ascii_art(v, emit, stop):
    try:
        from PIL import Image
    except Exception:
        emit("missing Pillow: pip install pillow\n", "err")
        return
    sets = {"Classic": "@%#*+=-:. ", "Blocks": "█▓▒░ ", "Simple": "#+-. "}
    chars = sets.get(v["set"], sets["Classic"])
    try:
        image = Image.open(v["src"]).convert("L")
    except Exception as exc:
        emit("could not open: {}\n".format(exc), "err")
        return
    width = v["width"]
    ratio = image.height / max(1, image.width)
    image = image.resize((width, max(1, int(width * ratio * 0.5))))
    for y in range(image.height):
        if stop():
            return
        row = "".join(chars[min(len(chars) - 1,
                                image.getpixel((x, y)) * len(chars) // 256)]
                      for x in range(image.width))
        emit(row + "\n", "out")
    emit("\n{}x{} characters\n".format(image.width, image.height), "dim")


spec(id="ping", cat="NETWORK", glyph="◉", name="Ping", action="PING",
     tagline="measure reach and latency",
     binary="ping", install=False,
     what="Sends ICMP to the host and measures the reply. It tells you whether the box is alive "
          "and how long the round trip takes.",
     docs=doc("Ping", ["Type the host.", "Choose how many packets.", "Press PING."],
              "Some servers block ICMP even while active."),
     groups=[("target", [T("host", "Host", "8.8.8.8", "IP or domain.")]),
             ("tuning", [N("count", "Packets", 1, 50, 4, "Number of sends.")])],
     validate=lambda v: "" if v["host"] else "the host is empty",
     build=lambda v: [exe("ping")] + (["-n"] if os.name == "nt" else ["-c"]) +
                     [str(v["count"]), v["host"]])

spec(id="traceroute", cat="NETWORK", glyph="⇢", name="Traceroute", action="TRACE",
     tagline="see the path to the host",
     binary="tracert", install=False,
     what="Lists the routers the traffic passes through on the way to the target. Hops with extra "
          "latency usually mean congestion.",
     docs=doc("Traceroute", ["Type the host.", "Press TRACE."],
              "On Windows it is <code>tracert</code>, on Unix <code>traceroute</code>."),
     groups=[("target", [T("host", "Host", "example.com", "Trace destination.")])],
     validate=lambda v: "" if v["host"] else "the host is empty",
     build=lambda v: ([exe("tracert")] if os.name == "nt" else [exe("traceroute")]) + [v["host"]])

spec(id="whois", cat="NETWORK", glyph="◷", name="Whois", action="QUERY",
     tagline="domain registration data",
     what="Queries the TLD whois server and shows registrar, dates and status. It works over a "
          "socket against port 43.",
     docs=doc("Whois", ["Type the domain without a scheme.", "Press QUERY."],
              "Many registrars hide data under GDPR; the dates stay visible."),
     groups=[("domain", [T("domain", "Domain", "example.com", "Domain only.")])],
     validate=lambda v: "" if v["domain"] else "the domain is empty",
     fn=lambda v, emit, stop: _whois(v, emit, stop))


def _whois(v, emit, stop):
    domain = v["domain"].lower().strip(".")
    tld = domain.rsplit(".", 1)[-1]
    server = "whois.iana.org"
    try:
        with socket.create_connection((server, 43), timeout=15) as sock:
            sock.sendall((domain + "\r\n").encode())
            chunks = []
            while True:
                block = sock.recv(4096)
                if not block:
                    break
                chunks.append(block)
        first = b"".join(chunks).decode("utf-8", "replace")
    except Exception as exc:
        emit("query failed: {}\n".format(exc), "err")
        return
    refer = re.search(r"refer:\s*(\S+)", first)
    if refer:
        server = refer.group(1)
        emit("server {} for .{}\n".format(server, tld), "dim")
        try:
            with socket.create_connection((server, 43), timeout=15) as sock:
                sock.sendall((domain + "\r\n").encode())
                chunks = []
                while True:
                    block = sock.recv(4096)
                    if not block:
                        break
                    chunks.append(block)
            first = b"".join(chunks).decode("utf-8", "replace")
        except Exception as exc:
            emit("TLD server failed: {}\n".format(exc), "err")
    for line in first.splitlines():
        if not line.strip() or line.startswith("%") or line.startswith("#"):
            continue
        level = "ok" if re.match(r"(registrar|creation|expiry|updated)", line, re.I) else "out"
        emit(line.rstrip() + "\n", level)

spec(id="netcat", cat="NETWORK", glyph="⋈", name="Netcat", action="CONNECT",
     tagline="connect and talk to a port",
     what="Opens a raw TCP connection, reads the banner or sends a payload. Implemented in Python "
          "so it needs no binary.",
     docs=doc("Netcat", ["Type host and port.", "Choose read banner or send payload.",
                         "Press CONNECT."],
              "An empty banner does not mean the port is closed, only that the service waits "
              "first."),
     groups=[("target", [T("host", "Host", "example.com", "IP or domain."),
                         N("port", "Port", 1, 65535, 80, "TCP port.")]),
             ("payload", [C("mode", "Mode", ["Read banner", "Send payload"],
                            "Sending requires text."),
                          A("payload", "Payload", "GET / HTTP/1.0\r\n\r\n", "Text to send.", 90)])],
     validate=lambda v: "" if v["host"] else "the host is empty",
     fn=lambda v, emit, stop: _netcat(v, emit, stop))


def _netcat(v, emit, stop):
    try:
        sock = socket.create_connection((v["host"], v["port"]), timeout=10)
    except Exception as exc:
        emit("connection failed: {}\n".format(exc), "err")
        return
    emit("connected to {}:{}\n".format(v["host"], v["port"]), "ok")
    try:
        if v["mode"] == "Send payload":
            sock.sendall(v["payload"].encode())
            emit("payload sent ({} bytes)\n".format(len(v["payload"])), "dim")
        sock.settimeout(4)
        total = 0
        while not stop():
            try:
                block = sock.recv(4096)
            except socket.timeout:
                break
            if not block:
                break
            total += len(block)
            emit(block.decode("utf-8", "replace"), "out")
        emit("\n{} bytes received\n".format(total), "accent")
    finally:
        sock.close()

spec(id="tcpdump", cat="NETWORK", glyph="≋", name="Packet Capture", action="CAPTURE",
     tagline="capture traffic with tcpdump",
     binary="tcpdump", install=False,
     what="Captures packets on an interface with a BPF filter. Needs administrator privileges.",
     docs=doc("Packet Capture", ["Pick an interface or leave it empty.", "Type a BPF filter.",
                                 "Set the packet count and press CAPTURE."],
              "On Windows use Npcap. Example filters: <code>port 53</code>, "
              "<code>host 1.1.1.1</code>."),
     groups=[("interface", [T("iface", "Interface", "eth0 or \\Device\\NPF_...", "Empty = automatic.")]),
             ("filter", [T("filter", "BPF filter", "port 443", "tcpdump syntax."),
                         N("count", "Packets", 1, 2000, 50, "Stops the capture.")])],
     build=lambda v: [exe("tcpdump"), "-n", "-c", str(v["count"])] +
                     (["-i", v["iface"]] if v["iface"] else []) +
                     ([v["filter"]] if v["filter"] else []))

spec(id="iperf3", cat="NETWORK", glyph="⇅", name="iperf3", action="MEASURE",
     tagline="measure real bandwidth",
     binary="iperf3", install=False,
     what="Measures TCP throughput against an iperf3 server. It is the honest way to know what "
          "the network delivers.",
     docs=doc("iperf3", ["Start a server with <code>iperf3 -s</code> on the other machine.",
                         "Type its IP and choose upload or download.", "Press MEASURE."],
              "Download at software.es.net/iperf."),
     groups=[("server", [T("host", "Server", "192.168.1.50", "IP of the iperf3 server."),
                         C("dir", "Direction", ["Upload (-R no)", "Download (-R)"],
                           "Download reverses the direction.")])],
     validate=lambda v: "" if v["host"] else "the server is empty",
     build=lambda v: [exe("iperf3"), "-c", v["host"]] + (["-R"] if "Download" in v["dir"] else []))

spec(id="macvendor", cat="NETWORK", glyph="⌗", name="MAC Vendor", action="LOOKUP",
     tagline="vendor by OUI prefix",
     what="Looks the vendor of a MAC up in the public database. Handy to identify devices on your "
          "own network.",
     docs=doc("MAC Vendor", ["Type the MAC.", "Press LOOKUP."],
              "Works with 6 or 8 character prefixes."),
     groups=[("mac", [T("mac", "MAC address", "00:1A:2B:3C:4D:5E", "With or without separators.")])],
     validate=lambda v: "" if v["mac"] else "the MAC is empty",
     fn=lambda v, emit, stop: _macvendor(v, emit, stop))


def _macvendor(v, emit, stop):
    mac = re.sub(r"[^0-9a-fA-F]", "", v["mac"]).lower()
    if len(mac) < 6:
        emit("MAC too short\n", "err")
        return
    prefix = mac[:6]
    emit("OUI  {}  {}\n".format(prefix.upper(), "local" if int(prefix[1], 16) & 2 else "global"),
         "dim")
    url = "https://api.macvendors.com/" + ":".join(prefix[i:i + 2] for i in range(0, 6, 2))
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=ua()), timeout=15) as res:
            emit("vendor  {}\n".format(res.read().decode("utf-8", "replace").strip()), "ok")
    except urllib.error.HTTPError as exc:
        emit("no record for that prefix (HTTP {})\n".format(exc.code), "warn")
    except Exception as exc:
        emit("query failed: {}\n".format(exc), "err")

spec(id="ipv6", cat="NETWORK", glyph="⊞", name="IPv6 Tool", action="ANALYZE",
     tagline="expand and classify IPv6",
     what="Normalises an IPv6 address, expands it, detects its type and computes the network. "
          "Sends no traffic.",
     docs=doc("IPv6 Tool", ["Type the address.", "Press ANALYZE."],
              "Use valid <code>::</code> compression."),
     groups=[("address", [T("addr", "IPv6", "2001:db8::1", "Address to study.")])],
     validate=lambda v: "" if v["addr"] else "the address is empty",
     fn=lambda v, emit, stop: _ipv6(v, emit, stop))


def _ipv6(v, emit, stop):
    try:
        addr = ipaddress.ip_address(v["addr"])
    except ValueError as exc:
        emit("{}\n".format(exc), "err")
        return
    emit("expanded   {}\n".format(addr.exploded), "out")
    emit("compressed {}\n".format(addr.compressed), "out")
    kinds = [name for name in ("is_private", "is_loopback", "is_link_local", "is_multicast",
                               "is_reserved", "is_global") if getattr(addr, name, False)]
    emit("type       {}\n".format(", ".join(kinds) or "unclassified"),
         "warn" if addr.is_private else "ok")
    emit("reverse    {}\n".format(addr.reverse_pointer), "dim")
    if addr.version == 6 and addr.prefixlen if hasattr(addr, "prefixlen") else False:
        pass
    net = ipaddress.ip_network("{}/64".format(addr), strict=False)
    emit("network /64 {}\n".format(net.network_address), "dim")

spec(id="banner", cat="NETWORK", glyph="⌁", name="Banner Grab", action="GRAB",
     tagline="read service banners",
     what="Connects and reads the first bytes a service announces. Identifies versions fast "
          "without external tools.",
     docs=doc("Banner Grab", ["Type host and port.", "Adjust the wait time.",
                              "Press GRAB."],
              "Typical ports: 21, 22, 25, 80, 3306."),
     groups=[("target", [T("host", "Host", "example.com", "IP or domain."),
                         N("port", "Port", 1, 65535, 22, "Port to test."),
                         N("wait", "Wait ms", 200, 5000, 1200, "Read timeout.")])],
     validate=lambda v: "" if v["host"] else "the host is empty",
     fn=lambda v, emit, stop: _banner(v, emit, stop))


def _banner(v, emit, stop):
    try:
        sock = socket.create_connection((v["host"], v["port"]), timeout=v["wait"] / 1000.0)
    except Exception as exc:
        emit("no answer: {}\n".format(exc), "err")
        return
    try:
        sock.settimeout(v["wait"] / 1000.0)
        try:
            block = sock.recv(1024)
        except socket.timeout:
            block = b""
        if not block:
            emit("port open, empty banner\n", "warn")
        else:
            emit(block.decode("utf-8", "replace").strip() + "\n", "ok")
    finally:
        sock.close()

DNS_TYPES = ["A", "AAAA", "CNAME", "MX", "NS", "TXT", "SOA", "SRV", "CAA", "DS",
             "DNSKEY", "PTR", "NAPTR", "TLSA", "SSHFP", "HTTPS", "SVCB", "ANY"]

DNS_RESOLVERS = ["Cloudflare DoH", "Google DoH", "System resolver"]

DNS_CODES = {1: "A", 2: "NS", 5: "CNAME", 6: "SOA", 12: "PTR", 15: "MX", 16: "TXT",
             28: "AAAA", 33: "SRV", 35: "NAPTR", 43: "DS", 44: "SSHFP", 46: "RRSIG",
             48: "DNSKEY", 52: "TLSA", 64: "SVCB", 65: "HTTPS", 257: "CAA", 255: "ANY"}

DNS_STATUS = {0: "NOERROR", 1: "FORMERR", 2: "SERVFAIL", 3: "NXDOMAIN",
              4: "NOTIMP", 5: "REFUSED"}


def _dns_label(code):
    return DNS_CODES.get(code, str(code))


def _dns_print(data, emit):
    total = 0
    for section, label in (("Answer", "answer"), ("Authority", "authority"),
                           ("Additional", "additional")):
        rows = data.get(section, [])
        if not rows:
            continue
        emit("\n{}\n".format(label), "dim")
        for row in rows:
            kind = row.get("type")
            level = "warn" if kind == 5 else "out"
            emit("  {:<6} ttl {:<6} {}\n".format(_dns_label(kind), row.get("TTL", "-"),
                                                 row.get("data", "")), level)
            total += 1
    if not total:
        emit("no records\n", "warn")


def _dns_doh(name, rtype, resolver, emit):
    base = ("https://cloudflare-dns.com/dns-query" if resolver == "Cloudflare DoH"
            else "https://dns.google/resolve")
    query = "{}?name={}&type={}".format(base, urllib.parse.quote(name), rtype)
    req = urllib.request.Request(query, headers={"Accept": "application/dns-json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            data = json.loads(res.read().decode("utf-8", "replace"))
    except Exception as exc:
        emit("query failed: {}\n".format(exc), "err")
        return
    status = data.get("Status", 0)
    emit("status {}\n".format(DNS_STATUS.get(status, status)),
         "ok" if status == 0 else "err")
    _dns_print(data, emit)


def _dns_system(name, rtype, emit):
    if os.name == "nt":
        args = ["nslookup", "-type={}".format(rtype), name]
    else:
        args = ["dig", "+noall", "+answer", "+authority", rtype, name]
    try:
        res = subprocess.run(args, capture_output=True, text=True, timeout=25)
    except Exception as exc:
        emit("resolver failed: {}\n".format(exc), "err")
        return
    body = ((res.stdout or "") + (res.stderr or "")).strip()
    if not body:
        emit("empty answer\n", "warn")
        return
    for line in body.splitlines():
        line = line.strip()
        if not line or line.startswith(";"):
            continue
        emit("{}\n".format(line), "out")

spec(id="doh", cat="NETWORK", glyph="⊙", name="DNS over HTTPS", action="RESOLVE",
     tagline="resolve over DoH",
     what="Resolves records over HTTPS against Cloudflare, useful when local DNS lies or is "
          "blocked.",
     docs=doc("DNS over HTTPS", ["Type the domain.", "Choose the type.", "Press RESOLVE."],
              "Returns the raw JSON answers."),
     groups=[("query", [T("domain", "Domain", "example.com", "No scheme."),
                        C("type", "Type", DNS_TYPES, "ANY dumps everything.")])],
     validate=lambda v: "" if v["domain"] else "the domain is empty",
     fn=lambda v, emit, stop: _doh(v, emit, stop))


def _doh(v, emit, stop):
    query = "https://cloudflare-dns.com/dns-query?name={}&type={}".format(
        urllib.parse.quote(v["domain"]), v["type"])
    req = urllib.request.Request(query, headers={"Accept": "application/dns-json"})
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            data = json.loads(res.read().decode("utf-8", "replace"))
    except Exception as exc:
        emit("failed: {}\n".format(exc), "err")
        return
    emit("DNS status {}\n".format(data.get("Status")), "dim")
    for answer in data.get("Answer", []):
        emit("{}  {}  {}\n".format(answer.get("type"), answer.get("TTL"),
                                   answer.get("data")), "ok")
    if not data.get("Answer"):
        emit("no answers\n", "warn")

spec(id="dnssec", cat="NETWORK", glyph="⛨", name="DNSSEC Check", action="CHECK",
     tagline="verify the DS chain",
     what="Looks for DS records of the domain over DoH. Without DS, the zone is not signed with "
          "DNSSEC.",
     docs=doc("DNSSEC Check", ["Type the domain.", "Press CHECK."],
              "A present DS does not guarantee validation at the client resolver."),
     groups=[("domain", [T("domain", "Domain", "example.com", "Domain to review.")])],
     validate=lambda v: "" if v["domain"] else "the domain is empty",
     fn=lambda v, emit, stop: _dnssec(v, emit, stop))


def _dnssec(v, emit, stop):
    for rtype in ("DS", "DNSKEY", "RRSIG"):
        query = "https://cloudflare-dns.com/dns-query?name={}&type={}".format(
            urllib.parse.quote(v["domain"]), rtype)
        req = urllib.request.Request(query, headers={"Accept": "application/dns-json"})
        try:
            with urllib.request.urlopen(req, timeout=20) as res:
                data = json.loads(res.read().decode("utf-8", "replace"))
        except Exception as exc:
            emit("{} failed: {}\n".format(rtype, exc), "err")
            continue
        answers = data.get("Answer", [])
        emit("{}  {} record(s)\n".format(rtype, len(answers)),
             "ok" if answers else "warn")
        for answer in answers[:6]:
            emit("  {}\n".format(answer.get("data")), "dim")

spec(id="rdns", cat="NETWORK", glyph="↺", name="Reverse DNS", action="RESOLVE",
     tagline="PTR for an IP",
     what="Asks for the name associated with an IP. Many hosting ranges publish no PTR.",
     docs=doc("Reverse DNS", ["Type the IP.", "Press RESOLVE."],
              "No PTR means nothing bad, only that none was published."),
     groups=[("ip", [T("ip", "IP address", "1.1.1.1", "IPv4 or IPv6.")])],
     validate=lambda v: "" if v["ip"] else "the IP is empty",
     fn=lambda v, emit, stop: _rdns(v, emit, stop))


def _rdns(v, emit, stop):
    try:
        name, aliases, _ = socket.gethostbyaddr(v["ip"])
        emit("PTR  {}\n".format(name), "ok")
        for alias in aliases:
            emit("alias  {}\n".format(alias), "dim")
    except Exception as exc:
        emit("no PTR: {}\n".format(exc), "warn")


spec(id="securitytxt", cat="RECON", glyph="✉", name="security.txt", action="FETCH",
     tagline="declared security contact",
     what="Looks for security.txt on the standard paths and shows contact, expiry and policy. It "
          "is the formal reporting channel.",
     docs=doc("security.txt", ["Type the domain.", "Press FETCH."],
              "Correct path: <code>/.well-known/security.txt</code>."),
     groups=[("domain", [T("url", "Base URL", "https://example.com", "Include the scheme.")])],
     validate=lambda v: "" if v["url"] else "the URL is empty",
     fn=lambda v, emit, stop: _securitytxt(v, emit, stop))


def _securitytxt(v, emit, stop):
    base = normalise(v["url"]).rstrip("/")
    for path in ("/.well-known/security.txt", "/security.txt"):
        emit("\n{}\n".format(path), "dim")
        try:
            with urllib.request.urlopen(urllib.request.Request(base + path, headers=ua()),
                                        timeout=15) as res:
                body = res.read(60000).decode("utf-8", "replace")
        except urllib.error.HTTPError as exc:
            emit("HTTP {}\n".format(exc.code), "warn")
            continue
        except Exception as exc:
            emit("failed: {}\n".format(exc), "err")
            continue
        for line in body.splitlines():
            if line.strip():
                emit("  {}\n".format(line.strip()),
                     "ok" if line.lower().startswith(("contact", "expires")) else "out")
        return
    emit("\nno security.txt\n", "warn")

spec(id="wellknown", cat="RECON", glyph="⌘", name=".well-known Probe", action="PROBE",
     tagline="published standard paths",
     what="Tests the usual .well-known paths and reports which ones exist. Many reveal app "
          "configuration.",
     docs=doc(".well-known Probe", ["Type the domain.", "Press PROBE."],
              "Only sends HEAD, no bodies are downloaded."),
     groups=[("domain", [T("url", "Base URL", "https://example.com", "Include the scheme.")])],
     validate=lambda v: "" if v["url"] else "the URL is empty",
     fn=lambda v, emit, stop: _wellknown(v, emit, stop))

WELLKNOWN = ["security.txt", "change-password", "openid-configuration", "apple-app-site-association",
             "assetlinks.json", "mta-sts.txt", "nodeinfo", "host-meta", "webfinger"]


def _wellknown(v, emit, stop):
    base = normalise(v["url"]).rstrip("/")
    for name in WELLKNOWN:
        if stop():
            return
        url = "{}/.well-known/{}".format(base, name)
        req = urllib.request.Request(url, method="HEAD", headers=ua())
        try:
            with urllib.request.urlopen(req, timeout=12) as res:
                emit("{:<4} {}\n".format(res.status, name), "ok")
        except urllib.error.HTTPError as exc:
            emit("{:<4} {}\n".format(exc.code, name), "dim" if exc.code == 404 else "warn")
        except Exception:
            emit("----  {}\n".format(name), "dim")

spec(id="waf", cat="RECON", glyph="⛒", name="WAF Detect", action="DETECT",
     tagline="detect a web application firewall",
     binary="wafw00f", install=True,
     what="Fires signatures at the URL to identify the WAF in front. Change your strategy if one "
          "shows up.",
     docs=doc("WAF Detect", ["Type the URL.", "Press DETECT."],
              "An undetected WAF does not mean there is none."),
     groups=[("target", [T("url", "URL", "https://example.com", "Include the scheme.")])],
     validate=lambda v: "" if v["url"] else "the URL is empty",
     build=lambda v: [exe("wafw00f"), "-a", normalise(v["url"])])

spec(id="whatweb", cat="RECON", glyph="❖", name="WhatWeb", action="FINGERPRINT",
     tagline="web technology fingerprint",
     binary="whatweb", install=False,
     what="Identifies CMS, servers and libraries by active signatures. Noisier than Site DNA.",
     docs=doc("WhatWeb", ["Type the URL.", "Choose aggression.", "Press FINGERPRINT."],
              "It is Ruby: install with gem, not pip."),
     groups=[("target", [T("url", "URL", "https://example.com", "Include the scheme."),
                         C("level", "Aggression", ["Stealthy (-a 1)", "Normal (-a 3)",
                                                   "Aggressive (-a 4)"],
                           "More level, more requests.")])],
     validate=lambda v: "" if v["url"] else "the URL is empty",
     build=lambda v: [exe("whatweb"), v["level"].split("(")[1].rstrip(")"),
                      normalise(v["url"])])

spec(id="httpx", cat="RECON", glyph="⌁", name="httpx", action="PROBE",
     tagline="probe hosts in bulk",
     binary="httpx", install=True,
     what="Tests status, title, TLS and technologies on many hosts at once. Built for large "
          "subdomain lists.",
     docs=doc("httpx", ["Paste one host per line.", "Pick the columns.", "Press PROBE."],
              "Without <code>-silent</code> the output is noisier than it needs to be."),
     groups=[("hosts", [A("hosts", "Hosts", "example.com\nsub.example.com", "One per line.", 130)]),
             ("options", [K("title", "Title", "Includes the HTML title.", True),
                          K("tech", "Technologies", "Includes detected fingerprints.", True),
                          K("status", "Status code", "Includes the HTTP status.", True)])],
     validate=lambda v: "" if v["hosts"].strip() else "there are no hosts",
     build=lambda v: [exe("httpx"), "-silent"] +
                     (["-title"] if v["title"] else []) +
                     (["-tech-detect"] if v["tech"] else []) +
                     (["-status-code"] if v["status"] else []) +
                     ["-l", "-"])

spec(id="subfinder", cat="RECON", glyph="◍", name="Subfinder", action="ENUMERATE",
     tagline="subdomains from passive sources",
     binary="subfinder", install=True,
     what="Collects subdomains from dozens of passive sources without touching the target. "
          "Complements the certificate search.",
     docs=doc("Subfinder", ["Type the domain.", "Press ENUMERATE."],
              "With <code>-all</code> it also uses sources that need a key."),
     groups=[("domain", [T("domain", "Domain", "example.com", "No wildcard.")])],
     validate=lambda v: "" if v["domain"] else "the domain is empty",
     build=lambda v: [exe("subfinder"), "-d", v["domain"], "-silent"])

spec(id="nuclei", cat="RECON", glyph="✳", name="Nuclei", action="SCAN",
     tagline="vulnerability templates",
     binary="nuclei", install=True,
     what="Runs community templates against the URL: CVEs, exposed panels, loose configs. Adjust "
          "severity so you do not drown.",
     docs=doc("Nuclei", ["Type the URL.", "Choose minimum severity.", "Press SCAN."],
              "First run: <code>nuclei -update-templates</code>."),
     groups=[("target", [T("url", "URL", "https://example.com", "Include the scheme."),
                         C("sev", "Severity", ["critical,high", "critical,high,medium",
                                               "critical,high,medium,low"],
                           "Comma separated list.")])],
     validate=lambda v: "" if v["url"] else "the URL is empty",
     build=lambda v: [exe("nuclei"), "-u", normalise(v["url"]), "-severity", v["sev"], "-silent"])

spec(id="trufflehog", cat="RECON", glyph="⌾", name="TruffleHog", action="SCAN",
     tagline="hunt secrets in a repo",
     binary="trufflehog", install=True,
     what="Scans git history or a file tree for keys and tokens, verifying them when possible.",
     docs=doc("TruffleHog", ["Pick a folder or git repo.", "Press SCAN."],
              "Without verification there are many false positives: always review."),
     groups=[("target", [Pth("path", "Folder or repo", "dir", "", "Local path."),
                         C("mode", "Mode", ["Files", "Git"], "Git reads the history.")])],
     validate=lambda v: "" if v["path"] else "pick a path",
     build=lambda v: [exe("trufflehog")] +
                     (["git", "file://" + v["path"], "--no-update"] if v["mode"] == "Git"
                      else ["filesystem", v["path"], "--no-update"]))

spec(id="mailauth", cat="RECON", glyph="✉", name="Mail Auth", action="CHECK",
     tagline="SPF, DMARC and DKIM",
     what="Reads the domain SPF and DMARC TXT records and evaluates the basics. Flags domains "
          "with no spoofing protection.",
     docs=doc("Mail Auth", ["Type the domain.", "Press CHECK."],
              "SPF with <code>~all</code> is soft; <code>-all</code> is hard."),
     groups=[("domain", [T("domain", "Domain", "example.com", "Domain to review.")])],
     validate=lambda v: "" if v["domain"] else "the domain is empty",
     fn=lambda v, emit, stop: _mailauth(v, emit, stop))


def _txt(name):
    query = "https://cloudflare-dns.com/dns-query?name={}&type=TXT".format(urllib.parse.quote(name))
    req = urllib.request.Request(query, headers={"Accept": "application/dns-json"})
    with urllib.request.urlopen(req, timeout=20) as res:
        data = json.loads(res.read().decode("utf-8", "replace"))
    return [a.get("data", "").strip('"') for a in data.get("Answer", [])]


def _mailauth(v, emit, stop):
    domain = v["domain"].lower()
    for record, label in ((domain, "SPF"), ("_dmarc." + domain, "DMARC")):
        try:
            rows = _txt(record)
        except Exception as exc:
            emit("{} failed: {}\n".format(label, exc), "err")
            continue
        hits = [r for r in rows if r.lower().startswith(("v=spf1", "v=dmarc1"))]
        if not hits:
            emit("{:<6} missing\n".format(label), "err")
            continue
        for hit in hits:
            level = "warn" if "~all" in hit or "+all" in hit else "ok"
            emit("{:<6} {}\n".format(label, hit), level)
        if label == "SPF" and any("+all" in h for h in hits):
            emit("       +all allows any sender\n", "warn")
        if label == "DMARC" and any("p=none" in h for h in hits):
            emit("       p=none only monitors\n", "warn")


spec(id="gobuster", cat="WEB", glyph="⊞", name="Gobuster", action="FUZZ",
     tagline="path and DNS brute force",
     binary="gobuster", install=True,
     what="Tries every word of a list against paths or subdomains. Fast and written in Go, a "
          "single binary with no dependencies.",
     docs=doc("Gobuster", ["Type the URL with a trailing <code>/</code> or the domain.",
                           "Choose mode and wordlist.", "Press FUZZ."],
              "In dns mode the input is the domain, not the URL."),
     groups=[("target", [T("target", "Target", "https://example.com/", "URL or domain."),
                         Pth("wordlist", "Wordlist", "file", "Text (*.txt *.lst)",
                             "Candidate list.")]),
             ("mode", [C("mode", "Mode", ["dir", "dns", "vhost"], "dir for paths."),
                       N("threads", "Threads", 1, 60, 20, "Parallelism.")])],
     validate=lambda v: "" if v["target"] and v["wordlist"] else "target and wordlist are required",
     build=lambda v: [exe("gobuster"), v["mode"], "-u", v["target"], "-w", v["wordlist"],
                      "-t", str(v["threads"]), "-q"])

spec(id="feroxbuster", cat="WEB", glyph="⊟", name="Feroxbuster", action="FUZZ",
     tagline="recursive discovery",
     binary="feroxbuster", install=True,
     what="Like Gobuster but recursive and with automatic noise filters. It finds nested "
          "directories a flat sweep misses.",
     docs=doc("Feroxbuster", ["Type the URL.", "Choose a wordlist.", "Press FUZZ."],
              "Start with a short list, recursion multiplies requests."),
     groups=[("target", [T("url", "URL", "https://example.com", "Include the scheme."),
                         Pth("wordlist", "Wordlist", "file", "Text (*.txt *.lst)",
                             "Candidate list.")])],
     validate=lambda v: "" if v["url"] and v["wordlist"] else "URL and wordlist are required",
     build=lambda v: [exe("feroxbuster"), "-u", normalise(v["url"]), "-w", v["wordlist"],
                      "-q", "--no-state"])

spec(id="nikto", cat="WEB", glyph="◈", name="Nikto", action="SCAN",
     tagline="classic web server scanner",
     binary="nikto", install=False,
     what="Checks known misconfigurations, dangerous files and old versions. Noisy and dated, but "
          "it finds things others skip.",
     docs=doc("Nikto", ["Type the host.", "Press SCAN."],
              "It is Perl: needs Strawberry Perl on Windows."),
     groups=[("target", [T("host", "Host or URL", "https://example.com", "Include the scheme.")])],
     validate=lambda v: "" if v["host"] else "the target is empty",
     build=lambda v: [exe("nikto"), "-h", normalise(v["host"]), "-nointeractive"])

spec(id="curl", cat="WEB", glyph="⇄", name="cURL", action="SEND",
     tagline="raw HTTP requests",
     binary="curl", install=False,
     what="Fires a request with an arbitrary method, headers and body. The direct way to see how "
          "an endpoint answers.",
     docs=doc("cURL", ["Type the URL.", "Choose method and headers.", "Press SEND."],
              "Headers as <code>Key: value</code>, one per line."),
     groups=[("request", [T("url", "URL", "https://example.com", "Include the scheme."),
                          C("method", "Method", ["GET", "POST", "PUT", "PATCH", "DELETE",
                                                 "OPTIONS", "HEAD"], "HTTP verb."),
                          A("headers", "Headers", "Content-Type: application/json",
                            "One per line.", 90),
                          A("body", "Body", "{\"x\":1}", "Only for POST/PUT/PATCH.", 90),
                          K("follow", "Follow redirects", "Adds -L.", False),
                          K("verbose", "Show headers", "Adds -i.", True)])],
     validate=lambda v: "" if v["url"] else "the URL is empty",
     build=lambda v: [exe("curl"), "-sS", "-X", v["method"]] +
                     (["-L"] if v["follow"] else []) +
                     (["-i"] if v["verbose"] else []) +
                     sum([["-H", line.strip()] for line in v["headers"].splitlines()
                          if line.strip()], []) +
                     (["--data", v["body"]] if v["body"] and v["method"] in
                      ("POST", "PUT", "PATCH") else []) +
                     [normalise(v["url"])])

spec(id="httpmethods", cat="WEB", glyph="⇄", name="Method Probe", action="PROBE",
     tagline="which verbs an endpoint accepts",
     what="Sends every method and compares statuses. An OPTIONS with Allow or an open PUT says a "
          "lot.",
     docs=doc("Method Probe", ["Type the URL.", "Press PROBE."],
              "401/405 are correct answers for disallowed verbs."),
     groups=[("target", [T("url", "URL", "https://example.com/api", "Include the scheme.")])],
     validate=lambda v: "" if v["url"] else "the URL is empty",
     fn=lambda v, emit, stop: _methods(v, emit, stop))


def _methods(v, emit, stop):
    url = normalise(v["url"])
    opener = urllib.request.build_opener(
        type("NoRedirect", (urllib.request.HTTPRedirectHandler,), {
            "redirect_request": lambda *a, **k: None})())
    for method in ("GET", "HEAD", "OPTIONS", "POST", "PUT", "PATCH", "DELETE", "TRACE"):
        if stop():
            return
        req = urllib.request.Request(url, method=method, headers=ua())
        try:
            with opener.open(req, timeout=15) as res:
                allow = res.headers.get("allow", "")
                emit("{:<8}{}  {}\n".format(method, res.status, allow),
                     "ok" if method in ("GET", "HEAD") else "warn")
        except urllib.error.HTTPError as exc:
            emit("{:<8}{}  {}\n".format(method, exc.code,
                                        (exc.headers or {}).get("allow", "")),
                 "dim" if exc.code in (401, 403, 405) else "warn")
        except Exception as exc:
            emit("{:<8}error {}\n".format(method, exc), "err")


spec(id="json", cat="DATA", glyph="{}", name="JSON Tool", action="RUN",
     tagline="format, minify and validate",
     what="Reindents JSON, minifies it or just validates. It reports the exact line of a syntax "
          "error.",
     docs=doc("JSON Tool", ["Paste the JSON.", "Choose the operation.", "Press RUN."],
              "Minifying is for sending; formatting, for reading."),
     groups=[("input", [A("text", "JSON", "{\"a\":1}", "Content to process.", 160)]),
             ("operation", [C("op", "Operation", ["Format", "Minify", "Validate"],
                              "Validate does not modify."),
                            N("indent", "Indent", 1, 8, 2, "Spaces when formatting.")])],
     validate=lambda v: "" if v["text"].strip() else "the JSON is empty",
     fn=lambda v, emit, stop: _json(v, emit, stop))


def _json(v, emit, stop):
    try:
        data = json.loads(v["text"])
    except json.JSONDecodeError as exc:
        emit("error line {} column {}: {}\n".format(exc.lineno, exc.colno, exc.msg), "err")
        return
    emit("valid, {} top level node(s)\n".format(
        len(data) if isinstance(data, (dict, list)) else 1), "ok")
    if v["op"] == "Validate":
        return
    if v["op"] == "Minify":
        emit("\n{}\n".format(json.dumps(data, separators=(",", ":"), ensure_ascii=False)),
             "accent")
    else:
        emit("\n{}\n".format(json.dumps(data, indent=v["indent"], ensure_ascii=False)), "accent")

spec(id="yaml", cat="DATA", glyph="⌸", name="YAML Tool", action="RUN",
     tagline="YAML to JSON and back",
     what="Converts between YAML and JSON. Uses PyYAML when available.",
     docs=doc("YAML Tool", ["Paste the content.", "Choose the direction.", "Press RUN."],
              "Install PyYAML with pip if missing."),
     groups=[("input", [A("text", "Content", "key: value", "YAML or JSON.", 160)]),
             ("direction", [C("op", "Direction", ["YAML to JSON", "JSON to YAML"],
                              "Choose the direction.")])],
     validate=lambda v: "" if v["text"].strip() else "the content is empty",
     fn=lambda v, emit, stop: _yaml(v, emit, stop))


def _yaml(v, emit, stop):
    try:
        import yaml
    except Exception:
        emit("missing PyYAML: pip install pyyaml\n", "err")
        return
    try:
        if v["op"] == "YAML to JSON":
            data = yaml.safe_load(v["text"])
            emit("\n{}\n".format(json.dumps(data, indent=2, ensure_ascii=False)), "accent")
        else:
            data = json.loads(v["text"])
            emit("\n{}\n".format(yaml.safe_dump(data, allow_unicode=True, sort_keys=False)),
                 "accent")
    except Exception as exc:
        emit("{}\n".format(exc), "err")

spec(id="csv", cat="DATA", glyph="▦", name="CSV Inspector", action="ANALYZE",
     tagline="columns and stats of a CSV",
     what="Reads a CSV, counts rows and columns and shows detected types. Writes nothing.",
     docs=doc("CSV Inspector", ["Paste the CSV.", "Choose the separator.", "Press ANALYZE."],
              "Adjust the separator if you use semicolons or tabs."),
     groups=[("input", [A("text", "CSV", "a,b,c\n1,2,3", "Content with a header.", 150),
                        C("sep", "Separator", [",", ";", "\\t", "|"], "Delimiter.")])],
     validate=lambda v: "" if v["text"].strip() else "the CSV is empty",
     fn=lambda v, emit, stop: _csv(v, emit, stop))


def _csv(v, emit, stop):
    import csv as csvmod
    import io
    sep = "\t" if v["sep"] == "\\t" else v["sep"]
    rows = list(csvmod.reader(io.StringIO(v["text"]), delimiter=sep))
    if not rows:
        emit("no rows\n", "warn")
        return
    width = max(len(r) for r in rows)
    emit("{} row(s), {} column(s)\n".format(len(rows), width), "accent")
    header = rows[0]
    for index, name in enumerate(header, 1):
        values = [r[index - 1] for r in rows[1:] if len(r) >= index]
        numeric = sum(1 for x in values if re.fullmatch(r"-?\d+(\.\d+)?", x.strip() or "x"))
        kind = "numeric" if values and numeric > len(values) / 2 else "text"
        emit("{:>2}. {:<24} {} values, {}\n".format(index, name[:24], len(values), kind), "out")

spec(id="xml", cat="DATA", glyph="◱", name="XML Formatter", action="RUN",
     tagline="indent and validate XML",
     what="Checks that XML is well formed and reindents it. Errors are reported with position.",
     docs=doc("XML Formatter", ["Paste the XML.", "Press RUN."],
              "It only checks form, not schema validity."),
     groups=[("input", [A("text", "XML", "<root><child/></root>", "Content.", 160)]),
             ("options", [N("indent", "Indent", 1, 8, 2, "Spaces.")])],
     validate=lambda v: "" if v["text"].strip() else "the XML is empty",
     fn=lambda v, emit, stop: _xml(v, emit, stop))


def _xml(v, emit, stop):
    from xml.dom import minidom
    try:
        parsed = minidom.parseString(v["text"])
    except Exception as exc:
        emit("malformed: {}\n".format(exc), "err")
        return
    emit("well formed\n", "ok")
    pretty = parsed.toprettyxml(indent=" " * v["indent"])
    emit("\n{}\n".format("\n".join(l for l in pretty.splitlines() if l.strip())), "accent")

spec(id="markdown", cat="DATA", glyph="¶", name="Markdown Preview", action="RENDER",
     tagline="markdown to HTML",
     what="Converts basic markdown to HTML to review how it looks before publishing.",
     docs=doc("Markdown Preview", ["Paste the markdown.", "Press RENDER."],
              "Covers headings, lists, emphasis, code and links."),
     groups=[("input", [A("text", "Markdown", "# Title\n\nText", "Content.", 170)]),
             ("options", [K("inline", "Fragment only", "No html or body wrapper.", True)])],
     validate=lambda v: "" if v["text"].strip() else "the markdown is empty",
     fn=lambda v, emit, stop: _markdown(v, emit, stop))


def _markdown(v, emit, stop):
    lines = v["text"].splitlines()
    out = []
    in_code = False
    in_list = False
    for line in lines:
        if line.startswith("```"):
            out.append("</code></pre>" if in_code else "<pre><code>")
            in_code = not in_code
            continue
        if in_code:
            out.append(line.replace("<", "&lt;"))
            continue
        if re.match(r"^\s*[-*+]\s", line):
            if not in_list:
                out.append("<ul>")
                in_list = True
            out.append("<li>{}</li>".format(line.lstrip("-*+ ")))
            continue
        if in_list:
            out.append("</ul>")
            in_list = False
        head = re.match(r"^(#{1,6})\s+(.*)$", line)
        if head:
            level = len(head.group(1))
            out.append("<h{0}>{1}</h{0}>".format(level, head.group(2)))
            continue
        if not line.strip():
            out.append("")
            continue
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
        text = re.sub(r"\*(.+?)\*", r"<i>\1</i>", text)
        text = re.sub(r"`(.+?)`", r"<code>\1</code>", text)
        text = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', text)
        out.append("<p>{}</p>".format(text))
    if in_list:
        out.append("</ul>")
    if in_code:
        out.append("</code></pre>")
    body = "\n".join(out)
    emit("\n{}\n".format(body if v["inline"] else
                         "<html><body>{}</body></html>".format(body)), "accent")

spec(id="lorem", cat="DATA", glyph="≡", name="Lorem Ipsum", action="GENERATE",
     tagline="filler text",
     what="Generates filler paragraphs or words for mockups. Adjust the amount.",
     docs=doc("Lorem Ipsum", ["Choose unit and amount.", "Press GENERATE."],
              "It does not repeat the same sentence every time: order is random."),
     groups=[("output", [C("unit", "Unit", ["Words", "Sentences", "Paragraphs"], "What to generate."),
                         N("count", "Amount", 1, 50, 3, "How many units.")])],
     fn=lambda v, emit, stop: _lorem(v, emit, stop))

LOREM = ("lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor "
         "incididunt ut labore et dolore magna aliqua enim ad minim veniam quis nostrud "
         "exercitation ullamco laboris nisi aliquip ex ea commodo consequat duis aute irure "
         "in reprehenderit voluptate velit esse cillum eu fugiat nulla pariatur excepteur "
         "sint occaecat cupidatat non proident sunt culpa qui officia deserunt mollit anim "
         "id est laborum").split()


def _lorem(v, emit, stop):
    def sentence():
        words = [random.choice(LOREM) for _ in range(random.randint(6, 14))]
        return " ".join(words).capitalize() + "."
    if v["unit"] == "Words":
        emit(" ".join(random.choice(LOREM) for _ in range(v["count"])) + "\n", "accent")
    elif v["unit"] == "Sentences":
        emit(" ".join(sentence() for _ in range(v["count"])) + "\n", "accent")
    else:
        for _ in range(v["count"]):
            emit(" ".join(sentence() for _ in range(random.randint(3, 6))) + "\n\n", "accent")

spec(id="slug", cat="DATA", glyph="⇢", name="Slugifier", action="RUN",
     tagline="text to a clean slug",
     what="Turns titles into safe slugs, with separator variants and no accents.",
     docs=doc("Slugifier", ["Paste the title.", "Choose the separator.", "Press RUN."],
              "Meant for URLs and file names."),
     groups=[("input", [T("text", "Title", "Hello world, how are you?", "Original text."),
                        C("sep", "Separator", ["-", "_", ""], "Join between words."),
                        K("lower", "Lowercase", "Recommended.", True)])],
     validate=lambda v: "" if v["text"] else "the title is empty",
     fn=lambda v, emit, stop: _slug(v, emit, stop))


def _slug(v, emit, stop):
    import unicodedata
    text = unicodedata.normalize("NFKD", v["text"])
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = re.sub(r"[^A-Za-z0-9]+", " ", text).strip()
    if v["lower"]:
        text = text.lower()
    emit("\n{}\n".format(text.replace(" ", v["sep"])), "accent")
    emit("{} characters\n".format(len(text)), "dim")

spec(id="wordfreq", cat="DATA", glyph="¶", name="Word Frequency", action="COUNT",
     tagline="most repeated words",
     what="Counts words and shows the ranking, skipping common stopwords. A good starting point "
          "for keywords.",
     docs=doc("Word Frequency", ["Paste the text.", "Choose how many to show.", "Press COUNT."],
              "Removing stopwords gives a more useful signal."),
     groups=[("input", [A("text", "Text", "paste here", "Content to analyse.", 150)]),
             ("options", [N("top", "Show", 5, 100, 20, "Ranking size."),
                          K("stop", "Ignore stopwords", "Drops articles and prepositions.",
                            True)])],
     validate=lambda v: "" if v["text"].strip() else "the text is empty",
     fn=lambda v, emit, stop: _wordfreq(v, emit, stop))

STOPWORDS = set(("de la que el en y a los se del las un por con no una su para es al lo como "
                 "más pero sus le ya o este sí porque esta entre cuando muy sin sobre también "
                 "me hasta hay donde quien desde todo nos durante todos uno les ni contra otros "
                 "ese eso ante ellos e esto mí antes algunos qué unos yo otro otras otra él tanto "
                 "esa estos mucho quienes nada muchos cual poco ella estar estas algunas algo "
                 "nosotros my mi tu the of and to in a is it that for on with as was at by be "
                 "this from or an are").split())


def _wordfreq(v, emit, stop):
    words = re.findall(r"[\wáéíóúñü]+", v["text"].lower())
    if v["stop"]:
        words = [w for w in words if w not in STOPWORDS and len(w) > 1]
    counts = {}
    for word in words:
        counts[word] = counts.get(word, 0) + 1
    if not counts:
        emit("no useful words\n", "warn")
        return
    emit("{} words, {} unique\n\n".format(len(words), len(counts)), "dim")
    for word, count in sorted(counts.items(), key=lambda kv: -kv[1])[:v["top"]]:
        bar = "▇" * min(40, count)
        emit("{:<20}{:>4}  {}\n".format(word, count, bar), "out")

spec(id="vigenere", cat="DATA", glyph="✎", name="Vigenère", action="RUN",
     tagline="classic cipher with a key",
     what="Encrypts or decrypts with Vigenère. Stronger than Caesar because the key changes the "
          "shift.",
     docs=doc("Vigenère", ["Paste the text.", "Type the key.", "Choose direction and press RUN."],
              "It only shifts A-Z; everything else is preserved."),
     groups=[("input", [A("text", "Text", "attack at dawn", "Content.", 110),
                        T("key", "Key", "key", "Letters only."),
                        C("dir", "Direction", ["Encrypt", "Decrypt"], "Direction.")])],
     validate=lambda v: "" if v["text"] and v["key"].isalpha() else "text and an alphabetic key",
     fn=lambda v, emit, stop: _vigenere(v, emit, stop))


def _vigenere(v, emit, stop):
    key = [ord(c.lower()) - 97 for c in v["key"] if c.isalpha()]
    if not key:
        emit("key without letters\n", "err")
        return
    sign = 1 if v["dir"] == "Encrypt" else -1
    out = []
    index = 0
    for ch in v["text"]:
        if ch.isalpha():
            base = 65 if ch.isupper() else 97
            shift = key[index % len(key)] * sign
            out.append(chr((ord(ch) - base + shift) % 26 + base))
            index += 1
        else:
            out.append(ch)
    emit("\n{}\n".format("".join(out)), "accent")

spec(id="xor", cat="DATA", glyph="⊕", name="XOR Tool", action="RUN",
     tagline="XOR with a hex key",
     what="Applies byte-wise XOR with a key. The same key gets you back to the original.",
     docs=doc("XOR Tool", ["Paste the text or the hex.", "Type the key in hex.",
                           "Press RUN."],
              "Example key: <code>2a</code>. Output is hex."),
     groups=[("input", [A("text", "Input", "plain text or 68656c6c6f", "Text or hex.", 110),
                        T("key", "Hex key", "2a", "Bytes in hexadecimal."),
                        C("dir", "Direction", ["Text to hex", "Hex to text"], "Direction.")])],
     validate=lambda v: "" if v["text"] and v["key"] else "input and key are required",
     fn=lambda v, emit, stop: _xor(v, emit, stop))


def _xor(v, emit, stop):
    try:
        key = bytes.fromhex(v["key"].strip())
    except ValueError:
        emit("key is not hexadecimal\n", "err")
        return
    if not key:
        emit("empty key\n", "err")
        return
    try:
        data = (v["text"].encode() if v["dir"] == "Text to hex"
                else bytes.fromhex(re.sub(r"[^0-9a-fA-F]", "", v["text"])))
    except ValueError:
        emit("input is not hexadecimal\n", "err")
        return
    out = bytes(b ^ key[i % len(key)] for i, b in enumerate(data))
    emit("\n{}\n".format(out.hex() if v["dir"] == "Text to hex"
                         else out.decode("utf-8", "replace")), "accent")

spec(id="crc32", cat="DATA", glyph="⌗", name="Checksums", action="COMPUTE",
     tagline="crc32 and adler32",
     what="Computes CRC32 and Adler-32 of a text or file. They are fast integrity sums, not "
          "cryptographic.",
     docs=doc("Checksums", ["Paste the text or pick a file.", "Press COMPUTE."],
              "For security use SHA-256, not CRC."),
     groups=[("input", [A("text", "Text", "optional", "Used when there is no file.", 90),
                        Pth("path", "File", "file", "", "Takes priority over the text.")])],
     fn=lambda v, emit, stop: _crc(v, emit, stop))


def _crc(v, emit, stop):
    data = b""
    if v["path"] and os.path.isfile(v["path"]):
        with open(v["path"], "rb") as handle:
            data = handle.read()
        emit("file  {}  {}\n".format(v["path"], human_size(len(data))), "dim")
    elif v["text"]:
        data = v["text"].encode()
        emit("text  {} bytes\n".format(len(data)), "dim")
    else:
        emit("nothing to hash\n", "err")
        return
    emit("crc32    {:08x}\n".format(binascii.crc32(data) & 0xFFFFFFFF), "accent")
    emit("adler32  {:08x}\n".format(binascii.adler32(data) & 0xFFFFFFFF), "accent")

spec(id="base58", cat="DATA", glyph="⇄", name="Base58", action="RUN",
     tagline="bitcoin style base58",
     what="Encodes or decodes base58, the ambiguous-character-free alphabet used by Bitcoin "
          "addresses.",
     docs=doc("Base58", ["Paste the text.", "Choose direction.", "Press RUN."],
              "Alphabet: no 0, O, I or l."),
     groups=[("input", [A("text", "Input", "text", "Content.", 100),
                        C("dir", "Direction", ["Encode", "Decode"], "Direction.")])],
     validate=lambda v: "" if v["text"] else "the input is empty",
     fn=lambda v, emit, stop: _base58(v, emit, stop))

B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def _b58enc(data):
    number = int.from_bytes(data, "big")
    out = ""
    while number:
        number, rem = divmod(number, 58)
        out = B58[rem] + out
    pad = len(data) - len(data.lstrip(b"\0"))
    return "1" * pad + (out or "")


def _b58dec(text):
    number = 0
    for char in text:
        number = number * 58 + B58.index(char)
    pad = len(text) - len(text.lstrip("1"))
    body = number.to_bytes((number.bit_length() + 7) // 8, "big") if number else b""
    return b"\0" * pad + body


def _base58(v, emit, stop):
    try:
        if v["dir"] == "Encode":
            emit("\n{}\n".format(_b58enc(v["text"].encode())), "accent")
        else:
            emit("\n{}\n".format(_b58dec(v["text"].strip()).decode("utf-8", "replace")), "accent")
    except Exception as exc:
        emit("{}\n".format(exc), "err")

spec(id="roman", cat="DATA", glyph="Ⅻ", name="Roman Numerals", action="RUN",
     tagline="numbers to roman and back",
     what="Converts integers to roman numerals and back, validating canonical form.",
     docs=doc("Roman Numerals", ["Type the value.", "Choose direction.", "Press RUN."],
              "Valid range: 1 to 3999."),
     groups=[("value", [T("value", "Value", "1987 or MCMLXXXVII", "Number or roman numeral."),
                        C("dir", "Direction", ["To roman", "To number"], "Direction.")])],
     validate=lambda v: "" if v["value"] else "the value is empty",
     fn=lambda v, emit, stop: _roman(v, emit, stop))

ROMAN = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"),
         (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]


def _roman(v, emit, stop):
    if v["dir"] == "To roman":
        try:
            number = int(v["value"])
        except ValueError:
            emit("not a number\n", "err")
            return
        if not 0 < number < 4000:
            emit("out of range\n", "err")
            return
        out = ""
        for value, glyph in ROMAN:
            while number >= value:
                out += glyph
                number -= value
        emit("\n{}\n".format(out), "accent")
        return
    text = v["value"].upper().strip()
    if not re.fullmatch(r"[IVXLCDM]+", text):
        emit("not a valid roman numeral\n", "err")
        return
    index = 0
    total = 0
    for value, glyph in ROMAN:
        while text.startswith(glyph, index):
            total += value
            index += len(glyph)
    emit("\n{}\n".format(total), "accent")
    emit("canonical  {}\n".format("yes" if index == len(text) else "no"), "dim")

spec(id="unicode", cat="DATA", glyph="𝐀", name="Unicode Lookup", action="LOOKUP",
     tagline="names, categories and escapes",
     what="Shows name, category, block and escapes for each character. Good for debugging "
          "homoglyphs.",
     docs=doc("Unicode Lookup", ["Paste the text.", "Press LOOKUP."],
              "It reports invisible and control characters."),
     groups=[("input", [A("text", "Text", "abc", "Analysed character by character.", 120)]),
             ("options", [K("escapes", "Show escapes", "Includes \\u and UTF-8.", True)])],
     validate=lambda v: "" if v["text"] else "the text is empty",
     fn=lambda v, emit, stop: _unicode(v, emit, stop))


def _unicode(v, emit, stop):
    import unicodedata
    for char in v["text"][:200]:
        try:
            name = unicodedata.name(char)
        except ValueError:
            name = "no name"
        emit("U+{:04X}  {}  {}\n".format(ord(char), unicodedata.category(char), name),
             "warn" if unicodedata.category(char).startswith("C") else "out")
        if v["escapes"]:
            emit("        \\u{:04x}  {}\n".format(ord(char), char.encode("utf-8").hex()), "dim")

UNITS = {
    "mm": ("long", 0.001), "cm": ("long", 0.01), "m": ("long", 1.0), "km": ("long", 1000.0),
    "in": ("long", 0.0254), "ft": ("long", 0.3048), "mi": ("long", 1609.344),
    "mg": ("mass", 0.000001), "g": ("mass", 0.001), "kg": ("mass", 1.0), "lb": ("mass", 0.45359237),
    "oz": ("mass", 0.028349523),
    "ml": ("vol", 0.001), "l": ("vol", 1.0), "gal": ("vol", 3.785411784), "cup": ("vol", 0.24),
    "B": ("data", 1.0), "KB": ("data", 1024.0), "MB": ("data", 1048576.0),
    "GB": ("data", 1073741824.0),
    "mps": ("speed", 1.0), "kmh": ("speed", 0.277777778), "mph": ("speed", 0.44704),
}


spec(id="unitconv", cat="UTILITIES", glyph="⇄", name="Unit Converter", action="CONVERT",
     tagline="length, mass, volume and more",
     what="Converts between units of the same family with exact factors.",
     docs=doc("Unit Converter", ["Type the value.", "Choose source and target.",
                                 "Press CONVERT."],
              "Families: length, mass, volume, data and speed."),
     groups=[("value", [T("value", "Value", "12", "Number to convert.")]),
             ("units", [C("src", "From", sorted(UNITS.keys()), "Source unit."),
                        C("dst", "To", sorted(UNITS.keys()), "Target unit.")])],
     validate=lambda v: "" if v["value"] else "the value is empty",
     fn=lambda v, emit, stop: _unitconv(v, emit, stop))


def _unitconv(v, emit, stop):
    try:
        value = float(v["value"].replace(",", "."))
    except ValueError:
        emit("non numeric value\n", "err")
        return
    src, dst = UNITS[v["src"]], UNITS[v["dst"]]
    if src[0] != dst[0]:
        emit("different families: {} and {}\n".format(src[0], dst[0]), "err")
        return
    emit("\n{:.6g} {}\n".format(value * src[1] / dst[1], v["dst"]), "accent")
    emit("{} {} = {:.6g} {}\n".format(value, v["src"], value * src[1] / dst[1], v["dst"]), "dim")

spec(id="timezone", cat="UTILITIES", glyph="◷", name="Timezone Grid", action="SHOW",
     tagline="one hour in several zones",
     what="Takes a UTC time and shows it in several zones. Useful to coordinate calls.",
     docs=doc("Timezone Grid", ["Type the UTC time.", "Press SHOW."],
              "Format: <code>YYYY-MM-DD HH:MM</code>."),
     groups=[("time", [T("stamp", "UTC time", "2026-01-01 18:00", "Base in UTC.")])],
     validate=lambda v: "" if v["stamp"] else "the time is empty",
     fn=lambda v, emit, stop: _timezone(v, emit, stop))

ZONES = ["UTC", "Europe/Madrid", "Europe/London", "America/New_York", "America/Los_Angeles",
         "America/Sao_Paulo", "Asia/Tokyo", "Asia/Kolkata", "Australia/Sydney"]


def _timezone(v, emit, stop):
    import zoneinfo
    try:
        base = datetime.datetime.strptime(v["stamp"], "%Y-%m-%d %H:%M").replace(
            tzinfo=datetime.timezone.utc)
    except ValueError:
        emit("invalid format\n", "err")
        return
    for name in ZONES:
        try:
            local = base.astimezone(zoneinfo.ZoneInfo(name))
        except Exception:
            continue
        offset = local.strftime("%z")
        emit("{:<22}{}  {}\n".format(name, local.strftime("%Y-%m-%d %H:%M"), offset), "out")

spec(id="rsa", cat="UTILITIES", glyph="⛨", name="RSA Keygen", action="GENERATE",
     tagline="demo keypair",
     what="Generates an RSA keypair in pure Python with random primes. Enough for testing, not "
          "for production.",
     docs=doc("RSA Keygen", ["Choose the size in bits.", "Press GENERATE."],
              "1024 takes a couple of seconds; 2048 much longer."),
     groups=[("keys", [C("bits", "Bits", ["512", "1024", "2048"], "Modulus size."),
                       K("show", "Show private", "Includes d.", True)])],
     fn=lambda v, emit, stop: _rsa(v, emit, stop))


def _is_probable_prime(n, rounds=24):
    if n < 2:
        return False
    for small in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % small == 0:
            return n == small
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def _prime(bits):
    while True:
        candidate = secrets.randbits(bits) | (1 << (bits - 1)) | 1
        if _is_probable_prime(candidate):
            return candidate


def _rsa(v, emit, stop):
    bits = int(v["bits"])
    emit("searching for {}-bit primes...\n".format(bits // 2), "dim")
    p = _prime(bits // 2)
    q = _prime(bits // 2)
    while q == p:
        q = _prime(bits // 2)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi)
    emit("\nmodulus n   {}\n".format(hex(n)), "accent")
    emit("public e    {}\n".format(e), "accent")
    if v["show"]:
        emit("private d   {}\n".format(hex(d)), "accent")
    emit("p           {}\n".format(hex(p)), "dim")
    emit("q           {}\n".format(hex(q)), "dim")
    emit("\n{} real bits\n".format(n.bit_length()), "out")

spec(id="pem", cat="UTILITIES", glyph="⛨", name="PEM Inspector", action="INSPECT",
     tagline="type and fingerprint of a PEM",
     what="Reads the header of a PEM block and computes its SHA-256 fingerprint over DER. It does "
          "not validate chains.",
     docs=doc("PEM Inspector", ["Paste the PEM block.", "Press INSPECT."],
              "The fingerprint is for comparing keys between machines."),
     groups=[("block", [A("text", "PEM", "-----BEGIN ...-----", "Full block.", 150)]),
             ("options", [K("der", "Show DER hex", "First decoded bytes.", False)])],
     validate=lambda v: "" if "-----BEGIN" in v["text"] else "no PEM detected",
     fn=lambda v, emit, stop: _pem(v, emit, stop))


def _pem(v, emit, stop):
    match = re.search(r"-----BEGIN ([A-Z0-9 ]+)-----(.*?)-----END", v["text"], re.S)
    if not match:
        emit("unrecognised header\n", "err")
        return
    label = match.group(1).strip()
    emit("type  {}\n".format(label), "accent")
    body = re.sub(r"\s+", "", match.group(2))
    try:
        der = base64.b64decode(body)
    except Exception as exc:
        emit("invalid base64: {}\n".format(exc), "err")
        return
    emit("der   {} bytes\n".format(len(der)), "dim")
    emit("sha256 {}\n".format(hashlib.sha256(der).hexdigest()), "ok")
    if v["der"]:
        emit("\n{}\n".format(der[:64].hex()), "dim")

spec(id="split", cat="UTILITIES", glyph="⌫", name="File Split", action="RUN",
     tagline="split and join files",
     what="Splits a file into fixed-size parts, or joins parts in order. Useful to move big "
          "things.",
     docs=doc("File Split", ["Pick a file or a folder of parts.", "Choose operation.",
                             "Set destination and press RUN."],
              "To join, the parts must share the same prefix."),
     groups=[("input", [Pth("src", "File or folder", "file", "", "Source."),
                        C("op", "Operation", ["Split", "Join"], "Direction."),
                        Pth("dst", "Destination", "dir", "", "Output folder."),
                        N("size", "MB per part", 1, 512, 10, "Only when splitting.")])],
     validate=lambda v: "" if v["src"] else "pick a source",
     fn=lambda v, emit, stop: _split(v, emit, stop))


def _split(v, emit, stop):
    dest = v["dst"] or os.path.dirname(v["src"]) or "."
    if v["op"] == "Split":
        if not os.path.isfile(v["src"]):
            emit("not a file\n", "err")
            return
        limit = v["size"] * 1024 * 1024
        base = os.path.basename(v["src"])
        index = 0
        with open(v["src"], "rb") as handle:
            while True:
                if stop():
                    return
                block = handle.read(limit)
                if not block:
                    break
                path = os.path.join(dest, "{}.part{:03d}".format(base, index))
                with open(path, "wb") as out:
                    out.write(block)
                emit("{}\n".format(path), "out")
                index += 1
        emit("\n{} part(s)\n".format(index), "accent")
        return
    if not os.path.isdir(v["src"]):
        emit("not a folder\n", "err")
        return
    parts = sorted(f for f in os.listdir(v["src"]) if ".part" in f)
    if not parts:
        emit("no parts\n", "warn")
        return
    target = os.path.join(dest, parts[0].split(".part")[0])
    with open(target, "wb") as out:
        for name in parts:
            with open(os.path.join(v["src"], name), "rb") as handle:
                out.write(handle.read())
            emit("+ {}\n".format(name), "dim")
    emit("\njoined into {}\n".format(target), "ok")

spec(id="rename", cat="UTILITIES", glyph="✎", name="Batch Rename", action="RENAME",
     tagline="pattern renaming",
     what="Batch renames with prefix, suffix and numbering, or replaces text. It shows a preview "
          "before touching anything.",
     docs=doc("Batch Rename", ["Pick the folder.", "Configure the pattern.", "Press RENAME."],
              "Leave apply unchecked to only preview."),
     groups=[("folder", [Pth("dir", "Folder", "dir", "", "Files to rename.")]),
             ("pattern", [T("find", "Find", "IMG_", "Text to replace."),
                          T("replace", "Replace with", "photo", "New text."),
                          T("prefix", "Prefix", "", "Added in front."),
                          N("pad", "Digits", 1, 6, 3, "Trailing numbering."),
                          K("apply", "Apply", "Unchecked only previews.", False)])],
     validate=lambda v: "" if v["dir"] else "pick a folder",
     fn=lambda v, emit, stop: _rename(v, emit, stop))


def _rename(v, emit, stop):
    if not os.path.isdir(v["dir"]):
        emit("invalid folder\n", "err")
        return
    files = sorted(f for f in os.listdir(v["dir"]) if os.path.isfile(os.path.join(v["dir"], f)))
    for index, name in enumerate(files, 1):
        stem, ext = os.path.splitext(name)
        if v["find"]:
            stem = stem.replace(v["find"], v["replace"])
        new = "{}{}_{:0{d}}".format(v["prefix"], stem, index, d=v["pad"]) + ext
        if new == name:
            continue
        emit("{:<40} -> {}\n".format(name, new), "out")
        if v["apply"]:
            try:
                os.rename(os.path.join(v["dir"], name), os.path.join(v["dir"], new))
            except Exception as exc:
                emit("  failed: {}\n".format(exc), "err")
    emit("\n{}{} file(s)\n".format("" if v["apply"] else "previewed ",
                                   len(files)), "accent")

spec(id="dupes", cat="UTILITIES", glyph="≠", name="Duplicate Finder", action="SCAN",
     tagline="repeated files by hash",
     what="Groups files by size and then by SHA-256 to find real duplicates. Deletes nothing.",
     docs=doc("Duplicate Finder", ["Pick the folder.", "Press SCAN."],
              "Review before deleting: the first of each group is the keeper."),
     groups=[("folder", [Pth("dir", "Folder", "dir", "", "Walked recursively.")]),
             ("options", [N("min", "Minimum size KB", 1, 10240, 64,
                            "Ignores small files.")])],
     validate=lambda v: "" if v["dir"] else "pick a folder",
     fn=lambda v, emit, stop: _dupes(v, emit, stop))


def _dupes(v, emit, stop):
    by_size = {}
    for root, _dirs, files in os.walk(v["dir"]):
        if stop():
            return
        for name in files:
            path = os.path.join(root, name)
            try:
                size = os.path.getsize(path)
            except OSError:
                continue
            if size >= v["min"] * 1024:
                by_size.setdefault(size, []).append(path)
    groups = 0
    wasted = 0
    for size, paths in by_size.items():
        if len(paths) < 2:
            continue
        by_hash = {}
        for path in paths:
            digest = hashlib.sha256()
            try:
                with open(path, "rb") as handle:
                    for block in iter(lambda: handle.read(1 << 20), b""):
                        digest.update(block)
            except OSError:
                continue
            by_hash.setdefault(digest.hexdigest(), []).append(path)
        for paths_same in by_hash.values():
            if len(paths_same) < 2:
                continue
            groups += 1
            wasted += size * (len(paths_same) - 1)
            emit("\n{} copies · {}\n".format(len(paths_same), human_size(size)), "warn")
            for path in paths_same:
                emit("  {}\n".format(path), "out")
    emit("\n{} group(s), {} recoverable\n".format(groups, human_size(wasted)), "accent")

spec(id="dirsize", cat="UTILITIES", glyph="⊟", name="Folder Size", action="MEASURE",
     tagline="real weight per subfolder",
     what="Sums sizes recursively and sorts descending. Finds what fills the disk.",
     docs=doc("Folder Size", ["Pick the folder.", "Press MEASURE."],
              "It can be slow on large trees with a slow disk."),
     groups=[("folder", [Pth("dir", "Folder", "dir", "", "Starting point.")])],
     validate=lambda v: "" if v["dir"] else "pick a folder",
     fn=lambda v, emit, stop: _dirsize(v, emit, stop))


def _dirsize(v, emit, stop):
    total = 0
    rows = []
    for root, dirs, files in os.walk(v["dir"]):
        if stop():
            return
        size = 0
        for name in files:
            try:
                size += os.path.getsize(os.path.join(root, name))
            except OSError:
                pass
        total += size
        rows.append((size, root))
    emit("total  {}\n\n".format(human_size(total)), "accent")
    for size, path in sorted(rows, key=lambda r: -r[0])[:40]:
        emit("{:>10}  {}\n".format(human_size(size), path), "out")


REPO_SEED = [
    ("yt-dlp", "https://github.com/yt-dlp/yt-dlp", "MEDIA", "the reference video downloader", "ka0s"),
    ("gallery-dl", "https://github.com/mikf/gallery-dl", "MEDIA", "galleries and full sets", "ka0s"),
    ("FFmpeg", "https://github.com/BtbN/FFmpeg-Builds", "MEDIA", "static ffmpeg builds", "n0va"),
    ("HandBrake", "https://github.com/HandBrake/HandBrake", "MEDIA", "transcoding with a GUI", "n0va"),
    ("LosslessCut", "https://github.com/mifi/lossless-cut", "MEDIA", "cutting without re-encoding", "mika"),
    ("OBS Studio", "https://github.com/obsproject/obs-studio", "MEDIA", "capture and streaming", "mika"),
    ("ffuf", "https://github.com/ffuf/ffuf", "WEB", "fast fuzzing in Go", "ka0s"),
    ("nuclei", "https://github.com/projectdiscovery/nuclei", "WEB", "vulnerability templates", "ka0s"),
    ("SecLists", "https://github.com/danielmiessler/SecLists", "WEB", "the list of lists", "n0va"),
    ("PayloadsAllTheThings", "https://github.com/swisskyrepo/PayloadsAllTheThings", "WEB", "payloads per scenario", "n0va"),
    ("httpx", "https://github.com/projectdiscovery/httpx", "RECON", "mass host probing", "ka0s"),
    ("subfinder", "https://github.com/projectdiscovery/subfinder", "RECON", "passive subdomains", "ka0s"),
    ("Amass", "https://github.com/owasp-amass/amass", "RECON", "surface mapping", "n0va"),
    ("theHarvester", "https://github.com/laramies/theHarvester", "RECON", "emails and names", "n0va"),
    ("trufflehog", "https://github.com/trufflesecurity/trufflehog", "RECON", "secrets in repos", "mika"),
    ("gitleaks", "https://github.com/gitleaks/gitleaks", "RECON", "secrets in git, fast", "mika"),
    ("Nmap", "https://github.com/nmap/nmap", "NETWORK", "port scanning", "ka0s"),
    ("Wireshark", "https://gitlab.com/wireshark/wireshark", "NETWORK", "traffic analysis", "n0va"),
    ("iperf3", "https://github.com/esnet/iperf", "NETWORK", "real bandwidth", "n0va"),
    ("jq", "https://github.com/jqlang/jq", "DATA", "process JSON in the console", "mika"),
    ("ripgrep", "https://github.com/BurntSushi/ripgrep", "DATA", "fast text search", "mika"),
    ("fd", "https://github.com/sharkdp/fd", "DATA", "find files, simple", "mika"),
    ("bat", "https://github.com/sharkdp/bat", "DATA", "cat with highlighting", "mika"),
    ("fzf", "https://github.com/junegunn/fzf", "UTILITIES", "universal fuzzy selector", "mika"),
    ("PowerToys", "https://github.com/microsoft/PowerToys", "UTILITIES", "Windows utilities", "ka0s"),
    ("Everything", "https://www.voidtools.com", "UTILITIES", "instant file search", "ka0s"),
    ("Flow Launcher", "https://github.com/Flow-Launcher/Flow.Launcher", "UTILITIES", "launcher with plugins", "n0va"),
    ("ShareX", "https://github.com/ShareX/ShareX", "UTILITIES", "capture and automation", "n0va"),
    ("Rclone", "https://github.com/rclone/rclone", "UTILITIES", "sync with the cloud", "mika"),
    ("7-Zip", "https://www.7-zip.org", "UTILITIES", "solid compression", "ka0s"),
    ("KeePassXC", "https://github.com/keepassxreboot/keepassxc", "UTILITIES", "local vault", "mika"),
    ("Bitwarden", "https://github.com/bitwarden/clients", "UTILITIES", "synced vault", "mika"),
    ("Syncthing", "https://github.com/syncthing/syncthing", "UTILITIES", "P2P sync", "n0va"),
    ("Tailscale", "https://github.com/tailscale/tailscale", "NETWORK", "WireGuard mesh", "n0va"),
    ("Stirling-PDF", "https://github.com/Stirling-Tools/Stirling-PDF", "UTILITIES", "everything PDF, local", "mika"),
    ("Tesseract", "https://github.com/tesseract-ocr/tesseract", "DATA", "open source OCR", "mika"),
    ("ExifTool", "https://exiftool.org", "MEDIA", "full metadata", "n0va"),
    ("mpv", "https://github.com/mpv-player/mpv", "MEDIA", "lightweight player", "ka0s"),
    ("uBlock Origin", "https://github.com/gorhill/uBlock", "UTILITIES", "actual ad blocking", "ka0s"),
    ("LibreWolf", "https://github.com/LibreWolf-Community/LibreWolf", "UTILITIES", "hardened browser", "n0va"),
]


class ReposPage(ToolPage):
    ACCENT = P.START

    def __init__(self):
        super().__init__(
            "repos", "Recommended repos", "★", "good repos, from people you trust",
            "List curated by friends: tools worth your time that do not show up on the usual "
            "lists. You can add your own, they are saved to a local JSON and survive a restart.",
            doc("Recommended repos",
                ["Search by name, category or author.",
                 "Copy the URL or open it in the browser.",
                 "Add your own repo with name, URL and reason."],
                "Nothing is downloaded on its own. The <code>repos.json</code> file stays next to "
                "the script."))

        self.group("add")
        row = QHBoxLayout()
        row.setSpacing(8)
        self.new_name = HoverLine()
        self.new_name.setPlaceholderText("name")
        self.new_name.setFixedHeight(34)
        self.new_url = HoverLine()
        self.new_url.setPlaceholderText("https://github.com/user/repo")
        self.new_url.setFixedHeight(34)
        self.new_why = HoverLine()
        self.new_why.setPlaceholderText("why it is worth it")
        self.new_why.setFixedHeight(34)
        add = PillButton("ADD", accent=P.WHITE, filled=True, height=34)
        add.clicked.connect(self.add_repo)
        row.addWidget(self.new_name, 1)
        row.addWidget(self.new_url, 2)
        row.addWidget(self.new_why, 2)
        row.addWidget(add)
        holder = QWidget()
        holder.setLayout(row)
        self.form.addWidget(holder)

        self.group("search")
        self.search = self.text_field("Filter", "video, recon, mika...",
                                      "Filters the list as you type.")
        self.search.textChanged.connect(self.reload)

        self.group("list")
        self.list_host = QWidget()
        self.list_lay = QVBoxLayout(self.list_host)
        self.list_lay.setContentsMargins(0, 0, 0, 0)
        self.list_lay.setSpacing(8)
        self.form.addWidget(self.list_host)

        self.path = os.path.join(os.getcwd(), "repos.json")
        self.extra = []
        self.load()
        self.reload()

    def check_env(self):
        self.mark_ready("{} repo(s) · {}".format(len(REPO_SEED) + len(self.extra),
                                                 "local save" if os.path.exists(self.path)
                                                 else "no save yet"))

    def load(self):
        try:
            with open(self.path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            if isinstance(data, list):
                self.extra = [tuple(row) for row in data if len(row) >= 5]
        except Exception:
            self.extra = []

    def save(self):
        try:
            with open(self.path, "w", encoding="utf-8") as handle:
                json.dump(self.extra, handle, ensure_ascii=False, indent=2)
        except Exception as exc:
            self.console.append("[error] could not save: {}\n".format(exc), "err")

    def add_repo(self):
        name = self.new_name.text().strip()
        url = normalise(self.new_url.text())
        why = self.new_why.text().strip() or "no description"
        if not name or not url:
            self.console.append("[error] name and URL are required\n", "err")
            return
        self.extra.append((name, url, "MINE", why, "me"))
        self.save()
        self.new_name.clear()
        self.new_url.clear()
        self.new_why.clear()
        self.console.append("[ok] added {}\n".format(name), "ok")
        self.check_env()
        self.reload()

    def reload(self, *_):
        while self.list_lay.count():
            item = self.list_lay.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        needle = self.search.text().strip().lower()
        rows = REPO_SEED + self.extra
        shown = [row for row in rows
                 if not needle or needle in " ".join(row).lower()]
        for name, url, cat, why, author in shown:
            card = HoverFrame(P.CAT.get(cat, P.WHITE) if cat in P.CAT else P.START, 14)
            lay = QVBoxLayout(card)
            lay.setContentsMargins(14, 11, 14, 11)
            lay.setSpacing(4)
            top = QHBoxLayout()
            top.setSpacing(8)
            title = QLabel(name)
            title.setFont(QFont("Segoe UI", 10, QFont.Weight.Bold))
            title.setStyleSheet("color: {}; background: transparent; border: none;".format(P.TEXT))
            tag = QLabel(cat)
            tag.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
            tag.setStyleSheet("color: {}; background: transparent; border: none;".format(P.DIM))
            top.addWidget(title)
            top.addWidget(tag)
            top.addStretch()
            copy = PillButton("COPY", height=24)
            copy.clicked.connect(lambda _=False, u=url: (
                QApplication.clipboard().setText(u),
                self.console.append("[copy] {}\n".format(u), "dim")))
            open_btn = PillButton("OPEN", accent=P.WHITE, height=24)
            open_btn.clicked.connect(lambda _=False, u=url: QDesktopServices.openUrl(QUrl(u)))
            top.addWidget(copy)
            top.addWidget(open_btn)
            lay.addLayout(top)
            body = QLabel(why)
            body.setWordWrap(True)
            body.setFont(QFont("Segoe UI", 9))
            body.setStyleSheet("color: {}; background: transparent; border: none;".format(P.MUTED))
            lay.addWidget(body)
            foot = QLabel("{}  ·  {}".format(url, "by @" + author))
            foot.setFont(QFont("Consolas", 8))
            foot.setStyleSheet("color: {}; background: transparent; border: none;".format(P.DIM))
            lay.addWidget(foot)
            self.list_lay.addWidget(card)
        if not shown:
            empty = QLabel("nothing matches")
            empty.setStyleSheet("color: {};".format(P.DIM))
            self.list_lay.addWidget(empty)
        self.console.append("{} repo(s) visible\n".format(len(shown)), "dim")


class YtDlpPage(ToolPage):
    ACCENT = P.MEDIA

    def __init__(self):
        super().__init__(
            "yt-dlp", "yt-dlp", "↓", "download video and audio",
            "Paste a link and it saves the media to your disk. Audio mode rips an MP3 out of the "
            "video, so pick that if you only want the sound. ffmpeg is required for MP3 and for "
            "merging high quality streams.",
            "<h2 style='color:#b9a8ff'>yt-dlp</h2>"
            "<p><b>1.</b> Paste the video or playlist link.</p>"
            "<p><b>2.</b> Choose a preset. Audio only extracts an MP3.</p>"
            "<p><b>3.</b> Pick the output folder.</p>"
            "<p><b>4.</b> Press DOWNLOAD and watch the log.</p>"
            "<h3>Common problems</h3>"
            "<p><b>ffmpeg not found</b>: press INSTALL above. Without it, MP3 conversion and "
            "1080p+ merging cannot work.</p>"
            "<p><b>Missing formats</b>: YouTube needs a JavaScript runtime. Install deno from "
            "deno.com and yt-dlp will use it automatically.</p>"
            "<p><b>Age restricted</b>: add cookies with the flag "
            "<code>--cookies-from-browser chrome</code>.</p>")

        self.group("source")
        self.url = self.text_field("Target URL", "https://www.youtube.com/watch?v=...",
                                   "Full video, short link, or playlist URL.")
        self.group("options")
        self.preset = self.combo_field("Preset", [
            "Best video + audio", "Audio only (MP3 320k)",
            "Video 1080p max", "Video 4K max", "Whole playlist",
        ], "Higher quality needs ffmpeg to merge the separate video and audio streams.")
        self.out = self.path_field("Output folder", "dir",
                                   help_text="Where the file is saved.",
                                   value=os.path.join(os.path.expanduser("~"), "Downloads"))
        self.group("extras")
        self.c_subs = self.checkbox("Subtitles", "Downloads subtitle tracks and embeds them.")
        self.c_thumb = self.checkbox("Thumbnail", "Embeds the cover image into the file.")
        self.c_meta = self.checkbox("Metadata", "Writes title and artist tags.")
        self.c_rate = self.checkbox("Limit 1 MB/s", "Caps the speed so your connection stays usable.")
        self.check_row(self.c_subs, self.c_thumb, self.c_meta, self.c_rate)
        self.action("DOWNLOAD", self.start)

    def check_env(self):
        tool = resolve_binary("yt-dlp")
        ffmpeg = resolve_binary("ffmpeg")
        if tool and ffmpeg:
            self.mark_ready("yt-dlp + ffmpeg ready")
        elif tool:
            self.mark_missing("ffmpeg missing, MP3 will fail", False)
            self.btn_install.setVisible(True)
            self.btn_install.setText("GET FFMPEG")
            try:
                self.btn_install.clicked.disconnect()
            except TypeError:
                pass
            self.btn_install.clicked.connect(self.install_ffmpeg)
        else:
            self.mark_missing("yt-dlp not found")

    def install_ffmpeg(self):
        self.btn_install.setEnabled(False)
        self.bar.setVisible(True)
        self.installer = Installer("ffmpeg")
        self.installer.progress.connect(self.bar.setValue)
        self.installer.log.connect(self.console.append)
        self.installer.done.connect(self._installed)
        self.installer.start()

    def start(self):
        url = self.url.text().strip()
        if not url:
            self.console.append("[error] target URL is empty\n", "err")
            return
        exe_path = resolve_binary("yt-dlp")
        cmd = [exe_path] if exe_path else [sys.executable, "-m", "yt_dlp"]
        preset = self.preset.currentText()
        if "Audio" in preset:
            cmd += ["-x", "--audio-format", "mp3", "--audio-quality", "0"]
        elif "1080p" in preset:
            cmd += ["-f", "bestvideo[height<=1080]+bestaudio/best"]
        elif "4K" in preset:
            cmd += ["-f", "bestvideo[height<=2160]+bestaudio/best"]
        if self.c_subs.isChecked():
            cmd += ["--write-sub", "--embed-subs"]
        if self.c_thumb.isChecked():
            cmd.append("--embed-thumbnail")
        if self.c_meta.isChecked():
            cmd.append("--add-metadata")
        if self.c_rate.isChecked():
            cmd += ["-r", "1M"]
        ffmpeg = resolve_binary("ffmpeg")
        if ffmpeg:
            cmd += ["--ffmpeg-location", os.path.dirname(ffmpeg)]
        if self.out.text().strip():
            cmd += ["-P", self.out.text().strip()]
        cmd.append(url)
        self.run(cmd, "yt-dlp")


class FFmpegPage(ToolPage):
    ACCENT = P.MEDIA

    def __init__(self):
        super().__init__(
            "ffmpeg", "ffmpeg", "≡", "convert and compress media",
            "Turns one media file into another format, rips audio out of a video, shrinks file "
            "size or builds a GIF. Pick the input first, then the output path.",
            "<h2 style='color:#b9a8ff'>ffmpeg</h2>"
            "<p><b>1.</b> Choose the source file.</p>"
            "<p><b>2.</b> Pick what you want to produce.</p>"
            "<p><b>3.</b> Choose the output file name and press PROCESS.</p>"
            "<h3>Presets</h3>"
            "<p><b>MP4</b> is the safest format for phones and TVs.</p>"
            "<p><b>Extract MP3</b> keeps only the audio.</p>"
            "<p><b>Compress</b> lowers quality on purpose to save space.</p>"
            "<p><b>GIF</b> makes a short silent loop, best for clips under 10 seconds.</p>")

        self.group("input")
        self.src = self.path_field("Input file", "file",
                                   "Media (*.mp4 *.mkv *.mov *.avi *.webm *.mp3 *.wav *.m4a)",
                                   "The file you want to convert.")
        self.group("operation")
        self.preset = self.combo_field("Operation", [
            "MP4 (H.264 / AAC)", "Extract MP3", "Compress (CRF 28)", "Animated GIF", "WebM (VP9)",
        ], "Each option sets a different encoder and quality target.")
        self.group("output")
        self.dst = self.path_field("Output file", "save", "", "Full path with the new extension.")
        self.action("PROCESS", self.start)

    def check_env(self):
        tool = resolve_binary("ffmpeg")
        if tool:
            self.mark_ready(tool)
        else:
            self.mark_missing("ffmpeg not found", True)

    def start(self):
        src, dst = self.src.text().strip(), self.dst.text().strip()
        if not src or not dst:
            self.console.append("[error] input and output are both required\n", "err")
            return
        exe_path = resolve_binary("ffmpeg") or "ffmpeg"
        cmd = [exe_path, "-i", src]
        preset = self.preset.currentText()
        if "MP3" in preset:
            cmd += ["-vn", "-acodec", "libmp3lame", "-q:a", "2"]
        elif "Compress" in preset:
            cmd += ["-vcodec", "libx264", "-crf", "28", "-preset", "fast"]
        elif "GIF" in preset:
            cmd += ["-vf", "fps=12,scale=420:-1:flags=lanczos"]
        elif "WebM" in preset:
            cmd += ["-c:v", "libvpx-vp9", "-crf", "34", "-b:v", "0"]
        cmd += [dst, "-y"]
        self.run(cmd, "ffmpeg")


class NmapPage(ToolPage):
    ACCENT = P.NETWORK

    def __init__(self):
        super().__init__(
            "nmap", "nmap", "◈", "network discovery and port scan",
            "Asks a machine which ports are open and what software answers. Use a single IP for "
            "one host, a CIDR like 192.168.1.0/24 for a whole network, or a domain name. "
            "SYN and UDP scans need administrator rights.",
            "<h2 style='color:#b9a8ff'>nmap</h2>"
            "<p><b>1.</b> Type a target. For your own router: <code>192.168.1.1</code>.</p>"
            "<p><b>2.</b> Pick a profile. Quick is the safest first step.</p>"
            "<p><b>3.</b> Press SCAN and read the log.</p>"
            "<h3>What the profiles mean</h3>"
            "<p><b>Quick</b> checks the 100 most common ports.</p>"
            "<p><b>Intense</b> adds service versions, OS guessing and traceroute.</p>"
            "<p><b>Ping sweep</b> lists live hosts without touching ports.</p>"
            "<p><b>Full TCP</b> tests all 65535 ports, slow but complete.</p>"
            "<p><b>Vulnerability</b> runs NSE scripts that flag known weaknesses.</p>")

        self.group("target")
        self.target = self.text_field("Target", "192.168.1.1  ·  10.0.0.0/24  ·  example.com",
                                      "IP address, CIDR block or hostname.")
        self.group("profile")
        self.profile = self.combo_field("Profile", [
            "Quick (-F)", "Intense (-T4 -A -v)", "Ping sweep (-sn)",
            "Full TCP (-p 1-65535)", "Vulnerability scripts (--script vuln)",
            "OS and version (-sV -O)",
        ], "Start with Quick. Intense is loud and slow but tells you much more.")
        self.group("modifiers")
        self.c_syn = self.checkbox("SYN stealth (-sS)", "Half-open scan. Faster and less likely to "
                                                       "show in logs, but needs admin.")
        self.c_udp = self.checkbox("UDP (-sU)", "Checks UDP services like DNS. Very slow.")
        self.c_tr = self.checkbox("Traceroute", "Shows the routers between you and the target.")
        self.check_row(self.c_syn, self.c_udp, self.c_tr)
        self.action("SCAN", self.start)

    def check_env(self):
        tool = resolve_binary("nmap")
        if tool:
            self.mark_ready(tool)
        else:
            self.mark_missing("nmap not found", True)

    def start(self):
        target = self.target.text().strip()
        if not target:
            self.console.append("[error] target is empty\n", "err")
            return
        exe_path = resolve_binary("nmap") or "nmap"
        cmd = [exe_path]
        profile = self.profile.currentText()
        if "Quick" in profile:
            cmd.append("-F")
        elif "Intense" in profile:
            cmd += ["-T4", "-A", "-v"]
        elif "Ping" in profile:
            cmd.append("-sn")
        elif "Full TCP" in profile:
            cmd += ["-p", "1-65535", "-T4"]
        elif "Vulnerability" in profile:
            cmd += ["--script", "vuln", "-T4"]
        elif "OS and version" in profile:
            cmd += ["-sV", "-O"]
        if self.c_syn.isChecked():
            cmd.append("-sS")
        if self.c_udp.isChecked():
            cmd.append("-sU")
        if self.c_tr.isChecked():
            cmd.append("--traceroute")
        cmd.append(target)
        self.run(cmd, "nmap")


class DnsPage(ToolPage):
    ACCENT = P.NETWORK

    def __init__(self):
        super().__init__(
            "dns", "DNS Lookup", "⊙", "resolve names to every record type",
            "Queries A, AAAA, MX, TXT, SRV, CAA, DS and the rest against the resolver you pick. "
            "ANY dumps everything at once. Cloudflare and Google go over HTTPS so a lying local "
            "DNS cannot interfere.",
            "<h2 style='color:#b9a8ff'>DNS Lookup</h2>"
            "<p><b>1.</b> Type a domain, or a service name for SRV like "
            "<code>_sip._tcp.example.com</code>.</p>"
            "<p><b>2.</b> Pick the record type. ANY returns everything the resolver holds.</p>"
            "<p><b>3.</b> Choose a resolver and press LOOKUP.</p>"
            "<h3>Record types</h3>"
            "<p><b>A / AAAA</b> addresses. <b>CNAME</b> alias. <b>MX</b> mail with priority.</p>"
            "<p><b>TXT</b> verification and policy. <b>SRV</b> service location.</p>"
            "<p><b>CAA</b> allowed certificate authorities. <b>DS / DNSKEY</b> DNSSEC.</p>"
            "<p><b>TLSA / SSHFP</b> pinned keys. <b>NAPTR</b> rewrite rules.</p>"
            "<p><b>HTTPS / SVCB</b> modern service binding.</p>"
            "<h3>Status codes</h3>"
            "<p><b>NXDOMAIN</b> the name does not exist. <b>SERVFAIL</b> the resolver broke.</p>")

        self.group("query")
        self.host = self.text_field("Domain", "example.com", "No scheme, no paths, no wildcard.")
        self.rtype = self.combo_field("Record type", DNS_TYPES, "ANY dumps everything.")
        self.group("resolver")
        self.resolver = self.combo_field("Resolver", DNS_RESOLVERS,
                                         "DoH options bypass the local resolver.")
        self.action("LOOKUP", self.start)

    def check_env(self):
        self.mark_ready("built in resolver")

    def start(self):
        host = self.host.text().strip().replace("http://", "").replace("https://", "").strip("/")
        if not host:
            self.console.append("[error] domain is empty\n", "err")
            return
        rtype = self.rtype.currentText()
        resolver = self.resolver.currentText()

        def job(emit, should_stop):
            emit("{} {} via {}\n".format(host, rtype, resolver), "dim")
            if resolver == "System resolver":
                _dns_system(host, rtype, emit)
            else:
                _dns_doh(host, rtype, resolver, emit)

        self.run_python(job, "dns lookup")


class ZonePage(ToolPage):
    ACCENT = P.NETWORK

    def __init__(self):
        super().__init__(
            "zone", "Zone Transfer", "⇉", "try AXFR against name servers",
            "Lists the authoritative name servers and asks each one for a full zone copy. A "
            "permissive server dumps every record it holds in one shot.",
            "<h2 style='color:#b9a8ff'>Zone Transfer</h2>"
            "<p><b>1.</b> Enter the domain.</p>"
            "<p><b>2.</b> Press TRANSFER.</p>"
            "<h3>Notes</h3>"
            "<p>Most servers refuse AXFR. When one answers, you get the whole zone: hosts, mail, "
            "TXT and internal names.</p>"
            "<p>On Windows this uses <code>nslookup</code>, which only reports the servers. On "
            "Unix it runs <code>dig AXFR</code> per server.</p>")

        self.group("domain")
        self.domain = self.text_field("Domain", "example.com", "Base domain, no wildcard.")
        self.action("TRANSFER", self.start)

    def check_env(self):
        self.mark_ready("built in resolver")

    def start(self):
        domain = self.domain.text().strip().lower().strip(".")
        if not domain:
            self.console.append("[error] domain is empty\n", "err")
            return

        def job(emit, should_stop):
            emit("looking up name servers for {}\n".format(domain), "dim")
            if os.name == "nt":
                args = ["nslookup", "-type=NS", domain]
            else:
                args = ["dig", "+short", "NS", domain]
            try:
                res = subprocess.run(args, capture_output=True, text=True, timeout=25)
            except Exception as exc:
                emit("lookup failed: {}\n".format(exc), "err")
                return
            output = (res.stdout or "") + (res.stderr or "")
            servers = []
            if os.name == "nt":
                for line in output.splitlines():
                    if "nameserver" in line.lower():
                        part = line.split("=")[-1].strip().rstrip(".")
                        if part and part not in servers:
                            servers.append(part)
            else:
                servers = [l.strip().rstrip(".") for l in output.splitlines() if l.strip()]
            if not servers:
                emit("no name servers found\n", "warn")
                emit(output.strip()[:800] + "\n", "dim")
                return
            for server in servers:
                emit("ns  {}\n".format(server), "ok")
            if os.name == "nt":
                emit("\nWindows nslookup cannot AXFR, showing servers only\n", "dim")
                return
            for server in servers:
                if should_stop():
                    emit("stopped\n", "warn")
                    return
                emit("\n── AXFR {} ──\n".format(server), "dim")
                try:
                    res = subprocess.run(["dig", "+noall", "+answer", "AXFR", domain, "@" + server],
                                         capture_output=True, text=True, timeout=40)
                except Exception as exc:
                    emit("failed: {}\n".format(exc), "err")
                    continue
                body = (res.stdout or "").strip()
                if not body:
                    emit("refused\n", "warn")
                    continue
                for line in body.splitlines()[:400]:
                    emit("  {}\n".format(line.strip()), "out")
                emit("  {} line(s)\n".format(len(body.splitlines())), "accent")

        self.run_python(job, "zone transfer")


class PortPage(ToolPage):
    ACCENT = P.NETWORK

    def __init__(self):
        super().__init__(
            "ports", "Port Probe", "⊞", "fast TCP port check",
            "Tries to open a TCP connection to each port in the range and reports the ones that "
            "answer. No nmap needed, works anywhere Python runs. Keep the range small on remote "
            "hosts.",
            "<h2 style='color:#b9a8ff'>Port Probe</h2>"
            "<p><b>1.</b> Enter a host, IP or domain.</p>"
            "<p><b>2.</b> Set a small range first, like 20 to 120.</p>"
            "<p><b>3.</b> Press PROBE.</p>"
            "<h3>Reading results</h3>"
            "<p><b>open</b> something accepted the connection.</p>"
            "<p><b>closed</b> the host answered but nothing listens there.</p>"
            "<p><b>filtered</b> no answer, probably a firewall dropped the packet.</p>")

        self.group("target")
        self.host = self.text_field("Host", "192.168.1.1 or example.com", "Target machine.")
        self.group("range")
        self.start_port = self.number_field("First port", 1, 65535, 20, "Beginning of the range.")
        self.end_port = self.number_field("Last port", 1, 65535, 120, "End of the range, inclusive.")
        self.group("tuning")
        self.timeout = self.number_field("Timeout ms", 100, 3000, 400,
                                         "Higher means fewer false results but slower.")
        self.action("PROBE", self.start)

    def check_env(self):
        self.mark_ready("built in TCP probe")

    def start(self):
        host = self.host.text().strip()
        if not host:
            self.console.append("[error] host is empty\n", "err")
            return
        low, high = self.start_port.value(), self.end_port.value()
        if low > high:
            low, high = high, low
        timeout = self.timeout.value() / 1000.0
        total = high - low + 1
        found = []
        lock = threading.Lock()

        def probe(port):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            try:
                code = sock.connect_ex((host, port))
            except Exception:
                code = 1
            finally:
                sock.close()
            return port, code

        def job(emit, should_stop):
            emit("probing {} ports {}-{} on {}\n".format(total, low, high, host), "dim")
            done = 0
            with concurrent.futures.ThreadPoolExecutor(max_workers=120) as pool:
                futures = [pool.submit(probe, p) for p in range(low, high + 1)]
                for fut in concurrent.futures.as_completed(futures):
                    if should_stop():
                        emit("stopped early\n", "warn")
                        return
                    port, code = fut.result()
                    done += 1
                    if code == 0:
                        with lock:
                            found.append(port)
                        try:
                            name = socket.getservbyport(port, "tcp")
                        except OSError:
                            name = "unknown"
                        emit("{}  open  {}\n".format(port, name), "ok")
                    if done % 25 == 0:
                        emit("... {}/{}\n".format(done, total), "dim")
            emit("\n{} open port(s): {}\n".format(len(found), found or "none"), "accent")

        self.run_python(job, "port probe")


class SubnetPage(ToolPage):
    ACCENT = P.NETWORK

    def __init__(self):
        super().__init__(
            "subnet", "Subnet Calculator", "⊟", "split networks into ranges",
            "Takes an address in CIDR form and explains the network: usable range, broadcast, "
            "mask and how many hosts fit. Useful before scanning so you know the real size.",
            "<h2 style='color:#b9a8ff'>Subnet Calculator</h2>"
            "<p><b>1.</b> Type an address with a prefix, for example <code>192.168.1.0/24</code>.</p>"
            "<p><b>2.</b> Press CALCULATE.</p>"
            "<h3>The prefix</h3>"
            "<p><code>/24</code> is 254 usable hosts. <code>/25</code> is 126. <code>/30</code> is 2.</p>"
            "<p>The bigger the number after the slash, the smaller the network.</p>")

        self.group("network")
        self.cidr = self.text_field("Network", "192.168.1.0/24", "Address followed by /prefix.")
        self.group("split")
        self.split = self.number_field("Split into", 0, 22, 0,
                                       "0 keeps the network whole. 2 splits it into 4 parts.")
        self.action("CALCULATE", self.start)

    def check_env(self):
        self.mark_ready("built in calculator")

    def start(self):
        raw = self.cidr.text().strip()
        try:
            net = ipaddress.ip_network(raw, strict=False)
        except ValueError as exc:
            self.console.append("[error] {}\n".format(exc), "err")
            return

        def job(emit, should_stop):
            emit("network     {}\n".format(net.network_address), "ok")
            emit("broadcast   {}\n".format(net.broadcast_address), "ok")
            emit("mask        {}\n".format(net.netmask), "out")
            emit("wildcard    {}\n".format(net.hostmask), "out")
            emit("prefix      /{}\n".format(net.prefixlen), "out")
            emit("hosts       {}\n".format(max(net.num_addresses - 2, 0)), "accent")
            emit("version     IPv{}\n".format(net.version), "dim")
            if net.num_addresses > 2:
                emit("usable      {} - {}\n".format(net.network_address + 1,
                                                    net.broadcast_address - 1), "out")
            extra = self.split.value()
            if extra:
                parts = list(net.subnets(prefixlen_diff=extra))
                emit("\n{} subnets of /{}\n".format(len(parts), net.prefixlen + extra), "accent")
                for part in parts[:256]:
                    emit("  {}\n".format(part), "out")
                if len(parts) > 256:
                    emit("  ... {} more\n".format(len(parts) - 256), "dim")

        self.run_python(job, "subnet calculation")


class SubdomainPage(ToolPage):
    ACCENT = P.RECON

    def __init__(self):
        super().__init__(
            "subdomains", "Subdomain Finder", "◍", "enumerate hosts from certificates",
            "Pulls every hostname ever seen in a certificate for the domain, then resolves them. "
            "Certificate transparency catches staging boxes, mail servers and forgotten panels "
            "that no wordlist contains.",
            "<h2 style='color:#b9a8ff'>Subdomain Finder</h2>"
            "<p><b>1.</b> Enter the bare domain, <code>example.com</code>.</p>"
            "<p><b>2.</b> Keep crt.sh enabled for passive discovery.</p>"
            "<p><b>3.</b> Add a wordlist if you also want brute force.</p>"
            "<p><b>4.</b> Press ENUMERATE.</p>"
            "<h3>Reading results</h3>"
            "<p>Only <b>resolved</b> hosts get printed. Names that exist in certificates but no "
            "longer answer DNS are counted separately.</p>")

        self.group("domain")
        self.domain = self.text_field("Domain", "example.com", "Base domain, no wildcard, no path.")
        self.group("sources")
        self.use_crt = self.checkbox("Certificate transparency (crt.sh)",
                                     "Passive and free. Works without a wordlist.")
        self.use_crt.setChecked(True)
        self.wordlist = self.path_field("Wordlist", "file", "Text (*.txt *.lst)",
                                        "Optional. One candidate per line, resolved over DNS.")
        self.group("tuning")
        self.workers = self.number_field("Workers", 2, 64, 20, "Parallel DNS lookups.")
        self.action("ENUMERATE", self.start)

    def check_env(self):
        self.mark_ready("built in resolver")

    def start(self):
        domain = self.domain.text().strip().lower().strip(".")
        if not domain:
            self.console.append("[error] domain is empty\n", "err")
            return
        use_crt = self.use_crt.isChecked()
        wl = self.wordlist.text().strip()
        if not use_crt and not wl:
            self.console.append("[error] enable crt.sh or pick a wordlist\n", "err")
            return
        workers = self.workers.value()

        def job(emit, should_stop):
            names = set()
            if use_crt:
                emit("querying certificate transparency\n", "dim")
                query = urllib.parse.quote("%." + domain)
                req = urllib.request.Request(
                    "https://crt.sh/?q={}&output=json".format(query), headers=ua())
                try:
                    with urllib.request.urlopen(req, timeout=40) as res:
                        rows = json.loads(res.read().decode("utf-8", "replace"))
                    for row in rows:
                        for name in str(row.get("name_value", "")).split("\n"):
                            name = name.strip().lower().lstrip("*.")
                            if name.endswith(domain) and name != domain:
                                names.add(name)
                    emit("{} name(s) in certificates\n".format(len(names)), "dim")
                except Exception as exc:
                    emit("crt.sh failed: {}\n".format(exc), "err")
            if wl:
                emit("brute forcing from wordlist\n", "dim")
                try:
                    with open(wl, "r", encoding="utf-8", errors="replace") as f:
                        for line in f:
                            word = line.strip().lower()
                            if word and not word.startswith("#"):
                                names.add("{}.{}".format(word, domain))
                except Exception as exc:
                    emit("wordlist failed: {}\n".format(exc), "err")
            if not names:
                emit("nothing to test\n", "warn")
                return
            emit("testing {} candidate(s)\n\n".format(len(names)), "dim")
            found = []
            dead = 0
            lock = threading.Lock()

            def probe(name):
                try:
                    return name, socket.gethostbyname(name)
                except Exception:
                    return name, None

            with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
                futures = [pool.submit(probe, n) for n in sorted(names)]
                for fut in concurrent.futures.as_completed(futures):
                    if should_stop():
                        emit("stopped early\n", "warn")
                        return
                    name, addr = fut.result()
                    if addr:
                        with lock:
                            found.append(name)
                        emit("{}  {}\n".format(name, addr), "ok")
                    else:
                        dead += 1
            emit("\n{} live, {} without DNS\n".format(len(found), dead), "accent")

        self.run_python(job, "subdomain enumeration")


RULES = {
    "WordPress": ["wp-content", "wp-includes", "wp-json", "wp-emoji"],
    "Drupal": ["sites/default/files", "drupal.js", "drupalSettings"],
    "Joomla": ["/media/jui/", "com_content", "com_modules"],
    "Shopify": ["cdn.shopify.com", "myshopify", "shopify.theme"],
    "Wix": ["wix.com", "wixstatic"],
    "Squarespace": ["squarespace.com", "static1.squarespace"],
    "Webflow": ["webflow.com", "assets.website-files.com"],
    "Ghost": ["ghost.org", "content/images/20"],
    "Next.js": ["/_next/", "__next_data__"],
    "Nuxt": ["/_nuxt/", "__nuxt"],
    "SvelteKit": ["sveltekit", "/_app/immutable/"],
    "React": ["react-dom", "data-reactroot", "react.production"],
    "Vue": ["vue.js", "vue.min.js", "data-v-"],
    "Angular": ["ng-version", "angular.min.js", "runtime.js"],
    "Alpine": ["alpinejs", "x-data="],
    "htmx": ["htmx.org", "hx-get"],
    "jQuery": ["jquery.min.js", "jquery-3", "jquery-2"],
    "Bootstrap": ["bootstrap.min.css", "bootstrap.css"],
    "Tailwind": ["tailwindcss", "tailwind.min.css"],
    "Bulma": ["bulma.min.css", "bulma.css"],
    "Cloudflare": ["cf-ray", "__cf_bm", "cloudflare"],
    "Fastly": ["fastly", "x-served-by"],
    "Akamai": ["akamai", "ak-bmsc"],
    "Nginx": ["nginx"],
    "Apache": ["apache", "x-powered-by: php"],
    "LiteSpeed": ["litespeed"],
    "Vercel": ["vercel", "x-vercel"],
    "Netlify": ["netlify"],
    "GitHub Pages": ["github.io", "githubusercontent"],
    "Firebase": ["firebase", "firestore"],
    "Supabase": ["supabase"],
    "Google Analytics": ["gtag(", "google-analytics.com", "ga('create"],
    "Google Tag Manager": ["googletagmanager.com", "gtm.js"],
    "Meta Pixel": ["connect.facebook.net", "fbq("],
    "Hotjar": ["hotjar"],
    "Sentry": ["sentry.io", "sentry_dsn"],
    "Stripe": ["js.stripe.com", "stripe.js"],
    "PayPal": ["paypalobjects.com", "paypal.com/sdk"],
    "Algolia": ["algolia", "algolianet"],
    "Intercom": ["intercom"],
    "Typekit": ["use.typekit.net"],
    "Cloudinary": ["cloudinary.com"],
    "Disqus": ["disqus.com"],
    "reCAPTCHA": ["recaptcha", "gstatic.com/recaptcha"],
    "AWS S3": ["s3.amazonaws.com", ".amazonaws.com"],
    "PHP": ["x-powered-by: php", ".php?"],
    "ASP.NET": ["asp.net", "x-aspnet-version"],
    "Express": ["x-powered-by: express"],
    "Django": ["csrfmiddlewaretoken", "django"],
    "Rails": ["csrf-token", "action_dispatch"],
}

SOCIALS = ["twitter.com", "x.com", "facebook.com", "instagram.com", "linkedin.com",
           "youtube.com", "tiktok.com", "github.com", "discord.gg", "t.me",
           "pinterest.com", "reddit.com", "threads.net", "bsky.app", "mastodon"]

SECURITY = ["strict-transport-security", "content-security-policy", "x-frame-options",
            "x-content-type-options", "referrer-policy", "permissions-policy",
            "cross-origin-opener-policy", "cross-origin-embedder-policy"]


class SiteDnaPage(ToolPage):
    ACCENT = P.RECON

    def __init__(self):
        super().__init__(
            "sitedna", "Site DNA", "❖", "fingerprint a whole website",
            "One request, six reports: branding assets, tech stack, social and Open Graph "
            "metadata, typography, security headers and page weight. Everything comes from the "
            "HTML the server actually returned.",
            "<h2 style='color:#b9a8ff'>Site DNA</h2>"
            "<p><b>1.</b> Paste a full URL.</p>"
            "<p><b>2.</b> Pick which modules to run.</p>"
            "<p><b>3.</b> Press ANALYZE.</p>"
            "<h3>Modules</h3>"
            "<p><b>Branding</b> favicons, logos, theme colour.</p>"
            "<p><b>Stack</b> frameworks, CDNs, analytics.</p>"
            "<p><b>SEO</b> Open Graph and social presence.</p>"
            "<p><b>Typography</b> font families in use.</p>"
            "<p><b>Security</b> missing hardening headers.</p>"
            "<p><b>Performance</b> weight and asset count.</p>")

        self.group("target")
        self.url = self.text_field("URL", "https://example.com", "Include the scheme.")
        self.group("modules")
        self.c_brand = self.checkbox("Branding", "Favicons, logo files, theme colour, palette.")
        self.c_stack = self.checkbox("Tech stack", "Frameworks, CDNs, analytics, backends.")
        self.c_seo = self.checkbox("SEO and social", "Open Graph, Twitter cards, social links.")
        self.c_type = self.checkbox("Typography", "Font families and web font sources.")
        self.c_sec = self.checkbox("Security", "Which hardening headers are missing.")
        self.c_perf = self.checkbox("Performance", "Response time, page weight, asset counts.")
        self.check_row(self.c_brand, self.c_stack, self.c_seo)
        self.check_row(self.c_type, self.c_sec, self.c_perf)
        for cb in (self.c_brand, self.c_stack, self.c_seo, self.c_type, self.c_sec, self.c_perf):
            cb.setChecked(True)
        self.action("ANALYZE", self.start)

    def check_env(self):
        self.mark_ready("built in HTTP client")

    def start(self):
        url = normalise(self.url.text())
        if not url:
            self.console.append("[error] URL is empty\n", "err")
            return
        flags = {
            "brand": self.c_brand.isChecked(),
            "stack": self.c_stack.isChecked(),
            "seo": self.c_seo.isChecked(),
            "type": self.c_type.isChecked(),
            "sec": self.c_sec.isChecked(),
            "perf": self.c_perf.isChecked(),
        }

        def job(emit, should_stop):
            started = time.time()
            req = urllib.request.Request(url, headers=ua())
            try:
                with urllib.request.urlopen(req, timeout=25) as res:
                    raw = res.read(900_000)
                    headers = {k.lower(): v for k, v in res.headers.items()}
                    status = res.status
            except urllib.error.HTTPError as exc:
                raw = exc.read(400_000) or b""
                headers = {k.lower(): v for k, v in (exc.headers or {}).items()}
                status = exc.code
            except Exception as exc:
                emit("request failed: {}\n".format(exc), "err")
                return
            elapsed = time.time() - started
            html = raw.decode("utf-8", "replace")
            low = html.lower()
            emit("{}  {}  {}\n".format(status, urllib.parse.urlsplit(url).netloc,
                                       human_size(len(raw))), "accent")

            if flags["brand"]:
                emit("\n── branding ──\n", "dim")
                icons = re.findall(r'<link[^>]+rel=["\']?[^"\'>]*icon[^"\'>]*["\']?[^>]*>',
                                   html, re.I)
                for tag in icons[:10]:
                    href = re.search(r'href=["\']([^"\']+)', tag)
                    if href:
                        emit("icon  {}\n".format(urllib.parse.urljoin(url, href.group(1))), "out")
                for tag in re.findall(r'<meta[^>]+theme-color[^>]*>', html, re.I)[:3]:
                    colour = re.search(r'content=["\']([^"\']+)', tag)
                    if colour:
                        emit("theme {}\n".format(colour.group(1)), "out")
                for logo in re.findall(r'<img[^>]+(?:logo|brand)[^>]*>', html, re.I)[:6]:
                    src = re.search(r'src=["\']([^"\']+)', logo)
                    if src:
                        emit("logo  {}\n".format(urllib.parse.urljoin(url, src.group(1))), "out")
                palette = {}
                for colour in re.findall(r"#(?:[0-9a-f]{6}|[0-9a-f]{3})\b", low):
                    palette[colour] = palette.get(colour, 0) + 1
                top = sorted(palette.items(), key=lambda kv: -kv[1])[:6]
                if top:
                    emit("palette {}\n".format(", ".join("{} x{}".format(c, n) for c, n in top)),
                         "dim")
                if not icons and not palette:
                    emit("nothing found\n", "dim")

            if flags["stack"]:
                emit("\n── tech stack ──\n", "dim")
                haystack = low + "\n" + "\n".join("{}: {}".format(k, v) for k, v in headers.items())
                hits = 0
                for label, needles in RULES.items():
                    if any(n.lower() in haystack for n in needles):
                        emit("hit  {}\n".format(label), "ok")
                        hits += 1
                server = headers.get("server")
                if server:
                    emit("server header  {}\n".format(server), "out")
                powered = headers.get("x-powered-by")
                if powered:
                    emit("x-powered-by  {}\n".format(powered), "warn")
                if not hits:
                    emit("no known signature\n", "dim")

            if flags["seo"]:
                emit("\n── seo and social ──\n", "dim")
                title = re.search(r"<title[^>]*>(.*?)</title>", html, re.I | re.S)
                emit("title  {}\n".format((title.group(1).strip()[:120] if title else "none")), "out")
                desc = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)',
                                 html, re.I)
                emit("description  {}\n".format(desc.group(1)[:160] if desc else "none"), "out")
                for prop in ("og:title", "og:description", "og:image", "twitter:card",
                             "twitter:image"):
                    match = re.search(r'<meta[^>]+(?:property|name)=["\']{}["\'][^>]+content=["\']([^"\']*)'
                                      .format(re.escape(prop)), html, re.I)
                    if match:
                        emit("{}  {}\n".format(prop, match.group(1)[:140]), "out")
                links = re.findall(r'href=["\'](https?://[^"\']+)', html, re.I)
                socials = sorted({s for s in SOCIALS for l in links if s in l})
                emit("social  {}\n".format(", ".join(socials) or "none"),
                     "ok" if socials else "dim")

            if flags["type"]:
                emit("\n── typography ──\n", "dim")
                families = set()
                for block in re.findall(r"font-family\s*:\s*([^;}\"']+)", html, re.I):
                    for part in block.split(","):
                        name = part.strip().strip("\"'").lower()
                        if name and name not in ("inherit", "initial", "sans-serif", "serif"):
                            families.add(name)
                for family in re.findall(r"fonts\.googleapis\.com/css2?\?family=([^&\"']+)", html):
                    for part in urllib.parse.unquote(family).split("|"):
                        families.add(part.split(":")[0].replace("+", " "))
                for family in sorted(families)[:24]:
                    emit("font  {}\n".format(family), "out")
                if not families:
                    emit("no font declarations in markup\n", "dim")

            if flags["sec"]:
                emit("\n── security ──\n", "dim")
                present = [h for h in SECURITY if h in headers]
                missing = [h for h in SECURITY if h not in headers]
                emit("{}  {}\n".format(url.split(":")[0].upper(),
                                       "TLS" if url.startswith("https") else "plain text"),
                     "ok" if url.startswith("https") else "err")
                emit("present  {}\n".format(", ".join(present) or "none"),
                     "ok" if present else "dim")
                emit("missing  {}\n".format(", ".join(missing) or "none"),
                     "warn" if missing else "ok")
                cookies = headers.get("set-cookie", "")
                if cookies:
                    if "httponly" not in cookies.lower():
                        emit("cookie without HttpOnly\n", "warn")
                    if "secure" not in cookies.lower():
                        emit("cookie without Secure\n", "warn")

            if flags["perf"]:
                emit("\n── performance ──\n", "dim")
                emit("time       {:.0f} ms\n".format(elapsed * 1000),
                     "ok" if elapsed < 1.0 else "warn")
                emit("html       {}\n".format(human_size(len(raw))),
                     "ok" if len(raw) < 200_000 else "warn")
                for tag, label in (("script", "scripts"), ("link", "stylesheets"),
                                   ("img", "images"), ("iframe", "iframes")):
                    emit("{:<11}{}\n".format(label, len(re.findall("<" + tag, low))), "out")
                emit("inline js  {}\n".format(len(re.findall(r"<script(?![^>]*src)", low))), "dim")
                emit("dom nodes  ~{}\n".format(len(re.findall(r"<[a-z]", low))), "dim")

            emit("\nanalysis complete in {:.0f} ms\n".format(elapsed * 1000), "accent")

        self.run_python(job, "site dna")


class SslPage(ToolPage):
    ACCENT = P.RECON

    def __init__(self):
        super().__init__(
            "ssl", "TLS Inspector", "⛨", "read a certificate chain",
            "Opens a real TLS connection and prints the certificate the server presents: subject, "
            "issuer, validity, SANs and negotiated cipher. Expired or self signed certificates "
            "show up immediately.",
            "<h2 style='color:#b9a8ff'>TLS Inspector</h2>"
            "<p><b>1.</b> Enter the hostname without a scheme.</p>"
            "<p><b>2.</b> Keep port 443 unless it is a mail or custom service.</p>"
            "<p><b>3.</b> Press INSPECT.</p>"
            "<h3>What to look at</h3>"
            "<p><b>days left</b> under 14 is a renewal warning.</p>"
            "<p><b>SAN list</b> shows every name the certificate covers.</p>")

        self.group("target")
        self.host = self.text_field("Hostname", "example.com", "No scheme, no path.")
        self.port = self.number_field("Port", 1, 65535, 443, "Usually 443, 465 or 993.")
        self.group("options")
        self.c_chain = self.checkbox("Show raw chain", "Prints every certificate in the chain.")
        self.c_chain.setChecked(True)
        self.action("INSPECT", self.start)

    def check_env(self):
        self.mark_ready("built in TLS stack")

    def start(self):
        host = self.host.text().strip().replace("https://", "").split("/")[0]
        if not host:
            self.console.append("[error] hostname is empty\n", "err")
            return
        port = self.port.value()

        def job(emit, should_stop):
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            try:
                with socket.create_connection((host, port), timeout=15) as raw:
                    with context.wrap_socket(raw, server_hostname=host) as tls:
                        cert = tls.getpeercert()
                        emit("{}:{}  {}\n".format(host, port, tls.version() or "?"), "accent")
                        emit("cipher  {}\n".format(tls.cipher()[0]), "out")
                        chain = tls.get_verified_chain() if hasattr(tls, "get_verified_chain") else []
                        if not cert:
                            emit("no certificate presented\n", "err")
                            return
            except Exception as exc:
                emit("connection failed: {}\n".format(exc), "err")
                return
            emit("TLS handshake OK, certificate is not validated\n", "dim")

            subject = dict(x[0] for x in cert.get("subject", []))
            issuer = dict(x[0] for x in cert.get("issuer", []))
            emit("\nsubject  {}\n".format(subject.get("commonName", "?")), "out")
            for key, value in subject.items():
                if key != "commonName":
                    emit("  {} = {}\n".format(key, value), "dim")
            emit("issuer   {}\n".format(issuer.get("organizationName",
                                                   issuer.get("commonName", "?"))), "out")
            emit("serial   {}\n".format(cert.get("serialNumber", "?")), "dim")
            emit("valid    {}  to  {}\n".format(cert.get("notBefore"), cert.get("notAfter")), "out")
            try:
                end = ssl.cert_time_to_seconds(cert["notAfter"])
                days = (end - time.time()) / 86400.0
                emit("days left {:.0f}\n".format(days), "ok" if days > 14 else "err")
            except Exception:
                pass
            sans = [value for kind, value in cert.get("subjectAltName", []) if kind == "DNS"]
            emit("SANs     {}\n".format(", ".join(sans[:40]) or "none"),
                 "out" if sans else "warn")
            if sans and host not in sans and not any(
                    s.startswith("*.") and host.endswith(s[2:]) for s in sans):
                emit("hostname not covered by any SAN\n", "err")
            if self.c_chain.isChecked() and chain:
                emit("\nchain  {} certificate(s)\n".format(len(chain)), "dim")

        self.run_python(job, "tls inspection")


class RdapPage(ToolPage):
    ACCENT = P.RECON

    def __init__(self):
        super().__init__(
            "rdap", "RDAP Lookup", "◷", "registration data for domains and IPs",
            "RDAP is the modern WHOIS. It returns registrar, creation and expiry dates, status "
            "flags and name servers for a domain, or the allocation block for an IP.",
            "<h2 style='color:#b9a8ff'>RDAP Lookup</h2>"
            "<p><b>1.</b> Enter a domain or an IP.</p>"
            "<p><b>2.</b> Press QUERY.</p>"
            "<h3>Notes</h3>"
            "<p>Redacted contact data is normal after GDPR. Dates and status codes are the "
            "interesting part.</p>")

        self.group("target")
        self.query = self.text_field("Domain or IP", "example.com", "No scheme, no path.")
        self.action("QUERY", self.start)

    def check_env(self):
        self.mark_ready("RDAP bootstrap")

    def start(self):
        target = self.query.text().strip().replace("https://", "").split("/")[0]
        if not target:
            self.console.append("[error] target is empty\n", "err")
            return
        try:
            ipaddress.ip_address(target)
            kind = "ip"
        except ValueError:
            kind = "domain"

        def job(emit, should_stop):
            req = urllib.request.Request("https://rdap.org/{}/{}".format(kind, target), headers=ua())
            try:
                with urllib.request.urlopen(req, timeout=25) as res:
                    data = json.loads(res.read().decode("utf-8", "replace"))
            except Exception as exc:
                emit("query failed: {}\n".format(exc), "err")
                return
            emit("{}\n\n".format(data.get("ldhName") or data.get("handle") or target), "accent")
            for event in data.get("events", []):
                emit("{}  {}\n".format(event.get("eventAction", "?"), event.get("eventDate", "?")),
                     "out")
            for entity in data.get("entities", []):
                roles = ",".join(entity.get("roles", []))
                name = ""
                for item in entity.get("vcardArray", [[], []])[1] if entity.get("vcardArray") else []:
                    if item[0] == "fn":
                        name = item[3]
                if name:
                    emit("{}  {}\n".format(roles or "entity", name), "warn")
            for server in data.get("nameservers", []):
                emit("ns  {}\n".format(server.get("ldhName", "?")), "dim")
            for status in data.get("status", []):
                emit("status  {}\n".format(status), "out")
            if data.get("startAddress"):
                emit("range  {} - {}\n".format(data["startAddress"], data.get("endAddress", "?")), "out")
            if data.get("name"):
                emit("network  {}\n".format(data["name"]), "dim")
            if data.get("country"):
                emit("country  {}\n".format(data["country"]), "dim")

        self.run_python(job, "rdap query")


class IpInfoPage(ToolPage):
    ACCENT = P.RECON

    def __init__(self):
        super().__init__(
            "ipinfo", "IP Info", "◎", "geolocation and ownership",
            "Resolves a hostname and reports the address class, then asks a public API for "
            "country, city, provider and hosting or proxy flags.",
            "<h2 style='color:#b9a8ff'>IP Info</h2>"
            "<p><b>1.</b> Enter an IP or a hostname.</p>"
            "<p><b>2.</b> Press LOOKUP.</p>"
            "<h3>Private ranges</h3>"
            "<p>10.x, 172.16-31.x and 192.168.x never leave your network, so they have no "
            "geolocation.</p>")

        self.group("target")
        self.ip = self.text_field("IP or hostname", "8.8.8.8", "Hostnames are resolved first.")
        self.action("LOOKUP", self.start)

    def check_env(self):
        self.mark_ready("built in resolver")

    def start(self):
        target = self.ip.text().strip()
        if not target:
            self.console.append("[error] target is empty\n", "err")
            return

        def job(emit, should_stop):
            try:
                addr = ipaddress.ip_address(target)
                emit("{} is already an address\n".format(addr), "dim")
            except ValueError:
                try:
                    addr = ipaddress.ip_address(socket.gethostbyname(target))
                except Exception as exc:
                    emit("resolve failed: {}\n".format(exc), "err")
                    return
                emit("{} -> {}\n".format(target, addr), "dim")
            emit("class     {}\n".format("private" if addr.is_private else
                                         "loopback" if addr.is_loopback else
                                         "multicast" if addr.is_multicast else
                                         "reserved" if addr.is_reserved else "public"),
                 "warn" if addr.is_private else "ok")
            emit("version   IPv{}\n".format(addr.version), "dim")
            if addr.is_private or addr.is_loopback:
                emit("no public record for private space\n", "dim")
                return
            req = urllib.request.Request(
                "http://ip-api.com/json/{}?fields=status,message,country,regionName,city,zip,"
                "lat,lon,timezone,isp,org,as,reverse,mobile,proxy,hosting".format(addr),
                headers=ua())
            try:
                with urllib.request.urlopen(req, timeout=20) as res:
                    data = json.loads(res.read().decode())
            except Exception as exc:
                emit("lookup failed: {}\n".format(exc), "err")
                return
            if data.get("status") != "success":
                emit("api said: {}\n".format(data.get("message", "unknown")), "err")
                return
            for key, label in (("country", "country"), ("regionName", "region"),
                               ("city", "city"), ("zip", "postcode"),
                               ("timezone", "timezone"), ("isp", "isp"), ("org", "org"),
                               ("as", "asn"), ("reverse", "reverse")):
                if data.get(key):
                    emit("{:<9}{}\n".format(label, data[key]), "out")
            emit("{:<9}{}, {}\n".format("coords", data.get("lat"), data.get("lon")), "dim")
            emit("hosting   {}\n".format("yes" if data.get("hosting") else "no"),
                 "warn" if data.get("hosting") else "ok")
            emit("proxy     {}\n".format("yes" if data.get("proxy") else "no"),
                 "warn" if data.get("proxy") else "ok")

        self.run_python(job, "ip info")


class RobotsPage(ToolPage):
    ACCENT = P.RECON

    def __init__(self):
        super().__init__(
            "robots", "Robots and Sitemap", "⌗", "read crawl rules and sitemaps",
            "Fetches robots.txt and sitemap.xml and lists what the site hides from crawlers. "
            "Disallowed paths usually point straight at admin panels and staging folders.",
            "<h2 style='color:#b9a8ff'>Robots and Sitemap</h2>"
            "<p><b>1.</b> Enter the site root.</p>"
            "<p><b>2.</b> Press FETCH.</p>"
            "<h3>Why it matters</h3>"
            "<p>A <code>Disallow</code> line is a hint, not a lock. Anything listed is worth a "
            "manual look.</p>")

        self.group("target")
        self.url = self.text_field("Site root", "https://example.com", "Scheme and host only.")
        self.group("files")
        self.c_robots = self.checkbox("robots.txt", "Crawl directives and disallowed paths.")
        self.c_sitemap = self.checkbox("sitemap.xml", "Published URL list.")
        self.c_robots.setChecked(True)
        self.c_sitemap.setChecked(True)
        self.check_row(self.c_robots, self.c_sitemap)
        self.action("FETCH", self.start)

    def check_env(self):
        self.mark_ready("built in HTTP client")

    def start(self):
        base = normalise(self.url.text()).rstrip("/")
        if not base:
            self.console.append("[error] URL is empty\n", "err")
            return
        jobs = []
        if self.c_robots.isChecked():
            jobs.append(("/robots.txt", "robots"))
        if self.c_sitemap.isChecked():
            jobs.append(("/sitemap.xml", "sitemap"))
        if not jobs:
            self.console.append("[error] pick at least one file\n", "err")
            return

        def job(emit, should_stop):
            for path, label in jobs:
                emit("\n── {} ──\n".format(label), "dim")
                req = urllib.request.Request(base + path, headers=ua())
                try:
                    with urllib.request.urlopen(req, timeout=20) as res:
                        body = res.read(300_000).decode("utf-8", "replace")
                except urllib.error.HTTPError as exc:
                    emit("HTTP {}\n".format(exc.code), "warn" if exc.code != 404 else "dim")
                    continue
                except Exception as exc:
                    emit("failed: {}\n".format(exc), "err")
                    continue
                lines = [l.strip() for l in body.splitlines() if l.strip()]
                emit("{} line(s)\n".format(len(lines)), "dim")
                for line in lines[:250]:
                    if line.lower().startswith("disallow"):
                        emit("  {}\n".format(line), "warn")
                    elif line.lower().startswith(("allow", "sitemap")):
                        emit("  {}\n".format(line), "ok")
                    else:
                        emit("  {}\n".format(line), "out")
                if label == "sitemap":
                    locs = re.findall(r"<loc>\s*([^<\s]+)\s*</loc>", body)
                    emit("\n{} URL(s) in sitemap\n".format(len(locs)), "accent")
                    for loc in locs[:80]:
                        emit("  {}\n".format(loc), "dim")
                sitemaps = [l for l in lines if l.lower().startswith("sitemap")]
                if sitemaps and label == "robots":
                    emit("\ndeclared sitemaps: {}\n".format(len(sitemaps)), "accent")

        self.run_python(job, "robots fetch")


class HeadersPage(ToolPage):
    ACCENT = P.WEB

    def __init__(self):
        super().__init__(
            "headers", "HTTP Headers", "☰", "inspect server responses",
            "Fetches a URL and shows the status code and every response header, plus a short audit "
            "of the security headers that are missing. Good first look at any web server.",
            "<h2 style='color:#b9a8ff'>HTTP Headers</h2>"
            "<p><b>1.</b> Paste a full URL with http:// or https://.</p>"
            "<p><b>2.</b> Press FETCH.</p>"
            "<h3>What matters</h3>"
            "<p><b>server</b> and <b>x-powered-by</b> reveal the stack.</p>"
            "<p><b>strict-transport-security</b>, <b>content-security-policy</b> and "
            "<b>x-frame-options</b> are the ones a hardened site sends.</p>")

        self.group("request")
        self.url = self.text_field("URL", "https://example.com", "Include the scheme.")
        self.method = self.combo_field("Method", ["GET", "HEAD"], "HEAD only asks for headers.")
        self.group("options")
        self.follow = self.checkbox("Follow redirects", "Jumps to the final destination.")
        self.action("FETCH", self.start)

    def check_env(self):
        self.mark_ready("built in HTTP client")

    def start(self):
        url = normalise(self.url.text())
        if not url:
            self.console.append("[error] URL is empty\n", "err")
            return
        method = self.method.currentText()
        follow = self.follow.isChecked()
        audit = SECURITY

        def job(emit, should_stop):
            req = urllib.request.Request(url, method=method, headers=ua())
            handler = (urllib.request.HTTPRedirectHandler() if follow else
                       type("NoRedirect", (urllib.request.HTTPRedirectHandler,), {
                           "redirect_request": lambda *a, **k: None})())
            opener = urllib.request.build_opener(handler)
            try:
                with opener.open(req, timeout=20) as res:
                    emit("{} {}\n\n".format(res.status, res.reason), "ok")
                    for key, value in res.headers.items():
                        emit("{}: {}\n".format(key, value), "out")
                    present = [h for h in audit if res.headers.get(h)]
                    missing = [h for h in audit if h not in present]
            except urllib.error.HTTPError as exc:
                emit("{} {}\n\n".format(exc.code, exc.reason), "warn")
                for key, value in exc.headers.items():
                    emit("{}: {}\n".format(key, value), "out")
                present, missing = [], audit
            except Exception as exc:
                emit("request failed: {}\n".format(exc), "err")
                return
            emit("\nsecurity audit\n", "accent")
            emit("present: {}\n".format(", ".join(present) or "none"), "ok" if present else "dim")
            emit("missing: {}\n".format(", ".join(missing) or "none"), "warn" if missing else "ok")

        self.run_python(job, "header fetch")


class CorsPage(ToolPage):
    ACCENT = P.WEB

    def __init__(self):
        super().__init__(
            "cors", "CORS Checker", "⇋", "test cross origin policy",
            "Sends a request with a foreign Origin header and reads back the CORS response. A "
            "wildcard or a reflected origin on a credentialed endpoint is worth a second look.",
            "<h2 style='color:#b9a8ff'>CORS Checker</h2>"
            "<p><b>1.</b> Enter the URL to test.</p>"
            "<p><b>2.</b> Set the origin you want to pretend to come from.</p>"
            "<p><b>3.</b> Press TEST.</p>"
            "<h3>Reading it</h3>"
            "<p><b>Access-Control-Allow-Origin: *</b> is permissive but blocks credentials.</p>"
            "<p>A reflected origin plus <b>Allow-Credentials: true</b> is the risky combination.</p>")

        self.group("target")
        self.url = self.text_field("URL", "https://example.com/api/me", "Endpoint to test.")
        self.origin = self.text_field("Origin", "https://evil.example", "Origin to send.")
        self.group("options")
        self.method = self.combo_field("Method", ["GET", "POST", "OPTIONS"],
                                       "OPTIONS sends a preflight.")
        self.action("TEST", self.start)

    def check_env(self):
        self.mark_ready("built in HTTP client")

    def start(self):
        url = normalise(self.url.text())
        origin = self.origin.text().strip() or "https://evil.example"
        if not url:
            self.console.append("[error] URL is empty\n", "err")
            return
        method = self.method.currentText()

        def job(emit, should_stop):
            headers = ua()
            headers["Origin"] = origin
            if method == "OPTIONS":
                headers["Access-Control-Request-Method"] = "GET"
                headers["Access-Control-Request-Headers"] = "content-type"
            req = urllib.request.Request(url, method=method, headers=headers)
            opener = urllib.request.build_opener(
                type("NoRedirect", (urllib.request.HTTPRedirectHandler,), {
                    "redirect_request": lambda *a, **k: None})())
            try:
                with opener.open(req, timeout=20) as res:
                    emit("{} {}  sent Origin {}\n\n".format(res.status, res.reason, origin), "ok")
                    found = {k.lower(): v for k, v in res.headers.items()}
            except urllib.error.HTTPError as exc:
                emit("{} {}  sent Origin {}\n\n".format(exc.code, exc.reason, origin), "warn")
                found = {k.lower(): v for k, v in (exc.headers or {}).items()}
            except Exception as exc:
                emit("request failed: {}\n".format(exc), "err")
                return
            allow = found.get("access-control-allow-origin")
            creds = found.get("access-control-allow-credentials", "")
            methods = found.get("access-control-allow-methods", "")
            exposed = found.get("access-control-expose-headers", "")
            if allow is None:
                emit("no CORS headers, browser blocks cross origin reads\n", "warn")
            elif allow == "*":
                emit("allow-origin  *\n", "warn")
                emit("wildcard, credentials cannot be sent\n", "dim")
            elif allow == origin:
                emit("allow-origin  reflects the sent origin\n", "err")
            else:
                emit("allow-origin  {}\n".format(allow), "out")
            emit("credentials   {}\n".format(creds or "no"),
                 "err" if creds.lower() == "true" and allow == origin else "out")
            if methods:
                emit("methods       {}\n".format(methods), "out")
            if exposed:
                emit("exposed       {}\n".format(exposed), "dim")
            if allow == origin and creds.lower() == "true":
                emit("\nreflected origin with credentials, any site can read authenticated data\n",
                     "err")
            elif allow:
                emit("\nCORS is active, policy looks {} \n".format(
                    "loose" if allow == "*" or allow == origin else "restrictive"),
                    "warn" if allow == "*" or allow == origin else "ok")

        self.run_python(job, "cors check")


class SqlMapPage(ToolPage):
    ACCENT = P.WEB

    def __init__(self):
        super().__init__(
            "sqlmap", "sqlmap", "⛁", "SQL injection testing",
            "Feeds a URL with a parameter to sqlmap, which tries payloads until the database leaks "
            "something. The URL must contain a parameter, for example ?id=1.",
            "<h2 style='color:#b9a8ff'>sqlmap</h2>"
            "<p><b>1.</b> Copy a URL that has a parameter, like <code>item.php?id=1</code>.</p>"
            "<p><b>2.</b> Start on Standard.</p>"
            "<p><b>3.</b> Press TEST and let it run, it can take minutes.</p>"
            "<h3>Levels and risk</h3>"
            "<p><b>Level</b> is how many payloads get tried. <b>Risk</b> is how aggressive they are.</p>"
            "<p>Higher values find more but can be slow or write to the database.</p>")

        self.group("target")
        self.url = self.text_field("Target URL", "http://example.com/item.php?id=1",
                                   "Must include a query parameter.")
        self.group("aggression")
        self.profile = self.combo_field("Profile", [
            "Standard (level 1 / risk 1)", "Medium (level 3 / risk 2)",
            "Aggressive (level 5 / risk 3)",
        ], "Start low. Aggressive can take a very long time.")
        self.action("TEST", self.start)

    def check_env(self):
        self.mark_ready("sqlmap module")

    def start(self):
        url = self.url.text().strip()
        if not url:
            self.console.append("[error] URL is empty\n", "err")
            return
        cmd = [sys.executable, "-m", "sqlmap", "-u", url, "--batch"]
        profile = self.profile.currentText()
        if "Medium" in profile:
            cmd += ["--level=3", "--risk=2"]
        elif "Aggressive" in profile:
            cmd += ["--level=5", "--risk=3"]
        self.run(cmd, "sqlmap")


class FfufPage(ToolPage):
    ACCENT = P.WEB

    def __init__(self):
        super().__init__(
            "ffuf", "ffuf", "✳", "web content fuzzing",
            "Swaps the word FUZZ in the URL for every line of a wordlist and keeps the answers. "
            "That reveals hidden folders, files and parameters.",
            "<h2 style='color:#b9a8ff'>ffuf</h2>"
            "<p><b>1.</b> Put FUZZ where the word should go, for example "
            "<code>https://site.com/FUZZ</code>.</p>"
            "<p><b>2.</b> Choose a wordlist.</p>"
            "<p><b>3.</b> Press FUZZ.</p>"
            "<h3>Filtering noise</h3>"
            "<p>A 404 for everything is normal. Sort by status code and size to spot real hits.</p>")

        self.group("target")
        self.url = self.text_field("URL with FUZZ", "https://example.com/FUZZ",
                                   "FUZZ is the placeholder, it is required.")
        self.group("wordlist")
        self.wordlist = self.path_field("Wordlist", "file", "Text (*.txt *.lst)",
                                        "One candidate per line.")
        self.action("FUZZ", self.start)

    def check_env(self):
        tool = resolve_binary("ffuf")
        if tool:
            self.mark_ready(tool)
        else:
            self.mark_missing("ffuf not found", True)

    def start(self):
        url, wl = self.url.text().strip(), self.wordlist.text().strip()
        if "FUZZ" not in url or not wl:
            self.console.append("[error] the URL needs FUZZ and a wordlist is required\n", "err")
            return
        exe_path = resolve_binary("ffuf") or "ffuf"
        self.run([exe_path, "-u", url, "-w", wl, "-c"], "ffuf")


class UrlPage(ToolPage):
    ACCENT = P.WEB

    def __init__(self):
        super().__init__(
            "url", "URL Inspector", "⇢", "break a link into parts",
            "Parses a URL into scheme, host, path and parameters, expands the redirect chain, and "
            "encodes or decodes components. Useful to see where a shortened link really goes.",
            "<h2 style='color:#b9a8ff'>URL Inspector</h2>"
            "<p><b>1.</b> Paste a full URL.</p>"
            "<p><b>2.</b> Pick an operation.</p>"
            "<p><b>3.</b> Press RUN.</p>"
            "<h3>Redirects</h3>"
            "<p>The chain mode follows each hop and prints the status and target without loading "
            "the body.</p>")

        self.group("url")
        self.url = self.text_field("URL", "https://example.com/path?x=1", "Include the scheme.")
        self.group("operation")
        self.mode = self.combo_field("Mode", ["Parse", "Query parameters", "Follow redirects",
                                              "Encode component", "Decode component"],
                                     "Parse is the safe default.")
        self.action("RUN", self.start)

    def check_env(self):
        self.mark_ready("built in URL parser")

    def start(self):
        raw = self.url.text().strip()
        if not raw:
            self.console.append("[error] URL is empty\n", "err")
            return
        mode = self.mode.currentText()

        def job(emit, should_stop):
            if mode == "Encode component":
                emit("\n{}\n".format(urllib.parse.quote(raw, safe="")), "accent")
                return
            if mode == "Decode component":
                emit("\n{}\n".format(urllib.parse.unquote(raw)), "accent")
                return
            url = normalise(raw)
            parts = urllib.parse.urlsplit(url)
            if mode == "Parse":
                emit("scheme    {}\n".format(parts.scheme or "-"), "out")
                emit("userinfo  {}\n".format(parts.username or "-"), "dim")
                emit("host      {}\n".format(parts.hostname or "-"), "ok")
                emit("port      {}\n".format(parts.port or "-"), "out")
                emit("path      {}\n".format(parts.path or "/"), "out")
                emit("fragment  {}\n".format(parts.fragment or "-"), "dim")
                query = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
                emit("params    {}\n".format(len(query)), "accent")
                for key, value in query:
                    emit("  {} = {}\n".format(key, value), "dim")
                if parts.hostname:
                    try:
                        emit("\nresolves  {}\n".format(socket.gethostbyname(parts.hostname)), "ok")
                    except Exception:
                        emit("\nno DNS answer\n", "warn")
                return
            if mode == "Query parameters":
                query = urllib.parse.parse_qsl(parts.query, keep_blank_values=True)
                if not query:
                    emit("no query string\n", "warn")
                    return
                for index, (key, value) in enumerate(query, 1):
                    emit("{:>2}. {} = {}\n".format(index, key, value), "out")
                return
            emit("following redirects from {}\n\n".format(url), "dim")
            current = url
            for hop in range(1, 16):
                if should_stop():
                    emit("stopped\n", "warn")
                    return
                req = urllib.request.Request(current, method="HEAD", headers=ua())
                opener = urllib.request.build_opener(
                    type("NoRedirect", (urllib.request.HTTPRedirectHandler,), {
                        "redirect_request": lambda *a, **k: None})())
                try:
                    with opener.open(req, timeout=15) as res:
                        emit("{:>2}. {}  {}\n".format(hop, res.status, current), "ok")
                        break
                except urllib.error.HTTPError as exc:
                    target = exc.headers.get("location")
                    emit("{:>2}. {}  {}\n".format(hop, exc.code, current),
                         "warn" if target else "err")
                    if not target:
                        break
                    current = urllib.parse.urljoin(current, target)
                    emit("    -> {}\n".format(current), "dim")
                except Exception as exc:
                    emit("failed: {}\n".format(exc), "err")
                    break
            emit("\nfinal  {}\n".format(current), "accent")

        self.run_python(job, "url inspection")


class CookiePage(ToolPage):
    ACCENT = P.WEB

    def __init__(self):
        super().__init__(
            "cookie", "Cookie Parser", "◔", "read Set-Cookie headers",
            "Splits Set-Cookie headers into name, value and attributes, then flags the ones "
            "missing Secure, HttpOnly or SameSite. Also decodes common encoded values.",
            "<h2 style='color:#b9a8ff'>Cookie Parser</h2>"
            "<p><b>1.</b> Paste one or more Set-Cookie headers.</p>"
            "<p><b>2.</b> Press PARSE.</p>"
            "<h3>Attributes</h3>"
            "<p><b>HttpOnly</b> hides the cookie from JavaScript. <b>Secure</b> keeps it off plain "
            "HTTP. <b>SameSite</b> limits cross site sending.</p>")

        self.group("input")
        self.raw = self.text_area("Set-Cookie headers",
                                  "session=abc123; Path=/; HttpOnly",
                                  "One header per line.", height=130)
        self.group("options")
        self.c_decode = self.checkbox("Decode values", "Base64 and URL decode each value.")
        self.action("PARSE", self.start)

    def check_env(self):
        self.mark_ready("built in parser")

    def start(self):
        raw = self.raw.toPlainText().strip()
        if not raw:
            self.console.append("[error] nothing pasted\n", "err")
            return
        decode = self.c_decode.isChecked()

        def job(emit, should_stop):
            for line in raw.splitlines():
                line = line.strip()
                if not line:
                    continue
                chunks = [c.strip() for c in line.split(";")]
                head = chunks[0]
                name, _, value = head.partition("=")
                emit("\n{}\n".format(name.strip() or "?"), "accent")
                emit("  value  {}\n".format(value.strip()[:200]), "out")
                attrs = {c.split("=")[0].strip().lower(): c for c in chunks[1:]}
                for attr in ("domain", "path", "expires", "max-age"):
                    if attr in attrs:
                        emit("  {}  {}\n".format(attr, attrs[attr].split("=", 1)[-1]), "dim")
                emit("  HttpOnly  {}\n".format("yes" if "httponly" in attrs else "NO"),
                     "ok" if "httponly" in attrs else "warn")
                emit("  Secure    {}\n".format("yes" if "secure" in attrs else "NO"),
                     "ok" if "secure" in attrs else "warn")
                same = attrs.get("samesite")
                emit("  SameSite  {}\n".format(same.split("=", 1)[-1] if same else "NO"),
                     "ok" if same else "warn")
                if decode and value.strip():
                    for label, decoder in (("b64", lambda v: base64.b64decode(
                            v + "=" * (-len(v) % 4)).decode("utf-8", "replace")),
                            ("url", urllib.parse.unquote)):
                        try:
                            decoded = decoder(value.strip())
                            if decoded and decoded != value.strip():
                                emit("  {} decode  {}\n".format(label, decoded[:200]), "dim")
                        except Exception:
                            pass

        self.run_python(job, "cookie parsing")


class HashPage(ToolPage):
    ACCENT = P.DATA

    def __init__(self):
        super().__init__(
            "hash", "Hash Checker", "#", "verify file integrity",
            "Computes the fingerprint of a file and compares it with a hash you were given. If both "
            "match, the file is byte for byte the original.",
            "<h2 style='color:#b9a8ff'>Hash Checker</h2>"
            "<p><b>1.</b> Choose the file.</p>"
            "<p><b>2.</b> Pick the same algorithm the publisher used.</p>"
            "<p><b>3.</b> Paste their hash and press COMPARE.</p>"
            "<h3>Algorithms</h3>"
            "<p><b>SHA-256</b> is the normal choice today. <b>MD5</b> still shows up on old "
            "download pages.</p>")

        self.group("file")
        self.path = self.path_field("File", "file", "", "File to fingerprint.")
        self.group("check")
        self.algo = self.combo_field("Algorithm", ["sha256", "sha1", "md5", "sha512"],
                                     "Match whatever the source published.")
        self.expected = self.text_field("Expected hash", "paste the published hash",
                                        "Optional. Leave empty to only compute.")
        self.action("COMPARE", self.start)

    def check_env(self):
        self.mark_ready("built in hashing")

    def start(self):
        path = self.path.text().strip()
        if not path or not os.path.isfile(path):
            self.console.append("[error] pick an existing file\n", "err")
            return
        algo = self.algo.currentText()
        expected = self.expected.text().strip().lower()

        def job(emit, should_stop):
            digest = hashlib.new(algo)
            size = os.path.getsize(path)
            with open(path, "rb") as f:
                while True:
                    if should_stop():
                        emit("stopped\n", "warn")
                        return
                    block = f.read(1 << 20)
                    if not block:
                        break
                    digest.update(block)
            value = digest.hexdigest()
            emit("\n{}  {}\n".format(algo, value), "accent")
            emit("size  {}\n".format(human_size(size)), "dim")
            if expected:
                emit("MATCH, the file is identical\n" if value == expected
                     else "MISMATCH, the file differs\n", "ok" if value == expected else "err")

        self.run_python(job, "hashing")


class HashIdPage(ToolPage):
    ACCENT = P.DATA

    def __init__(self):
        super().__init__(
            "hashid", "Hash Identifier", "?", "guess a hash algorithm",
            "Looks at length and character set to suggest which algorithm produced a hash. Only a "
            "starting point, several algorithms share the same shape.",
            "<h2 style='color:#b9a8ff'>Hash Identifier</h2>"
            "<p><b>1.</b> Paste the hash.</p>"
            "<p><b>2.</b> Press IDENTIFY.</p>"
            "<h3>Reading the guess</h3>"
            "<p>Length is the strongest signal, prefixes like <code>$2b$</code> are decisive. "
            "Anything else is a candidate list.</p>")

        self.group("hash")
        self.value = self.text_field("Hash", "5f4dcc3b5aa765d61d8327deb882cf99",
                                     "Paste the full hash string.")
        self.action("IDENTIFY", self.start)

    def check_env(self):
        self.mark_ready("built in heuristics")

    def start(self):
        value = self.value.text().strip()
        if not value:
            self.console.append("[error] hash is empty\n", "err")
            return

        def job(emit, should_stop):
            emit("length {}\n".format(len(value)), "dim")
            prefixes = {"$2a$": "bcrypt", "$2b$": "bcrypt", "$2y$": "bcrypt",
                        "$argon2": "Argon2", "$6$": "sha512-crypt", "$5$": "sha256-crypt",
                        "$1$": "md5-crypt", "$y$": "yescrypt", "$P$": "phpass",
                        "{SSHA}": "SSHA", "{SHA}": "SHA-1 base64"}
            for prefix, name in prefixes.items():
                if value.startswith(prefix):
                    emit("\n{} (by prefix)\n".format(name), "ok")
                    return
            shapes = {
                16: ["MySQL 3.23 / DES crypt", "half of an MD5"],
                24: ["ObjectId", "truncated hash"],
                32: ["MD5", "MD4", "NTLM", "LM"],
                40: ["SHA-1", "RIPEMD-160", "MySQL 4.1"],
                48: ["SHA-384 truncated", "bcrypt base64 fragment"],
                56: ["SHA-224"],
                64: ["SHA-256", "SHA3-256", "BLAKE2s", "Keccak-256"],
                96: ["SHA-384"],
                128: ["SHA-512", "SHA3-512", "Whirlpool", "BLAKE2b"],
            }
            hexish = all(c in "0123456789abcdefABCDEF" for c in value)
            if not hexish:
                if all(c in string.ascii_letters + string.digits + "+/=" for c in value):
                    emit("\nnot hex, looks like base64 encoded digest\n", "warn")
                else:
                    emit("\ncontains unusual characters, may be salted or encoded\n", "warn")
                return
            guesses = shapes.get(len(value))
            if guesses:
                emit("\npossible:\n", "accent")
                for guess in guesses:
                    emit("  {}\n".format(guess), "out")
                emit("\nconfirm with a known plaintext test\n", "dim")
            else:
                emit("\nno standard algorithm matches this length\n", "warn")

        self.run_python(job, "hash identification")


class EncodePage(ToolPage):
    ACCENT = P.DATA

    def __init__(self):
        super().__init__(
            "encode", "Encoder", "⇄", "base64, hex and URL encoding",
            "Converts text between plain and encoded forms. Useful for reading payloads, cookies "
            "and long query strings.",
            "<h2 style='color:#b9a8ff'>Encoder</h2>"
            "<p><b>1.</b> Paste your text.</p>"
            "<p><b>2.</b> Choose a scheme and a direction.</p>"
            "<p><b>3.</b> Press RUN.</p>"
            "<h3>Schemes</h3>"
            "<p><b>Base64</b> hides text from a quick glance but does not encrypt it.</p>"
            "<p><b>Hex</b> shows the raw bytes. <b>URL</b> escapes characters so they survive in a "
            "link.</p>")

        self.group("text")
        self.text = self.text_area("Input", "paste here", "The text to transform.", height=110)
        self.group("scheme")
        self.scheme = self.combo_field("Scheme", ["Base64", "Base32", "Hex", "URL", "Binary"],
                                       "Encoding format.")
        self.direction = self.combo_field("Direction", ["Encode", "Decode"], "Which way.")
        self.action("RUN", self.start)

    def check_env(self):
        self.mark_ready("built in codecs")

    def start(self):
        raw = self.text.toPlainText()
        if not raw:
            self.console.append("[error] text is empty\n", "err")
            return
        scheme = self.scheme.currentText()
        encode = self.direction.currentText() == "Encode"

        def job(emit, should_stop):
            data = raw.encode()
            try:
                if scheme == "Base64":
                    out = base64.b64encode(data) if encode else base64.b64decode(data)
                elif scheme == "Base32":
                    out = base64.b32encode(data) if encode else base64.b32decode(data.upper())
                elif scheme == "Hex":
                    out = binascii.hexlify(data) if encode else binascii.unhexlify(raw.strip())
                elif scheme == "Binary":
                    out = (" ".join(format(b, "08b") for b in data) if encode else
                           bytes(int(p, 2) for p in raw.split()))
                else:
                    out = (urllib.parse.quote(raw, safe="") if encode
                           else urllib.parse.unquote(raw)).encode()
            except Exception as exc:
                emit("invalid input: {}\n".format(exc), "err")
                return
            emit("\n{}\n".format(out.decode(errors="replace")), "accent")
            emit("{} bytes\n".format(len(out)), "dim")

        self.run_python(job, "encoding")


class CodecPage(ToolPage):
    ACCENT = P.DATA

    def __init__(self):
        super().__init__(
            "codec", "Classic Ciphers", "✎", "rot, morse, atbash and more",
            "Toy ciphers and encodings for puzzles, CTFs and reading obfuscated text. None of this "
            "is real encryption.",
            "<h2 style='color:#b9a8ff'>Classic Ciphers</h2>"
            "<p><b>1.</b> Paste the text.</p>"
            "<p><b>2.</b> Pick a cipher and a direction.</p>"
            "<p><b>3.</b> Press RUN.</p>"
            "<h3>Caesar</h3>"
            "<p>The shift field matters only for Caesar. 13 is ROT13.</p>")

        self.group("text")
        self.text = self.text_area("Input", "paste here", "The text to transform.", height=110)
        self.group("cipher")
        self.scheme = self.combo_field("Cipher", ["Caesar", "Atbash", "Morse", "A1Z26", "Reverse"],
                                       "Caesar uses the shift below.")
        self.direction = self.combo_field("Direction", ["Encode", "Decode"], "Which way.")
        self.shift = self.number_field("Shift", 1, 25, 13, "Only used by Caesar.")
        self.action("RUN", self.start)

    def check_env(self):
        self.mark_ready("built in ciphers")

    def start(self):
        raw = self.text.toPlainText()
        if not raw:
            self.console.append("[error] text is empty\n", "err")
            return
        scheme = self.scheme.currentText()
        encode = self.direction.currentText() == "Encode"
        shift = self.shift.value()

        def caesar(text, n):
            out = []
            for ch in text:
                if ch.isupper():
                    out.append(chr((ord(ch) - 65 + n) % 26 + 65))
                elif ch.islower():
                    out.append(chr((ord(ch) - 97 + n) % 26 + 97))
                else:
                    out.append(ch)
            return "".join(out)

        def job(emit, should_stop):
            try:
                if scheme == "Caesar":
                    out = caesar(raw, shift if encode else -shift)
                elif scheme == "Atbash":
                    out = "".join(
                        chr(219 - ord(c)) if c.islower() else
                        chr(155 - ord(c)) if c.isupper() else c for c in raw)
                elif scheme == "Reverse":
                    out = raw[::-1]
                elif scheme == "Morse":
                    if encode:
                        out = " / ".join(
                            " ".join(MORSE.get(c.upper(), c) for c in word)
                            for word in raw.split(" "))
                    else:
                        out = " ".join(
                            "".join(MORSE_REV.get(code, code) for code in word.split(" "))
                            for word in raw.split("/")).strip()
                else:
                    if encode:
                        out = " ".join(
                            str(ord(c) - 96) if c.islower() else
                            str(ord(c) - 64) if c.isupper() else c for c in raw)
                    else:
                        out = "".join(
                            chr(int(p) + 96) if p.isdigit() and 1 <= int(p) <= 26 else p
                            for p in raw.split())
            except Exception as exc:
                emit("failed: {}\n".format(exc), "err")
                return
            emit("\n{}\n".format(out), "accent")

        self.run_python(job, "cipher")


class BaseConvPage(ToolPage):
    ACCENT = P.DATA

    def __init__(self):
        super().__init__(
            "base", "Base Converter", "⤨", "convert between number bases",
            "Translates an integer between binary, octal, decimal, hex and base 36. Also shows the "
            "ASCII character and byte layout of the value.",
            "<h2 style='color:#b9a8ff'>Base Converter</h2>"
            "<p><b>1.</b> Type the number.</p>"
            "<p><b>2.</b> Pick the source base and the target base.</p>"
            "<p><b>3.</b> Press CONVERT.</p>"
            "<h3>Example</h3>"
            "<p><code>255</code> from decimal is <code>ff</code> in hex and <code>11111111</code> "
            "in binary.</p>")

        self.group("value")
        self.value = self.text_field("Number", "255", "Digits valid for the source base.")
        self.group("bases")
        bases = ["2", "8", "10", "16", "36"]
        self.src = self.combo_field("From base", bases, "Base of the input.")
        self.src.setCurrentText("10")
        self.dst = self.combo_field("To base", bases, "Base of the output.")
        self.dst.setCurrentText("16")
        self.action("CONVERT", self.start)

    def check_env(self):
        self.mark_ready("built in integer maths")

    def start(self):
        raw = self.value.text().strip().replace(" ", "").replace("_", "")
        if not raw:
            self.console.append("[error] number is empty\n", "err")
            return
        try:
            number = int(raw, int(self.src.currentText()))
        except ValueError:
            self.console.append("[error] not a valid digit string for that base\n", "err")
            return
        target = int(self.dst.currentText())

        def job(emit, should_stop):
            digits = "0123456789abcdefghijklmnopqrstuvwxyz"
            if number == 0:
                out = "0"
            else:
                out = ""
                n = abs(number)
                while n:
                    out = digits[n % target] + out
                    n //= target
                if number < 0:
                    out = "-" + out
            emit("\n{}\n".format(out), "accent")
            emit("decimal   {}\n".format(number), "dim")
            emit("hex       {:x}\n".format(number), "dim")
            emit("binary    {:b}\n".format(number), "dim")
            if 0 < number < 0x110000:
                emit("codepoint U+{:04X}  {}\n".format(number, chr(number)), "out")
            if 0 < number < 256:
                emit("byte      0x{:02x}\n".format(number), "dim")

        self.run_python(job, "base conversion")


class LetterPage(ToolPage):
    ACCENT = P.DATA

    def __init__(self):
        super().__init__(
            "letters", "Letter Converter", "𝐀", "fancy unicode alphabets",
            "Rewrites text with Unicode lookalikes: bold, script, circled, fullwidth, small caps, "
            "upside down and more. Everything pastes straight into social bios.",
            "<h2 style='color:#b9a8ff'>Letter Converter</h2>"
            "<p><b>1.</b> Type your text.</p>"
            "<p><b>2.</b> Pick a style, or use ALL to preview every one.</p>"
            "<p><b>3.</b> Press CONVERT and copy from the log.</p>"
            "<h3>Compatibility</h3>"
            "<p>Some styles fall back to plain letters on fonts without coverage. Circled and "
            "fullwidth are the safest.</p>")

        self.group("text")
        self.text = self.text_area("Input", "hello world", "Plain text to restyle.", height=100)
        self.group("style")
        self.style = self.combo_field("Style", ["ALL"] + sorted(STYLES.keys()) + ["zalgo"],
                                      "ALL prints every style at once.")
        self.action("CONVERT", self.start)

    def check_env(self):
        self.mark_ready("built in tables")

    def start(self):
        raw = self.text.toPlainText()
        if not raw:
            self.console.append("[error] text is empty\n", "err")
            return
        style = self.style.currentText()

        def apply_style(text, key):
            if key == "zalgo":
                return "".join(
                    ch + "".join(random.choice(ZALGO) for _ in range(random.randint(0, 4)))
                    if ch != " " else ch for ch in text)
            if key == "upside down":
                table = STYLES[key]
                return "".join(table.get(c, c) for c in reversed(text))
            table = STYLES[key]
            return "".join(table.get(c, c) for c in text)

        def job(emit, should_stop):
            keys = sorted(STYLES.keys()) + ["zalgo"] if style == "ALL" else [style]
            for key in keys:
                emit("\n{}\n".format(key), "dim")
                emit("{}\n".format(apply_style(raw, key)), "accent")

        self.run_python(job, "letter conversion")


class TextPage(ToolPage):
    ACCENT = P.DATA

    def __init__(self):
        super().__init__(
            "text", "Text Tools", "¶", "case changes and statistics",
            "Switches case, sorts or dedupes lines, trims whitespace and counts characters, words "
            "and entropy. Handy before pasting text into a form.",
            "<h2 style='color:#b9a8ff'>Text Tools</h2>"
            "<p><b>1.</b> Paste your text.</p>"
            "<p><b>2.</b> Pick an operation.</p>"
            "<p><b>3.</b> Press RUN.</p>"
            "<h3>Statistics</h3>"
            "<p>Entropy is bits per character. Above 4.5 usually means random or compressed.</p>")

        self.group("text")
        self.text = self.text_area("Input", "paste here", "The text to process.", height=140)
        self.group("operation")
        self.mode = self.combo_field("Operation", [
            "UPPERCASE", "lowercase", "Title Case", "Sentence case", "iNVERT cASE",
            "Reverse", "Sort lines", "Dedupe lines", "Trim lines", "Statistics",
        ], "Statistics does not modify the text.")
        self.action("RUN", self.start)

    def check_env(self):
        self.mark_ready("built in text tools")

    def start(self):
        raw = self.text.toPlainText()
        if not raw:
            self.console.append("[error] text is empty\n", "err")
            return
        mode = self.mode.currentText()

        def job(emit, should_stop):
            if mode == "Statistics":
                words = len(raw.split())
                lines = len(raw.splitlines())
                counts = {}
                for ch in raw:
                    counts[ch] = counts.get(ch, 0) + 1
                entropy = -sum((n / len(raw)) * math.log2(n / len(raw))
                               for n in counts.values()) if raw else 0.0
                emit("characters  {}\n".format(len(raw)), "out")
                emit("without spaces {}\n".format(len(raw.replace(" ", ""))), "out")
                emit("words       {}\n".format(words), "out")
                emit("lines       {}\n".format(lines), "out")
                emit("bytes utf8  {}\n".format(len(raw.encode())), "dim")
                emit("unique chars {}\n".format(len(counts)), "dim")
                emit("entropy     {:.2f} bits/char\n".format(entropy),
                     "warn" if entropy > 4.5 else "ok")
                top = sorted(counts.items(), key=lambda kv: -kv[1])[:8]
                emit("common      {}\n".format(
                    " ".join("{}x{}".format(repr(c), n) for c, n in top)), "dim")
                return
            if mode == "UPPERCASE":
                out = raw.upper()
            elif mode == "lowercase":
                out = raw.lower()
            elif mode == "Title Case":
                out = raw.title()
            elif mode == "Sentence case":
                out = ". ".join(s.strip().capitalize() for s in raw.split("."))
            elif mode == "iNVERT cASE":
                out = raw.swapcase()
            elif mode == "Reverse":
                out = raw[::-1]
            elif mode == "Sort lines":
                out = "\n".join(sorted(raw.splitlines()))
            elif mode == "Dedupe lines":
                seen = []
                for line in raw.splitlines():
                    if line not in seen:
                        seen.append(line)
                out = "\n".join(seen)
            else:
                out = "\n".join(line.strip() for line in raw.splitlines() if line.strip())
            emit("\n{}\n".format(out), "accent")
            emit("{} characters\n".format(len(out)), "dim")

        self.run_python(job, "text processing")


class DiffPage(ToolPage):
    ACCENT = P.DATA

    def __init__(self):
        super().__init__(
            "diff", "Diff Checker", "≠", "compare two blocks of text",
            "Shows line by line what changed between two texts, with additions and removals "
            "marked. Useful for comparing configs, headers or responses.",
            "<h2 style='color:#b9a8ff'>Diff Checker</h2>"
            "<p><b>1.</b> Paste the original on the left.</p>"
            "<p><b>2.</b> Paste the changed version on the right.</p>"
            "<p><b>3.</b> Press COMPARE.</p>"
            "<h3>Output</h3>"
            "<p>Lines starting with <code>-</code> were removed, <code>+</code> were added.</p>")

        self.group("original")
        self.left = self.text_area("Original", "first version", None, 120)
        self.group("changed")
        self.right = self.text_area("Changed", "second version", None, 120)
        self.group("options")
        self.c_case = self.checkbox("Ignore case", "Treat A and a as the same.")
        self.c_space = self.checkbox("Ignore whitespace", "Collapse runs of spaces.")
        self.check_row(self.c_case, self.c_space)
        self.action("COMPARE", self.start)

    def check_env(self):
        self.mark_ready("built in difflib")

    def start(self):
        left = self.left.toPlainText()
        right = self.right.toPlainText()
        if not left and not right:
            self.console.append("[error] both sides are empty\n", "err")
            return
        ignore_case = self.c_case.isChecked()
        ignore_space = self.c_space.isChecked()

        def prep(text):
            lines = text.splitlines()
            if ignore_space:
                lines = [" ".join(line.split()) for line in lines]
            if ignore_case:
                lines = [line.lower() for line in lines]
            return lines

        def job(emit, should_stop):
            added = removed = 0
            for line in difflib.unified_diff(prep(left), prep(right), "original", "changed", n=2):
                if should_stop():
                    emit("stopped\n", "warn")
                    return
                if line.startswith("+++") or line.startswith("---"):
                    emit("{}\n".format(line.rstrip()), "dim")
                elif line.startswith("+"):
                    added += 1
                    emit("{}\n".format(line.rstrip()), "ok")
                elif line.startswith("-"):
                    removed += 1
                    emit("{}\n".format(line.rstrip()), "err")
                elif line.startswith("@@"):
                    emit("{}\n".format(line.rstrip()), "accent")
                else:
                    emit("{}\n".format(line.rstrip()), "dim")
            if not added and not removed:
                emit("\nidentical\n", "ok")
            else:
                emit("\n{} added, {} removed\n".format(added, removed), "accent")

        self.run_python(job, "diff")


class RegexPage(ToolPage):
    ACCENT = P.DATA

    def __init__(self):
        super().__init__(
            "regex", "Regex Tester", ".*", "test patterns against text",
            "Runs a regular expression over your sample text and lists every match with its "
            "position and groups. Compile errors are reported exactly.",
            "<h2 style='color:#b9a8ff'>Regex Tester</h2>"
            "<p><b>1.</b> Type a pattern.</p>"
            "<p><b>2.</b> Paste sample text.</p>"
            "<p><b>3.</b> Press TEST.</p>"
            "<h3>Groups</h3>"
            "<p>Capture groups print indented under each match. <code>findall</code> order follows "
            "the text.</p>")

        self.group("pattern")
        self.pattern = self.text_field("Pattern", r"\b\w+@\w+\.\w+", "Python regex syntax.")
        self.group("sample")
        self.subject = self.text_area("Sample text", "paste text to search", None, 130)
        self.group("flags")
        self.c_i = self.checkbox("Ignore case", "re.IGNORECASE")
        self.c_m = self.checkbox("Multiline", "re.MULTILINE, ^ and $ per line")
        self.c_s = self.checkbox("Dot matches newline", "re.DOTALL")
        self.check_row(self.c_i, self.c_m, self.c_s)
        self.action("TEST", self.start)

    def check_env(self):
        self.mark_ready("built in re module")

    def start(self):
        pattern = self.pattern.text()
        subject = self.subject.toPlainText()
        if not pattern:
            self.console.append("[error] pattern is empty\n", "err")
            return
        flags = 0
        if self.c_i.isChecked():
            flags |= re.IGNORECASE
        if self.c_m.isChecked():
            flags |= re.MULTILINE
        if self.c_s.isChecked():
            flags |= re.DOTALL

        def job(emit, should_stop):
            try:
                compiled = re.compile(pattern, flags)
            except re.error as exc:
                emit("compile error: {}\n".format(exc), "err")
                return
            matches = list(compiled.finditer(subject))
            if not matches:
                emit("no match\n", "warn")
                return
            for match in matches[:200]:
                line = subject.count("\n", 0, match.start()) + 1
                emit("{:>3}:{:<3} {}\n".format(line, match.start(), match.group(0)[:120]), "accent")
                for index, group in enumerate(match.groups(), 1):
                    emit("      group {}  {}\n".format(index, group), "dim")
            emit("\n{} match(es)\n".format(len(matches)), "ok")

        self.run_python(job, "regex test")


class JwtPage(ToolPage):
    ACCENT = P.DATA

    def __init__(self):
        super().__init__(
            "jwt", "JWT Decoder", "⬡", "read token claims",
            "Splits a JSON Web Token and decodes header and payload. Optionally verifies an HS256 "
            "signature and flags expired tokens.",
            "<h2 style='color:#b9a8ff'>JWT Decoder</h2>"
            "<p><b>1.</b> Paste the token.</p>"
            "<p><b>2.</b> Add the secret if you want the signature checked.</p>"
            "<p><b>3.</b> Press DECODE.</p>"
            "<h3>Reminder</h3>"
            "<p>Decoding is not verification. A token is only trusted after the signature checks "
            "out.</p>")

        self.group("token")
        self.token = self.text_area("Token", "eyJhbGciOi...", "The full three part token.", 110)
        self.group("verification")
        self.secret = self.text_field("HS256 secret", "optional", "Only works for HMAC tokens.")
        self.action("DECODE", self.start)

    def check_env(self):
        self.mark_ready("built in base64")

    def start(self):
        token = self.token.toPlainText().strip()
        if not token:
            self.console.append("[error] token is empty\n", "err")
            return
        secret = self.secret.text()

        def job(emit, should_stop):
            parts = token.split(".")
            if len(parts) != 3:
                emit("expected 3 segments, got {}\n".format(len(parts)), "err")
                return

            def decode(segment):
                return json.loads(base64.urlsafe_b64decode(
                    segment + "=" * (-len(segment) % 4)).decode("utf-8", "replace"))

            try:
                header = decode(parts[0])
                payload = decode(parts[1])
            except Exception as exc:
                emit("decode failed: {}\n".format(exc), "err")
                return
            emit("\nheader\n", "accent")
            emit("{}\n".format(json.dumps(header, indent=2)), "out")
            emit("\npayload\n", "accent")
            emit("{}\n".format(json.dumps(payload, indent=2)), "out")
            now = time.time()
            for claim, label in (("exp", "expires"), ("iat", "issued"), ("nbf", "not before")):
                if claim in payload:
                    try:
                        stamp = datetime.datetime.fromtimestamp(
                            payload[claim], datetime.timezone.utc)
                        emit("{}  {} UTC\n".format(label, stamp.strftime("%Y-%m-%d %H:%M:%S")),
                             "dim")
                    except Exception:
                        pass
            if "exp" in payload:
                if payload["exp"] < now:
                    emit("token EXPIRED\n", "err")
                else:
                    emit("valid for {:.0f} more minute(s)\n".format((payload["exp"] - now) / 60),
                         "ok")
            if header.get("alg") == "none":
                emit("alg is none, signature not enforced\n", "warn")
            if secret:
                import hmac
                signing = "{}.{}".format(parts[0], parts[1]).encode()
                expected = base64.urlsafe_b64encode(
                    hmac.new(secret.encode(), signing, hashlib.sha256).digest()
                ).rstrip(b"=").decode()
                emit("\nsignature {}\n".format("VALID" if expected == parts[2] else "INVALID"),
                     "ok" if expected == parts[2] else "err")

        self.run_python(job, "jwt decode")


class UuidPage(ToolPage):
    ACCENT = P.UTILS

    def __init__(self):
        super().__init__(
            "uuid", "Identifier Generator", "◇", "uuids and random tokens",
            "Generates identifiers with the system CSPRNG: UUID v4, hex strings, URL safe tokens or "
            "readable passphrases.",
            "<h2 style='color:#b9a8ff'>Identifier Generator</h2>"
            "<p><b>1.</b> Pick a format.</p>"
            "<p><b>2.</b> Set the count and size.</p>"
            "<p><b>3.</b> Press GENERATE.</p>"
            "<h3>Formats</h3>"
            "<p><b>UUID v4</b> is standard for records. <b>Token</b> is shorter and URL safe.</p>")

        self.group("format")
        self.kind = self.combo_field("Format", ["UUID v4", "UUID v7", "Hex string",
                                                "URL safe token", "Passphrase"],
                                     "Passphrase uses a small built in wordlist.")
        self.group("size")
        self.count = self.number_field("How many", 1, 100, 5, "Batch size.")
        self.size = self.number_field("Bytes", 4, 64, 16, "Ignored for UUIDs and passphrases.")
        self.words = self.number_field("Words", 3, 8, 4, "Only for passphrases.")
        self.action("GENERATE", self.start)

    def check_env(self):
        self.mark_ready("built in secrets module")

    def start(self):
        kind = self.kind.currentText()
        count = self.count.value()
        size = self.size.value()
        words = self.words.value()
        vocab = ("amber anchor basalt beacon cinder cobalt copper coral crimson delta drift "
                 "ember falcon flint garnet glacier granite harbor indigo ivory jasper kernel "
                 "lantern lunar marble meadow nectar nickel onyx opal orbit pebble quartz "
                 "raven ripple saffron slate solar summit thistle timber umber velvet walnut "
                 "willow zephyr").split()

        def job(emit, should_stop):
            for _ in range(count):
                if kind.startswith("UUID v4"):
                    emit("{}\n".format(uuid.uuid4()), "accent")
                elif kind.startswith("UUID v7"):
                    millis = int(time.time() * 1000)
                    rand = secrets.token_hex(12)
                    value = "{:012x}-{}-7{}-{}-{}".format(
                        millis, rand[:4], rand[4:7], "8" + rand[7:10], rand[10:22])
                    emit("{}\n".format(value), "accent")
                elif kind == "Hex string":
                    emit("{}\n".format(secrets.token_hex(size)), "accent")
                elif kind == "URL safe token":
                    emit("{}\n".format(secrets.token_urlsafe(size)), "accent")
                else:
                    emit("{}\n".format("-".join(secrets.choice(vocab) for _ in range(words))),
                         "accent")
            emit("\n{} item(s) from 8 bits of entropy per byte\n".format(count), "dim")

        self.run_python(job, "identifier generation")


class TimePage(ToolPage):
    ACCENT = P.UTILS

    def __init__(self):
        super().__init__(
            "time", "Timestamp Converter", "◷", "unix time and ISO 8601",
            "Converts between epoch seconds and ISO 8601 in UTC and local time, and breaks a "
            "timestamp into readable parts. Also reports the current epoch.",
            "<h2 style='color:#b9a8ff'>Timestamp Converter</h2>"
            "<p><b>1.</b> Enter a value.</p>"
            "<p><b>2.</b> Pick a direction.</p>"
            "<p><b>3.</b> Press CONVERT.</p>"
            "<h3>Units</h3>"
            "<p>Values with 13 digits are treated as milliseconds.</p>")

        self.group("value")
        self.value = self.text_field("Value", "1700000000",
                                     "Epoch seconds, milliseconds, or an ISO 8601 string.")
        self.group("direction")
        self.direction = self.combo_field("Direction", ["Epoch to date", "Date to epoch"],
                                          "Auto detects milliseconds.")
        self.action("CONVERT", self.start)

    def check_env(self):
        self.mark_ready("built in datetime")

    def start(self):
        raw = self.value.text().strip()
        if not raw:
            self.console.append("[error] value is empty\n", "err")
            return
        forward = self.direction.currentText().startswith("Epoch")

        def job(emit, should_stop):
            if forward:
                try:
                    number = float(raw)
                except ValueError:
                    emit("not a number\n", "err")
                    return
                if number > 1e11:
                    number /= 1000.0
                try:
                    stamp = datetime.datetime.fromtimestamp(number, datetime.timezone.utc)
                except Exception as exc:
                    emit("out of range: {}\n".format(exc), "err")
                    return
                emit("\n{}\n".format(stamp.strftime("%Y-%m-%d %H:%M:%S UTC")), "accent")
                emit("iso  {}\n".format(stamp.isoformat()), "out")
                emit("local  {}\n".format(
                    datetime.datetime.fromtimestamp(number).strftime("%Y-%m-%d %H:%M:%S")), "dim")
                emit("weekday {}\n".format(stamp.strftime("%A")), "dim")
                delta = number - time.time()
                emit("relative {}\n".format(
                    "in {:.0f} days".format(delta / 86400) if delta > 0
                    else "{:.0f} days ago".format(-delta / 86400)), "dim")
            else:
                text = raw.replace("Z", "+00:00")
                try:
                    parsed = datetime.datetime.fromisoformat(text)
                except ValueError:
                    try:
                        parsed = datetime.datetime.strptime(raw, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        emit("cannot parse, use ISO 8601\n", "err")
                        return
                if parsed.tzinfo is None:
                    parsed = parsed.replace(tzinfo=datetime.timezone.utc)
                emit("\n{}\n".format(int(parsed.timestamp())), "accent")
                emit("milliseconds  {}\n".format(int(parsed.timestamp() * 1000)), "dim")

        self.run_python(job, "timestamp conversion")


class PasswordPage(ToolPage):
    ACCENT = P.UTILS

    def __init__(self):
        super().__init__(
            "password", "Password Generator", "✦", "strong random passwords",
            "Builds passwords with the system's cryptographic randomness. Length and character sets "
            "are up to you.",
            "<h2 style='color:#b9a8ff'>Password Generator</h2>"
            "<p><b>1.</b> Set a length. 16 or more is a good default.</p>"
            "<p><b>2.</b> Pick the sets you want.</p>"
            "<p><b>3.</b> Press GENERATE and copy the result.</p>"
            "<h3>Rules of thumb</h3>"
            "<p>Length beats complexity. A long passphrase survives guessing far better.</p>"
            "<p>Nothing is stored. Copy before closing.</p>")

        self.group("size")
        self.length = self.number_field("Length", 6, 128, 20, "Characters. 16 minimum recommended.")
        self.count = self.number_field("How many", 1, 40, 5, "Batch size.")
        self.group("character sets")
        self.c_lower = self.checkbox("a-z", "Lowercase letters.")
        self.c_upper = self.checkbox("A-Z", "Uppercase letters.")
        self.c_digits = self.checkbox("0-9", "Digits.")
        self.c_symbols = self.checkbox("Symbols", "Punctuation.")
        self.check_row(self.c_lower, self.c_upper, self.c_digits, self.c_symbols)
        self.c_lower.setChecked(True)
        self.c_upper.setChecked(True)
        self.c_digits.setChecked(True)
        self.action("GENERATE", self.start)

    def check_env(self):
        self.mark_ready("built in secrets module")

    def start(self):
        pool = ""
        if self.c_lower.isChecked():
            pool += string.ascii_lowercase
        if self.c_upper.isChecked():
            pool += string.ascii_uppercase
        if self.c_digits.isChecked():
            pool += string.digits
        if self.c_symbols.isChecked():
            pool += "!@#$%^&*()-_=+[]{};:,.<>/?"
        if not pool:
            self.console.append("[error] select at least one character set\n", "err")
            return
        length, count = self.length.value(), self.count.value()

        def job(emit, should_stop):
            for _ in range(count):
                emit("".join(secrets.choice(pool) for _ in range(length)) + "\n", "accent")
            bits = math.log2(len(pool)) * length
            emit("\n~{:.0f} bits of entropy per password\n".format(bits),
                 "ok" if bits >= 80 else "warn")

        self.run_python(job, "password generation")


class ShredPage(ToolPage):
    ACCENT = P.UTILS

    def __init__(self):
        super().__init__(
            "shred", "File Shredder", "⌫", "overwrite files before deleting",
            "Deleting a file only drops the pointer. This overwrites the content with random bytes "
            "first, so recovery tools find nothing.",
            "<h2 style='color:#b9a8ff'>File Shredder</h2>"
            "<p><b>1.</b> Choose the file.</p>"
            "<p><b>2.</b> Pick passes. Three is enough for a normal disk.</p>"
            "<p><b>3.</b> Press SHRED. This is permanent.</p>"
            "<h3>Limits</h3>"
            "<p>On SSDs the controller spreads writes, so a shredder cannot always guarantee every "
            "block.</p>")

        self.group("file")
        self.path = self.path_field("File", "file", "", "File to destroy.")
        self.group("overwrite")
        self.passes = self.number_field("Passes", 1, 7, 3, "More passes means more writes.")
        self.action("SHRED", self.start)

    def check_env(self):
        self.mark_ready("built in overwrite")

    def start(self):
        path = self.path.text().strip()
        if not path or not os.path.isfile(path):
            self.console.append("[error] pick an existing file\n", "err")
            return
        passes = self.passes.value()

        def job(emit, should_stop):
            size = os.path.getsize(path)
            emit("{} · {}\n".format(path, human_size(size)), "dim")
            with open(path, "r+b") as f:
                for index in range(passes):
                    if should_stop():
                        emit("stopped, file kept\n", "warn")
                        return
                    f.seek(0)
                    left = size
                    while left > 0:
                        block = min(left, 1 << 20)
                        f.write(os.urandom(block))
                        left -= block
                    f.flush()
                    os.fsync(f.fileno())
                    emit("pass {}/{} done\n".format(index + 1, passes), "out")
            os.remove(path)
            emit("\nfile shredded and removed\n", "ok")

        self.run_python(job, "shredding")


class StatusPage(ToolPage):
    ACCENT = P.UTILS

    def __init__(self):
        super().__init__(
            "status", "Status Codes", "ℹ", "HTTP response reference",
            "Searchable reference of HTTP status codes with what they mean in practice and whether "
            "they are worth investigating during a review.",
            "<h2 style='color:#b9a8ff'>Status Codes</h2>"
            "<p><b>1.</b> Type a number or a word.</p>"
            "<p><b>2.</b> Press SEARCH.</p>"
            "<h3>Quick read</h3>"
            "<p><b>401/403</b> exist but are closed. <b>500</b> is a broken backend. <b>200</b> with "
            "a tiny body is often a soft 404.</p>")

        self.group("filter")
        self.filter = self.text_field("Filter", "403 or redirect", "Matches code or description.")
        self.action("SEARCH", self.start)

    def check_env(self):
        self.mark_ready("built in table")

    def start(self):
        needle = self.filter.text().strip().lower()
        table = [
            (100, "Continue", "interim, body follows"),
            (101, "Switching Protocols", "upgrade accepted"),
            (200, "OK", "normal success"),
            (201, "Created", "resource made"),
            (204, "No Content", "success without body"),
            (206, "Partial Content", "range request honoured"),
            (301, "Moved Permanently", "cached redirect, watch for loops"),
            (302, "Found", "temporary redirect"),
            (303, "See Other", "redirect with GET"),
            (304, "Not Modified", "conditional request hit"),
            (307, "Temporary Redirect", "method preserved"),
            (308, "Permanent Redirect", "method preserved and cached"),
            (400, "Bad Request", "malformed input"),
            (401, "Unauthorized", "authentication missing or wrong"),
            (403, "Forbidden", "authenticated but not allowed"),
            (404, "Not Found", "no such resource"),
            (405, "Method Not Allowed", "endpoint exists, verb wrong"),
            (406, "Not Acceptable", "content negotiation failed"),
            (408, "Request Timeout", "client too slow"),
            (409, "Conflict", "state clash"),
            (410, "Gone", "deliberately removed"),
            (413, "Payload Too Large", "body over limit"),
            (415, "Unsupported Media Type", "wrong content type"),
            (418, "I'm a teapot", "short and stout"),
            (422, "Unprocessable Entity", "valid syntax, bad semantics"),
            (429, "Too Many Requests", "rate limited"),
            (500, "Internal Server Error", "unhandled exception"),
            (501, "Not Implemented", "verb unsupported"),
            (502, "Bad Gateway", "upstream broke"),
            (503, "Service Unavailable", "overloaded or maintenance"),
            (504, "Gateway Timeout", "upstream too slow"),
            (505, "HTTP Version Not Supported", "protocol mismatch"),
        ]

        def job(emit, should_stop):
            hits = [row for row in table
                    if not needle or needle in str(row[0]) or needle in row[1].lower()
                    or needle in row[2].lower()]
            if not hits:
                emit("nothing matches\n", "warn")
                return
            for code, title, note in hits:
                level = "ok" if code < 300 else "warn" if code < 400 else "err" if code >= 500 else "out"
                emit("{:<4}{}\n".format(code, title), level)
                emit("    {}\n".format(note), "dim")
            emit("\n{} code(s)\n".format(len(hits)), "accent")

        self.run_python(job, "status reference")


REGISTRY = [
    ("overview", "START", "◆", "Overview", "", None),
    ("repos", "START", "★", "Repos", "recommended by friends", ReposPage),
    ("yt-dlp", "MEDIA", "↓", "yt-dlp", "download media", YtDlpPage),
    ("ffmpeg", "MEDIA", "≡", "ffmpeg", "convert media", FFmpegPage),
    ("gallerydl", "MEDIA", "▤", "gallery-dl", "download galleries", None),
    ("magick", "MEDIA", "◫", "ImageMagick", "resize and convert", None),
    ("mediainfo", "MEDIA", "◱", "MediaInfo", "read codecs", None),
    ("exiftool", "MEDIA", "⌾", "ExifTool", "metadata", None),
    ("sox", "MEDIA", "♪", "SoX", "audio processing", None),
    ("mkvmerge", "MEDIA", "◧", "MKVToolNix", "remux tracks", None),
    ("sevenzip", "MEDIA", "◨", "7-Zip", "archives", None),
    ("asciiart", "MEDIA", "▚", "ASCII Art", "image to text", None),
    ("nmap", "NETWORK", "◈", "nmap", "port scan", NmapPage),
    ("dns", "NETWORK", "⊙", "DNS Lookup", "resolve records", DnsPage),
    ("zone", "NETWORK", "⇉", "Zone Transfer", "AXFR attempt", ZonePage),
    ("ports", "NETWORK", "⊞", "Port Probe", "TCP check", PortPage),
    ("subnet", "NETWORK", "⊟", "Subnet", "CIDR math", SubnetPage),
    ("ping", "NETWORK", "◉", "Ping", "latency check", None),
    ("traceroute", "NETWORK", "⇢", "Traceroute", "path to host", None),
    ("whois", "NETWORK", "◷", "Whois", "registration", None),
    ("netcat", "NETWORK", "⋈", "Netcat", "raw TCP", None),
    ("tcpdump", "NETWORK", "≋", "Capture", "packet capture", None),
    ("iperf3", "NETWORK", "⇅", "iperf3", "bandwidth", None),
    ("macvendor", "NETWORK", "⌗", "MAC Vendor", "OUI lookup", None),
    ("ipv6", "NETWORK", "⊞", "IPv6 Tool", "address math", None),
    ("banner", "NETWORK", "⌁", "Banner Grab", "service banners", None),
    ("doh", "NETWORK", "⊙", "DoH", "resolve over https", None),
    ("dnssec", "NETWORK", "⛨", "DNSSEC", "DS records", None),
    ("rdns", "NETWORK", "↺", "Reverse DNS", "PTR lookup", None),
    ("subdomains", "RECON", "◍", "Subdomains", "certificate hosts", SubdomainPage),
    ("sitedna", "RECON", "❖", "Site DNA", "full site fingerprint", SiteDnaPage),
    ("ssl", "RECON", "⛨", "TLS Inspector", "certificate chain", SslPage),
    ("rdap", "RECON", "◷", "RDAP Lookup", "registration data", RdapPage),
    ("ipinfo", "RECON", "◎", "IP Info", "geolocation", IpInfoPage),
    ("robots", "RECON", "⌗", "Robots", "crawl rules", RobotsPage),
    ("securitytxt", "RECON", "✉", "security.txt", "security contact", None),
    ("wellknown", "RECON", "⌘", ".well-known", "standard paths", None),
    ("waf", "RECON", "⛒", "WAF Detect", "firewall probe", None),
    ("whatweb", "RECON", "❖", "WhatWeb", "web fingerprint", None),
    ("httpx", "RECON", "⌁", "httpx", "host probing", None),
    ("subfinder", "RECON", "◍", "Subfinder", "passive subs", None),
    ("nuclei", "RECON", "✳", "Nuclei", "templates", None),
    ("trufflehog", "RECON", "⌾", "TruffleHog", "secret scan", None),
    ("mailauth", "RECON", "✉", "Mail Auth", "SPF and DMARC", None),
    ("headers", "WEB", "☰", "HTTP Headers", "server inspection", HeadersPage),
    ("cors", "WEB", "⇋", "CORS Checker", "cross origin policy", CorsPage),
    ("sqlmap", "WEB", "⛁", "sqlmap", "SQL injection", SqlMapPage),
    ("ffuf", "WEB", "✳", "ffuf", "content fuzzing", FfufPage),
    ("url", "WEB", "⇢", "URL Inspector", "link breakdown", UrlPage),
    ("cookie", "WEB", "◔", "Cookie Parser", "header analysis", CookiePage),
    ("gobuster", "WEB", "⊞", "Gobuster", "path brute force", None),
    ("feroxbuster", "WEB", "⊟", "Feroxbuster", "recursive discovery", None),
    ("nikto", "WEB", "◈", "Nikto", "server scanner", None),
    ("curl", "WEB", "⇄", "cURL", "raw requests", None),
    ("httpmethods", "WEB", "⇄", "Method Probe", "verb testing", None),
    ("hash", "DATA", "#", "Hash Checker", "verify files", HashPage),
    ("hashid", "DATA", "?", "Hash ID", "identify digest", HashIdPage),
    ("encode", "DATA", "⇄", "Encoder", "base64 / hex / url", EncodePage),
    ("codec", "DATA", "✎", "Ciphers", "rot / morse / atbash", CodecPage),
    ("base", "DATA", "⤨", "Base Converter", "number bases", BaseConvPage),
    ("letters", "DATA", "𝐀", "Letters", "fancy unicode", LetterPage),
    ("text", "DATA", "¶", "Text Tools", "case and stats", TextPage),
    ("diff", "DATA", "≠", "Diff Checker", "compare text", DiffPage),
    ("regex", "DATA", ".*", "Regex Tester", "pattern testing", RegexPage),
    ("jwt", "DATA", "⬡", "JWT Decoder", "token claims", JwtPage),
    ("json", "DATA", "{}", "JSON Tool", "format and validate", None),
    ("yaml", "DATA", "⌸", "YAML Tool", "yaml to json", None),
    ("csv", "DATA", "▦", "CSV Inspector", "columns and stats", None),
    ("xml", "DATA", "◱", "XML Formatter", "indent markup", None),
    ("markdown", "DATA", "¶", "Markdown", "to html preview", None),
    ("lorem", "DATA", "≡", "Lorem Ipsum", "filler text", None),
    ("slug", "DATA", "⇢", "Slugifier", "clean slugs", None),
    ("wordfreq", "DATA", "¶", "Word Frequency", "keyword counts", None),
    ("vigenere", "DATA", "✎", "Vigenère", "key cipher", None),
    ("xor", "DATA", "⊕", "XOR Tool", "byte xor", None),
    ("crc32", "DATA", "⌗", "Checksums", "crc and adler", None),
    ("base58", "DATA", "⇄", "Base58", "bitcoin alphabet", None),
    ("roman", "DATA", "Ⅻ", "Roman Numerals", "convert numerals", None),
    ("unicode", "DATA", "𝐀", "Unicode Lookup", "codepoints", None),
    ("password", "UTILITIES", "✦", "Passwords", "generate secrets", PasswordPage),
    ("uuid", "UTILITIES", "◇", "Identifiers", "uuid and tokens", UuidPage),
    ("time", "UTILITIES", "◷", "Timestamps", "epoch conversion", TimePage),
    ("shred", "UTILITIES", "⌫", "Shredder", "destroy files", ShredPage),
    ("status", "UTILITIES", "ℹ", "Status Codes", "HTTP reference", StatusPage),
    ("unitconv", "UTILITIES", "⇄", "Units", "measurement math", None),
    ("timezone", "UTILITIES", "◷", "Timezone Grid", "zone offsets", None),
    ("rsa", "UTILITIES", "⛨", "RSA Keygen", "demo keypair", None),
    ("pem", "UTILITIES", "⛨", "PEM Inspector", "key fingerprint", None),
    ("split", "UTILITIES", "⌫", "File Split", "split and join", None),
    ("rename", "UTILITIES", "✎", "Batch Rename", "pattern rename", None),
    ("dupes", "UTILITIES", "≠", "Duplicates", "hash compare", None),
    ("dirsize", "UTILITIES", "⊟", "Folder Size", "disk usage", None),
]

TOOL_COUNT = len([r for r in REGISTRY if r[0] != "overview"])


class BootOverlay(QFrame):
    LINES = [
        ("[build] mate-toolkit v{}".format(VERSION), "ok"),
        ("[scan] registering modules ......... {} tools".format(TOOL_COUNT), "out"),
        ("[link] wiring pages and consoles", "dim"),
        ("[anim] preparing the motion layer", "dim"),
        ("[data] loading recommended repos", "dim"),
        ("[env] detecting local binaries", "dim"),
        ("[ready] all set", "ok"),
    ]

    def __init__(self, parent):
        super().__init__(parent)
        self.setStyleSheet("QFrame { background-color: #050505; border: none; }")
        lay = QVBoxLayout(self)
        lay.setContentsMargins(46, 40, 46, 34)
        lay.setSpacing(12)
        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)
        self.log.setFrameStyle(0)
        self.log.setFont(QFont("Consolas", 10))
        self.log.setStyleSheet(
            "QPlainTextEdit { background: #050505; color: #9fd8b4; border: none; }")
        lay.addWidget(self.log, 1)
        self.bar = QProgressBar()
        self.bar.setFixedHeight(3)
        self.bar.setTextVisible(False)
        self.bar.setRange(0, 100)
        self.bar.setStyleSheet(
            "QProgressBar { border: none; background: #121212; border-radius: 2px; }"
            "QProgressBar::chunk { background: #f1f1f1; border-radius: 2px; }")
        lay.addWidget(self.bar)
        self._fx = QGraphicsOpacityEffect(self)
        self.setGraphicsEffect(self._fx)
        self._index = 0
        self._timer = QTimer(self)
        self._timer.timeout.connect(self._step)
        self._timer.start(105)
        self.setGeometry(parent.rect())
        self.raise_()
        self.show()

    def _step(self):
        if self._index >= len(self.LINES):
            self._timer.stop()
            self.bar.setValue(100)
            QTimer.singleShot(320, self._out)
            return
        text, level = self.LINES[self._index]
        color = P.OK if level == "ok" else P.DIM if level == "dim" else "#cfcfcf"
        self.log.appendHtml('<span style="color:{};">{}</span>'.format(color, text))
        self._index += 1
        self.bar.setValue(int(100 * self._index / len(self.LINES)))

    def _out(self):
        anim = QVariantAnimation(self)
        anim.setStartValue(1.0)
        anim.setEndValue(0.0)
        anim.setDuration(320)
        anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        anim.valueChanged.connect(lambda v: self._fx.setOpacity(float(v)))
        anim.finished.connect(self.deleteLater)
        anim.start()


class Overview(QWidget):
    open_tool = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameStyle(0)
        scroll.setStyleSheet(
            "QScrollArea {{ background: transparent; border: none; }}"
            "QScrollBar:vertical {{ background: transparent; width: 6px; }}"
            "QScrollBar::handle:vertical {{ background: #242424; border-radius: 3px; }}"
            "QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}")
        outer.addWidget(scroll)

        host = QWidget()
        host.setStyleSheet("background: transparent;")
        root = QVBoxLayout(host)
        root.setContentsMargins(26, 22, 26, 22)
        root.setSpacing(14)
        scroll.setWidget(host)

        banner = HoverFrame(P.WHITE, 18)
        bl = QVBoxLayout(banner)
        bl.setContentsMargins(22, 20, 22, 20)
        bl.setSpacing(6)
        tag = QLabel("MATE-TOOLKIT  ·  v{}  ·  {} MODULES".format(VERSION, TOOL_COUNT))
        tag.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        tag.setStyleSheet("color: {}; background: transparent; border: none;".format(P.DIM))
        hero = QLabel("Overview")
        hero.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        hero.setStyleSheet("color: {}; background: transparent; border: none;".format(P.TEXT))
        sub = QLabel("CLIs wrapped in a GUI, nothing installs until you ask. Every option carries "
                     "a ? that expands animated and explains what it does before you touch it.")
        sub.setWordWrap(True)
        sub.setFont(QFont("Segoe UI", 8))
        sub.setStyleSheet("color: {}; background: transparent; border: none;".format(P.MUTED))
        bl.addWidget(tag)
        bl.addWidget(hero)
        bl.addWidget(sub)
        root.addWidget(banner)

        grid = QGridLayout()
        grid.setSpacing(12)
        cats = [
            ("MEDIA", P.MEDIA, "Download, convert and process media.",
             ["yt-dlp", "ffmpeg", "gallerydl", "magick", "mediainfo", "exiftool", "sox",
              "mkvmerge", "sevenzip", "asciiart"]),
            ("NETWORK", P.NETWORK, "Map hosts, ports and traffic.",
             ["nmap", "dns", "zone", "ports", "subnet", "ping", "traceroute", "whois",
              "netcat", "tcpdump", "iperf3", "macvendor", "ipv6", "banner", "doh", "dnssec",
              "rdns"]),
            ("RECON", P.RECON, "Profile the target before touching it.",
             ["subdomains", "sitedna", "ssl", "rdap", "ipinfo", "robots", "securitytxt",
              "wellknown", "waf", "whatweb", "httpx", "subfinder", "nuclei", "trufflehog",
              "mailauth"]),
            ("WEB", P.WEB, "Inspect and fuzz servers.",
             ["headers", "cors", "sqlmap", "ffuf", "url", "cookie", "gobuster", "feroxbuster",
              "nikto", "curl", "httpmethods"]),
            ("DATA", P.DATA, "Transform, compare and decode.",
             ["hash", "hashid", "encode", "codec", "base", "letters", "text", "diff", "regex",
              "jwt", "json", "yaml", "csv", "xml", "markdown", "lorem", "slug", "wordfreq",
              "vigenere", "xor", "crc32", "base58", "roman", "unicode"]),
            ("UTILITIES", P.UTILS, "Secrets, time and files.",
             ["password", "uuid", "time", "shred", "status", "unitconv", "timezone", "rsa",
              "pem", "split", "rename", "dupes", "dirsize"]),
        ]
        for column, (title, color, text, tools) in enumerate(cats):
            box = HoverFrame(color, 16)
            lay = QVBoxLayout(box)
            lay.setContentsMargins(18, 15, 18, 15)
            lay.setSpacing(4)
            head = QLabel(title)
            head.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
            head.setStyleSheet("color: {}; background: transparent; border: none;".format(color))
            body = QLabel(text)
            body.setWordWrap(True)
            body.setFont(QFont("Segoe UI", 8))
            body.setStyleSheet("color: {}; background: transparent; border: none;".format(P.MUTED))
            lay.addWidget(head)
            lay.addWidget(body)
            lay.addSpacing(8)
            for tool in tools:
                btn = QPushButton(tool.upper())
                btn.setCursor(Qt.CursorShape.PointingHandCursor)
                btn.setFont(QFont("Segoe UI", 8))
                btn.setFixedHeight(22)
                btn.setStyleSheet(
                    "QPushButton {{ background: transparent; color: {c}; border: none;"
                    " text-align: left; padding: 0 0 0 2px; }}"
                    "QPushButton:hover {{ color: {h}; padding-left: 8px; }}".format(c=P.TEXT, h=color))
                btn.clicked.connect(lambda _=False, t=tool: self.open_tool.emit(t))
                lay.addWidget(btn)
            lay.addStretch()
            grid.addWidget(box, column // 3, column % 3)
        root.addLayout(grid)

        tips = HoverFrame(P.GREEN, 16)
        tl = QVBoxLayout(tips)
        tl.setContentsMargins(18, 15, 18, 15)
        tl.setSpacing(5)
        head = QLabel("FIRST TIME")
        head.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        head.setStyleSheet("color: {}; background: transparent; border: none;".format(P.DIM))
        tl.addWidget(head)
        for text in [
            "Every external tool installs from its own INSTALL button. Nothing downloads by itself.",
            "Press the ? on any option: it expands animated with the explanation.",
            "The console folds with FOLD and grows by dragging the divider.",
            "Only scan or fuzz hosts that are yours or where you have written permission.",
            "Ctrl+F filters, Ctrl+Enter runs, Escape stops.",
        ]:
            row = QLabel("· " + text)
            row.setWordWrap(True)
            row.setFont(QFont("Segoe UI", 9))
            row.setStyleSheet("color: {}; background: transparent; border: none;".format(P.MUTED))
            tl.addWidget(row)
        root.addWidget(tips)
        root.addStretch()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mate-Toolkit")
        self.resize(1300, 880)
        self.setMinimumSize(1040, 720)
        self.setWindowIcon(build_icon())

        self.root = RootWidget()
        self.setCentralWidget(self.root)
        root = QVBoxLayout(self.root)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(10)

        header = QFrame()
        header.setObjectName("Header")
        header.setFixedHeight(56)
        hl = QHBoxLayout(header)
        hl.setContentsMargins(12, 0, 12, 0)
        hl.setSpacing(10)
        self.logo = LogoMark(26)
        self.logo.mousePressEvent = lambda e: self.play_intro()
        hl.addWidget(self.logo)
        name = QLabel("Mate-Toolkit")
        name.setFont(QFont("Segoe UI", 11, QFont.Weight.Bold))
        name.setStyleSheet("color: {}; background: transparent; border: none;".format(P.TEXT))
        hl.addWidget(name)
        hl.addSpacing(10)

        self.island = QFrame()
        self.island.setStyleSheet(
            "QFrame {{ background-color: {}; border: 1px solid {}; border-radius: 999px; }}".format(
                P.PANEL_2, P.BORDER))
        il = QHBoxLayout(self.island)
        il.setContentsMargins(12, 4, 14, 4)
        il.setSpacing(8)
        self.island_dot = PulseDot(P.WHITE, 7)
        self.island_label = QLabel("overview")
        self.island_label.setFont(QFont("Segoe UI", 8))
        self.island_label.setStyleSheet(
            "color: {}; background: transparent; border: none;".format(P.MUTED))
        il.addWidget(self.island_dot)
        il.addWidget(self.island_label)
        hl.addWidget(self.island)

        hl.addStretch()
        self.badge_admin = Badge("no admin", P.ERR, P.PANEL_3)
        hl.addWidget(self.badge_admin)
        hl.addWidget(Badge("v{}".format(VERSION), P.MUTED, P.PANEL_3))
        root.addWidget(header)

        body = QHBoxLayout()
        body.setSpacing(10)

        rail = QFrame()
        rail.setObjectName("Rail")
        rail.setFixedWidth(216)
        rl = QVBoxLayout(rail)
        rl.setContentsMargins(10, 12, 10, 12)
        rl.setSpacing(8)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Filter tools")
        self.search.setFixedHeight(32)
        self.search.setFont(QFont("Segoe UI", 9))
        self.search.setStyleSheet(
            "QLineEdit {{ background-color: {}; color: {}; border: 1px solid {};"
            " border-radius: 999px; padding: 0 14px; }}"
            "QLineEdit:hover {{ border-color: {}; }}"
            "QLineEdit:focus {{ border-color: {}; }}".format(
                P.BG, P.TEXT, P.BORDER, P.BORDER_HI, P.TEXT))
        self.search.textChanged.connect(self.filter_nav)
        rl.addWidget(self.search)

        nav_scroll = QScrollArea()
        nav_scroll.setWidgetResizable(True)
        nav_scroll.setFrameStyle(0)
        nav_scroll.setStyleSheet(
            "QScrollArea {{ background: transparent; border: none; }}"
            "QScrollBar:vertical {{ background: transparent; width: 5px; }}"
            "QScrollBar::handle:vertical {{ background: #242424; border-radius: 3px; }}"
            "QScrollBar::add-line, QScrollBar::sub-line {{ height: 0; }}")
        nav_host = QWidget()
        nav_host.setStyleSheet("background: transparent;")
        self.nav = QVBoxLayout(nav_host)
        self.nav.setContentsMargins(0, 0, 0, 0)
        self.nav.setSpacing(3)
        nav_scroll.setWidget(nav_host)
        rl.addWidget(nav_scroll, 1)

        self.count = QLabel("")
        self.count.setFont(QFont("Segoe UI", 8))
        self.count.setStyleSheet("color: {}; background: transparent; border: none;".format(P.DIM))
        self.count.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rl.addWidget(self.count)
        body.addWidget(rail)

        self.stack = QStackedWidget()
        body.addWidget(self.stack, 1)
        root.addLayout(body, 1)

        footer = QFrame()
        footer.setObjectName("Footer")
        fl = QVBoxLayout(footer)
        fl.setContentsMargins(16, 9, 16, 12)
        fl.setSpacing(7)
        top = QHBoxLayout()
        top.setSpacing(9)
        self.dot = PulseDot(P.WHITE, 9)
        self.status_label = QLabel("ready")
        self.status_label.setFont(QFont("Segoe UI", 9))
        self.status_label.setStyleSheet("color: {}; background: transparent; border: none;".format(P.MUTED))
        self.pct = QLabel("0 %")
        self.pct.setFont(QFont("Consolas", 8))
        self.pct.setStyleSheet("color: {}; background: transparent; border: none;".format(P.DIM))
        top.addWidget(self.dot)
        top.addWidget(self.status_label, 1)
        top.addWidget(self.pct)
        fl.addLayout(top)
        self.progress = QProgressBar()
        self.progress.setFixedHeight(3)
        self.progress.setTextVisible(False)
        self.progress.setRange(0, 100)
        self.progress.setStyleSheet(
            "QProgressBar {{ border: none; background-color: {}; border-radius: 2px; }}"
            "QProgressBar::chunk {{ background-color: {}; border-radius: 2px; }}".format(
                P.PANEL_3, P.WHITE))
        fl.addWidget(self.progress)
        root.addWidget(footer)

        self.setStyleSheet(self.sheet())

        self.pages = {}
        self.items = {}
        self.current = None
        self._anim = None
        self.boot = None
        self._build_pages()
        self.toast = Toast(self.root)
        self.check_admin()
        self.open("overview")
        QApplication.instance().installEventFilter(self)
        QTimer.singleShot(120, self.play_intro)
        QTimer.singleShot(0, self.fade_in)

    def sheet(self):
        return """
        QWidget#Root { background-color: %s; }
        QWidget { color: %s; font-family: 'Segoe UI'; }
        QLabel { background: transparent; border: none; }
        QFrame#Header, QFrame#Footer, QFrame#Rail {
            background-color: %s; border: 1px solid %s; border-radius: 16px;
        }
        QFrame#Rail { background-color: %s; }
        QToolTip {
            background-color: %s; color: %s; border: 1px solid %s;
            border-radius: 10px; padding: 6px;
        }
        """ % (P.BG, P.TEXT, P.PANEL, P.BORDER, P.RAIL, P.PANEL_2, P.TEXT, P.BORDER_HI)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.Type.MouseMove and self.root is not None:
            try:
                self.root.set_pointer(self.root.mapFromGlobal(event.globalPosition().toPoint()))
            except Exception:
                pass
        return super().eventFilter(obj, event)

    def _build_pages(self):
        overview = Overview()
        overview.open_tool.connect(self.open)
        self.stack.addWidget(overview)
        self.pages["overview"] = overview

        head = QLabel("START")
        head.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
        head.setStyleSheet(
            "color: {}; background: transparent; border: none; padding: 10px 4px 4px;".format(P.DIM))
        self.nav.addWidget(head)

        for tool_id, label, glyph in (("overview", "Overview", "◆"), ("repos", "Repos", "★")):
            page = self.pages.get(tool_id)
            if page is None:
                continue
            item = NavItem(glyph, label, P.START)
            item.setToolTip("Recommended repos" if tool_id == "repos" else "Start here")
            item.mousePressEvent = lambda e, t=tool_id, it=item: (it.press_fx(), self.open(t))
            self.items[tool_id] = (item, "START")
            self.nav.addWidget(item)

        section = None
        for tool_id, category, glyph, name, tagline, cls in REGISTRY[1:]:
            if tool_id == "repos":
                continue
            if category != section:
                section = category
                head = QLabel(category)
                head.setFont(QFont("Segoe UI", 7, QFont.Weight.Bold))
                head.setStyleSheet(
                    "color: {}; background: transparent; border: none; padding: 12px 4px 4px;".format(
                        tint(P.CAT.get(category, P.WHITE), 0.8)))
                self.nav.addWidget(head)

            if cls is None:
                found = next((s for s in SPECS if s["id"] == tool_id), None)
                page = DynamicPage(found) if found else None
            else:
                page = cls()
            if page is None:
                continue
            page.status.connect(self.set_status)
            self.pages[tool_id] = page
            self.stack.addWidget(page)

            item = NavItem(glyph, name, P.CAT.get(category, P.WHITE))
            item.setToolTip(tagline)
            item.mousePressEvent = lambda e, t=tool_id, it=item: (it.press_fx(), self.open(t))
            self.items[tool_id] = (item, category)
            self.nav.addWidget(item)

        self.nav.addStretch()
        self.count.setText("{} modules".format(TOOL_COUNT))

    def play_intro(self):
        if self.boot is not None:
            return
        self.boot = BootOverlay(self.root)
        self.boot.destroyed.connect(lambda: setattr(self, "boot", None))

    def filter_nav(self, text):
        needle = text.strip().lower()
        for item, _cat in self.items.values():
            item.setVisible(not needle or needle in item.label.text().lower())

    def open(self, tool_id):
        page = self.pages.get(tool_id)
        if not page or page is self.current:
            return
        try:
            for tid, (item, _cat) in self.items.items():
                item.set_active(tid == tool_id)
            previous = self.current
            self.current = page
            self.island_label.setText(getattr(page, "name", tool_id).lower())
            self.set_status("ready", "info", 0.0)

            if previous is None:
                self.stack.setCurrentWidget(page)
                if isinstance(page, ToolPage):
                    QTimer.singleShot(80, page.reveal)
                return

            snapshot = self.stack.grab()
            overlay = QLabel(self.stack)
            overlay.setPixmap(snapshot)
            overlay.setGeometry(self.stack.rect())
            overlay.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, True)
            overlay.show()
            overlay.raise_()
            self.stack.setCurrentWidget(page)

            fx = QGraphicsOpacityEffect(overlay)
            overlay.setGraphicsEffect(fx)
            anim = QPropertyAnimation(fx, b"opacity", self)
            anim.setDuration(180)
            anim.setStartValue(1.0)
            anim.setEndValue(0.0)
            anim.setEasingCurve(QEasingCurve.Type.OutQuad)
            anim.finished.connect(overlay.deleteLater)
            anim.start()
            self._anim = anim
            if isinstance(page, ToolPage):
                QTimer.singleShot(70, page.reveal)
        except Exception:
            traceback.print_exc()

    def set_status(self, text, level="info", value=None):
        color = {"info": P.MUTED, "ok": P.OK, "warn": P.WARN, "err": P.ERR}.get(level, P.MUTED)
        self.status_label.setText(text)
        self.status_label.setStyleSheet(
            "color: {}; background: transparent; border: none;".format(color))
        self.dot.set_color(color)
        self.island_dot.set_color(color)
        if value is not None:
            anim = QPropertyAnimation(self.progress, b"value", self)
            anim.setDuration(220)
            anim.setStartValue(self.progress.value())
            anim.setEndValue(int(max(0.0, min(1.0, value)) * 100))
            anim.valueChanged.connect(lambda v: self.pct.setText("{} %".format(int(v))))
            anim.start()
            self._prog = anim
        if level in ("ok", "err") and text:
            self.toast.show_message(text[:70], level)

    def check_admin(self):
        try:
            import ctypes
            admin = bool(ctypes.windll.shell32.IsUserAnAdmin())
        except Exception:
            admin = False
        self.badge_admin.set_state("admin" if admin else "no admin",
                                   P.OK if admin else P.ERR, P.PANEL_3)

    def fade_in(self):
        self.setWindowOpacity(0.0)
        anim = QPropertyAnimation(self, b"windowOpacity", self)
        anim.setDuration(240)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        self._fade = anim

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            if isinstance(self.current, ToolPage):
                self.current.stop()
            else:
                self.open("overview")
        elif event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter) and \
                event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            if isinstance(self.current, ToolPage):
                for button in self.current.findChildren(QPushButton):
                    if button.height() == 40 and button.isEnabled():
                        button.click()
                        break
        elif event.key() == Qt.Key.Key_F and \
                event.modifiers() & Qt.KeyboardModifier.ControlModifier:
            self.search.setFocus()
            self.search.selectAll()
        super().keyPressEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        if self.boot is not None:
            self.boot.setGeometry(self.root.rect())
        if hasattr(self, "toast") and self.toast.isVisible():
            self.toast._place()


def main():
    sys.excepthook = lambda t, v, tb: traceback.print_exception(t, v, tb)
    if os.name == "nt":
        try:
            import ctypes
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("MateAG.MultiToolkit")
        except Exception:
            pass
    app = QApplication(sys.argv)
    app.setApplicationName("Mate-Toolkit")
    app.setWindowIcon(build_icon())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()