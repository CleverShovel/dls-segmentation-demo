from flask import current_app as app
from flask import Blueprint, render_template, request, redirect, url_for, flash, Markup, abort
from werkzeug.utils import secure_filename
from os import path
import uuid
from pathlib import Path
from .forms import UploadImage, images
from .seg_model import evaluate_image

from pathlib import PurePath

from PIL import Image


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
        filename = uuid.uuid4().hex + '.jpg'
        path = app.config['UPLOADED_IMAGES_DEST']+'/'+filename
        image = request.files['image']
        with Image.open(image) as pil_image:
            old_size = pil_image.size
            if max(old_size) > 1000:
                pil_image = pil_image.resize(
                    (int(1000/max(old_size)*old_size[0]), int(1000/max(old_size)*old_size[1])))
            pil_image.save(path)
        in_url = images.url(filename)
        out_url = images.url(evaluate_image(path))
        return render_template('seg.html', form=form, in_url=in_url, out_url=out_url)
    return render_template('seg.html', form=form, in_url=in_url, out_url=out_url)
