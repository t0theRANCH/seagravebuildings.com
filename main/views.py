from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.views.generic import TemplateView

from .calculate_angles import calculate_angles
from .models import NavMenuItem, VerifyAccount, NewUser
from .forms import QuoteForm, Register, Login, ForgotPassword, ChangePassword, RectangleForm
from .image_processing import TransformImage
from .confirm_registration import email_verification_token

from random import randint


# Helper functions
def get_user(response, uid, object_type):
    try:
        user = object_type.objects.get(pk=uid)
        verify = VerifyAccount.objects.get(user_id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user, verify = None, None
    return user, verify


def send_verification_email(response, instance, instance_type, email, subject):
    templates = {'verify_account': {'subject': 'Verify your account', 'template': 'verify_email.html'},
                 'forgot_password': {'subject': 'Reset your password', 'template': 'forgot_password_email.html'}}
    current_site = get_current_site(response)
    mail_subject = f"Seagravebuildings.com: {templates[subject]['subject']}."
    message = render_to_string(f"registration/{templates[subject]['template']}", {
        'user': instance,
        'domain': current_site.domain,
        'uid': instance.pk,
        'token': email_verification_token.make_token(instance)
    })
    to_list = [email]
    from_email = settings.EMAIL_HOST_USER
    usr = get_object_or_404(instance_type, id=instance.id)
    obj = VerifyAccount.objects.create(user_id=usr.id, hash_code=message, is_verified=False)
    obj.save()
    send_mail(mail_subject, message, from_email, to_list)


# Beginning of views
class MainView(TemplateView):
    banner_image = ''
    banner_images = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.header_image = None
        self.menu_items = NavMenuItem.objects.all()
        self.user = None

    def make_top_banner(self):
        if not self.banner_images or self.banner_image:
            self.banner_image = 'main/static/pictures/buildings/building.jpg'
        if self.banner_images:
            self.banner_image = self.banner_images[randint(0, len(self.banner_images) - 1)]
        target_resolution = (1366, 768)
        banner_resolution = (466, 69)
        header_image = TransformImage(image_path=self.banner_image)
        header_image.set_target_resolution(target_resolution)
        header_image.set_banner_resolution(banner_resolution)
        header_image.rotate()
        header_image.resize()
        header_image.make_top_bar()
        self.header_image = {'top_bar_height': f"{header_image.image_out.size[1]}px",
                             'content_margin': f"{header_image.image_out.size[1] + 20}px",
                             'top_bar': header_image.image_out_path.split('/')[-1],
                             'banner_height': header_image.logo_banner_resolution[1],
                             'banner_width': header_image.logo_banner_resolution[0]}

    def get_user(self, response):
        self.user = response.user if response.user.is_authenticated else None

    def get(self, response, *args, **kwargs):
        self.get_user(response)
        self.make_top_banner()
        context = {'url': self.template_name.split('/')[-1], 'menu_items': self.menu_items,
                   'user': self.user} | self.header_image
        return render(response, self.template_name, context)


class QuoteView(MainView):

    @staticmethod
    def compile_form_fields(form):
        contact_info = [form['full_name'], form['email'], form['phone'], form['country'], form['province'],
                        form['county'],
                        form['city'], form['postal_code']]
        property_info = [form['zoning'], form['purpose'], form['property'], form['timeline']]
        basic_info = [form['width'], form['length'], form['height']]
        basic_info_choices = [form['style'], form['colour'], form['install']]
        insulation = [form['insul_roof'], form['insul_walls']]
        trim = [form['gutters']]
        door_info = [form['walk_doors'], form['overhead_doors'], form['oh_door_height']]
        door_location = [form['oh_door_LE'], form['oh_door_RE'], form['oh_door_FS'], form['oh_door_BS']]
        additional_info = form['additional']
        return {'contact_info': contact_info, 'property_info': property_info, 'basic_info': basic_info,
                'basic_info_choices': basic_info_choices, 'insulation': insulation, 'trim': trim,
                'door_info': door_info,
                'door_location': door_location, 'additional_info': additional_info}

    def get(self, response, *args, **kwargs):
        self.get_user(response)
        self.make_top_banner()
        form = QuoteForm()
        return self.render_page(response, form)

    def post(self, response, *args, **kwargs):
        self.get_user(response)
        form = QuoteForm(response.POST)
        if form.is_valid():
            # save to database
            form.save()
            response.session['name'] = form.cleaned_data['full_name']
            response.session['phone'] = form.cleaned_data['phone']
            return redirect('request-quote')
        return self.render_page(response, form)

    def render_page(self, response, form):
        form_sections = self.compile_form_fields(form)
        context = {'url': 'quote.html', 'menu_items': self.menu_items, 'form_sections': form_sections, 'form': form,
                   'quote': True, 'user': self.user} | self.header_image
        return render(response, 'main/quote.html', context)


class ConfirmationView(TemplateView):
    info = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.context = {}

    def get_context(self, response):
        self.context = {key: value if key not in response.session else response.session[key]
                        for key, value in self.info.items()}

    def get(self, response, *args, **kwargs):
        self.get_context(response)
        return render(response, self.template_name, self.context)


def sign_up(response):
    form = Register(response.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.is_active = False
        instance.save()
        send_verification_email(response, instance, NewUser, form.cleaned_data.get('email'), 'verify_account')
        return redirect('confirmation-sent')
    return render(response, 'registration/sign_up.html', {'form': form})


def confirmation_sent(response):
    return render(response, 'registration/confirm_email.html', {})


def activate(response, uid, token):
    new_user, verify = get_user(response, uid, NewUser)
    if new_user is not None and email_verification_token.check_token(new_user, token):
        # TO DO check for proper permissions
        user = User.objects.create_user(username=new_user.username, email=new_user.email, password=new_user.password1)
        user.is_active = True
        user.save()
        verify.is_verified = True
        verify.save()
        return redirect('activated')
    else:
        return HttpResponse('Activation link is invalid!')


def change_password(response, uid, token):
    user, verify = get_user(response, uid, User)
    if user is not None and email_verification_token.check_token(user, token):
        form = ChangePassword(response.POST or None)
        if form.is_valid():
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('change-password-complete')
        return render(response, 'registration/change_password.html', {'user': user, 'form': form})
    else:
        return HttpResponse('Reset Link is invalid')


def sign_in(response):
    form = Login(response.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        if user := authenticate(response, username=username, password=password):
            login(response, user)
            return redirect('home')
        return render(response, 'registration/login.html',
                      {'form': form, 'error_message': 'Oops, Something went wrong'})
    return render(response, 'registration/login.html', {'form': form})


def sign_out(response):
    logout(response)
    return redirect('home')


def password_reset(response):
    form = ForgotPassword(response.POST or None)
    if form.is_valid():
        email = form.cleaned_data['email']
        user = get_object_or_404(User, email=email)
        send_verification_email(response, user, User, email, 'forgot_password')
        response.session['email'] = email
        return redirect('password-reset-sent')
    return render(response, 'registration/forgot_password.html', {'form': form})


def layout_calculator(response):
    form = RectangleForm(response.POST or None)
    if form.is_valid():
        sides = {'side_ab': form.cleaned_data['side_ab'], 'side_ac': form.cleaned_data['side_ac'],
                 'side_bd': form.cleaned_data['side_bd'], 'side_cd': form.cleaned_data['side_cd'],
                 'diag_ad': form.cleaned_data['diag_ad'], 'diag_bc': form.cleaned_data['diag_bc']}
        angles = calculate_angles(sides)
        return render(response, 'main/rectangle_calculator.html', {'form': form, 'angles': angles})
    return render(response, 'main/rectangle_calculator.html', {'form': form})
