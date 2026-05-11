from PySide6.QtWidgets import QWidget, QFormLayout, QLineEdit, QLabel
from PySide6.QtCore import Qt

class PropertiesPanel(QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.current_node_id = None
        
        # Un layout en formulaire (Label à gauche, Champ à droite)
        layout = QFormLayout()
        
        self.id_field = QLineEdit()
        self.id_field.setReadOnly(True) # L'ID ne change pas
        
        self.name_field = QLineEdit()
        self.invariant_field = QLineEdit() # Pour la DBM (texte simple pour l'instant)
        
        layout.addRow("ID :", self.id_field)
        layout.addRow("Nom :", self.name_field)
        layout.addRow("Invariant :", self.invariant_field)
        
        self.setLayout(layout)
        
        # --- CONNEXION : Quand on tape, on met à jour le buffer ---
        self.name_field.editingFinished.connect(self.save_to_buffer)
        self.invariant_field.editingFinished.connect(self.save_to_buffer)

    def load_node_data(self, node_id, data):
        """Remplit les champs avec les données du Modèle"""
        self.current_node_id = node_id
        self.id_field.setText(node_id)
        # S'il n'y a pas de nom, on met vide
        self.name_field.setText(data.get("name", "")) 
        # On affiche l'invariant (en vrai il faudra formater la liste DBM en texte lisible)
        self.invariant_field.setText(str(data.get("invariant", "")))

    def save_to_buffer(self):
        """Envoie les modifications au contrôleur quand on a fini de taper"""
        if self.current_node_id:
            new_name = self.name_field.text()
            new_inv = self.invariant_field.text()
            # Le contrôleur s'occupera de mettre à jour le Model
            self.controller.update_node_properties(self.current_node_id, new_name, new_inv)