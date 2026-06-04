from PySide6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsLineItem
from PySide6.QtGui import QPen
from PySide6.QtCore import Signal, Qt
from .items import NodeItem, TransitionItem, NailItem

class AutomataView(QGraphicsView):
    # Signal pour envoyer les coordonnées EXACTES de la scène cliquée
    canvas_clicked = Signal(float, float)
    # Signal émis quand la transition est validée (avec liste de clous)
    transition_created = Signal(str, str, list)
    
    # Signaux pour le Dock de propriétés
    selection_cleared = Signal()
    node_selected = Signal(str)
    transition_selected = Signal(str, str)
    
    # Signaux pour le déplacement (mise à jour du modèle)
    node_moved = Signal(str, float, float) # node_id, x, y
    nail_moved = Signal(str, str, int, float, float) # source_id, target_id, nail_index, x, y
    
    # Signaux pour les requêtes de suppression
    node_delete_requested = Signal(str)
    transition_delete_requested = Signal(str, str)

    # Signal émis lorsque le mode de création est annulé
    mode_cleared = Signal()

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        
        self.setScene(self.scene)
        self.setMouseTracking(True) # OBLIGATOIRE pour suivre la souris sans clic !
        
        # --- NOUVEAU : Fixer l'alignement pour éviter les sauts visuels ---
        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self.creation_mode = None # Ex: "location", "transition", etc.
        self.nodes = {} # Dictionnaire pour retrouver les NodeItems par leur ID
        self.drag_source_id = None
        self.temp_lines = [] # Lignes visuelles temporaires
        self.transition_nails_pos = [] # Coordonnées des clous posés
        
        # Écoute la sélection native de QGraphicsScene
        self.scene.selectionChanged.connect(self._on_selection_changed)

    def _on_selection_changed(self):
        """Capture les éléments sélectionnés et relaie les bons identifiants vers la fenêtre."""
        selected = self.scene.selectedItems()
        if not selected:
            self.selection_cleared.emit()
            return

    def set_creation_mode(self, mode):
        """Change le mode de création et modifie le curseur."""
        if self.creation_mode == mode:
            return
        self._cleanup_temp_transition()
        self.creation_mode = mode
        if mode in ["location", "transition"]:
            self.setCursor(Qt.CrossCursor)
        else:
            self.setCursor(Qt.ArrowCursor)
            self.mode_cleared.emit()

    def _cleanup_temp_transition(self):
        """Nettoie les variables de dessin en cours."""
        for line in self.temp_lines:
            if line in self.scene.items():
                self.scene.removeItem(line)
        self.temp_lines = []
        self.drag_source_id = None
        self.transition_nails_pos = []

    def draw_node(self, node_id, x, y, is_initial=False):
        """Instancie le cercle et l'ajoute à la scène"""
        node = NodeItem(node_id, x, y, is_initial)
        self.nodes[node_id] = node
        self.scene.addItem(node)

    def remove_node_visual(self, node_id):
        """Supprime visuellement le nœud de la scène."""
        if node_id in self.nodes:
            node = self.nodes.pop(node_id)
            if node in self.scene.items():
                self.scene.removeItem(node)

    def remove_transition_visual(self, source_id, target_id):
        """Supprime visuellement la transition de la scène."""
        source_node = self.nodes.get(source_id)
        if source_node:
            for t in list(source_node.transitions):
                if t.target.id == target_id:
                    # Détache des références
                    t.source.transitions.remove(t)
                    t.target.transitions.remove(t)
                    # Retire les clous visuels
                    for nail in t.nails:
                        if nail in self.scene.items():
                            self.scene.removeItem(nail)
                    # Retire la ligne
                    if t in self.scene.items():
                        self.scene.removeItem(t)
                    break

    def draw_transition(self, source_id, target_id, nails_pos=None):
        """Crée visuellement une flèche entre deux noeuds existants"""
        source_node = self.nodes.get(source_id)
        target_node = self.nodes.get(target_id)
        if source_node and target_node:
            transition = TransitionItem(source_node, target_node, nails_pos)
            self.scene.addItem(transition)
            for nail in transition.nails:
                self.scene.addItem(nail)
            transition.update_position() # Force le calcul d'esquive avec la scène active

    def keyPressEvent(self, event):
        """Gère l'appui sur la touche Échap pour annuler le mode en cours."""
        if event.key() == Qt.Key_Escape:
            if self.creation_mode == "transition" and self.drag_source_id:
                self._cleanup_temp_transition()
            elif self.creation_mode is not None:
                self.set_creation_mode(None)
        super().keyPressEvent(event)

    def mousePressEvent(self, event):
        """Capture le clic pour la création selon le mode actif"""
        # Clic droit pour annuler le dessin en cours ou le mode
        if event.button() == Qt.RightButton:
            if self.creation_mode == "transition" and self.drag_source_id:
                self._cleanup_temp_transition()
                return
            elif self.creation_mode is not None:
                self.set_creation_mode(None)
                return
            else:
                # --- NOUVEAU : Focus d'édition des transitions sur Clic Droit ---
                clicked_item = self.itemAt(event.pos())
                curr = clicked_item
                while curr:
                    if isinstance(curr, TransitionItem):
                        self.scene.clearSelection()
                        curr.setSelected(True)
                        # On émet explicitement le signal pour ouvrir le panneau d'édition
                        self.transition_selected.emit(curr.source.id, curr.target.id)
                        return
                    curr = curr.parentItem()
                # Si aucun mode de création n'est actif, on laisse passer le clic droit vers les objets.

        # --- NOUVEAU : Ignorer le clic gauche sur les transitions (sauf les clous) ---
        if event.button() == Qt.LeftButton and self.creation_mode is None:
            clicked_item = self.itemAt(event.pos())
            curr = clicked_item
            while curr:
                if isinstance(curr, TransitionItem) and not isinstance(clicked_item, NailItem):
                    return # On bloque la sélection par défaut avec le clic gauche
                curr = curr.parentItem()

        item = None
        # On parcourt tous les items sous le clic pour ignorer la ligne temporaire (qui bloque le clic)
        for it in self.items(event.pos()):
            curr = it
            while curr and not hasattr(curr, 'id') and not isinstance(curr, NailItem):
                curr = curr.parentItem()
            if curr:
                item = curr
                break
            
        if self.creation_mode == "transition":
            if not self.drag_source_id:
                # 1. Début de la transition
                if item and hasattr(item, 'id'):
                    self.drag_source_id = item.id
                    self.transition_nails_pos = []
                    self.temp_lines = []
                    
                    scene_pos = self.mapToScene(event.pos())
                    temp_line = QGraphicsLineItem()
                    temp_line.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                    
                    center = item.sceneBoundingRect().center()
                    temp_line.setLine(center.x(), center.y(), scene_pos.x(), scene_pos.y())
                    self.scene.addItem(temp_line)
                    self.temp_lines.append(temp_line)
                    return
            else:
                # 2. En cours de dessin
                if item and hasattr(item, 'id'):
                    # Fin : Clic sur une cible
                    target_id = item.id
                    if target_id != self.drag_source_id:
                        self.transition_created.emit(self.drag_source_id, target_id, self.transition_nails_pos)
                        self._cleanup_temp_transition()
                    return
                else:
                    # Milieu : Poser un clou
                    scene_pos = self.mapToScene(event.pos())
                    self.transition_nails_pos.append((scene_pos.x(), scene_pos.y()))
                    
                    # Figer la ligne actuelle
                    line = self.temp_lines[-1].line()
                    line.setP2(scene_pos)
                    self.temp_lines[-1].setLine(line)
                    
                    # Nouvelle ligne partant du clou
                    temp_line = QGraphicsLineItem()
                    temp_line.setPen(QPen(Qt.black, 1, Qt.SolidLine))
                    temp_line.setLine(scene_pos.x(), scene_pos.y(), scene_pos.x(), scene_pos.y())
                    self.scene.addItem(temp_line)
                    self.temp_lines.append(temp_line)
                    return
        elif self.creation_mode == "location":
            if not (item and hasattr(item, 'id')):
                scene_pos = self.mapToScene(event.pos())
                self.canvas_clicked.emit(scene_pos.x(), scene_pos.y())
                return
                
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Met à jour le point d'arrivée de la ligne temporaire"""
        if self.creation_mode == "transition" and self.temp_lines:
            scene_pos = self.mapToScene(event.pos())
            line = self.temp_lines[-1].line()
            line.setP2(scene_pos)
            self.temp_lines[-1].setLine(line)
            return # On bloque la propagation aux items en dessous
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        # Le dessin se valide maintenant au clic (mousePressEvent).
        super().mouseReleaseEvent(event)