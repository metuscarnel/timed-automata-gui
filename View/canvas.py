from PySide6.QtWidgets import QGraphicsView, QGraphicsScene
from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem
from PySide6.QtGui import QPen
from PySide6.QtCore import Signal, Qt
from .items import NodeItem, TransitionItem

class AutomataView(QGraphicsView):
    # Signal pour envoyer les coordonnées EXACTES de la scène cliquée
    canvas_clicked = Signal(float, float)
    # NOUVEAU : Signal émis quand un noeud existant est cliqué
    node_clicked = Signal(str)
    # Signal émis uniquement quand le Drag & Drop d'une transition est validé
    transition_created = Signal(str, str)

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.creation_mode = None # Ex: "location", "transition", etc.
        self.nodes = {} # Dictionnaire pour retrouver les NodeItems par leur ID
        self.temp_line = None # Ligne visuelle temporaire pour le drag & drop
        self.drag_source_id = None # Mémorise la source du drag

    def set_creation_mode(self, mode):
        """Change le mode de création et modifie le curseur."""
        self.creation_mode = mode
        if mode in ["location", "transition"]:
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)

    def draw_node(self, node_id, x, y, is_initial=False):
        """Instancie le cercle et l'ajoute à la scène"""
        node = NodeItem(node_id, x, y, is_initial)
        self.nodes[node_id] = node
        self.scene.addItem(node)

    def draw_transition(self, source_id, target_id):
        """Crée visuellement une flèche entre deux noeuds existants"""
        source_node = self.nodes.get(source_id)
        target_node = self.nodes.get(target_id)
        if source_node and target_node:
            transition = TransitionItem(source_node, target_node)
            self.scene.addItem(transition)

    def mousePressEvent(self, event):
        """Capture le clic pour la création selon le mode actif"""
        item = self.itemAt(event.pos())
        
        while item and not hasattr(item, 'id'):
            item = item.parentItem()
            
        if item and hasattr(item, 'id'):
            self.node_clicked.emit(item.id)
            if self.creation_mode == "transition":
                # Début du drag & drop : ancrage de la ligne temporaire
                self.drag_source_id = item.id
                scene_pos = self.mapToScene(event.pos())
                self.temp_line = QGraphicsLineItem()
                self.temp_line.setPen(QPen(Qt.black, 1.5, Qt.DashLine)) # Feedback : ligne pointillée
                
                center = item.sceneBoundingRect().center()
                self.temp_line.setLine(center.x(), center.y(), scene_pos.x(), scene_pos.y())
                self.scene.addItem(self.temp_line)
                return # On bloque l'événement pour ne pas déclencher le déplacement du noeud
        else:
            if self.creation_mode:
                scene_pos = self.mapToScene(event.pos())
                self.canvas_clicked.emit(scene_pos.x(), scene_pos.y())
                return
                
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Met à jour le point d'arrivée de la ligne temporaire pendant le drag"""
        if self.creation_mode == "transition" and self.temp_line:
            scene_pos = self.mapToScene(event.pos())
            line = self.temp_line.line()
            line.setP2(scene_pos)
            self.temp_line.setLine(line)
            return # On bloque la propagation aux items en dessous
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        """Valide ou annule la création de la transition à la fin du drag"""
        if self.creation_mode == "transition" and self.temp_line:
            # 1. Destruction de l'affichage temporaire de la vue
            self.scene.removeItem(self.temp_line)
            self.temp_line = None
            
            # 2. Vérification de la cible
            item = self.itemAt(event.pos())
            while item and not hasattr(item, 'id'):
                item = item.parentItem()
                
            if item and hasattr(item, 'id'):
                target_id = item.id
                # On évite les auto-transitions (self-loop) pour l'instant
                if self.drag_source_id and self.drag_source_id != target_id:
                    # 3. Émission du signal métier vers le Contrôleur
                    self.transition_created.emit(self.drag_source_id, target_id)
                    
            self.drag_source_id = None
            return
        super().mouseReleaseEvent(event)