from flask import Blueprint, request, redirect, url_for, jsonify, current_app
from sslcommerz_lib import SSLCOMMERZ
import uuid

# Create the payment blueprint
payment_bp = Blueprint('payment_bp', __name__)

# Configure the SSLCommerz settings
sslcommerz_settings = {
    'store_id': 'your_store_id',
    'store_pass': 'your_store_pass',
    'issandbox': True  # Change to False when in production
}

# Instantiate SSLCOMMERZ object
sslcz = SSLCOMMERZ(sslcommerz_settings)

# Initiate the payment route
@payment_bp.route('/initiate_payment', methods=['POST'])
def initiate_payment():
    try:
        # Create a unique transaction ID for the payment
        transaction_id = str(uuid.uuid4())

        # Get necessary info from request, like amount and customer details
        amount = request.form.get('amount')
        customer_name = request.form.get('customer_name')
        customer_email = request.form.get('customer_email')
        customer_phone = request.form.get('customer_phone')
        payment_method = request.form.get('payment_method')

        # Prepare the payment data
        payment_data = {
            'total_amount': amount,
            'currency': 'BDT',
            'tran_id': transaction_id,
            'success_url': url_for('payment_bp.payment_success', _external=True),
            'fail_url': url_for('payment_bp.payment_failure', _external=True),
            'cancel_url': url_for('payment_bp.payment_cancel', _external=True),
            'cus_name': customer_name,
            'cus_email': customer_email,
            'cus_phone': customer_phone,
            'product_name': 'Vet Services',
            'product_category': 'Services',
            'product_profile': 'general',
            'multi_card_name': payment_method
        }

        # Initiate the payment session
        response = sslcz.createSession(payment_data)

        if response['status'] == 'SUCCESS':
            # Redirect the user to the payment gateway URL
            return redirect(response['GatewayPageURL'])
        else:
            return jsonify({'error': 'Failed to initiate payment'}), 400

    except Exception as e:
        current_app.logger.error(f"Payment initiation failed: {e}")
        return jsonify({'error': 'Payment initiation error'}), 500

# Payment success route
@payment_bp.route('/payment_success', methods=['POST'])
def payment_success():
    try:
        # SSLCommerz returns a POST request with the transaction ID
        transaction_id = request.form.get('tran_id')
        response = sslcz.transaction_query_tranid(transaction_id)

        if response['status'] == 'VALID':
            # Here you can confirm and finalize the transaction (e.g., update DB)
            return jsonify({'message': 'Payment successful', 'transaction_id': transaction_id}), 200
        else:
            return jsonify({'error': 'Payment validation failed'}), 400

    except Exception as e:
        current_app.logger.error(f"Payment success handling failed: {e}")
        return jsonify({'error': 'Payment success error'}), 500

# Payment failure route
@payment_bp.route('/payment_failure', methods=['POST'])
def payment_failure():
    try:
        transaction_id = request.form.get('tran_id')
        return jsonify({'message': 'Payment failed', 'transaction_id': transaction_id}), 200

    except Exception as e:
        current_app.logger.error(f"Payment failure handling failed: {e}")
        return jsonify({'error': 'Payment failure error'}), 500

# Payment cancel route
@payment_bp.route('/payment_cancel', methods=['POST'])
def payment_cancel():
    try:
        transaction_id = request.form.get('tran_id')
        return jsonify({'message': 'Payment canceled', 'transaction_id': transaction_id}), 200

    except Exception as e:
        current_app.logger.error(f"Payment cancel handling failed: {e}")
        return jsonify({'error': 'Payment cancel error'}), 500
