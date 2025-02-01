import firebase_admin
from firebase_admin import credentials, firestore, auth, storage,messaging
from config import Config

class FirebaseConnection:
    def __init__(self):
        super().__init__()
        self.connection_status = self.connect()

    def connect(self):
        try:
            cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
            self.app = firebase_admin.initialize_app(cred)
            self.db = firestore.client()
            self.auth = auth
            self.storage = storage
            self.messaging = messaging
            return True
        except Exception as e:
            print( f"Connection error to Firebase: {e}")
            return False

    def close_connection(self):
        firebase_admin.delete_app(self.app)
        return "Connection closed successfully."

    # Firestore CRUD operations
    def get_collection(self, collection_name):
        if self.connection_status:
            try:
                documents = self.db.collection(collection_name).get()
                data_list = [(doc.id, doc.to_dict()) for doc in documents]
                return data_list
            except Exception as e:
                return f"Error retrieving collection: {e}"
        else:
            return "No connection to Firebase"

    def insert_document(self, collection_name, data, doc_id=None):
        print(data)
        if self.connection_status:
            try:
                if doc_id is None:
                    _, doc_ref = self.db.collection(collection_name).add(data)
                else:
                    _, doc_ref = self.db.collection(collection_name).add(data,doc_id)
                return f"Document inserted successfully with ID: {doc_ref.id}"
            except Exception as e:
                return f"Error inserting document: {e}"
        else:
            return "No connection to Firebase"

    def delete_document(self, collection_name, doc_id):
        if self.connection_status:
            try:
                self.db.collection(collection_name).document(doc_id).delete()
                return "Document deleted successfully."
            except Exception as e:
                return f"Error deleting document: {e}"
        else:
            return "No connection to Firebase"

    def update_document(self, collection_name, doc_id, new_data):
        
        if self.connection_status:
            try:
                self.db.collection(collection_name).document(doc_id).update(new_data)
                return "Document updated successfully."
            except Exception as e:
                return f"Error updating document: {e}"
        else:
            return "No connection to Firebase"

    # Authentication CRUD operations
    def create_user(self, email, password):
        if self.connection_status:
            try:
                user = self.auth.create_user(email=email, password=password)
                return f"User created successfully with UID: {user.uid}"
            except Exception as e:
                return f"Error creating user: {e}"
        else:
            return "No connection to Firebase"

    def get_user(self, uid):
        if self.connection_status:
            try:
                user = self.auth.get_user(uid)
                return f"User found: {user.email}"
            except Exception as e:
                return f"Error retrieving user: {e}"
        else:
            return "No connection to Firebase"

    def update_user(self, uid, email=None, password=None):
        if self.connection_status:
            try:
                user = self.auth.update_user(uid, email=email, password=password)
                return f"User updated successfully with UID: {user.uid}"
            except Exception as e:
                return f"Error updating user: {e}"
        else:
            return "No connection to Firebase"

    def delete_user(self, uid):
        if self.connection_status:
            try:
                self.auth.delete_user(uid)
                return "User deleted successfully."
            except Exception as e:
                return f"Error deleting user: {e}"
        else:
            return "No connection to Firebase"


    # Operaciones CRUD para el almacenamiento (Storage)
    def subir_archivo(self, source_file_name, destination_blob_name):
        try:
            bucket = self.storage.bucket(app=self. app)
            blob = bucket.blob(destination_blob_name)
            blob.upload_from_string(source_file_name)
            return "Archivo subido exitosamente."
        except Exception as e:
            return "Error al subir archivo:", e

    def descargar_archivo(self, bucket_name, source_blob_name, destination_file_name):
        try:
            bucket = self.storage.Client().bucket(bucket_name)
            blob = bucket.blob(source_blob_name)
            blob.download_to_filename(destination_file_name)
            print("Archivo descargado exitosamente.")
        except Exception as e:
            print("Error al descargar archivo:", e)

    def eliminar_archivo(self, bucket_name, blob_name):
        try:
            bucket = self.storage.Client().bucket(bucket_name)
            blob = bucket.blob(blob_name)
            blob.delete()
            print("Archivo eliminado exitosamente.")
        except Exception as e:
            print("Error al eliminar archivo:", e)

