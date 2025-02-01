from models.topic import Topic

class TopicService:
    def __init__(self, firebase_connection):
        self.firebase_connection = firebase_connection
        self.collection_name = "topics"

    def create_topic(self, topic_data, doc_id=None):
        """
        Crea un nuevo documento de topic en la colección de Firestore.
        `topic_data` es una instancia de Topic.
        """
        data = topic_data.to_json()  # Convierte Topic a JSON antes de guardarlo
        return self.firebase_connection.insert_document(self.collection_name, data, doc_id)

    def get_topic(self, doc_id):
        """
        Recupera un documento de topic de Firestore por su ID.
        Retorna una instancia de Topic si el documento existe.
        """
        topics = self.firebase_connection.get_collection(self.collection_name)
        for uid, data in topics:
            if uid == doc_id:
                return Topic.from_json(data)  # Retorna el topic como instancia de Topic
        return None

    def get_all_topics(self):
        """
        Recupera todos los documentos de topic en Firestore.
        Retorna una lista de instancias de Topic.
        """
        if not self.firebase_connection.connection_status:
            return "Error: No connection to Firebase"
        
        topics_data = self.firebase_connection.get_collection(self.collection_name)
        topics = [Topic.from_json(data) for _, data in topics_data]  # Convierte cada documento en Topic
        return topics
    
    def find_topic_by_name(self, name):
        """
        Busca un documento de Topic en Firestore por su topic_name.
        Retorna una instancia de Topic si se encuentra, o None si no existe.
        """
        if not self.firebase_connection.connection_status:
            return "Error: No connection to Firebase"
        
        try:
            topics = self.firebase_connection.get_collection(self.collection_name)
            for _, data in topics:
                if data.get("TopicName") == name:
                    return Topic.from_json(data)  # Retorna el topic como instancia de Topic
            return None  # Retorna None si no encuentra el topic
        except Exception as e:
            return f"Error buscando el topic: {e}"

    def update_topic(self, doc_id, new_data):
        """
        Actualiza un documento de topic en Firestore con nuevos datos.
        `new_data` es una instancia de Topic.
        """
        data = new_data.to_json()  # Convierte Topic a JSON antes de actualizar
        return self.firebase_connection.update_document(self.collection_name, doc_id, data)

    def delete_topic(self, doc_id):
        """
        Elimina un documento de topic de Firestore por su ID.
        """
        return self.firebase_connection.delete_document(self.collection_name, doc_id)
