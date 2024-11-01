import firebase_admin
from firebase_admin import credentials, messaging
from config import Config

# Inicializa la aplicación de Firebase
cred = credentials.Certificate(Config.FIREBASE_CREDENTIALS)
firebase_admin.initialize_app(cred)

def send_notification(token, titulo, mensaje):
    mensaje = messaging.Message(
        notification=messaging.Notification(
            title=titulo,
            body=mensaje,
        ),
        token=token,
        data={
            'title': titulo,
            'body': mensaje,
        }
    )
    response = messaging.send(mensaje)
    return response

def subcribe_to_topic(topicName, tokens=[]):
    response = messaging.subscribe_to_topic(tokens=tokens, topic=topicName)
    return response

def topic_send_notification(topic, titulo, mensaje):
    mensaje = messaging.Message(
        notification=messaging.Notification(
            title=titulo,
            body=mensaje,
        ),
        topic=topic,
        data={
            'title': titulo,
            'body': mensaje,
        }
    )
    response = messaging.send(mensaje)
    return response
