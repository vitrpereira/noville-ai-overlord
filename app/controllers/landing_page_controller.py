from flask import Blueprint, render_template, redirect, url_for

landing_page = Blueprint('landing_page', __name__)

@landing_page.route('/')
def index():
    return render_template('landing_page/index.html')
