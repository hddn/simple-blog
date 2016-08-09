from flask import render_template
from flask.views import View


class TemplateView(View):

    def get_template_name(self):
        raise NotImplementedError()

    def render_template(self, context):
        return render_template(self.get_template_name(), posts=context)

    def dispatch_request(self):
        context = self.get_context()
        return self.render_template(context)
