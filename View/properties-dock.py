from PySide6.QtWidgets import (QDockWidget, QWidget, QFormLayout, QLineEdit, QLabel,
                               QComboBox, QListWidget, QPushButton, QSpinBox, QVBoxLayout)
from PySide6.QtCore import Qt

class PropertiesDock(QDockWidget):
    def __init__(self, controller):
        super().__init__("Propriétés de l'élément")
        self.controller = controller
        
        # Variables d'état pour suivre la sélection actuelle
        self.current_node_id = None
        self.current_source_id = None
        self.current_target_id = None
        
        # Widget principal pour le contenu du dock
        self.main_widget = QWidget()
        self.main_layout = QVBoxLayout(self.main_widget)
        
        # --- Section pour l'ID et le Nom (similaire à PropertiesPanel) ---
        self.id_field = QLineEdit()
        self.id_field.setReadOnly(True)
        self.name_field = QLineEdit()
        
        basic_props_layout = QFormLayout()
        basic_props_layout.addRow("ID :", self.id_field)
        basic_props_layout.addRow("Nom :", self.name_field)
        self.main_layout.addLayout(basic_props_layout)

        # --- Widgets d'édition de contraintes ---
        self.combo_clock1 = QComboBox()
        self.combo_operator = QComboBox()
        self.combo_operator.addItems(["<=", ">=", "=="]) # Exemple d'opérateurs
        self.combo_clock2 = QComboBox()
        self.combo_clock2.addItem("---") # Option pour "pas de deuxième horloge"
        self.line_value = QLineEdit() # Ou QSpinBox si vous préférez
        # self.line_value = QSpinBox() # Si vous utilisez QSpinBox
        # self.line_value.setRange(-9999, 9999) # Exemple de plage pour QSpinBox
        
        constraint_input_layout = QFormLayout()
        constraint_input_layout.addRow("Horloge 1:", self.combo_clock1)
        constraint_input_layout.addRow("Opérateur:", self.combo_operator)
        constraint_input_layout.addRow("Horloge 2:", self.combo_clock2)
        constraint_input_layout.addRow("Valeur/Offset:", self.line_value)
        self.main_layout.addLayout(constraint_input_layout)
        
        # --- Bouton Ajouter/Modifier Contrainte ---
        self.btn_add_constraint = QPushButton("Ajouter")
        # Connecter ce bouton à la logique d'ajout/modification du contrôleur
        # Exemple: self.btn_add_constraint.clicked.connect(self.controller.add_constraint_handler)
        self.main_layout.addWidget(self.btn_add_constraint)
        
        # --- Liste des contraintes ---
        self.list_constraints = QListWidget()
        self.main_layout.addWidget(QLabel("Contraintes :"))
        self.main_layout.addWidget(self.list_constraints)

        # --- CONNEXION DU DOUBLE-CLIC (LA SOLUTION) ---
        self.list_constraints.itemDoubleClicked.connect(self.controller.handle_constraint_double_click)

        self.setWidget(self.main_widget)

        # --- Connexions pour la mise à jour du modèle (si nécessaire) ---
        # self.name_field.editingFinished.connect(self.save_to_buffer) # À adapter si besoin
        # self.line_value.editingFinished.connect(self.save_to_buffer) # À adapter si besoin

    def show_node_props(self, node_id, node_data, available_clocks):
        """
        Affiche les propriétés d'une localité dans le dock.
        Le contrôleur appelle cette méthode.
        """
        self.current_node_id = node_id
        self.current_source_id = None
        self.current_target_id = None
        
        self.id_field.setText(node_id)
        self.name_field.setText(node_data.get("name", node_id))

        # Mettre à jour les ComboBox d'horloges
        self.combo_clock1.clear()
        self.combo_clock2.clear()
        self.combo_clock2.addItem("---") # Option "pas de deuxième horloge"
        self.combo_clock1.addItems(available_clocks)
        self.combo_clock2.addItems(available_clocks)

        # Remplir la QListWidget avec les invariants
        self.list_constraints.clear()
        for inv in node_data.get("invariants", []):
            # Formater l'affichage de l'invariant pour la liste
            if inv["type"] == "value":
                self.list_constraints.addItem(f"{inv['clock']} {inv['operator']} {inv['value']}")
            elif inv["type"] == "clock":
                self.list_constraints.addItem(f"{inv['clock']} {inv['operator']} {inv['value']} + {inv.get('offset', 0)}")

    def show_transition_props(self, source_id, target_id, trans_data, available_actions, available_clocks):
        """
        Affiche les propriétés d'une transition dans le dock.
        Le contrôleur appelle cette méthode.
        """
        self.current_node_id = None
        self.current_source_id = source_id
        self.current_target_id = target_id
        
        self.id_field.setText(f"{source_id} -> {target_id}")
        self.name_field.setText(trans_data.get("action", "Aucune action"))

        # ... (Logique similaire pour remplir les ComboBox et la QListWidget avec les gardes)
        self.list_constraints.clear()
        for guard in trans_data.get("guards", []):
            if guard["type"] == "value":
                self.list_constraints.addItem(f"{guard['clock']} {guard['operator']} {guard['value']}")
            elif guard["type"] == "clock":
                self.list_constraints.addItem(f"{guard['clock']} {guard['operator']} {guard['value']} + {guard.get('offset', 0)}")

    def load_node_data(self, node_id, data):
        """Remplit les champs avec les données du Modèle"""
        self.current_node_id = node_id
        self.id_field.setText(node_id)
        # S'il n'y a pas de nom, on met vide
        self.name_field.setText(data.get("name", ""))
        # On affiche l'invariant (en vrai il faudra formater la liste DBM en texte lisible)
        # self.invariant_field.setText(str(data.get("invariant", ""))) # Cette ligne n'est plus pertinente avec la nouvelle structure

    def save_to_buffer(self):
        """Envoie les modifications au contrôleur quand on a fini de taper"""
        if self.current_node_id:
            new_name = self.name_field.text()
            # Le contrôleur s'occupera de mettre à jour le Model
            # self.controller.update_node_properties(self.current_node_id, new_name) # À adapter