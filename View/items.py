from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsPathItem, QGraphicsItem, QStyle
from PySide6.QtGui import QBrush, QPen, QFont, QPainterPath, QColor, QPainterPathStroker
from PySide6.QtCore import Qt, QPointF
import math

class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_id, x, y, is_initial=False):
        # Cercle de rayon 20 (centré en -20, -20)
        super().__init__(-20, -20, 40, 40)
        self.id = node_id
        
        self.setPos(x, y)
        self.setBrush(QBrush(Qt.white))
        self.setPen(QPen(Qt.black, 1)) # Bordure noire de 1px
        
        # Rendre le noeud déplaçable et sélectionnable
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        
        # Activer les notifications de mouvement pour les flèches
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.transitions = [] # Liste des flèches connectées
        
        # Ajouter un cercle intérieur pour l'état initial
        if is_initial:
            # Cercle légèrement plus petit, centré
            inner_circle = QGraphicsEllipseItem(-16, -16, 32, 32, self)
            inner_circle.setPen(QPen(Qt.black, 1))

        # Ajouter le texte (ID) centré
        self.text = QGraphicsTextItem(self.id, self)
        self.text.setFont(QFont("IBM Plex Mono", 12, italic=True))
        self.text.setDefaultTextColor(Qt.black)
        
        # Centrer le texte par rapport au centre du cercle (-20, -20)
        rect = self.text.boundingRect()
        self.text.setPos(-rect.width() / 2, -rect.height() / 2)

    def add_transition(self, transition):
        """Mémorise une transition connectée à ce noeud."""
        self.transitions.append(transition)

    def paint(self, painter, option, widget=None):
        # Supprimer le cadre pointillé par défaut de Qt
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)

    def itemChange(self, change, value):
        """Écoute les mouvements du noeud et met à jour ses flèches en temps réel."""
        if change == QGraphicsItem.ItemPositionHasChanged:
            # 1. Met à jour les flèches connectées à ce noeud
            for transition in self.transitions:
                transition.update_position()
                
            # 2. Met à jour les AUTRES flèches de la scène pour esquiver ce noeud dynamiquement
            if self.scene():
                for item in self.scene().items():
                    if isinstance(item, TransitionItem) and item not in self.transitions:
                        item.update_position()
                        
        elif change == QGraphicsItem.ItemSelectedHasChanged:
            # Changement de couleur de la bordure
            if value:
                self.setPen(QPen(QColor("#0D99FF"), 2)) # Couleur de sélection
            else:
                self.setPen(QPen(Qt.black, 1)) # Retour à la normale
        return super().itemChange(change, value)
        
    def mousePressEvent(self, event):
        """Ouvre le Dock de propriétés au clic gauche sur le noeud."""
        if event.button() == Qt.LeftButton:
            if self.scene() and self.scene().views():
                # Forcer la sélection unique en désélectionnant tout le reste d'abord
                for item in self.scene().selectedItems():
                    item.setSelected(False)
                self.setSelected(True)

                view = self.scene().views()[0]
                if hasattr(view, 'node_selected'):
                    view.node_selected.emit(self.id)
        super().mousePressEvent(event)
        
    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # Notifier la vue du déplacement final au relâchement du clic
        if self.scene() and self.scene().views():
            view = self.scene().views()[0]
            if hasattr(view, 'node_moved'):
                view.node_moved.emit(self.id, self.scenePos().x(), self.scenePos().y())

class NailItem(QGraphicsEllipseItem):
    def __init__(self, x, y, transition):
        super().__init__(-4, -4, 8, 8)
        self.setPos(x, y)
        self.setBrush(QBrush(Qt.black))
        self.setPen(QPen(Qt.black, 1))
        
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.transition = transition
        self.setZValue(0)
        
    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            if self.transition:
                self.transition.update_position()
        return super().itemChange(change, value)
        
    def mousePressEvent(self, event):
        """Ouvre le Dock de propriétés de la transition au clic sur un clou."""
        if event.button() == Qt.LeftButton:
            if self.transition and self.scene() and self.scene().views():
                # Forcer la sélection unique en désélectionnant tout le reste d'abord
                for item in self.scene().selectedItems():
                    item.setSelected(False)
                self.setSelected(True)

                view = self.scene().views()[0]
                if hasattr(view, 'transition_selected'):
                    view.transition_selected.emit(self.transition.id)
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        super().mouseReleaseEvent(event)
        # Trouver l'index de ce clou et notifier la vue au relâchement du clic
        if self.transition and self.scene() and self.scene().views():
            try:
                nail_index = self.transition.nails.index(self)
                view = self.scene().views()[0]
                if hasattr(view, 'nail_moved'):
                    view.nail_moved.emit(self.transition.id, nail_index, self.scenePos().x(), self.scenePos().y())
            except ValueError:
                pass

class TransitionItem(QGraphicsPathItem):
    def __init__(self, trans_id, source_node, target_node, nails_pos=None):
        super().__init__()
        self.id = trans_id
        self.source = source_node
        self.target = target_node
        self.nails = []
        
        if nails_pos:
            for nx, ny in nails_pos:
                nail = NailItem(nx, ny, self)
                self.nails.append(nail)
                
        # On informe les deux noeuds qu'ils ont une nouvelle flèche accrochée
        self.source.add_transition(self)
        self.target.add_transition(self)
        
        self.setPen(QPen(Qt.black, 1))
        self.setZValue(-1) # Dessiner la ligne DERRIÈRE les noeuds
        
        # Rendre la flèche cliquable et sélectionnable
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        
        self.ctrl_x = 0 # Position X du point de courbure
        self.ctrl_y = 0 # Position Y du point de courbure
        self.update_position()
        
    def boundingRect(self):
        """Surcharge la boîte englobante pour inclure la pointe de flèche et l'épaisseur du trait."""
        extra = 15.0  # Marge de sécurité (pointe de flèche de taille 10 + épaisseur de ligne)
        return super().boundingRect().adjusted(-extra, -extra, extra, extra)

    def shape(self):
        """Élargit la zone de clic (hitbox) pour faciliter la sélection à la souris."""
        path = self.path()
        stroker = QPainterPathStroker()
        stroker.setWidth(10) # 10 pixels de large pour attraper le clic facilement
        return stroker.createStroke(path)

    def update_position(self):
        """Calcule la courbe pour éviter les noeuds ou gérer les retours."""
        self.prepareGeometryChange() # Prévient la scène graphique que la géométrie (et la boîte englobante) va changer
        p1 = self.source.scenePos()
        p2 = self.target.scenePos()

        if self.nails:
            path = QPainterPath(p1)
            for nail in self.nails:
                path.lineTo(nail.scenePos())
            path.lineTo(p2)
            self.setPath(path)
            
            last_nail_pos = self.nails[-1].scenePos()
            self.ctrl_x = last_nail_pos.x()
            self.ctrl_y = last_nail_pos.y()
            return
            
        # Gestion des flèches multiples
        same_dir = [t for t in self.source.transitions if t.target == self.target]
        try:
            idx = same_dir.index(self)
        except ValueError:
            idx = len(same_dir)
            
        # Gestion de l'auto-boucle
        if self.source == self.target:
            offset_x = 40 + (idx * 20)
            offset_y = 80 + (idx * 30)
            cp1x = p1.x() - offset_x
            cp1y = p1.y() - offset_y
            cp2x = p1.x() + offset_x
            cp2y = p1.y() - offset_y
            
            path = QPainterPath(p1)
            path.cubicTo(cp1x, cp1y, cp2x, cp2y, p2.x(), p2.y())
            self.setPath(path)
            
            # Point de contrôle final pour le calcul de l'angle de la pointe de la flèche
            self.ctrl_x = cp2x
            self.ctrl_y = cp2y
            return

        dx, dy = p2.x() - p1.x(), p2.y() - p1.y()
        length = math.hypot(dx, dy)
        if length == 0:
            return
            
        curve_offset = 0
        
        # 1. Esquive si transition réciproque et multi-transitions
        has_reciprocal = any(t.source == self.target and t.target == self.source for t in self.source.transitions)
        if has_reciprocal:
            curve_offset = 40 + (40 * idx)
        elif idx > 0:
            # Alternance : 1=40, 2=-40, 3=80, 4=-80...
            step = 40 * ((idx + 1) // 2)
            sign = 1 if idx % 2 != 0 else -1
            curve_offset = step * sign
        else:
            # 2. Esquive dynamique (uniquement pour la ligne centrale)
            if self.scene():
                for item in self.scene().items():
                    if isinstance(item, NodeItem) and item != self.source and item != self.target:
                        cx, cy = item.scenePos().x(), item.scenePos().y()
                        # Projection géométrique du centre du noeud-obstacle sur le segment de la flèche
                        t = max(0, min(1, ((cx - p1.x()) * dx + (cy - p1.y()) * dy) / (length * length)))
                        proj_x, proj_y = p1.x() + t * dx, p1.y() + t * dy
                        distance_to_line = math.hypot(cx - proj_x, cy - proj_y)
                        
                        if distance_to_line < 45: # Si obstacle trop proche (Rayon 20 + marge 25)
                            # On détermine le côté de l'esquive via le produit vectoriel
                            cross = dx * (cy - p1.y()) - dy * (cx - p1.x())
                            direction = -1 if cross > 0 else 1
                            curve_offset = 60 * direction
                            break # Un seul obstacle évité suffit pour courber
                            
        # Calcul du point de contrôle de la courbe de Bézier (Perpendiculaire au milieu)
        mid_x, mid_y = (p1.x() + p2.x()) / 2, (p1.y() + p2.y()) / 2
        nx, ny = -dy / length, dx / length # Vecteur normal
        
        self.ctrl_x = mid_x + nx * curve_offset
        self.ctrl_y = mid_y + ny * curve_offset
        
        # Création du tracé courbé
        path = QPainterPath(p1)
        path.quadTo(self.ctrl_x, self.ctrl_y, p2.x(), p2.y())
        self.setPath(path)

    def itemChange(self, change, value):
        # Changement de couleur de la flèche
        if change == QGraphicsItem.ItemSelectedHasChanged:
            if value:
                self.setPen(QPen(QColor("#0D99FF"), 2)) # Couleur de sélection
            else:
                self.setPen(QPen(Qt.black, 1)) # Retour à la normale
        return super().itemChange(change, value)

    def mousePressEvent(self, event):
        """Ouvre le Dock de propriétés au clic."""
        if event.button() == Qt.LeftButton:
            if self.scene() and self.scene().views():
                # Forcer la sélection unique en désélectionnant tout le reste d'abord
                for item in self.scene().selectedItems():
                    item.setSelected(False)
                self.setSelected(True) # Force la sélection visuelle (bordure bleue)

                view = self.scene().views()[0]
                if hasattr(view, 'transition_selected'):
                    view.transition_selected.emit(self.id)
        super().mousePressEvent(event)

    def paint(self, painter, option, widget=None):
        """Surcharge du dessin pour la pointe de flèche orientée selon la courbe"""
        # Supprimer le cadre pointillé par défaut de Qt
        option.state &= ~QStyle.State_Selected
        super().paint(painter, option, widget)
        
        # La tangente (direction de l'angle) à l'arrivée d'une courbe quad est P2 - ControlPoint
        p2 = self.target.scenePos()
        vx, vy = p2.x() - self.ctrl_x, p2.y() - self.ctrl_y
        v_len = math.hypot(vx, vy)
        if v_len == 0: 
            return
        
        tx, ty = vx / v_len, vy / v_len
        
        # On recule la pointe de flèche pour qu'elle s'arrête sur le bord du noeud (rayon = 20)
        end_x, end_y = p2.x() - tx * 20, p2.y() - ty * 20
        
        # Dessin du triangle de la flèche
        arrow_size = 10
        angle = math.atan2(vy, vx)
        wing1 = QPointF(end_x - arrow_size * math.cos(angle + math.pi / 6), end_y - arrow_size * math.sin(angle + math.pi / 6))
        wing2 = QPointF(end_x - arrow_size * math.cos(angle - math.pi / 6), end_y - arrow_size * math.sin(angle - math.pi / 6))
        
        painter.setPen(self.pen()) # Utilise le même style que la courbe
        painter.setBrush(QBrush(self.pen().color())) # Utilise la couleur active (Gris ou Noir) pour remplir la pointe
        painter.drawPolygon([QPointF(end_x, end_y), wing1, wing2])