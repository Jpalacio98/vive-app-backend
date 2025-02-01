import hashlib
import json

class Usuario:
    def __init__(self, correo, nombre, image_url, password, user_id, device_token=""):
        self.correo = correo
        self.nombre = nombre
        self.image_url = image_url
        self.password = password
        self.user_id = user_id
        self.device_token = device_token

    def to_json(self):
        return {
            'correo': self.correo,
            'nombre': self.nombre,
            'image_url': self.image_url,
            'password': self.password,
            'user_id': self.user_id,
            'deviceToken': self.device_token,
        }

    @classmethod
    def from_json(cls, json_data):
        return cls(
            correo=json_data['correo'],
            nombre=json_data['nombre'],
            image_url=json_data['image_url'],
            password=json_data['password'],
            user_id=json_data['user_id'],
            device_token=json_data.get('deviceToken', "")
        )

    @classmethod
    def from_map(cls, map_data):
        return cls(
            correo=map_data.get('correo', ""),
            nombre=map_data.get('nombre', ""),
            image_url=map_data.get('image_url', ""),
            password=map_data.get('password', ""),
            user_id=map_data.get('user_id', ""),
            device_token=map_data.get('deviceToken', "")
        )

    @staticmethod
    def encrypt_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    def set_device_token(self, token):
        self.device_token = token
