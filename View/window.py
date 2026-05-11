from PySide6.QtWidgets import QMainWindow, QToolBar
from PySide6.QtGui import QAction, QKeySequence, QActionGroup
from .canvas import AutomataView
from resources.icons import get_icons

class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.resize(800, 600)
        
        # Le Canvas au centre
        self.canvas = AutomataView()
        self.setCentralWidget(self.canvas)
        
        # --- NOUVEAU : Connexion du clic de la zone de dessin au contrôleur ---
        self.canvas.canvas_clicked.connect(self.controller.handle_canvas_click)
        self.canvas.node_clicked.connect(self.controller.handle_node_click)
        self.canvas.transition_created.connect(self.controller.handle_transition_created)
        
        # --- NOUVEAU : Appel de la création du menu ---
        self._setup_menubar()
        
        # (Ton code précédent pour la Toolbar avec le bouton + Nouvelle Localité...)
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        # --- NOUVEAU : Groupe d'actions pour n'avoir qu'un seul mode actif à la fois ---
        self.action_group = QActionGroup(self)
        self.action_group.setExclusionPolicy(QActionGroup.ExclusionPolicy.ExclusiveOptional)

        btn_add = QAction(get_icons()["state"], "Nouvelle Localité", self)
        btn_add.setToolTip("Ajouter une nouvelle localité")
        btn_add.setCheckable(True)
        self.action_group.addAction(btn_add)
        btn_add.triggered.connect(self.controller.handle_add_location)
        toolbar.addAction(btn_add)
        
        # Bouton Transition
        btn_transition = QAction(get_icons()["transition"], "Nouvelle Transition", self)
        btn_transition.setToolTip("Ajouter une nouvelle transition")
        btn_transition.setCheckable(True)
        self.action_group.addAction(btn_transition)
        btn_transition.triggered.connect(self.controller.handle_add_transition)
        toolbar.addAction(btn_transition)
        
        toolbar.addSeparator()
        
        # Bouton Action
        btn_action = QAction(get_icons()["action"], "Nouvelle Action", self)
        btn_action.setToolTip("Ajouter une nouvelle action")
        btn_action.triggered.connect(self.controller.handle_add_action)
        toolbar.addAction(btn_action)
        
        # Bouton Horloge
        btn_clock = QAction(get_icons()["clock"], "Nouvelle Horloge", self)
        btn_clock.setToolTip("Ajouter une nouvelle horloge")
        btn_clock.triggered.connect(self.controller.handle_add_clock)
        toolbar.addAction(btn_clock)

    def _setup_menubar(self):
        """Configure la barre de menus"""
        menubar = self.menuBar()
        
        # --- LA LIGNE MAGIQUE POUR MAC ---
        menubar.setNativeMenuBar(False) 
        
        # 1. Création du menu "Fichier"
        menu_fichier = menubar.addMenu("Fichier")
        
        # Action Nouveau
        action_new = QAction("Nouveau", self)
        action_new.setShortcut(QKeySequence.New)
        action_new.triggered.connect(self.controller.handle_new_file)
        
        # Action Ouvrir
        action_open = QAction("Ouvrir", self)
        action_open.setShortcut(QKeySequence.Open)
        action_open.triggered.connect(self.controller.handle_open_file)
        
        # Action Sauvegarder
        action_save = QAction("Sauvegarder", self)
        action_save.setShortcut(QKeySequence.Save)
        action_save.triggered.connect(self.controller.handle_save_file)
        
        # Ajout des actions au menu
        menu_fichier.addAction(action_new)
        menu_fichier.addAction(action_open)
        menu_fichier.addAction(action_save)
        
        menu_fichier.addSeparator()
        
        # Action Quitter
        action_quit = QAction("Quitter", self)
        action_quit.setShortcut(QKeySequence.Quit)
        action_quit.triggered.connect(self.close)
        menu_fichier.addAction(action_quit)