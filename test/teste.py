import firebase_admin
from firebase_admin import credentials, messaging

# Inicializa la aplicación de Firebase
cred = credentials.Certificate('utils\serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Función para enviar una notificación
def send_notification(token, titulo, mensaje):
    # Crea el mensaje
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

    # Envía el mensaje
    response = messaging.send(mensaje)
    print('Mensaje enviado:', response)



# subcribinmos un dispositivo a un grupo(tema) 
def subcribe_to_topic(topicName,tokens =[]):
        response = messaging.subscribe_to_topic(tokens=tokens,topic=topicName)
        
        print(f"""
              responses success:{response.success_count}
              responses failure:{response.failure_count}
              responses Errors:{[res.reason for res in response.errors]}
        """)

def topic_send_notification(topic, titulo, mensaje):
    # Crea el mensaje
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

    # Envía el mensaje
    response = messaging.send(mensaje)
    print('Mensaje enviado:', response)



# Ejemplo de uso
token_dispositivo = 'cpfDoliKS8WHC_nhm2dUHX:APA91bF_5EzsbFNOZrmQmHSfcDR-MNEe38JFrFHI1YNs641r7FflY6zQ37yLJ1y5Pqzv8RM8m4uKk2s1EKsiDre7SfAVTZQ3qyYiohjWDRcqhB1A8qtwg7E'
token_dispositivo2 ='fTQiSb9LTBi4KhxC7fSFTI:APA91bGkgCY-sef3e_m8Blasnf2lm36-fVgI0XwmGBdQvHNXexPZtmK8lqyM5IzkqwLnhtaTEO7wYYc8QBJuqeKTC9ZTNwHRvRpBytxoDEggbTU30wrX5kM'
titulo = 'Hola'
mensaje = 'Esta es una notificación de prueba'
topic= "Codsito"
#enviar_notificacion(token_dispositivo, titulo, mensaje)
#subcribe_to_topic(topicName=topic,tokens=[token_dispositivo2])
topic_send_notification(topic=topic,titulo= "Hola soy ViveAssistant",mensaje=f"Bienbenidos a su grupo {topic}")