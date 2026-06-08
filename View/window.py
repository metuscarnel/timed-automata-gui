from PySide6.QtWidgets import QMainWindow, QToolBar, QWidget, QLabel, QToolButton, QHBoxLayout, QComboBox, QMenu, QInputDialog, QMessageBox
from PySide6.QtGui import QAction, QKeySequence, QActionGroup, QIcon
from PySide6.QtCore import Qt, QPoint

from .canvas import AutomataView
from resources.icons import get_icons
from .properties_dock import PropertiesDock
from .popups import InlineAddPopup
from .data_editor import DataEditorDialog


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        
        # Taille dynamique : 80% de la résolution de l'écran disponible
        screen_geom = self.screen().availableGeometry()
        self.resize(int(screen_geom.width() * 0.8), int(screen_geom.height() * 0.8))
        
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
        add_btn.setFixedSize(24, 24)
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
        menu_fichier.addAction(action_debug)
        menu_fichier.addSeparator()
        action_quit = QAction("Quitter", self)
        action_quit.setShortcut(QKeySequence.Quit)
        action_quit.triggered.connect(self.close)
        menu_fichier.addAction(action_quit)
        
        # --- NOUVEAU : Menu Aide ---
        menu_aide = menubar.addMenu("Aide")
        
        action_about = QAction("À propos", self)
        action_about.triggered.connect(self.show_about)
        menu_aide.addAction(action_about)

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
        lbl.setContextMenuPolicy(Qt.CustomContextMenu)
        lbl.customContextMenuRequested.connect(lambda pos, label=lbl, t=item_type: self._show_item_context_menu(label, pos, t))
        return lbl

    def _show_item_context_menu(self, label, pos, item_type):
        menu = QMenu(self)
        mod_action = menu.addAction("Modifier")
        del_action = menu.addAction("Supprimer")
        action = menu.exec(label.mapToGlobal(pos))
        popup_style = """
            QDialog, QMessageBox, QInputDialog {
                background-color: #FAFAFA;
            }
            QLabel {
                color: #2C2C2C;
                font-family: 'IBM Plex Mono';
                font-size: 12pt;
            }
            QLineEdit {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px;
                font-family: 'IBM Plex Mono';
                font-size: 12pt;
            }
            QLineEdit:focus {
                border: 1px solid #0D99FF;
            }
            QPushButton {
                background-color: #EBEBEB;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px 16px;
                color: #2C2C2C;
                font-family: 'IBM Plex Mono';
            }
            QPushButton:hover {
                background-color: #E0E0E0;
            }
        """
        
        if action == mod_action:
            dialog = QInputDialog(self)
            dialog.setWindowTitle(f"Modifier {item_type}")
            dialog.setLabelText("Nouveau nom :")
            dialog.setTextValue(label.text())
            dialog.setStyleSheet(popup_style)
            
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
            msg_box.setStyleSheet(popup_style)
            
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
            self.canvas.draw_transition(source_id, target_id, clean_nails)

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

    def show_about(self):
        QMessageBox.about(
            self,
            "À propos",
            "<h3>Interface de Dessin d'Automates Temporisés étendus par la donnée</h3>"
            "<p>Projet COSMO - CILS 2025.</p>"
            "<p>Interface graphique pour modéliser, éditer et exporter des automates temporisés au format JSON.</p>"
        )