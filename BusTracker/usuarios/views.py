from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
import folium
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
import logging
from django.db.models import Q
from django.core.mail import EmailMessage
from .forms import  CustomPasswordChangeForm
from django.http import JsonResponse
import openai
import geocoder



from datetime import datetime
from datetime import timedelta
import time

import responses

import googlemaps

destination  = ''
# Create your views here.

def home(request):
    return render(request, 'home.html')


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'register.html', {"form": UserCreationForm, "error": "Ese usuario ya existe, intente de nuevo porfavor"})

        return render(request, 'register.html', {"form": UserCreationForm, "error": "Las contraseñas no coinciden, intente de nuevo porfavor"})

def user_login(request):
    if request.method == 'GET':
        return render(request, 'login.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'login.html', {"form": AuthenticationForm, "error": "Usuario o contraseña incorrectas, intente de nuevo por favor"})

        login(request, user)
        return redirect('home')

# def register(request):
#     if request.method == 'GET':
#         return render(request, 'register.html', {"form": UserCreationForm()})
#     else:
#         # Instanciar el formulario con los datos enviados
#         form = UserCreationForm(request.POST)
#         if form.is_valid():
#             try:
#                 user = form.save()  # Esto guarda al usuario y lo valida
#                 login(request, user)
#                 # Redirigir al usuario con un mensaje de éxito
#                 return redirigir_con_mensaje(request, 'home', "Registro exitoso.")
#             except IntegrityError:
#                 # Usar la función de utilidad para manejar el error de integridad
#                 return manejar_error_autenticacion(
#                     request, 
#                     UserCreationForm(), 
#                     'register.html', 
#                     "Ese nombre de usuario ya existe. Por favor, elija uno diferente.")
#         else:
#             # Si el formulario no es válido, puede ser debido a contraseñas que no coinciden u otros errores de validación
#             return manejar_error_autenticacion(
#                 request, 
#                 form, 
#                 'register.html', 
#                 "Hubo un error en su registro. Por favor, revise los datos introducidos.")


# def login(request):
#     if request.method == 'GET':
#         return render(request, 'login.html', {"form": AuthenticationForm})
#     else:
#         user = authenticate(
#             request, username=request.POST['username'], password=request.POST['password']
#         )
#         if user is None:
#             return manejar_error_autenticacion(
#                 request, AuthenticationForm, 'login.html',
#                 "Usuario o contraseña incorrectas, intente de nuevo por favor")
#         login(request, user)
#         return redirigir_con_mensaje(request, 'home', "Inicio de sesión exitoso")
    


@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def edit_user(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Tu perfil ha sido actualizado con éxito.')
            return redirect('home')  # Cambia 'home' a la URL de la página de inicio de tu aplicación
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'edit_user.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Actualiza la sesión del usuario para evitar que se cierre la sesión
            messages.success(request, 'Tu contraseña ha sido actualizada con éxito.')
            return redirect('home')  # Cambia 'home' a la URL de la página de inicio de tu aplicación
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, 'change_password.html', {'form': form})



def redirigir_con_mensaje(request, url_name, mensaje, nivel=messages.INFO):
    messages.add_message(request, nivel, mensaje)
    return redirect(url_name)

def manejar_error_autenticacion(request, form, template_name, mensaje_error):
    return render(request, template_name, {
        "form": form,
        "error": mensaje_error
    })



######################################################################################################





# Create your views here.

open_ai_key = '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'


openai.api_key = open_ai_key

def ask_openai(message):
    response = openai.Completion.create( 
        model = 'text-davinci-003',
        prompt =  "Identifica la ubicación a la cual se quiere dirigir el usuario en el siguiente mensaje y devuelvela sola para poder ingresarla en la Api de GCP de lamanera mas especifica posible"+message,
        max_tokens = 150,
        n = 1,
        stop = None,
        temperature = 0.7,
    )
    answer = response.choices[0].text.strip()
    return answer


def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')
        response = ask_openai(message)
        loc = response
        destination = geocoder.osm(loc)
        print(destination)
        return JsonResponse({'response': response})
    return render(request, 'chatbot.html')




def mapa(request):
    return render(request, 'mapa.html', {'destination':destination})

###################################################

@responses.activate
def direction(self, destination):
        responses.add(
            responses.GET,
            "https://maps.googleapis.com/maps/api/directions/json",
            body='{"status":"OK","routes":[]}',
            status=200,
            content_type="application/json",
        )

        now = datetime.now()
        routes = self.client.directions(
            "Brooklyn", destination, mode="transit", departure_time=now
        )

        self.assertEqual(1, len(responses.calls))
        self.assertURLEqual(
            "https://maps.googleapis.com/maps/api/directions/json?"
            "origin=Brooklyn&key=%s&destination=Queens&mode=transit&"
            "departure_time=%d" % (self.key, time.mktime(now.timetuple())),
            responses.calls[0].request.url,
        )


