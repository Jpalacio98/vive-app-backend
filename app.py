from flask import Flask, request, jsonify
from utils.firebase_config import send_notification, subcribe_to_topic, topic_send_notification

app = Flask(__name__)

@app.route('/send_notification', methods=['POST'])
def api_send_notification():
    data = request.json
    token = data.get('token')
    titulo = data.get('titulo')
    mensaje = data.get('mensaje')
    
    response = send_notification(token, titulo, mensaje)
    return jsonify({'response': str(response)})

@app.route('/subscribe', methods=['POST'])
def api_subscribe():
    data = request.json
    topic_name = data.get('topicName')
    tokens = data.get('tokens', [])
    
    response = subcribe_to_topic(topic_name, tokens)
    return jsonify({
        'success_count': response.success_count,
        'failure_count': response.failure_count,
        'errors': [res.reason for res in response.errors]
    })

@app.route('/topic/send_notification', methods=['POST'])
def api_topic_send_notification():
    data = request.json
    topic = data.get('topic')
    titulo = data.get('titulo')
    mensaje = data.get('mensaje')
    
    response = topic_send_notification(topic, titulo, mensaje)
    return jsonify({'response': str(response)})

if __name__ == '__main__':
    app.run(debug=True)
