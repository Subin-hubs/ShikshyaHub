from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models.payment import Payment
from app.models.user import User
import hashlib

payment_bp = Blueprint('payment', __name__, url_prefix='/payment')

@payment_bp.route('/premium')
@login_required
def premium():
    if current_user.is_admin():
        return redirect(url_for('admin.dashboard'))
    
    return render_template('user/premium.html')

@payment_bp.route('/esewa/initiate', methods=['POST'])
@login_required
def esewa_initiate():
    amount = request.form.get('amount', 500)  # Default premium price: NPR 500
    
    # Create payment record
    payment = Payment(
        user_id=current_user.id,
        amount=float(amount),
        status='pending',
        payment_method='esewa'
    )
    db.session.add(payment)
    db.session.commit()
    
    # Prepare eSewa parameters
    esewa_params = {
        'amt': amount,
        'psc': 0,  # Service charge
        'pdc': 0,  # Delivery charge
        'txAmt': 0,  # Tax amount
        'tAmt': amount,  # Total amount
        'pid': f'FLAVORHIVE-{payment.id}',  # Product ID (unique)
        'scd': current_app.config['ESEWA_MERCHANT_CODE'],
        'su': current_app.config['ESEWA_SUCCESS_URL'] + f'?q=su&oid={payment.id}',
        'fu': current_app.config['ESEWA_FAILURE_URL'] + f'?q=fu&oid={payment.id}'
    }
    
    return render_template('user/esewa_redirect.html', 
                         esewa_url=current_app.config['ESEWA_PAYMENT_URL'],
                         params=esewa_params)

@payment_bp.route('/success')
@login_required
def success():
    # Get parameters from eSewa
    oid = request.args.get('oid')
    refId = request.args.get('refId')
    amt = request.args.get('amt')
    
    if oid:
        payment = Payment.query.get(int(oid))
        if payment and payment.user_id == current_user.id:
            payment.status = 'success'
            payment.transaction_id = refId
            
            # Update user to premium
            current_user.is_premium = True
            
            db.session.commit()
            
            flash('Payment successful! You are now a premium member.', 'success')
            return render_template('user/payment_success.html', payment=payment)
    
    flash('Payment verification failed.', 'danger')
    return redirect(url_for('user.dashboard'))

@payment_bp.route('/failure')
@login_required
def failure():
    oid = request.args.get('oid')
    
    if oid:
        payment = Payment.query.get(int(oid))
        if payment and payment.user_id == current_user.id:
            payment.status = 'failed'
            db.session.commit()
    
    flash('Payment failed. Please try again.', 'danger')
    return render_template('user/payment_failure.html')
