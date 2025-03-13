from email.mime.text import MIMEText
import random
import smtplib
import string
from flask import Flask, flash, request, jsonify, render_template, redirect, url_for, session
from flask_cors import CORS
import stripe
from services.notificationService import send_notification, subcribe_to_topic, topic_send_notification, get_tokens_for_topic_excluding_sender
import os
from config import Config
from services.stripeService import save_firebase_payment
from services.userService import UsuarioService
from utils.firebaseConection import FirebaseConnection

app = Flask(__name__)
app.secret_key ="@ViveAppApi2025"
CORS(app)
fb = FirebaseConnection()
scv = UsuarioService(fb)

stripe.api_key = Config.STRIPE_KEY
@app.route('/notificationApi/send_notification', methods=['POST'])
def api_send_notification():
    data = request.get_json()
    token = data.get('token')
    titulo = data.get('titulo')
    mensaje = data.get('mensaje')
    
    response = send_notification(token, titulo, mensaje,fb)
    return jsonify({'response': str(response)})

@app.route('/notificationApi/subscribe', methods=['POST'])
def api_subscribe():
    data = request.get_json()
    topic_name = data.get('topicName')
    tokens = data.get('tokens')
    print(tokens)
    response = subcribe_to_topic(topic_name, tokens,fb)
    
    res = jsonify({
        'success_count': response.success_count,
        'failure_count': response.failure_count,
        'errors': [res.reason for res in response.errors]
    })
    print(res.get_json())
    return res

@app.route('/notificationApi/topic/send_notification', methods=['POST'])
def send_topic_notification():
    try:
        data = request.get_json()
        topic = data.get('topic')
        titulo = data.get('titulo')
        mensaje = data.get('mensaje')
        #tokens = data.get('deviceTokens', [])
        deviceTokenSender = data.get('deviceTokenSender')
        tokens = get_tokens_for_topic_excluding_sender(topic, deviceTokenSender,fb)
        print(tokens)
        responses = []
        for token in tokens:
            response = send_notification(token, titulo, mensaje,fb)
            responses.append({'response': str(response)})

        if responses:
            return jsonify({'responses': responses}), 200
        else:
            return jsonify({"error": "Failed to send notification."}), 500
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/donate', methods=['POST'])
def donate():
    try:
        data = request.get_json()

        # Datos necesarios: nombre, correo, monto y detalles de la tarjeta
        name = data['name']
        email = data['email']
        amount = data['amount']
        payment = data['payment_intent']  # Debe contener number, exp_month, exp_year, cvc

        # Procesar el pago y guardar en Firebase
        result = save_firebase_payment(name, email, amount, payment,fb)

        return jsonify(result)

    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

@app.route('/crear-payment-intent', methods=['POST'])
def crear_payment_intent():
    try:
        data = request.get_json()
        amount = data['amount']
        currency = data.get('currency', 'mxn')  # Moneda por defecto: MXN

        # Crear PaymentIntent en Stripe
        payment_intent = stripe.PaymentIntent.create(
            amount=int(amount),
            currency=currency,
            payment_method_types=['card']
        )

        return payment_intent, 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/notificationApi/topic/get_tokens', methods=['GET'])
def get_tokens_for_topic():
    try:
        topic_name = request.args.get('topic')
        if not topic_name:
            return jsonify({"error": "No topic specified."}), 400

        tokens = get_tokens_for_topic_excluding_sender(topic_name, "",fb)

        if not tokens:
            return jsonify({"error": "No tokens found for the specified topic."}), 404

        return jsonify({"tokens": tokens}), 200

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/users', methods=['GET'])
def get_all_usuarios():
    usuarios = scv.get_all_usuarios()
    
    if isinstance(usuarios, str):  # En caso de error
        return jsonify({'error': usuarios}), 500
    else:
        return jsonify({'usuarios': usuarios}), 200

@app.route('/privacy_policies', methods=['GET'])
def Privacy_policies():
    return render_template('privacy_policy.html')

# Simulación de una base de datos de usuarios (usaremos un diccionario)

# Función para generar un código de verificación aleatorio
def generar_codigo():
    return str(random.randint(100000, 999999))

# Función para enviar el correo con el código de verificación
def enviar_correo(destinatario, codigo):
    remitente = "viveappmovile@gmail.com"  # Cambia esto con tu correo real
    contraseña = "pcrg bhhg xxvc ijsd"  # ⚠ Usa una contraseña segura (o credenciales de app)
    
    email_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }}
        .container {{ width: 100%; padding: 20px; background-color: #ffffff; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); margin: 40px auto; max-width: 600px; border-radius: 8px; text-align: center; }}
        .header {{ background-color: #4caf50; color: white; padding: 10px; font-size: 24px; border-radius: 8px 8px 0 0; }}
        .content {{ padding: 20px; font-size: 16px; }}
        .code {{ font-size: 24px; font-weight: bold; background-color: #f4f4f4; padding: 10px; border-radius: 5px; color: #4caf50; display: inline-block; margin: 20px 0; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #888888; }}
        .img-container {{ width: 150px; height: 150px; background-color: #A1D0FF; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 20px; }}
        .img-container img {{ width: 80%; height: auto; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">¡Tu Código de Verificación!</div>
        <div class="content">
          <div class="img-container" style="justify-content: center; padding: 20px;">
            <img src="https://firebasestorage.googleapis.com/v0/b/vive-69b25.appspot.com/o/logo-vive.png?alt=media&token=6b879fb1-2e3b-480f-a1d0-fac22c784e38" alt="Logo de la aplicación">
          </div>
          <p>Hola, gracias por utilizar nuestra aplicación. Tu código de verificación es el siguiente:</p>
          <div class="code">{codigo}</div>
          <p>Por favor, introduce este código en la aplicación para continuar.</p>
          <p>Si no solicitaste este código, simplemente ignora este mensaje.</p>
        </div>
        <div class="footer">© 2025 Vive - Todos los derechos reservados</div>
      </div>
    </body>
    </html>
    """
    print()
    msg = MIMEText(email_html, 'html')
    msg['Subject'] = "Código de Confirmación"
    msg['From'] = remitente
    msg['To'] = destinatario
    
    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.sendmail(remitente, destinatario, msg.as_string())
        servidor.quit()
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

def enviar_correo_eliminacion(destinatario):
    remitente = "viveappmovile@gmail.com"  # Cambia esto con tu correo real
    contraseña = "pcrg bhhg xxvc ijsd"  # ⚠ Usa una contraseña segura (o credenciales de app)
    
    email_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body {{ font-family: Arial, sans-serif; background-color: #f4f4f4; margin: 0; padding: 0; }}
        .container {{ width: 100%; padding: 20px; background-color: #ffffff; box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1); margin: 40px auto; max-width: 600px; border-radius: 8px; text-align: center; }}
        .header {{ background-color: #ff4d4d; color: white; padding: 10px; font-size: 24px; border-radius: 8px 8px 0 0; }}
        .content {{ padding: 20px; font-size: 16px; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #888888; }}
        .img-container {{ width: 150px; height: 150px; background-color: #FFA1A1; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin: 0 auto 20px; }}
        .img-container img {{ width: 80%; height: auto; }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">Cuenta Eliminada</div>
        <div class="content">
          <div class="img-container" style="justify-content: center; padding: 20px;">
            <img src="https://firebasestorage.googleapis.com/v0/b/vive-69b25.appspot.com/o/logo-vive.png?alt=media&token=6b879fb1-2e3b-480f-a1d0-fac22c784e38" alt="Logo de la aplicación">
          </div>
          <p>Hola, lamentamos verte partir.</p>
          <p>Tu cuenta ha sido eliminada de nuestra plataforma. Si esto fue un error o necesitas ayuda, contáctanos.</p>
          <p>Gracias por haber sido parte de nuestra comunidad.</p>
        </div>
        <div class="footer">© 2025 Vive - Todos los derechos reservados</div>
      </div>
    </body>
    </html>
    """
    
    msg = MIMEText(email_html, 'html')
    msg['Subject'] = "Confirmación de Eliminación de Cuenta"
    msg['From'] = remitente
    msg['To'] = destinatario
    
    try:
        servidor = smtplib.SMTP("smtp.gmail.com", 587)
        servidor.starttls()
        servidor.login(remitente, contraseña)
        servidor.sendmail(remitente, destinatario, msg.as_string())
        servidor.quit()
        print(f"Correo de eliminación enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

# Ruta para solicitar el correo
@app.route('/delete-account', methods=['GET', 'POST'])
def delete_account():
    if request.method == 'POST':
        email = request.form['email']
        us = scv.get_all_usuarios()
        usuarios = [user.correo for user in us]

        # Validar si el correo existe en la base de datos
        if email not in usuarios:
            flash('⚠ El correo ingresado no existe.', 'error')
            return redirect(url_for('delete_account'))

        # Generar código y guardarlo en sesión
        codigo = generar_codigo()
        session['email'] = email
        session['codigo'] = codigo
        print(codigo)
        # Enviar código al correo
        enviar_correo(email, codigo)
        return redirect(url_for('verify_code'))

    return render_template('delete_account.html')

# Ruta para verificar el código de confirmación
@app.route('/verify-code', methods=['GET', 'POST'])
def verify_code():
    if request.method == 'POST':
        codigo_ingresado = request.form['codigo']
        print(f"session code: {session['codigo']}")
        if 'codigo' in session and codigo_ingresado == session['codigo']:
            
            res = scv.delete_usuario_by_email(session['email'])
            if res:
                enviar_correo_eliminacion(session['email'])
                return redirect(url_for('account_deleted'))
            else:
                flash('⚠ Algo salio mal ponte en contacto con soporte tecnico', 'error')
                return redirect(url_for('verify_code'))
            
            

        flash('⚠ Código incorrecto. Intenta de nuevo.', 'error')
        return redirect(url_for('verify_code'))

    return render_template('verify_code.html')

# Ruta de confirmación de eliminación
@app.route('/account-deleted')
def account_deleted():
    email = session.get('email', 'Desconocido')
    return render_template('account_deleted.html', email=email)

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"Running on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=True)
