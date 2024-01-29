from flask import Blueprint, request, redirect, url_for, g, render_template
from .auth import login_required
from .models import Post
from blogr import db

bp = Blueprint('post', __name__, url_prefix='/post')


@bp.route('/posts')
@login_required
def posts():
    posts = Post.query.all()
    return render_template('admin/posts.html', posts = posts)

@bp.route('/create', methods = ('GET', 'POST'))
@login_required
def create():
    result_message = None

    if request.method == 'POST':
        url = request.form.get('url')
        title = request.form.get('title')
        info = request.form.get('info')
        content = request.form.get('content')

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
    return render_template('admin/create.html', result_message=result_message)

@bp.route('/update')
def update():
    return 'Pagina de update'