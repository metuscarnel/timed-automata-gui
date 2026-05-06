import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QMenu, QToolBar,
                               QGraphicsView, QGraphicsScene, QDockWidget,
                               QWidget, QFormLayout, QLineEdit, QMessageBox,
                               QToolButton, QGraphicsEllipseItem, QGraphicsTextItem)
from PySide6.QtGui import QAction, QKeySequence, QBrush, QPen
from PySide6.QtCore import Qt
class AutomataView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GUI pour Automate Temporisés par la Donnée")
        self.resize(1100, 700)

        # Configuration de la barre de menu pour macOS
        self.menuBar().setNativeMenuBar(False)

        # Zone Centrale (La Vue graphique)
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        # Initialisation des composants
        self.create_actions()
        self.create_menus()
        self.create_toolbar()

    def create_actions(self):
        # --- FICHIER ---
        self.new_act = QAction("Nouveau", self)
        self.new_act.setShortcut(QKeySequence.New)
        
        self.open_act = QAction("Ouvrir", self)
        self.open_act.setShortcut(QKeySequence.Open)
        
        self.save_act = QAction("Enregistrer", self)
        self.save_act.setShortcut(QKeySequence.Save)


    def create_menus(self):
        # Menu Fichier
        file_menu = self.menuBar().addMenu("&Fichier")
        file_menu.addAction(self.new_act)
        file_menu.addAction(self.open_act)
        file_menu.addAction(self.save_act)


    def create_toolbar(self):
        # Barre d'outils avec les actions principales
        toolbar = self.addToolBar("toolbar")

        # Boutons d'outil
        self.new_state_btn = QToolButton(self)
        self.new_state_btn.setText("Nouvelle Localité")
        toolbar.addWidget(self.new_state_btn)

        self.new_trans_btn = QToolButton(self)
        self.new_trans_btn.setText("Nouvelle Transition")
        toolbar.addWidget(self.new_trans_btn)

        toolbar.addSeparator()

        self.action_btn = QToolButton(self)
        self.action_btn.setText("Action")
        toolbar.addWidget(self.action_btn)

        self.clock_btn = QToolButton(self)
        self.clock_btn.setText("Horloge")
        toolbar.addWidget(self.clock_btn)
    def add_node_to_scene(self):
        radius = 20
        x, y = 100, 100  # Position arbitraire pour le test
    
        # 1. Créer le cercle
        ellipse = QGraphicsEllipseItem(-radius, -radius, radius * 2, radius * 2)
        ellipse.setPos(x, y) # On place le centre du cercle à (x,y)
    
        # 2. Style (contour blanc, fond transparent ou gris)
        ellipse.setPen(QPen(Qt.white, 2))
        ellipse.setBrush(QBrush(Qt.transparent))
    
        # 3. Rendre l'objet interactif (Déplaçable et Sélectionnable)
        ellipse.setFlags(QGraphicsEllipseItem.ItemIsMovable | 
                     QGraphicsEllipseItem.ItemIsSelectable)
    
        # 4. Ajouter à la scène[cite: 1]
        self.scene.addItem(ellipse)
    
        # 5. Ajouter un petit label texte au milieu
        label = QGraphicsTextItem("L", ellipse) # Parenté au cercle pour qu'il bouge avec
        label.setDefaultTextColor(Qt.white)
        label.setPos(-10, -10)