from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
from PySide6.QtGui import QBrush, QPen, QFont
from PySide6.QtCore import Qt, QPointF
import math

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, x, y, is_initial=False):
        # Un cercle de rayon 20 (donc -20, -20 pour centrer, taille 40x40)
        super().__init__(-20, -20, 40, 40)
        self.id = node_id
        
        self.setPos(x, y)
        self.setBrush(QBrush(Qt.white))
        self.setPen(QPen(Qt.black, 1)) # Bordure noire de 1px
        
        # --- NOUVEAU : Rendre le noeud déplaçable et sélectionnable ---
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        
        # --- NOUVEAU : Ajouter un cercle intérieur si c'est l'état initial ---
        if is_initial:
            # Cercle légèrement plus petit, centré
            inner_circle = QGraphicsEllipseItem(-16, -16, 32, 32, self)
            inner_circle.setPen(QPen(Qt.black, 1))

        # --- NOUVEAU : Ajouter le texte (ID) centré ---
        self.text = QGraphicsTextItem(self.id, self)
        self.text.setFont(QFont("Palatino", 12, italic=True))
        self.text.setDefaultTextColor(Qt.black)
        
        # Centrer le texte par rapport au centre du cercle (-20, -20)
        rect = self.text.boundingRect()
        self.text.setPos(-rect.width() / 2, -rect.height() / 2)

class TransitionItem(QGraphicsLineItem):
    def __init__(self, source_node, target_node):
        super().__init__()
        self.source = source_node
        self.target = target_node
        
        self.setPen(QPen(Qt.black, 1.5))
        self.setZValue(-1) # Dessiner la ligne DERRIÈRE les noeuds
        self.update_position()
        
    def update_position(self):
        """Met à jour les coordonnées de la ligne entre les deux noeuds"""
        p1 = self.source.scenePos()
        p2 = self.target.scenePos()
        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())

    def paint(self, painter, option, widget=None):
        """Surcharge du dessin pour ajouter une pointe de flèche"""
        super().paint(painter, option, widget)
        
        line = self.line()
        p1, p2 = line.p1(), line.p2()
        
        dx, dy = p2.x() - p1.x(), p2.y() - p1.y()
        length = math.hypot(dx, dy)
        if length == 0:
            return
            
        # Vecteur unitaire et calcul de l'intersection avec le bord du cercle cible (rayon=20)
        nx, ny = dx / length, dy / length
        end_x, end_y = p2.x() - nx * 20, p2.y() - ny * 20
        
        # Dessin du triangle de la flèche
        arrow_size = 10
        angle = math.atan2(dy, dx)
        wing1 = QPointF(end_x - arrow_size * math.cos(angle + math.pi / 6), end_y - arrow_size * math.sin(angle + math.pi / 6))
        wing2 = QPointF(end_x - arrow_size * math.cos(angle - math.pi / 6), end_y - arrow_size * math.sin(angle - math.pi / 6))
        
        painter.setBrush(Qt.black)
        painter.drawPolygon([QPointF(end_x, end_y), wing1, wing2])