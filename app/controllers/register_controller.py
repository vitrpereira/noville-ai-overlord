from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.user import User
from app.controllers.whatsapp_transcription_controller import (
    WhatsappTranscriptionController
)
import re

register = Blueprint('register', __name__)


@register.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        name = request.form.get('name')
        phone_number = request.form.get('phone_number')

        try:
            # Format the phone number
            formatted_phone = format_phone_number(phone_number)

            # Check if user already exists
            if User.exists_user_by_phone_number_and_product_id(
                formatted_phone, 1
            ):
                flash('Este número de telefone já está cadastrado.', 'error')
                return redirect(url_for('register.register_user'))

            # Register new user with formatted phone
            User.register_user(
                phone_number=formatted_phone,
                name=name,
                product_id=1
            )

            # Send welcome message
            WhatsappTranscriptionController().send_welcome_message(
                formatted_phone,
                name
            )

            return redirect(url_for('register.success'))

        except ValueError:
            flash(
                'Número de telefone inválido. Use o formato: +55 (11) 99999-9999',  # noqa
                'error'
            )
            return redirect(url_for('register.register_user'))
        except Exception:
            flash(
                'Erro ao realizar cadastro. Por favor, tente novamente.',
                'error'
            )
            return redirect(url_for('register.register_user'))

    return render_template('register/index.html')


@register.route('/success')
def success():
    return render_template('register/success.html')


def format_phone_number(phone):
    """Remove all non-numeric characters and ensure proper format"""
    numbers_only = re.sub(r'\D', '', phone)

    if len(numbers_only) == 11:
        numbers_only = '55' + numbers_only
    elif len(numbers_only) == 13 and numbers_only.startswith('55'):
        pass
    else:
        raise ValueError('Número de telefone inválido')

    return numbers_only
