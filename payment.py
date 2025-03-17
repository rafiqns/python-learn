from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import User, Payment
from forms import PaymentForm
import midtransclient
import os
import json
from datetime import datetime
import uuid

payment = Blueprint('payment', __name__)

# Konfigurasi Midtrans
MIDTRANS_SERVER_KEY = os.environ.get('MIDTRANS_SERVER_KEY', 'SB-Mid-server-YOUR_KEY_HERE')
MIDTRANS_CLIENT_KEY = os.environ.get('MIDTRANS_CLIENT_KEY', 'SB-Mid-client-YOUR_KEY_HERE')
MIDTRANS_MERCHANT_ID = os.environ.get('MIDTRANS_MERCHANT_ID', 'YOUR_MERCHANT_ID')

# Inisialisasi Midtrans
snap = midtransclient.Snap(
    is_production=False,
    server_key=MIDTRANS_SERVER_KEY,
    client_key=MIDTRANS_CLIENT_KEY
)

@payment.route('/upgrade-to-pro', methods=['GET', 'POST'])
@login_required
def upgrade_to_pro():
    if current_user.is_pro:
        flash('Anda sudah menjadi pengguna Pro!', 'info')
        return redirect(url_for('main.index'))
    
    form = PaymentForm()
    if form.validate_on_submit():
        # Buat ID transaksi unik
        transaction_id = f"PL-{uuid.uuid4().hex[:8]}"
        
        # Buat parameter untuk Midtrans
        transaction_details = {
            'order_id': transaction_id,
            'gross_amount': 99000  # Rp 99.000
        }
        
        customer_details = {
            'first_name': current_user.username,
            'email': current_user.email
        }
        
        item_details = [{
            'id': 'pythonlearn-pro',
            'price': 99000,
            'quantity': 1,
            'name': 'Python Learn Pro Membership'
        }]
        
        transaction = {
            'transaction_details': transaction_details,
            'customer_details': customer_details,
            'item_details': item_details
        }
        
        try:
            # Buat transaksi di Midtrans
            transaction_token = snap.create_transaction_token(transaction)
            
            # Simpan informasi pembayaran di database
            payment_record = Payment(
                user_id=current_user.id,
                amount=99000,
                status='pending',
                payment_id=transaction_id
            )
            db.session.add(payment_record)
            db.session.commit()
            
            return render_template('payment/checkout.html', 
                                  client_key=MIDTRANS_CLIENT_KEY,
                                  transaction_token=transaction_token,
                                  payment_id=transaction_id)
        
        except Exception as e:
            flash(f'Terjadi kesalahan: {str(e)}', 'danger')
            return redirect(url_for('payment.upgrade_to_pro'))
    
    return render_template('payment/upgrade.html', form=form)

@payment.route('/payment-notification', methods=['POST'])
def payment_notification():
    try:
        notification = json.loads(request.data)
        transaction_status = notification['transaction_status']
        order_id = notification['order_id']
        
        # Cari pembayaran di database
        payment_record = Payment.query.filter_by(payment_id=order_id).first()
        
        if not payment_record:
            return jsonify({'status': 'error', 'message': 'Payment not found'}), 404
        
        # Update status pembayaran
        if transaction_status in ['capture', 'settlement']:
            payment_record.status = 'success'
            
            # Update status pengguna menjadi Pro
            user = User.query.get(payment_record.user_id)
            user.is_pro = True
            db.session.commit()
            
        elif transaction_status in ['cancel', 'deny', 'expire']:
            payment_record.status = 'failed'
            db.session.commit()
            
        elif transaction_status == 'pending':
            payment_record.status = 'pending'
            db.session.commit()
        
        return jsonify({'status': 'success'}), 200
    
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@payment.route('/payment-success')
@login_required
def payment_success():
    flash('Pembayaran berhasil! Anda sekarang adalah pengguna Pro', 'success')
    return redirect(url_for('main.index'))

@payment.route('/payment-failed')
@login_required
def payment_failed():
    flash('Pembayaran gagal. Silakan coba lagi', 'danger')
    return redirect(url_for('payment.upgrade_to_pro')) 