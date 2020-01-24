from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from flask_uploads import UploadSet, IMAGES


images = UploadSet('images', IMAGES)


class UploadImage(FlaskForm):
  """Upload sound form."""
  image = FileField(validators=[
    FileAllowed(images, 'Image only!'), 
    FileRequired('File was empty!')])