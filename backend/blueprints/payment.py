import uuid

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from sslcommerz_lib import SSLCOMMERZ

from .forms import PaymentForm

# Create the payment blueprint
payment_bp = Blueprint('payment_bp', __name__)

# Configure the SSLCommerz settings
sslcommerz_settings = {
    'store_id': 'petbu66ed81f7a55af',
    'store_pass': 'petbu66ed81f7a55af@ssl',
    'issandbox': True  # Change to False when in production
}

# Instantiate SSLCOMMERZ object
sslcz = SSLCOMMERZ(sslcommerz_settings)

# Initiate the payment route
@payment_bp.route('/initiate_payment', methods=['GET', 'POST'])
def initiate_payment():
    form = PaymentForm()

    if form.validate_on_submit():
        try:
            # Create a unique transaction ID for the payment
            transaction_id = str(uuid.uuid4())

            # Get necessary info from the form
            amount = request.form.get('amount')
            customer_name = request.form.get('customer_name')
            customer_email = request.form.get('customer_email')
            customer_phone = request.form.get('customer_phone')
            customer_address = request.form.get('customer_address')  # Customer Address
            customer_city = request.form.get('customer_city')  # Customer City
            customer_country = request.form.get('customer_country')  # Customer Country
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
                'cus_add1': customer_address,  # Customer Address
                'cus_city': customer_city,  # Customer City
                'cus_country': customer_country,  # Customer Country
                'product_name': 'Vet Services',
                'product_category': 'Services',
                'product_profile': 'general',
                'multi_card_name': payment_method,
                'shipping_method': 'NO'
            }

            # Send data to SSLCommerz and get the response
            response = sslcz.createSession(payment_data)

            # Log the response to debug if needed
            current_app.logger.info(f"SSLCommerz response: {response}")

            # Check if the response was successful
            if response.get('status') == 'SUCCESS':
                # Extract the GatewayPageURL from the response
                gateway_url = response.get('GatewayPageURL')

                # Redirect the user to the SSLCommerz payment page
                return redirect(gateway_url)
            else:
                # If the response indicates failure, log the error and show a message
                flash('Failed to initiate payment', 'error')
                current_app.logger.error(f"Payment initiation failed: {response}")

        except Exception as e:
            # Handle and log any exceptions that occur
            current_app.logger.error(f"Payment initiation failed: {e}")
            flash('Payment initiation error', 'error')

    # If form validation fails or no submission, render the form again
    return render_template('payment_form.html', form=form)



    
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
