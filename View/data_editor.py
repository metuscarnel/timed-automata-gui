from PySide6.QtWidgets import (QDialog, QVBoxLayout, QTabWidget,
                               QWidget, QDialogButtonBox, QTextEdit, QHBoxLayout, QLabel, QToolButton, QListWidget, QComboBox, QLineEdit, QPushButton, QScrollArea)
from PySide6.QtCore import QPoint, Qt

from .popups import InlineAddPopup

class DataEditorDialog(QDialog):
    """Fenêtre de dialogue dédiée à l'édition des variables de données, opérations et paramètres."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Éditeur de Données")
        self.resize(500, 400)

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
                border: 1px solid #0D99FF; /* Bordure bleu électrique au focus */
            }
            QPushButton {
                background-color: #EBEBEB;
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 6px 16px;
                color: #2C2C2C;
            }
            QPushButton:hover {
                background-color: #E0E0E0;
                border: 1px solid #AAAAAA;
            }
            QPushButton:pressed {
                background-color: #D5D5D5;
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

        # Layout principal de la boîte de dialogue
        main_layout = QVBoxLayout(self)

        # Création du QTabWidget contenant les différents onglets
        self.tab_widget = QTabWidget()
        
      

        # Onglet 2 : Opérations (avec layout basique vide)
        self.tab_definitions = QWidget()
        self.layout_definitions = QHBoxLayout(self.tab_definitions)
        
        # Section Define
        self.layout_define = QVBoxLayout()
        self.label_define = QLabel("Define")
        self.content_define = QTextEdit()
        self.content_define.setPlaceholderText("Saisissez le contenu pour Define...")
        self.layout_define.addWidget(self.label_define)
        self.layout_define.addWidget(self.content_define)
        self.layout_definitions.addLayout(self.layout_define)
        
        # Section Alias
        self.layout_alias = QVBoxLayout()
        self.label_alias = QLabel("Alias")
        self.content_alias = QTextEdit()
        self.content_alias.setPlaceholderText("contenu textuel...")
        self.layout_alias.addWidget(self.label_alias)
        self.layout_alias.addWidget(self.content_alias)
        self.layout_definitions.addLayout(self.layout_alias)
        
        self.tab_widget.addTab(self.tab_definitions, "Opérations")
        # Onglet 1 : Variables (avec layout basique vide)
        self.tab_variables = QWidget()
        self.layout_variables = QVBoxLayout(self.tab_variables)
        
        # --- NOUVEAU : En-tête avec le bouton + pour les variables ---
        self.header_variables = QHBoxLayout()
        self.label_variables = QLabel("Liste des variables")
        self.btn_add_variable = QToolButton()
        self.btn_add_variable.setText("+")
        self.btn_add_variable.setFixedSize(24, 24)
        self.btn_add_variable.setToolTip("Ajouter une nouvelle variable")
        
        self.header_variables.addWidget(self.label_variables)
        self.header_variables.addStretch() # Pousse le bouton à droite
        self.header_variables.addWidget(self.btn_add_variable)
        self.layout_variables.addLayout(self.header_variables)
        
        # --- NOUVEAU : Zone défilante pour lister des widgets complexes (Label + TextEdit) ---
        self.scroll_variables = QScrollArea()
        self.scroll_variables.setWidgetResizable(True)
        self.scroll_variables.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.container_variables = QWidget()
        self.layout_variables_list = QVBoxLayout(self.container_variables)
        self.layout_variables_list.setAlignment(Qt.AlignTop)
        self.scroll_variables.setWidget(self.container_variables)
        self.layout_variables.addWidget(self.scroll_variables)

        self.btn_add_variable.clicked.connect(self._show_add_variable_popup)
        self.tab_widget.addTab(self.tab_variables, "Variables")

        # Onglet 3 : Contraintes (Initialisation des variables)
        self.tab_constraints = QWidget()
        self.layout_constraints = QVBoxLayout(self.tab_constraints)
        
        self.constraint_edit_layout = QHBoxLayout()
        
        self.combo_constraint_var = QComboBox()
        
        self.label_constraint_eq = QLabel("=")
        
        self.line_constraint_value = QLineEdit()
        self.line_constraint_value.setPlaceholderText("Valeur d'initialisation...")
        
        self.btn_add_constraint = QPushButton("+")
        
        self.constraint_edit_layout.addWidget(self.combo_constraint_var)
        self.constraint_edit_layout.addWidget(self.label_constraint_eq)
        self.constraint_edit_layout.addWidget(self.line_constraint_value)
        self.constraint_edit_layout.addWidget(self.btn_add_constraint)
        self.layout_constraints.addLayout(self.constraint_edit_layout)
        
        self.list_constraints = QListWidget()
        self.layout_constraints.addWidget(self.list_constraints)
        
        self.btn_add_constraint.clicked.connect(self._add_constraint_to_list)

        # --- NOUVEAU : Zone défilante pour les contraintes par variable ---
        self.label_var_constraints = QLabel("Contraintes des variables :")
        self.layout_constraints.addWidget(self.label_var_constraints)
        
        self.scroll_var_constraints = QScrollArea()
        self.scroll_var_constraints.setWidgetResizable(True)
        self.scroll_var_constraints.setStyleSheet("QScrollArea { border: none; background-color: transparent; }")
        
        self.container_var_constraints = QWidget()
        self.layout_var_constraints_list = QVBoxLayout(self.container_var_constraints)
        self.layout_var_constraints_list.setAlignment(Qt.AlignTop)
        self.scroll_var_constraints.setWidget(self.container_var_constraints)
        self.layout_constraints.addWidget(self.scroll_var_constraints)

        self.tab_widget.addTab(self.tab_constraints, "Contraintes")

        main_layout.addWidget(self.tab_widget)

        # Boutons de validation (Ok et Annuler) en bas de la fenêtre
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        
        main_layout.addWidget(self.button_box)

    def _show_add_variable_popup(self):
        """Affiche la popup pour ajouter une variable."""
        popup = InlineAddPopup(self)
        popup.validated.connect(self._add_variable_to_list)
        
        # Positionner la popup sous le bouton '+'
        btn_pos = self.btn_add_variable.mapToGlobal(QPoint(0, self.btn_add_variable.height()))
        popup.show_at(btn_pos)

    def _add_variable_to_list(self, var_name):
        """Ajoute la variable et sa zone de texte 'update-function' associée."""
        var_widget = QWidget()
        var_layout = QHBoxLayout(var_widget)
        var_layout.setContentsMargins(0, 0, 0, 0)
        
        var_label = QLabel(var_name)
        var_label.setFixedWidth(100) # Fixe la largeur pour que tous les champs textes soient alignés
        
        var_textedit = QTextEdit()
        var_textedit.setPlaceholderText(f"update-function pour {var_name}...")
        var_textedit.setMaximumHeight(60) # Limite la hauteur pour pouvoir voir plusieurs variables à la fois
        
        var_layout.addWidget(var_label)
        var_layout.addWidget(var_textedit)
        
        self.layout_variables_list.addWidget(var_widget)
        
        # --- NOUVEAU : Ajout de la contrainte associée dans l'onglet Contraintes ---
        var_constraint_widget = QWidget()
        var_constraint_layout = QHBoxLayout(var_constraint_widget)
        var_constraint_layout.setContentsMargins(0, 0, 0, 0)
        
        var_constraint_label = QLabel(var_name)
        var_constraint_label.setFixedWidth(100) # Fixe la largeur pour que tous les champs textes soient alignés
        
        var_constraint_textedit = QTextEdit()
        var_constraint_textedit.setPlaceholderText(f"Contrainte pour {var_name}...")
        var_constraint_textedit.setMaximumHeight(60) # Limite la hauteur
        
        var_constraint_layout.addWidget(var_constraint_label)
        var_constraint_layout.addWidget(var_constraint_textedit)
        
        self.layout_var_constraints_list.addWidget(var_constraint_widget)
        
        # On ajoute aussi la variable au menu déroulant pour l'initialisation
        self.combo_constraint_var.addItem(var_name)

    def _add_constraint_to_list(self):
        """Ajoute la contrainte d'initialisation dans la liste."""
        var = self.combo_constraint_var.currentText()
        val = self.line_constraint_value.text().strip()
        if var and val:
            self.list_constraints.addItem(f"{var} = {val}")
            self.line_constraint_value.clear()