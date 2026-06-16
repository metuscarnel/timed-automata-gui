from PySide6.QtWidgets import QDialog, QVBoxLayout, QTabWidget, QWidget, QDialogButtonBox, QTextEdit, QHBoxLayout, QLabel, QToolButton, QScrollArea, QLineEdit
from PySide6.QtCore import QPoint, Qt

from .popups import InlineAddPopup

class DataEditorDialog(QDialog):
    """Fenêtre de dialogue dédiée à l'édition des variables de données, opérations et paramètres."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Éditeur de Données")
        if parent:
            self.resize(int(parent.width() * 0.7), int(parent.height() * 0.7))
        else:
            self.resize(1000, 600)

        # --- STYLESHEET (Uniformisation avec le reste de l'application) ---
        self.setStyleSheet("""
            QWidget {
                font-family: 'IBM Plex Mono';
            }
            QTextEdit, QListWidget, QLineEdit, QComboBox {
                background-color: #FFFFFF;
                color: #000000;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px;
            }
            QTextEdit:hover, QListWidget:hover, QLineEdit:hover, QComboBox:hover {
                border: 1px solid #AAAAAA;
            }
            QTextEdit:focus, QListWidget:focus, QLineEdit:focus, QComboBox:focus {
                border: 1px solid #0D99FF;
            }
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                background-color: #FFFFFF;
            }
            QTabBar::tab {
                background-color: #FAFAFA;
                border: 1px solid #CCCCCC;
                border-bottom-color: #CCCCCC;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                padding: 8px 16px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background-color: #FFFFFF;
                border-bottom-color: #FFFFFF;
                font-weight: bold;
            }
            QTabBar::tab:hover:!selected {
                background-color: #E0E0E0;
            }
            QLabel {
                font-weight: bold;
                color: #2C2C2C;
            }
        """)
        
        # --- Dictionnaires pour référencer les champs de textes dynamiques ---
        self.action_widgets = {}
        self.structure_widgets = {}
        self.alias_widgets = {}

        # Layout principal de la boîte de dialogue
        main_layout = QVBoxLayout(self)

        # Création du QTabWidget contenant les différents onglets
        self.tab_widget = QTabWidget()
        
      

        # Onglet 2 : Variable (Anciennement Opérations)
        self.tab_definitions = QWidget()
        self.layout_definitions = QVBoxLayout(self.tab_definitions)
        
        # Section Variable
        self.layout_variable = QVBoxLayout()
        self.label_variable = QLabel("Variables")
        self.content_variable = QTextEdit()
        self.content_variable.setPlaceholderText("Variables...")
        self.layout_variable.addWidget(self.label_variable)
        self.layout_variable.addWidget(self.content_variable)
        self.layout_definitions.addLayout(self.layout_variable)
        
        # Section Initialisation
        self.layout_initialisation = QVBoxLayout()
        self.label_initialisation = QLabel("Initialisation")
        self.content_initialisation = QTextEdit()
        self.content_initialisation.setPlaceholderText("Initialisations...")
        self.layout_initialisation.addWidget(self.label_initialisation)
        self.layout_initialisation.addWidget(self.content_initialisation)
        self.layout_definitions.addLayout(self.layout_initialisation)
        
        self.tab_widget.addTab(self.tab_definitions, "Variable")
        
        # Onglet 1 : Données Additionelles (Anciennement Variables)
        self.tab_additional_data = QScrollArea()
        self.tab_additional_data.setWidgetResizable(True)
        self.tab_additional_data.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.container_additional_data = QWidget()
        self.layout_additional_data = QVBoxLayout(self.container_additional_data)
        self.layout_additional_data.setAlignment(Qt.AlignTop)
        self.tab_additional_data.setWidget(self.container_additional_data)
        
        # Section Define
        self.layout_define = QVBoxLayout()
        self.label_define = QLabel("Define")
        self.content_define = QTextEdit()
        self.content_define.setPlaceholderText("Define...")
        self.content_define.setMinimumHeight(200)
        self.layout_define.addWidget(self.label_define)
        self.layout_define.addWidget(self.content_define)
        self.layout_additional_data.addLayout(self.layout_define)
        
        # Section Alias
        self.header_alias = QHBoxLayout()
        self.label_alias = QLabel("Alias")
        self.btn_add_alias = QToolButton()
        self.btn_add_alias.setText("+")
        self.btn_add_alias.setFixedSize(28, 28)
        self.btn_add_alias.setObjectName("miniAddBtn")
        self.btn_add_alias.setToolTip("Ajouter un nouvel alias")
        self.btn_add_alias.clicked.connect(self._show_add_alias_popup)
        
        self.header_alias.addWidget(self.label_alias)
        self.header_alias.addStretch()
        self.header_alias.addWidget(self.btn_add_alias)
        self.layout_additional_data.addLayout(self.header_alias)
        
        self.layout_aliases_list = QVBoxLayout()
        self.layout_aliases_list.setAlignment(Qt.AlignTop)
        self.layout_additional_data.addLayout(self.layout_aliases_list)

        # Section Structures
        self.header_structures = QHBoxLayout()
        self.label_structures = QLabel("Structures")
        self.btn_add_structure = QToolButton()
        self.btn_add_structure.setText("+")
        self.btn_add_structure.setFixedSize(28, 28)
        self.btn_add_structure.setObjectName("miniAddBtn")
        self.btn_add_structure.setToolTip("Ajouter une nouvelle structure")
        self.btn_add_structure.clicked.connect(self._show_add_structure_popup)
        
        self.header_structures.addWidget(self.label_structures)
        self.header_structures.addStretch()
        self.header_structures.addWidget(self.btn_add_structure)
        self.layout_additional_data.addLayout(self.header_structures)
        
        self.layout_structures_list = QVBoxLayout()
        self.layout_structures_list.setAlignment(Qt.AlignTop)
        self.layout_additional_data.addLayout(self.layout_structures_list)

        self.tab_widget.addTab(self.tab_additional_data, "Données Additionelles")

        # Onglet 3 : Actions
        self.tab_actions = QWidget()
        self.layout_actions = QVBoxLayout(self.tab_actions)
        
        self.actions_tab_widget = QTabWidget()
        self.layout_actions.addWidget(self.actions_tab_widget)
        
        self.tab_widget.addTab(self.tab_actions, "Actions")

        main_layout.addWidget(self.tab_widget)

        # Boutons de validation (Ok et Annuler) en bas de la fenêtre
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        main_layout.addWidget(self.button_box)

    def _show_add_structure_popup(self):
        """Affiche la popup pour ajouter une structure."""
        popup = InlineAddPopup(self)
        popup.validated.connect(self._on_structure_added_from_popup)
        btn_pos = self.btn_add_structure.mapToGlobal(QPoint(0, self.btn_add_structure.height()))
        popup.show_at(btn_pos)

    def _show_add_alias_popup(self):
        """Affiche la popup pour ajouter un alias."""
        popup = InlineAddPopup(self)
        popup.validated.connect(self._on_alias_added_from_popup)
        btn_pos = self.btn_add_alias.mapToGlobal(QPoint(0, self.btn_add_alias.height()))
        popup.show_at(btn_pos)

    def _on_alias_added_from_popup(self, alias_name):
        self._add_alias_to_list(alias_name)

    def _on_structure_added_from_popup(self, struct_name):
        self._add_structure_to_list(struct_name)

    def load_data(self, data, actions=None):
        """Remplit les onglets avec les données existantes du modèle."""
        if actions is None: 
            actions = []
        # 1. Données Additionelles (Define / Alias)
        define_list = data.get("definition", {}).get("define", [])
        self.content_define.setText("\n".join(define_list))
        
        alias_data = data.get("definition", {}).get("typedef", {}).get("alias", {})
        if isinstance(alias_data, dict):
            for a_name, a_val in alias_data.items():
                self._add_alias_to_list(a_name, str(a_val))
        elif isinstance(alias_data, list):
            # Rétrocompatibilité avec d'anciens fichiers où les alias auraient pu être une liste
            for i, a_val in enumerate(alias_data):
                self._add_alias_to_list(f"alias_{i}", str(a_val))
        
        structure_data = data.get("definition", {}).get("typedef", {}).get("structure", {})
        for struct_name, struct_content in structure_data.items():
            if struct_name == "Variable":
                continue # On ignore la clé "Variable" ici pour ne pas créer un onglet supplémentaire
            content_text = "\n".join(struct_content) if isinstance(struct_content, list) else str(struct_content) if struct_content else ""
            self._add_structure_to_list(struct_name, content_text)
        
        # 2. Variable (Variable / Initialisation)
        var_list = structure_data.get("Variable", [])
        self.content_variable.setText("\n".join(var_list) if isinstance(var_list, list) else str(var_list))
        
        # Chargement des variables d'initialisation
        init_list = data.get("init_variables", [])
        self.content_initialisation.setText("\n".join(init_list) if isinstance(init_list, list) else str(init_list))
        
        # 3. Actions (Update-functions et Contraintes par sous-onglets)
        self.actions_tab_widget.clear()
        self.action_widgets = {}
        
        update_funcs = data.get("update_functions", {})
        constraints = data.get("constraints", {})
        
        for action in actions:
            tab = QWidget()
            layout = QVBoxLayout(tab)
            
            label_update = QLabel(f"Update-function pour '{action}'")
            text_update = QTextEdit()
            text_update.setPlaceholderText(f"Saisissez la fonction de mise à jour pour {action}...")
            u_data = update_funcs.get(action, [])
            text_update.setText("\n".join(u_data) if isinstance(u_data, list) else str(u_data) if u_data else "")
            
            label_constraint = QLabel(f"Contrainte pour '{action}'")
            text_constraint = QTextEdit()
            text_constraint.setPlaceholderText(f"Saisissez la contrainte pour {action}...")
            c_data = constraints.get(action, [])
            text_constraint.setText("\n".join(c_data) if isinstance(c_data, list) else str(c_data) if c_data else "")
            
            layout.addWidget(label_update)
            layout.addWidget(text_update)
            layout.addWidget(label_constraint)
            layout.addWidget(text_constraint)
            
            self.actions_tab_widget.addTab(tab, action)
            self.action_widgets[action] = {"update": text_update, "constraint": text_constraint}

    def get_data(self):
        """Extrait toutes les données saisies sous forme de dictionnaire."""
        define_text = self.content_define.toPlainText().strip()
        
        alias_dict = {}
        for a_name, a_widget in self.alias_widgets.items():
            a_text = a_widget.text().strip()
            if a_text:
                alias_dict[a_name] = a_text

        variable_text = self.content_variable.toPlainText().strip()
        initialisation_text = self.content_initialisation.toPlainText().strip()
        
        structures_dict = {}
        if variable_text:
            structures_dict["Variable"] = variable_text.split('\n')
            
        for s_name, s_widget in self.structure_widgets.items():
            s_text = s_widget.toPlainText().strip()
            structures_dict[s_name] = s_text.split('\n') if s_text else []
                
        update_functions_dict = {}
        constraints_dict = {}
        for action, widgets in self.action_widgets.items():
            u_text = widgets["update"].toPlainText().strip()
            c_text = widgets["constraint"].toPlainText().strip()
            if u_text:
                update_functions_dict[action] = u_text.split('\n')
            if c_text:
                constraints_dict[action] = c_text.split('\n')
        
        return {
            "definition": {
                "define": define_text.split('\n') if define_text else [],
                "typedef": { "structure": structures_dict, "alias": alias_dict }
            },
            "init_variables": initialisation_text.split('\n') if initialisation_text else [],
            "update_functions": update_functions_dict,
            "constraints": constraints_dict
        }

    def _add_structure_to_list(self, struct_name, content_text=""):
        """Ajoute une structure et sa zone de texte associée."""
        if struct_name in self.structure_widgets: 
            return
        
        struct_widget = QWidget()
        struct_layout = QVBoxLayout(struct_widget)
        struct_layout.setContentsMargins(0, 0, 0, 0)
        
        struct_label = QLabel(struct_name)
        struct_textedit = QTextEdit()
        struct_textedit.setPlaceholderText(f"Contenu de la structure {struct_name}...")
        struct_textedit.setText(content_text)
        struct_textedit.setMinimumHeight(200)
        
        struct_layout.addWidget(struct_label)
        struct_layout.addWidget(struct_textedit)
        
        self.layout_structures_list.addWidget(struct_widget)
        self.structure_widgets[struct_name] = struct_textedit

    def _add_alias_to_list(self, alias_name, content_text=""):
        """Ajoute un alias sous forme clé-valeur sur une seule ligne."""
        if alias_name in self.alias_widgets: 
            return
        
        alias_widget = QWidget()
        alias_layout = QHBoxLayout(alias_widget)
        alias_layout.setContentsMargins(0, 0, 0, 0)
        
        alias_label = QLabel(f"{alias_name} :")
        alias_lineedit = QLineEdit(self)
        alias_lineedit.setPlaceholderText(f"Valeur pour {alias_name}...")
        alias_lineedit.setText(content_text)
        
        alias_layout.addWidget(alias_label)
        alias_layout.addWidget(alias_lineedit)
        
        self.layout_aliases_list.addWidget(alias_widget)
        self.alias_widgets[alias_name] = alias_lineedit