from app import create_app, app_celery

app = create_app()
app.app_context().push()

