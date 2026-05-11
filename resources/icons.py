"""Définitions des icônes SVG pour la toolbar"""

from PySide6.QtGui import QIcon, QPixmap, QPainter
from PySide6.QtCore import Qt
from PySide6.QtSvg import QSvgRenderer


# Définitions SVG des icônes
SVG_STATE = '''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <circle cx="32" cy="32" r="20" fill="none" stroke="#111111" stroke-width="2"/>
</svg>'''

SVG_TRANSITION = '''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <path d="M 10 32 L 50 32" stroke="black" stroke-width="2" fill="none"/>
    <path d="M 45 27 L 54 32 L 45 37 Z" fill="black"/>
</svg>'''

SVG_ACTION = '''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <rect x="12" y="12" width="40" height="40" fill="none" stroke="black" stroke-width="2" rx="4"/>
    <text x="32" y="40" text-anchor="middle" fill="black" font-size="20" font-weight="bold">A</text>
</svg>'''

SVG_CLOCK = '''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <circle cx="32" cy="32" r="24" fill="none" stroke="black" stroke-width="2"/>
    <line x1="32" y1="16" x2="32" y2="24" stroke="black" stroke-width="2"/>
    <line x1="32" y1="32" x2="44" y2="32" stroke="black" stroke-width="2"/>
</svg>'''

SVG_PLUS = '''<svg viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
    <line x1="32" y1="8" x2="32" y2="56" stroke="black" stroke-width="3" stroke-linecap="round"/>
    <line x1="8" y1="32" x2="56" y2="32" stroke="black" stroke-width="3" stroke-linecap="round"/>
</svg>'''


def svg_to_icon(svg_data: str) -> QIcon:
    """Convertit une chaîne SVG en QIcon"""
    pixmap = QPixmap(64, 64)
    pixmap.fill(Qt.transparent)
    
    renderer = QSvgRenderer(svg_data.encode())
    painter = QPainter(pixmap)
    renderer.render(painter)
    painter.end()
    
    return QIcon(pixmap)


def get_icons():
    """Retourne un dictionnaire avec toutes les icônes"""
    return {
        "state": svg_to_icon(SVG_STATE),
        "transition": svg_to_icon(SVG_TRANSITION),
        "action": svg_to_icon(SVG_ACTION),
        "clock": svg_to_icon(SVG_CLOCK),
        "plus": svg_to_icon(SVG_PLUS),
    }
