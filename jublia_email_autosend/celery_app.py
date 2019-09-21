from jublia_email_autosend.app import init_celery

app = init_celery()
app.conf.imports = app.conf.imports + ('jublia_email_autosend.tasks',)
