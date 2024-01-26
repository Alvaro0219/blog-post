import functools
from flask import (
    Blueprint, render_template, redirect, url_for, flash, request, session, g
)
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from blogr import db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    result_message = None

    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifica si el usuario ya existe en la base de datos
        existing_user = User.query.filter_by(email=email).first()

        if existing_user is None:
            # Crea una nueva instancia de User utilizando el constructor
            new_user = User(username=username, email=email, password=generate_password_hash(password))

            # Agrega el nuevo usuario a la base de datos
            db.session.add(new_user)
            db.session.commit()

            result_message = 'Registro exitoso. Ahora puedes iniciar sesión.'
            return render_template('auth/login.html', result_message=result_message, alert_type='success')
        else:
            result_message = f'El correo {email} ya está registrado.'
            return render_template('auth/register.html', result_message=result_message, alert_type='danger')

    return render_template('auth/register.html', result_message=result_message, alert_type=None)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    result_message = None

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session.clear()
            session['user_id'] = user.id
            result_message = 'Inicio de sesión exitoso.'
            return redirect(url_for('post.posts'))
        else:
            result_message = 'Email o contraseña incorrecta.'
            return render_template('auth/login.html', result_message=result_message, alert_type='danger')

    return render_template('auth/login.html', result_message=result_message, alert_type=None)

# Mantener un usuario logueado
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home.index'))

# Decorador para requerir inicio de sesión
def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            flash(('Debes iniciar sesión para acceder a esta página.', 'danger'))
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

#Funcion para subir fotos
from werkzeug.utils import secure_filename

def get_photo(id):
    user = User.query.get_or_404(id)
    photo = None

    if photo != None:
        photo = user.photo

    return photo

@bp.route('/profile/<int:id>', methods=('GET','POST'))
@login_required
def profile(id):
    # Obtener el usuario actual
    user = User.query.get_or_404(id)
    photo = get_photo(id)

    # Inicializar result_message con None
    result_message = None

    if request.method == 'POST':
        # Obtener los datos del formulario
        new_username = request.form.get('username')
        new_email = request.form.get('email')
        current_password = request.form.get('password')
        new_password = request.form.get('new_password')

        #Subir foto
        if request.files['photo']:
            photo = request.files['photo']
            #Guardamos foto en una direccion del proyecto 'media'
            photo.save(f'blogr/static/media/{secure_filename(photo.filename)}')
            #guardar en la bd
            user.photo = f'media/{secure_filename(photo.filename)}'

        # Verificar la contraseña actual
        if check_password_hash(user.password, current_password):
            # Actualizar los datos del usuario
            user.username = new_username
            user.email = new_email

            # Si se proporciona una nueva contraseña, hashearla y actualizarla
            if new_password:
                user.password = generate_password_hash(new_password)

            # Guardar los cambios en la base de datos
            db.session.commit()

            result_message = 'Perfil actualizado correctamente.'
        else:
            result_message = 'Contraseña actual incorrecta. No se realizaron cambios.'

    return render_template('auth/profile.html', user=user, photo=photo, result_message=result_message)

