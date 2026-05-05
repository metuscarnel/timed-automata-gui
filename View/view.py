from PySide6.QtWidgets import (QMainWindow, QGraphicsView, QGraphicsScene, 
                             QWidget, QToolBar, QToolButton, 
                             QDockWidget, QLineEdit, QFormLayout)
from PySide6.QtCore import Qt

class AutomataView(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("MainWindow - maquette.ui")
        self.resize(1200, 800)

        # Désactiver le menu natif Mac pour voir "Fichier" dans la fenêtre
        self.menuBar().setNativeMenuBar(False)
        self.menuBar().addMenu("Fichier")

        # --- 1. BARRE D'OUTILS (ToolBar avec QToolButtons) ---
        self.toolbar = QToolBar("Barre d'outils")
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)
        self._setup_tool_buttons()

        # --- 2. ZONE DE DESSIN (Centre) ---
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        # Fond sombre comme sur ta capture d'écran
        self.view.setStyleSheet("background-color: #2b2b2b; border: none;") 
        self.setCentralWidget(self.view)

        # --- 3. PANNEAU DE PROPRIÉTÉS (Droite) ---
        self._setup_properties_panel()

    def _setup_tool_buttons(self):
        """Crée les QToolButton selon ta maquette"""
        
        # Liste des boutons à créer
        buttons = [
            ("+ Nouvelle Localité", "loc"),
            ("--> Nouvelle transition", "trans"),
            ("Nouvelle Horloge", "clock"),
            ("Nouvelle Action", "action"),
            ("Zoom +", "z_in"),
            ("Zoom -", "z_out")
        ]

        for text, key in buttons:
            btn = QToolButton()
            btn.setText(text)
            btn.setToolButtonStyle(Qt.ToolButtonTextOnly) # Texte visible comme sur l'image[cite: 1]
            
            # Ajout d'un peu d'espace entre les groupes de boutons
            if key == "z_in":
                self.toolbar.addSeparator()
                
            self.toolbar.addWidget(btn)
            
            # Connexion rapide pour tester
            btn.clicked.connect(lambda k=key: print(f"Mode activé : {k}"))

    def _setup_properties_panel(self):
        """Le dock de droite pour les propriétés de l'élément sélectionné[cite: 1]"""
        dock = QDockWidget("Propriétés d'élément sélectionné", self)
        dock.setAllowedAreas(Qt.RightDockWidgetArea)
        
        container = QWidget()
        layout = QFormLayout(container)
        
        # Champs correspondant aux barres grises de ta capture[cite: 1]
        layout.addRow("ID :", QLineEdit())
        layout.addRow("Nom :", QLineEdit())
        layout.addRow("Invariant :", QLineEdit())
        layout.addRow("Position :", QLineEdit())
        
        dock.setWidget(container)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)