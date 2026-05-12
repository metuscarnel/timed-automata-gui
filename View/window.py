from PySide6.QtWidgets import QMainWindow, QToolBar, QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton
from PySide6.QtGui import QAction, QKeySequence, QActionGroup
from PySide6.QtCore import Signal
from .canvas import AutomataView
from resources.icons import get_icons

class DeclarationDialog(QDialog):
    """Boîte de dialogue volante pour la création d'éléments globaux (Actions, Horloges)."""
    validated = Signal(str)

    def __init__(self, title, parent=None):
        super().__init__(parent)
        self.setWindowTitle(title)
        
        # --- STYLESHEET (Design) ---
        self.setStyleSheet("""
            QDialog {
                background-color: #FAFAFA; /* Force le fond de la popup en clair */
            }
            QLineEdit {
                background-color: #FFFFFF; /* Force le fond du champ en blanc */
                color: #000000;            /* Force le texte en noir */
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 4px;
            }
            QPushButton {
                background-color: #EBEBEB;
                border: 1px solid #D5D5D5;
                border-radius: 6px;
                padding: 6px 12px;
                color: #000000;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
            QPushButton:pressed {
                background-color: #D0D0D0;
            }
        """)
        
        layout = QVBoxLayout(self)
        self.input_field = QLineEdit(self)
        layout.addWidget(self.input_field)
        
        btn_layout = QHBoxLayout()
        self.btn_validate = QPushButton("Valider", self)
        self.btn_close = QPushButton("Fermer", self)
        
        btn_layout.addWidget(self.btn_validate)
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)
        
        # --- SIGNALS ---
        self.btn_validate.clicked.connect(self._handle_validation)
        self.input_field.returnPressed.connect(self._handle_validation)  # Validation par touche Entrée
        self.btn_close.clicked.connect(self.close)

    def showEvent(self, event):
        """Surcharge pour positionner la popup un peu plus haut que le centre au moment de l'affichage."""
        super().showEvent(event)
        if self.parent():
            parent_geom = self.parent().geometry()
            x = parent_geom.x() + (parent_geom.width() - self.width()) // 2
            y = parent_geom.y() + (parent_geom.height() - self.height()) // 2
            # Décaler de 200 pixels vers le haut (encore plus haut)
            self.move(x, max(0, y - 200))

    def _handle_validation(self):
        text = self.input_field.text().strip()
        if text:
            self.validated.emit(text)
            self.input_field.clear() # UX : vide le champ après soumission
            self.input_field.setFocus()

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

    def show_action_dialog(self):
        """Affiche la popup et connecte le résultat au contrôleur."""
        dialog = DeclarationDialog("Nouvelle Action", self)
        dialog.validated.connect(self.controller.submit_action)
        dialog.exec()

    def show_clock_dialog(self):
        """Affiche la popup et connecte le résultat au contrôleur."""
        dialog = DeclarationDialog("Nouvelle Horloge", self)
        dialog.validated.connect(self.controller.submit_clock)
        dialog.exec()

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