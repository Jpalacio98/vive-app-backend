from models.user import Usuario


class UsuarioService:
    def __init__(self, firebase_connection):
        self.firebase_connection = firebase_connection
        self.collection_name = "users"

    def create_usuario(self, usuario_data, doc_id=None):
        """
        Crea un nuevo documento de usuario en la colección de Firestore.
        `usuario_data` es una instancia de Usuario.
        """
        data = usuario_data.to_json()  # Convierte Usuario a JSON antes de guardarlo
        return self.firebase_connection.insert_document(self.collection_name, data, doc_id)

    def get_usuario(self, doc_id):
        """
        Recupera un documento de usuario de Firestore por su ID.
        Retorna una instancia de Usuario si el documento existe.
        """
        usuarios = self.firebase_connection.get_collection(self.collection_name)
        for uid, data in usuarios:
            if uid == doc_id:
                return Usuario.from_map(data)  # Retorna el usuario como instancia de Usuario
        return None  # O puedes retornar un mensaje si prefieres

    def get_all_usuarios(self):
        """
        Recupera todos los documentos de usuario en Firestore.
        Retorna una lista de instancias de Usuario.
        """
        if not self.firebase_connection.connection_status:
            return "Error: No connection to Firebase"
        
        usuarios_data = self.firebase_connection.get_collection(self.collection_name)
        usuarios = [Usuario.from_map(data) for _, data in usuarios_data]  # Convierte cada documento en Usuario
        return usuarios

    def update_usuario(self, doc_id, new_data):
        """
        Actualiza un documento de usuario en Firestore con nuevos datos.
        `new_data` es una instancia de Usuario.
        """
        data = new_data.to_json()  # Convierte Usuario a JSON antes de actualizar
        return self.firebase_connection.update_document(self.collection_name, doc_id, data)

    def delete_usuario(self, doc_id):
        """
        Elimina un documento de usuario de Firestore por su ID.
        """
        return self.firebase_connection.delete_document(self.collection_name, doc_id)

    def get_usuario_by_email(self, email):
        """
        Busca un usuario en la colección de Firestore por su correo electrónico.
        Retorna una instancia de Usuario si el usuario existe, de lo contrario, retorna None.
        """
        usuarios = self.firebase_connection.get_collection(self.collection_name)
        for uid, data in usuarios:
            if data.get("email") == email:
                return Usuario.from_map(data)  # Retorna el usuario como instancia de Usuario
        return None  # Retorna None si no se encuentra el usuario

    def delete_usuario_by_email(self, email):
        """
        Busca y elimina un usuario en la colección de Firestore por su correo electrónico.
        Retorna True si el usuario fue eliminado, False si no se encontró.
        """
        usuarios = self.firebase_connection.get_collection(self.collection_name)
        
        for uid, data in usuarios:
            if data.get("email") == email:
                self.firebase_connection.delete_document(self.collection_name, uid)
                return True  # Usuario eliminado exitosamente
        
        return False  # Usuario no encontrado
