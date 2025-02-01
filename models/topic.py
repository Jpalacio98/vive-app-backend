class Topic:
    def __init__(self, uid, members, topic_name):
        self.uid = uid
        self.members = members if isinstance(members, list) else []  # Asegura que member sea una lista
        self.topic_name = topic_name

    def to_json(self):
        """
        Convierte la instancia de Topic en un diccionario (JSON) para almacenar en Firestore.
        """
        return {
            'uid': self.uid,
            'members': self.members,
            'TopicName': self.topic_name
        }

    @classmethod
    def from_json(cls, json_data):
        """
        Crea una instancia de Topic desde un diccionario (JSON).
        """
        return cls(
            uid=json_data['uid'],
            members=json_data.get('members', []),  # Asegura que member sea una lista, incluso si está vacío
            topic_name=json_data['TopicName']
        )
