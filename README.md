# BlogPosts App

BlogPosts es una aplicación web que permite a los usuarios registrados crear y gestionar publicaciones en un blog. La aplicación consta de dos módulos principales: Autenticación y Publicaciones.

## Funcionalidades

### Módulo de Autenticación

1. **Registro de Usuario:** Los usuarios pueden crear una cuenta proporcionando un nombre de usuario, correo electrónico y contraseña. Se verifica si el correo electrónico ya está registrado antes de crear la cuenta.
2. **Inicio de Sesión:** Permite a los usuarios iniciar sesión proporcionando su correo electrónico y contraseña. Se verifican las credenciales del usuario y se crea una sesión si son válidas.
3. **Cierre de Sesión:** Cierra la sesión del usuario y lo redirige a la página de inicio.
4. **Perfil de Usuario:** Permite a los usuarios ver y actualizar su información de perfil, incluyendo cambio de nombre de usuario, correo electrónico y contraseña, así como cargar una foto de perfil.

### Módulo de Publicaciones (Post)

1. **Listar Publicaciones:** Muestra una lista de todas las publicaciones disponibles.
2. **Crear Publicación:** Permite a los usuarios crear nuevas publicaciones.
3. **Ver Detalles de la Publicación:** Muestra los detalles completos de una publicación específica.
4. **Actualizar Publicación:** Permite a los usuarios editar una publicación existente.
5. **Eliminar Publicación:** Elimina una publicación específica.

### Plantillas

1. **Listado de Publicaciones (index.html):** Muestra una lista de todas las publicaciones disponibles y proporciona un formulario de búsqueda para filtrar las publicaciones.
2. **Crear/Editar Publicación (create.html y update.html):** Formulario para crear o editar una publicación.
3. **Detalles de la Publicación (blog.html):** Muestra todos los detalles de una publicación específica.

## Requisitos de Instalación

# Clona el repositorio
git clone https://github.com/tuusuario/BlogPosts.git

# Navega al directorio del proyecto
cd BlogPosts

# Instala las dependencias
pip install -r requirements.txt

# Ejecuta la aplicación
python app.py
