from PySide6.QtWidgets import QMainWindow, QToolBar, QWidget, QLabel, QToolButton, QHBoxLayout
from PySide6.QtGui import QAction, QKeySequence, QActionGroup, QIcon, QFont
from PySide6.QtCore import Signal, Qt, QPoint
from .canvas import AutomataView
from resources.icons import get_icons
from .properties_dock import PropertiesDock
from .popups import InlineAddPopup


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.resize(1000, 600)
        
        # Le Canvas au centre
        self.canvas = AutomataView()
        self.setCentralWidget(self.canvas)
        
        # --- NOUVEAU : Connexion du clic de la zone de dessin au contrôleur ---
        self.canvas.canvas_clicked.connect(self.controller.handle_canvas_click)
        self.canvas.transition_created.connect(self.controller.handle_transition_created)
        
        # --- NOUVEAU : Connexion des signaux de sélection au contrôleur ---
        self.canvas.selection_cleared.connect(self.controller.handle_selection_cleared)
        self.canvas.node_selected.connect(self.controller.handle_node_selected)
        self.canvas.transition_selected.connect(self.controller.handle_transition_selected)
        
        # --- NOUVEAU : Connexion des signaux de déplacement au contrôleur ---
        self.canvas.node_moved.connect(self.controller.update_node_position)
        self.canvas.nail_moved.connect(self.controller.update_nail_position)
        
        # --- NOUVEAU : Instanciation du Panneau Latéral (Dock) ---
        self.properties_dock = PropertiesDock(self.controller)
        self.addDockWidget(Qt.RightDockWidgetArea, self.properties_dock)
        self.properties_dock.hide() # Masqué par défaut
        
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
        
        # --- NOUVEAU : Section Actions ---
        self.actions_widget = self._create_declaration_widget(
            get_icons()["action"], 
            self._show_add_action_popup
        )
        toolbar.addWidget(self.actions_widget)
        self.actions_label = self.actions_widget.findChild(QLabel, "items_label")

        toolbar.addSeparator()

        # --- NOUVEAU : Section Horloges ---
        self.clocks_widget = self._create_declaration_widget(
            get_icons()["clock"], 
            self._show_add_clock_popup
        )
        toolbar.addWidget(self.clocks_widget)
        self.clocks_label = self.clocks_widget.findChild(QLabel, "items_label")

    def _create_declaration_widget(self, icon: QIcon, on_add_clicked):
        """Crée un widget composite pour la toolbar (Icon, Label, Bouton +)."""
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(4)

        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(16, 16))
        layout.addWidget(icon_label)

        items_label = QLabel("Aucune")
        items_label.setObjectName("items_label") # Pour le retrouver plus tard
        
        # --- NOUVEAU : Police IBM Plex Mono italique et couleur bleu électrique ---
        items_label.setStyleSheet("""
            color: #0D99FF; 
            font-family: 'IBM Plex Mono'; 
            font-size: 12pt; 
            font-style: italic;
        """)
        
        layout.addWidget(items_label)

        add_btn = QToolButton()
        add_btn.setText("+")
        add_btn.setFixedSize(24, 24)
        add_btn.clicked.connect(on_add_clicked)
        layout.addWidget(add_btn)
        
        return widget

    def _show_add_action_popup(self):
        """Affiche la popup pour ajouter une action."""
        add_btn = self.actions_widget.findChild(QToolButton)
        popup = InlineAddPopup(self)
        popup.validated.connect(self.controller.submit_action)
        
        # Positionner la popup sous le bouton '+'
        btn_pos = add_btn.mapToGlobal(QPoint(0, add_btn.height()))
        popup.show_at(btn_pos)

    def _show_add_clock_popup(self):
        """Affiche la popup pour ajouter une horloge."""
        add_btn = self.clocks_widget.findChild(QToolButton)
        popup = InlineAddPopup(self)
        popup.validated.connect(self.controller.submit_clock)
        
        # Positionner la popup sous le bouton '+'
        btn_pos = add_btn.mapToGlobal(QPoint(0, add_btn.height()))
        popup.show_at(btn_pos)

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
        
        # Action Debug (Afficher l'instance)
        action_debug = QAction("Afficher l'instance Modèle", self)
        action_debug.setShortcut("Ctrl+D")
        action_debug.triggered.connect(self.controller.debug_print_model_instance)
        
        # Ajout des actions au menu
        menu_fichier.addAction(action_new)
        menu_fichier.addAction(action_open)
        menu_fichier.addAction(action_save)
        
        menu_fichier.addSeparator()
        menu_fichier.addAction(action_debug)
        menu_fichier.addSeparator()
        
        # Action Quitter
        action_quit = QAction("Quitter", self)
        action_quit.setShortcut(QKeySequence.Quit)
        action_quit.triggered.connect(self.close)
        menu_fichier.addAction(action_quit)

    def update_actions_display(self, actions: list):
        """Met à jour le label des actions dans la toolbar."""
        text = ", ".join(actions) if actions else "Aucune"
        self.actions_label.setText(text)

    def update_clocks_display(self, clocks: list):
        """Met à jour le label des horloges dans la toolbar."""
        text = ", ".join(clocks) if clocks else "Aucune"
        self.clocks_label.setText(text)