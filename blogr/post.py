from flask import Blueprint, request, redirect, url_for, g, render_template
from .auth import login_required
from .models import Post
from blogr import db

bp = Blueprint('post', __name__, url_prefix='/post')

@bp.route('/posts')
@login_required
def posts():
    posts = Post.query.all()
    result_message = request.args.get('result_message', None)
    return render_template('admin/posts.html', posts=posts, result_message=result_message)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    result_message = None

    try:
        if request.method == 'POST':
            url = request.form.get('url')
            title = request.form.get('title')
            info = request.form.get('info')
            content = request.form.get('ckeditor')

            # Verifica si la URL ya está en uso
            existing_post = Post.query.filter_by(url=url).first()

            if existing_post:
                result_message = f'La URL {url} ya está en uso. Elige otra.'
            else:
                # Crea una nueva instancia de Post
                post = Post(g.user.id, url, title, info, content)

                # Agrega y guarda el nuevo post en la base de datos
                db.session.add(post)
                db.session.commit()

                result_message = 'Blog creado exitosamente.'
                return redirect(url_for('post.posts'))
    except Exception as e:
        # Manejar errores
        result_message = 'Error al crear el blog. Inténtalo de nuevo.'

    return render_template('admin/create.html', result_message=result_message)

@bp.route('/update/<int:id>', methods=('GET', 'POST'))
@login_required
def update(id):
   # Obtener el post existente de la base de datos
    post = Post.query.get_or_404(id)

    result_message = None

    if request.method == 'POST':
        # Obtener los nuevos datos del formulario
        new_title = request.form.get('title')
        new_info = request.form.get('info')
        new_content = request.form.get('ckeditor')

        # Actualizar los datos del post existente
        post.title = new_title
        post.info = new_info
        post.content = new_content

        # Guardar los cambios en la base de datos
        db.session.commit()

        result_message = 'Post actualizado exitosamente.'
        return redirect(url_for('post.posts'))

    # Renderizar la plantilla con los datos actuales del post
    return render_template('admin/update.html', post=post, result_message=result_message)

@bp.route('/delete/<int:id>')
@login_required
def delete(id):
    result_message = None

    post = Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    
    result_message = 'El blog se eliminó correctamente'

    return redirect(url_for('post.posts', result_message=result_message))


