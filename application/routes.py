from flask import current_app as app
from flask import Blueprint, render_template, request, redirect, url_for, flash, Markup, abort
from werkzeug.utils import secure_filename
from os import path
from pathlib import Path
from .forms import UploadImage, images


main_bp = Blueprint('main_bp', __name__,
                    template_folder='templates')


@main_bp.route('/')
@main_bp.route('/index')
def index():
    return render_template('index.html')


@main_bp.route('/seg', methods=['GET', 'POST'])
def segmentation():
    form = UploadImage()
    in_url = None
    out_url = None
    if form.validate_on_submit():
        filename = images.save(form.image.data)
        in_url = images.url(filename)
    return render_template('seg.html', form=form, in_url=in_url, out_url=out_url)

# @main_bp.route('/user/<int:id>', methods=['GET', 'POST'])
# @login_required
# def user_page(id):
#     password_form = PasswordForm()
#     user_row = User.query.get(id)
#     if      (request.method == 'POST' and 
#             password_form.validate_on_submit()):
#         new_password = request.form.get('new_password')
#         user_row.password = generate_password_hash(
#                                 new_password, method='sha256')
#         db.session.commit()
#         flash('Password was changed successfully', 'success')
#         return redirect(url_for('main_bp.index'))
#     elif user_row:
#         return render_template('user.html', user_row=user_row, form=password_form)
#     abort(404)
