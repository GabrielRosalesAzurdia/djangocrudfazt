# Segundo curso de Fazt de Django

## Hacer una app conocida para django

Ir al settings.py de la la aplicación root y en el array installed apps 
agregar el nombre de la app que se ha creado

## Login

Django ya permite hacer login, para usarlo hacemos lo siguiente:

primero importamos el user creation form:

> from django.contrib.auth.forms import UserCreationForm

Luego enviamos el user creation form para que pueda ser mostrado en la página

>     return render(request,"auth/signup.html",{'form':UserCreationForm})

Todo esto no está dentro de un etiqueta form por lo que tenemos que 
hacer lo siguiente:

>    < form action="/signup/" method="post">
>        {% csrf_token %}
>        {{form.as_p}}
>        < button type="submit">
>            sigup
>        </ button>
>    </ form>

Siendo action la url a la cual aplicará el método que se detalla

Para guardar los usuarios también usaremos algo dado por Django, que es así:

> from django.contrib.auth.models import User

Y acá puedo crear usuarios 

>        if request.POST["password1"] == request.POST["password2"]:

>             try:
>                user = User.objects.create_user(username=request.POST["username"],password=request.POST["password1"])
>                user.save()
>                return HttpResponse("User added")
>            except:
>                return HttpResponse("User already exists")
>        else:
>            return HttpResponse("The passwords are not the same")

## Manejando errores de mejor manera

La mejor manera de manejar errores es no solo enviar un texto a renderizar sino
enviar un parámetro a un template html para que sepa qué mostrar 

## Proteger rutas

Sirve para limitar quién entra a una o varias rutas en específico,
importamos una entidad de django que verifica que un usuario
esté logiado para que permita acceso

> from django.contrib.auth.decorators import login_required

La forma de colocarlo es escribir sobre una función esto:

> @login_required

> def signout(request):

Esto va a redigir al login a las personas que no estén logiadas, esto lo
podemos configurar en el settings.py

> LOGIN_URL = "/signin"

Siendo "/signin" la ruta donde está la página del login

# Deploy
Se utilizará un servicio llamado render el cual es un servivio de despliegue rápido
las otras opciones son como aws o google que necesitan más configuración para 
funcionar - yo inicié con github -
Tiene opciones para páginas estáticas que solo utilizan javascript y css
Y también para workers que son aplicaciones que están siempre ejecutandose, 
lo que a nosotros nos interesa es los web services

Entramos y le damos en new web service, este nos pedirá un repositorio de git y
varias configuracione que debemos hacer en el proyecto

https://render.com/docs/deploy-django

Primero modificamos la secret key importando el os 

> import os

> SECRET_KEY = os.environ.get('SECRET_KEY',default='your secret key')

Cambiar el debug a false

> DEBUG = 'RENDER' not in os.environ

También debemos cambiar los host que están permitidos por Django
esto es otra vez con una variable de entorno

>RENDER_EXTERNAL_HOSTNAME = os.environ.get('RENDER_EXTERNAL_HOSTNAME')

>if RENDER_EXTERNAL_HOSTNAME:    
>    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

Ahora también vamos a cambiar la base de datos para ya no utilizar squlite3 
sino que postgresql en este caso

Primero instalamos un paquete

> pip install dj-database-url psycopg2-binary

importamos al primero

> import dj_database_url

y lo ponemos como default

>DATABASES = {
>    'default': dj_database_url.config(
>        default='postgresql://postgres:postgres@localhost/postgres',
>        conn_max_age=600
>    )
>}

Y configuramos los archivos estáticos

Es importante tener esto en mente, django no es un servidor es un framework que 
necesita de un servidor web por lo que necesitamos una herramienta
para esto

> pip install whitenoise[brotli]

Y lo agregamos al middleware

> 'whitenoise.middleware.WhiteNoiseMiddleware',

Y al final alteramos el directorio de los archivos estáticos

>if not DEBUG:    # Tell Django to copy statics to the `staticfiles` directory
>    # in your application directory on Render.
>    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
>    # Turn on WhiteNoise storage backend that takes care of compressing static files
>    # and creating unique names for each version so they can safely be cached >forever.
>    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

Creamos un archivio build.sh donde agregamos los comandos 
a ejecutar estando ya en el web server, allí agregamos lo siguiente

> #!/usr/bin/env bash
> # exit on error
>set -o errexit

> # poetry install

> python manage.py collectstatic --no-input
> python manage.py migrate

luego abrimos una git bash en este directorio y ejecutamos

> chmod a+x build.sh

y por úlitmo installamos gunicorn en la cmd normal

> pip install gunicorn

y obtenemos los requerimientos corriendo el siguiente archivo
> pip list --format=freeze > requirements.txt  

y en el archivo build.sh agregamos la linea antes de pytho manage.py ...

> pip install -r requirements.txt

Listo ahora creamos un .gitignore para ignorar la base de datos sqlite3
para eliminar un repo de git usen >del .git

ahora cremos un repo normal de git

>git init
>git add .
>git commit -m "primer commit"

Creamos un repositorio en github

Podemos retirar y comentar el pip install -r requirements.txt pues ya lo ejecuta
render, esto lo hacemos comentando la linea y luego haciendo un push al remote repo

La instalación fallará, vamos a enviroment variables y agregamos 
una con nombre: PYTHON_VERSION y de valor le damos 3.10.8 que es la 
versión a la fecha de creada esta app