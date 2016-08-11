import os
from flask import (request, render_template,
                   redirect, flash, url_for)
from werkzeug.utils import secure_filename
from flask.views import View

from ..util import allowed_file
from ..img_resizer import edit_image
from ..config import APPLICATION_ROOT, ALLOWED_FILES


class UploadFileView(View):
    methods = ['POST']

    def dispatch_request(self):
        path = os.path.join(APPLICATION_ROOT, 'static', 'uploads')
        if request.method == 'POST':
            file = request.files['file']
            if file.filename == '':
                flash('No file selected!', 'warning')
                return redirect(url_for('add_post'))
            if file and allowed_file(file.filename, ALLOWED_FILES):
                filename = secure_filename(file.filename)
                if filename.rsplit('.', 1)[1] != 'mp3':
                    edit_image(file, filename)
                else:
                    file.save(os.path.join(path, filename))
        return redirect(url_for('add_post'))
