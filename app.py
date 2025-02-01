from flask import Flask, request, jsonify
from flask_cors import CORS
import stripe
from services.notificationService import send_notification, subcribe_to_topic, topic_send_notification, get_tokens_for_topic_excluding_sender
import os
from datetime import datetime
from config import Config
from services.stripeService import save_firebase_payment
from services.userService import UsuarioService
from utils.firebaseConection import FirebaseConnection

app = Flask(__name__)
CORS(app)
fb = FirebaseConnection()
scv = UsuarioService(fb)

stripe.api_key = Config.STRIPE_KEY
@app.route('/send_notification', methods=['POST'])
def api_send_notification():
    data = request.get_json()
    token = data.get('token')
    titulo = data.get('titulo')
    mensaje = data.get('mensaje')
    
    response = send_notification(token, titulo, mensaje,fb)
    return jsonify({'response': str(response)})

@app.route('/subscribe', methods=['POST'])
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

@app.route('/topic/send_notification', methods=['POST'])
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

@app.route('/topic/get_tokens', methods=['GET'])
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

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    print(f"Running on port {port}")
    
    app.run(host='0.0.0.0', port=port, debug=True)
