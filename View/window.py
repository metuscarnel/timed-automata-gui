import sys
import os
from PySide6.QtWidgets import QMainWindow, QToolBar, QWidget, QLabel, QToolButton, QHBoxLayout, QComboBox, QMenu, QInputDialog, QMessageBox, QDialog, QVBoxLayout, QTextBrowser, QPushButton
from PySide6.QtGui import QAction, QKeySequence, QActionGroup, QIcon, QGuiApplication
from PySide6.QtCore import Qt, QPoint, QFileInfo

from .canvas import AutomataView
from resources.icons import get_icons
from .properties_dock import PropertiesDock
from .popups import InlineAddPopup
from .data_editor import DataEditorDialog


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        self.update_window_title(None)

        # Taille dynamique : 80% de l'écran principal et centrage automatique (Fiable sous Linux)
        screen = QGuiApplication.primaryScreen()
        screen_geom = screen.availableGeometry()
        w = int(screen_geom.width() * 0.8)
        h = int(screen_geom.height() * 0.8)
        x = int(screen_geom.x() + (screen_geom.width() - w) / 2)
        y = int(screen_geom.y() + (screen_geom.height() - h) / 2)
        self.setGeometry(x, y, w, h)
        
        self.canvas = AutomataView()
        self.setCentralWidget(self.canvas)
        
        self.canvas.canvas_clicked.connect(self.controller.handle_canvas_click)
        self.canvas.transition_created.connect(self.controller.handle_transition_created)
        
        self.canvas.selection_cleared.connect(self.controller.handle_selection_cleared)
        self.canvas.node_selected.connect(self.controller.handle_node_selected)
        self.canvas.transition_selected.connect(self.controller.handle_transition_selected)
        
        self.canvas.node_moved.connect(self.controller.update_node_position)
        self.canvas.nail_moved.connect(self.controller.update_nail_position)
        
        self.canvas.mode_cleared.connect(self.clear_toolbar_modes)
        
        self.properties_dock = PropertiesDock(self.controller)
        self.addDockWidget(Qt.RightDockWidgetArea, self.properties_dock)
        self.properties_dock.hide()
        self._setup_menubar()
        toolbar = QToolBar()
        # Empêche l'apparition du menu natif Qt listant les panneaux (docks)
        toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        self.addToolBar(toolbar)
        self.action_group = QActionGroup(self)
        self.action_group.setExclusionPolicy(QActionGroup.ExclusionPolicy.ExclusiveOptional)

        btn_add = QAction(get_icons()["state"], "Nouvelle Localité", self)
        btn_add.setToolTip("Ajouter une nouvelle localité")
        btn_add.setCheckable(True)
        self.action_group.addAction(btn_add)
        btn_add.triggered.connect(self.controller.handle_add_location)
        toolbar.addAction(btn_add)
        
        btn_transition = QAction(get_icons()["transition"], "Nouvelle Transition", self)
        btn_transition.setToolTip("Ajouter une nouvelle transition")
        btn_transition.setCheckable(True)
        self.action_group.addAction(btn_transition)
        btn_transition.triggered.connect(self.controller.handle_add_transition)
        toolbar.addAction(btn_transition)
        
        toolbar.addSeparator()
        self.init_state_widget = QWidget()
        init_layout = QHBoxLayout(self.init_state_widget)
        init_layout.setContentsMargins(4, 0, 4, 0)
        init_layout.setSpacing(4)
        
        init_label = QLabel("Init :")
        init_label.setStyleSheet("color: #2C2C2C; font-weight: bold; font-family: 'IBM Plex Mono';")
        self.init_state_combo = QComboBox()
        self.init_state_combo.setToolTip("Choisir la localité initiale")
        self.init_state_combo.currentTextChanged.connect(self.controller.handle_initial_state_changed)
        
        init_layout.addWidget(init_label)
        init_layout.addWidget(self.init_state_combo)
        toolbar.addWidget(self.init_state_widget)
        toolbar.addSeparator()
        self.clocks_widget, self.clocks_layout = self._create_declaration_widget(
            get_icons()["clock"], 
            self._show_add_clock_popup
        )
        toolbar.addWidget(self.clocks_widget)
        toolbar.addSeparator()
        self.actions_widget, self.actions_layout = self._create_declaration_widget(
            get_icons()["action"], 
            self._show_add_action_popup
        )
        toolbar.addWidget(self.actions_widget)
        toolbar.addSeparator()
        btn_data = QToolButton(self)
        btn_data.setText("Data")
        btn_data.setToolTip("Ouvrir l'éditeur de variables et de données")
        btn_data.setStyleSheet("""
            font-family: 'IBM Plex Mono'; font-size: 14pt; font-weight: bold; color:  #2C2C2C;
        """)
        btn_data.clicked.connect(self.open_data_editor)
        toolbar.addWidget(btn_data)
        
        toolbar.addSeparator()
        btn_run = QToolButton(self)
        btn_run.setText("▶ Exécuter")
        btn_run.setToolTip("Sélectionner et exécuter un script externe sur le JSON")
        btn_run.setStyleSheet("""
            font-family: 'IBM Plex Mono'; font-size: 14pt; font-weight: bold; color:  #2C2C2C;
        """)
        btn_run.clicked.connect(self.controller.handle_run_script)
        toolbar.addWidget(btn_run)

    def clear_toolbar_modes(self):
        """Décoche le bouton actif dans la toolbar quand le canvas quitte un mode."""
        checked_action = self.action_group.checkedAction()
        if checked_action:
            checked_action.setChecked(False)

    def _create_declaration_widget(self, icon: QIcon, on_add_clicked):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(4, 0, 4, 0)
        layout.setSpacing(4)

        icon_label = QLabel()
        icon_label.setPixmap(icon.pixmap(16, 16))
        layout.addWidget(icon_label)

        items_container = QWidget()
        items_layout = QHBoxLayout(items_container)
        items_layout.setContentsMargins(0, 0, 0, 0)
        items_layout.setSpacing(4)
        layout.addWidget(items_container)

        add_btn = QToolButton()
        add_btn.setText("+")
        add_btn.setFixedSize(28, 28)
        add_btn.setObjectName("miniAddBtn")
        add_btn.clicked.connect(on_add_clicked)
        layout.addWidget(add_btn)
        
        return widget, items_layout

    def _show_add_action_popup(self):
        add_btn = self.actions_widget.findChild(QToolButton)
        popup = InlineAddPopup(self)
        popup.validated.connect(self.controller.submit_action)
        
        # Positionner la popup sous le bouton '+'
        btn_pos = add_btn.mapToGlobal(QPoint(0, add_btn.height()))
        popup.show_at(btn_pos)

    def _show_add_clock_popup(self):
        add_btn = self.clocks_widget.findChild(QToolButton)
        popup = InlineAddPopup(self)
        popup.validated.connect(self.controller.submit_clock)
        
        # Positionner la popup sous le bouton '+'
        btn_pos = add_btn.mapToGlobal(QPoint(0, add_btn.height()))
        popup.show_at(btn_pos)

    def _setup_menubar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False) 
        
        menu_fichier = menubar.addMenu("Fichier")
        action_new = QAction("Nouveau", self)
        action_new.setShortcut(QKeySequence.New)
        action_new.triggered.connect(self.controller.handle_new_file)
        action_open = QAction("Ouvrir", self)
        action_open.setShortcut(QKeySequence.StandardKey.Open)
        action_open.triggered.connect(self.controller.trigger_open_dialog)
        action_save = QAction("Sauvegarder", self)
        action_save.setShortcut(QKeySequence.StandardKey.Save)
        action_save.triggered.connect(self.controller.trigger_save_dialog)
        action_debug = QAction("Afficher l'instance Modèle", self)
        action_debug.setShortcut("Ctrl+D")
        action_debug.triggered.connect(self.controller.debug_print_model_instance)
        menu_fichier.addAction(action_new)
        menu_fichier.addAction(action_open)
        menu_fichier.addAction(action_save)
        
        menu_fichier.addSeparator()
        #menu_fichier.addAction(action_debug)
        menu_fichier.addSeparator()
        action_quit = QAction("Quitter", self)
        action_quit.setShortcut(QKeySequence.Quit)
        action_quit.triggered.connect(self.close)
        menu_fichier.addAction(action_quit)
        
        # Menu Aide
        menu_aide = menubar.addMenu("Aide")
        
        action_about = QAction("À propos", self)
        action_about.triggered.connect(self.show_about)
        menu_aide.addAction(action_about)
        action_manual = QAction("Manuel d'utilisation", self)
        action_manual.triggered.connect(self.show_user_manual)
        menu_aide.addAction(action_manual)

    def update_actions_display(self, actions: list):
        self._clear_layout(self.actions_layout)
        if not actions:
            lbl = QLabel("Aucune")
            lbl.setStyleSheet("color: #0D99FF; font-family: 'IBM Plex Mono'; font-size: 12pt; font-style: italic;")
            self.actions_layout.addWidget(lbl)
        else:
            for i, act in enumerate(actions):
                lbl = self._create_context_label(act, "action")
                self.actions_layout.addWidget(lbl)
                if i < len(actions) - 1:
                    sep = QLabel(",")
                    sep.setStyleSheet("color: #0D99FF; font-family: 'IBM Plex Mono'; font-size: 12pt;")
                    self.actions_layout.addWidget(sep)

    def update_clocks_display(self, clocks: list):
        self._clear_layout(self.clocks_layout)
        if not clocks:
            lbl = QLabel("Aucune")
            lbl.setStyleSheet("color: #0D99FF; font-family: 'IBM Plex Mono'; font-size: 12pt; font-style: italic;")
            self.clocks_layout.addWidget(lbl)
        else:
            for i, clk in enumerate(clocks):
                lbl = self._create_context_label(clk, "clock")
                self.clocks_layout.addWidget(lbl)
                if i < len(clocks) - 1:
                    sep = QLabel(",")
                    sep.setStyleSheet("color: #0D99FF; font-family: 'IBM Plex Mono'; font-size: 12pt;")
                    self.clocks_layout.addWidget(sep)

    def _clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def _create_context_label(self, text, item_type):
        lbl = QLabel(text)
        lbl.setStyleSheet("color: #0D99FF; font-family: 'IBM Plex Mono'; font-size: 12pt; font-style: italic;")
        lbl.setCursor(Qt.PointingHandCursor)
        
        # Remplacer le clic droit par un clic gauche pour le menu
        def show_menu_on_left_click(event, label=lbl, item_type=item_type):
            if event.button() == Qt.LeftButton:
                self._show_item_context_menu(label, event.pos(), item_type)
        lbl.mousePressEvent = show_menu_on_left_click
        return lbl

    def _show_item_context_menu(self, label, pos, item_type):
        menu = QMenu(self)
        mod_action = menu.addAction("Modifier")
        del_action = menu.addAction("Supprimer")
        action = menu.exec(label.mapToGlobal(pos))
        
        if action == mod_action:
            dialog = QInputDialog(self)
            dialog.setWindowTitle(f"Modifier {item_type}")
            dialog.setLabelText("Nouveau nom :")
            dialog.setTextValue(label.text())
            
            ok = dialog.exec()
            new_name = dialog.textValue()
            
            if ok and new_name.strip() and new_name.strip() != label.text():
                if item_type == "action":
                    self.controller.handle_modify_action(label.text(), new_name.strip())
                else:
                    self.controller.handle_modify_clock(label.text(), new_name.strip())
        elif action == del_action:
            msg_box = QMessageBox(self)
            msg_box.setWindowTitle("Confirmation")
            msg_box.setText(f"Voulez-vous vraiment supprimer '{label.text()}' (et toutes les contraintes associées) ?")
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            
            reply = msg_box.exec()
            
            if reply == QMessageBox.Yes:
                if item_type == "action":
                    self.controller.handle_delete_action(label.text())
                else:
                    self.controller.handle_delete_clock(label.text())

    def update_locations_list(self, locations: list, current_init: str):
        self.init_state_combo.blockSignals(True)
        self.init_state_combo.clear()
        self.init_state_combo.addItems(locations)
        if current_init in locations:
            self.init_state_combo.setCurrentText(current_init)
        self.init_state_combo.blockSignals(False)

    def refresh_graph_display(self):
        self.canvas.scene.clear()
        self.canvas.nodes.clear()
        self.canvas._cleanup_temp_transition()
        
        # Récupération des données depuis le Modèle
        data = self.controller.model.data
        
        # Mise à jour des listes d'actions et d'horloges dans la barre d'outils
        self.update_actions_display(data.get("actions", []))
        self.update_clocks_display(data.get("clocks", []))
        
        locations = data.get("locations", {})
        init_node = data.get("init", "")
        
        # Mise à jour de la liste de sélection de l'état initial
        self.update_locations_list(list(locations.keys()), init_node)

        # 2. Dessin des Nœuds (Localités)
        for node_id, node_data in locations.items():
            # Extraire les coordonnées
            pos = node_data.get("node_pos", {})
            try:
                x_val = float(pos.get("x", 0.0))
                y_val = float(pos.get("y", 0.0))
            except (ValueError, TypeError):
                x_val, y_val = 0.0, 0.0
            is_initial = (node_id == init_node)
            
            # Instancier le nœud graphique (Utilisation de la méthode existante draw_node qui gère le NodeItem)
            self.canvas.draw_node(node_id, x_val, y_val, is_initial)
            
        # 3. Dessin des Transitions
        transitions = data.get("transitions", [])
        for t in transitions:
            trans_id = t.get("id")
            source_id = t.get("source")
            target_id = t.get("target")
            nails_pos = t.get("nails", [])
            
            clean_nails = []
            if isinstance(nails_pos, list):
                for n in nails_pos:
                    try:
                        if isinstance(n, dict):
                            clean_nails.append((float(n.get("x", 0.0)), float(n.get("y", 0.0))))
                        elif isinstance(n, (list, tuple)) and len(n) >= 2:
                            clean_nails.append((float(n[0]), float(n[1])))
                    except (ValueError, TypeError):
                        pass

            # Déléguer la création à la logique MVC existante du Canvas
            self.canvas.draw_transition(trans_id, source_id, target_id, clean_nails)

    def open_data_editor(self):
        """Instancie et affiche la fenêtre de l'éditeur de données."""
        dialog = DataEditorDialog(self)
        
        # 1. Charger les données du modèle
        dialog.load_data(
            self.controller.model.data.get("variables", {}), 
            self.controller.model.data.get("actions", [])
        )
        
        # 2. Si l'utilisateur valide (Ok), on récupère et sauvegarde les données
        if dialog.exec():
            new_variables_data = dialog.get_data()
            self.controller.update_variables_data(new_variables_data)
            
    def update_window_title(self, filepath=None):
        if filepath:
            filename = QFileInfo(filepath).fileName()
            self.setWindowTitle(f"{filename}")
        else:
            self.setWindowTitle("Untitled")

    def show_about(self):
        QMessageBox.about(
            self,
            "À propos",
            "<h3>Interface de Dessin d'Automates Temporisés étendus par la donnée</h3>"
            "<p>Projet COSMO - CILS 2025.</p>"
            "<p>Interface graphique pour modéliser, éditer et exporter des automates temporisés au format JSON.</p>"
        )

    def show_user_manual(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Guide d'utilisation")
        dialog.resize(super().width() * 0.8, super().height() * 0.8)  # Taille initiale de la fenêtre (70% de la taille du parent)
        
        
        dialog.setStyleSheet("""
            QTextBrowser {
                background-color: #FFFFFF;
                color: #2C2C2C;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 10px;
            }
        """)
        
        layout = QVBoxLayout(dialog)
        
        text_browser = QTextBrowser(dialog)
        text_browser.setOpenExternalLinks(True)
        
        # Calcul du chemin absolu dynamique pour la compatibilité avec PyInstaller (--onefile)
        if hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
            
        # Indique au navigateur web interne où chercher le dossier "resources/images/"
        text_browser.setSearchPaths([base_path.replace('\\', '/')])

        html_content = """
        <style>
            body { font-family: 'IBM Plex Mono', monospace; font-size: 11pt; }
            h2 { color: #2C2C2C; border-bottom: 1px solid #CCCCCC; padding-bottom: 5px; margin-top: 20px; }
            h3 { color: #2C2C2C; margin-top: 15px; }
            ul { margin-top: 5px; }
            li { margin-bottom: 8px; }
            img {
                max-width: 100%;
                height: auto;
            }
            .screenshot-placeholder { background-color: #EBEBEB; padding: 15px; border-left: 4px solid #AAAAAA; margin: 15px 0; color: #555555; font-style: italic; font-weight: bold; text-align: center;}
        </style>

        <h1>Guide d'Utilisation</h1>
        <p>Bienvenue dans l'éditeur graphique d'automates temporisés étendus par la donnée.</p>
        
        <p align="center"><img src="resources/images/main-window.png"></p>

        <h2>1. Modélisation Graphique & Propriétés</h2>
        
        <h3>1.1. Les Localités (États) et Invariants</h3>
        <ul>
            <li><b>Création :</b> Activez l'outil <b>Nouvelle Localité</b> dans la barre d'outils, puis cliquez n'importe où sur l'espace de travail.</li>
            <li><b>État Initial :</b> La première localité créée est automatiquement définie comme état initial (double bordure). Vous pouvez modifier l'état initial via le menu déroulant <b>Init :</b> situé dans la barre d'outils.</li>
            <li><b>Invariants :</b> Faites un <b>clic gauche</b> sur la localité pour ouvrir le panneau latéral de propriétés. Choisissez l'horloge, l'opérateur (<=, >=, ==), une horloge et/ou une valeur constante. Cliquez sur le bouton <b>+</b> pour valider. Double-cliquez sur un invariant existant pour le modifier.</li>
            <li><b>Déplacement & Suppression :</b> Cliquez et glissez pour déplacer. Pour supprimer, faites un clic gauche (qui ouvre le panneau latéral) puis cliquez sur le bouton rouge <b>Supprimer la localité</b>.</li>
        </ul>
        <p align="center"><img src="resources/images/node.png" alt="Localité et Invariants"></p>

        <h3>1.2. Les Transitions, Gardes et Actions</h3>
        <ul>
            <li><b>Création :</b> Activez l'outil <b>Nouvelle Transition</b>. Cliquez sur la source, ajoutez des points de courbure (clous) en cliquant dans le vide si besoin, puis cliquez sur la cible.</li>
            <li><b>Gardes :</b> Faites un <b>clic gauche</b> sur la flèche pour ouvrir le panneau de propriétés. Ajoutez des conditions de franchissement (gardes) de la même manière que les invariants.</li>
            <li><b>Actions & Resets :</b> Toujours dans les propriétés, associez une <b>Action</b> déclarée via le menu déroulant, et cochez les horloges à remettre à zéro (<b>Resets</b>) lors du franchissement.</li>
            <li><b>Modification :</b> Réassignez facilement la source ou la cible via les menus déroulants en haut du panneau de propriétés.</li>
            <li><b>Annulation :</b> Appuyez sur la touche <b>Échap</b> pendant la création pour annuler.</li>
        </ul>
        <p align="center"><img src="resources/images/transition.png" alt="Transition et Propriétés"></p>

        <h2>2. Déclarations Globales (Barre d'outils)</h2>
        <p>Dans la barre d'outils, cliquez sur le petit bouton <b>+</b> à côté de l'icône Horloge ou Action pour afficher la popup de saisie. Renseignez le nom et appuyez sur Entrée. Un <b>clic gauche</b> sur le nom déclaré permet de le renommer ou de le supprimer.</p>
        <p align="center"><img src="resources/images/add-action.png" alt="Barre d'outils (Horloges et Actions)"></p>
        <p align="center"><img src="resources/images/delete-action.png"  alt="Barre d'outils (Horloges et Actions)"></p>

        <h2>3. L'Éditeur de Données (Bouton "Data")</h2>
        <p>Cliquez sur le bouton <b>Data</b> pour ouvrir la fenêtre</p>
        
        <h3>3.1. Variable et Initialisation</h3>
        <p>Dans le premier onglet, tapez librement vos déclarations de variables globales (ex: <i>int timer;</i>) et l'initialisation de ces variables (ex: <i>timer = 0;</i>).</p>
        <p align="center"><img src="resources/images/data-variable.png"  alt="Éditeur de données"></p>

        <h3>3.2. Données Additionnelles (Define, Alias & Structures)</h3>
        <p>Cet onglet centralise les définitions de types et macros C/C++</p>
        <ul>
            <li><b>Define :</b> Un éditeur de texte libre pour saisir vos directives de préprocesseur et constantes globales (ex: <code>#define MAX_SIZE 100</code>).</li>
            <li><b>Alias :</b> Cliquez sur le bouton <b>+</b> de la ligne Alias pour ajouter un nouvel alias. Entrez le nom (ex: <i>uint8</i>) puis sa définition dans le champ apparu.</li>
            <li><b>Structures :</b> Cliquez sur le <b>+</b> pour nommer et générer un nouveau bloc de définition de structure de structure (<code>struct</code>). Vous pouvez ensuite y taper le code C/C++ correspondant.</li>
        </ul>
        <p align="center"><img src="resources/images/data-addi.png" alt="Éditeur de données additionnelles"></p>

        <h3>3.3. Actions (Update functions & Contraintes)</h3>
        <p>L'onglet "Actions" crée automatiquement un sous-onglet pour chaque action du modèle. Vous pouvez y associer des fonctions de mise à jour spécifiques (Update functions) et écrire des contraintes.</p>
        <p align="center"><img src="resources/images/data-actions.png" alt="Actions Data Editor"></p>
        <h2>4. Exécution</h2>
        <p align="center"><img src="resources/images/script-run.png" alt="Exécution de Script"></p>
        <ul>
            <li><b>Exécuter :</b> Permet de sélectionner un script externeet de l'exécuter sur le fichier JSON du modèle actuel (sauvegarde en arrière-plan de la dernière version), et si le modèle est vierge, propose d'en sélectionner un et d'exécuter ensuite le script sélectionné juste après.</li>
        </ul>

        <h2>5. Menus et Raccourcis Clavier</h2>
        
        <h3>5.1. Menu Fichier</h3>
        <p align="center"><img src="resources/images/menu-file.png" alt="Menu Fichier"></p>
        
        <ul>
            <li><b>Nouveau (Ctrl+N / Cmd+N) :</b> Crée un nouveau modèle vierge.</li>
            <li><b>Ouvrir (Ctrl+O / Cmd+O) :</b> Charge un modèle existant au format JSON.</li>
            <li><b>Sauvegarder (Ctrl+S / Cmd+S) :</b> Enregistre votre modèle actuel au format JSON.</li>
            <li><b>Quitter (Ctrl+Q / Cmd+Q) :</b> Ferme l'application.</li>
        </ul>

        <h3>5.2. Menu Aide</h3>
        <p align="center"><img src="resources/images/menu-help.png" alt="Menu Aide"></p>

        <ul>
            <li><b>À propos :</b> Affiche une brève description de l'outil.</li>
            <li><b>Manuel d'utilisation :</b> Ouvre ce guide d'utilisation.</li>
        </ul>
        
        
        <h3>5.3. Autres Actions</h3>
            <ul>
                <li><b>Échap :</b> Annule le mode de création en cours (utile si vous avez commencé à tracer une transition et souhaitez l'annuler).</li>
            </ul>

        """
        
        text_browser.setHtml(html_content)
        
        btn_close = QPushButton("Fermer")
        btn_close.clicked.connect(dialog.accept)
        
        layout.addWidget(text_browser)
        layout.addWidget(btn_close)
        
        dialog.exec()