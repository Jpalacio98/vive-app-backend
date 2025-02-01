
import stripe


# def process_payment(name, email, amount, card_details,firebase):
#     """
#     Procesa el pago con Stripe y guarda la donación en Firebase.
#     """
#     try:
#         # Convertir el monto a centavos (Stripe trabaja en la unidad más pequeña)
#         amount_in_cents = int(float(amount) * 100)

#         # Crear un cliente en Stripe
#         customer = stripe.Customer.create(
#             name=name,
#             email=email,
#         )
#           # Crear un PaymentMethod primero
#         payment_method = stripe.PaymentMethod.create(
#             type="card",
#             card={
#                 "number": card_details["number"],
#                 "exp_month": card_details["exp_month"],
#                 "exp_year": card_details["exp_year"],
#                 "cvc": card_details["cvc"],
#             },
#         )

#         # Crear un PaymentIntent
#         payment_intent = stripe.PaymentIntent.create(
#             amount=amount_in_cents,
#             currency="usd",
#             payment_method=payment_method.id,
#             confirm=True,  # Confirma el pago automáticamente
#             customer=customer.id,
#             automatic_payment_methods={
#         "enabled": False  # Deshabilitar métodos de pago automáticos para evitar redirecciones
#     }
#         )

#         # Si el pago fue exitoso, guardar los datos en Firebase
#         if payment_intent["status"] == "succeeded":
#             donation_data = {
#                 "name": name,
#                 "email": email,
#                 "amount": amount,
#                 "payment_status": payment_intent["status"],
#                 "payment_id": payment_intent["id"],
#             }
#             #db.collection("donations").add(donation_data)
#             firebase.insert_document("donations",donation_data)
#             return {"success": True, "message": "Payment processed successfully!"}
#         else:
#             return {"success": False, "message": "Payment failed."}

#     except stripe.error.CardError as e:
#         return {"success": False, "message": f"Card error: {e.user_message}"}
#     except Exception as e:
#         return {"success": False, "message": f"An error occurred: {str(e)}"}


def save_firebase_payment(name, email, amount, payment_intent,firebase):
    """
    Procesa el pago con Stripe y guarda la donación en Firebase.
    """
    try:

        
            donation_data = {
                "name": name,
                "email": email,
                "amount": amount,
                "payment_status": payment_intent["status"],
                "payment_id": payment_intent["id"],
            }
            #db.collection("donations").add(donation_data)
            firebase.insert_document("donations",donation_data)
            return {"success": True, "message": "Payment processed successfully!"}
    
    except Exception as e:
        return {"success": False, "message": f"An error occurred: {str(e)}"}
