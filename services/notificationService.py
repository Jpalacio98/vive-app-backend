from services.topicService import TopicService
from services.userService import UsuarioService
from utils.firebaseConection import FirebaseConnection



def send_notification(token, titulo, mensaje,fb):
    mensaje = fb.messaging.Message(
        notification=fb.messaging.Notification(
            title=titulo,
            body=mensaje,
        ),
        token=token,
        data={
            'title': titulo,
            'body': mensaje,
        }
    )
    response = fb.messaging.send(mensaje)
    return response


def subcribe_to_topic(topicName, fb,tokens=[],):
    response = fb.messaging.subscribe_to_topic(tokens=tokens, topic=topicName)
    return response




def get_tokens_for_topic_excluding_sender(topic_name, sender_device_id,fb):
    deviceTokens = []
    tsvc = TopicService(fb)
    usvc = UsuarioService(fb)
    topic = tsvc.find_topic_by_name(topic_name)
    print(topic.to_json())
    for member in topic.members:
        user =  usvc.get_usuario(member)
        print(user.nombre)
        deviceTokens.append(user.device_token)
    tokens = []
    tokens.extend(
        [token for token in deviceTokens if token != sender_device_id])
    return tokens


def topic_send_notification(tokens, message_title, message_body,fb):
    # Crear el mensaje para FCM
    message = fb.messaging.MulticastMessage(
        notification=fb.messaging.Notification(
            title=message_title,
            body=message_body
        ),
        tokens=tokens,
        data={
            'title': message_title,
            'body': message_body,
        }
    )

    try:
        # Enviar la notificación
        response = fb.messaging.send_multicast(message)
        return response
    except Exception as e:
        print(f"Error al enviar la notificación: {e}")
        return None


