from djoser.conf import settings
from django.conf import settings as base_settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from djoser import utils
from templated_mail.mail import BaseEmailMessage


class CustomEmailMessage(BaseEmailMessage):
    def send(self, *args, **kwargs):
        context = self.get_context_data()
        subject = 'Activation email'
        html_data = render_to_string(self.template_name, context)
        send_mail(subject, None, 'HLove <HLoveHosting@gmail.com>',
                  [context['hlove_email']], html_message=html_data)


class CustomActivationEmail(CustomEmailMessage):
    template_name = "activation_email.html"

    def get_context_data(self):
        context = super().get_context_data()

        user = context.get("user")
        context["uid"] = utils.encode_uid(user.pk)
        context["token"] = default_token_generator.make_token(user)
        context["url"] = settings.ACTIVATION_URL.format(**context)
        context["base_url"] = base_settings.BASE_BACK_URL
        context["name"] = user.username
        context["hlove_email"] = user.email
        return context
