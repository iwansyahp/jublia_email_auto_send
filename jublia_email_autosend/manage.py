import click
from flask.cli import FlaskGroup

from jublia_email_autosend.app import create_app


def create_jublia_email_autosend(info):
    return create_app(cli=True)


@click.group(cls=FlaskGroup, create_app=create_jublia_email_autosend)
def cli():
    """Main entry point"""


@cli.command("init")
def init():
    """Init application, create database tables with some initial email recipients
    """
    from jublia_email_autosend.extensions import db
    from jublia_email_autosend.models import User
    click.echo("create database")
    db.create_all()
    click.echo("done")

    click.echo("create initial email recipients")
    
    # TODO: create initial email recipients
    #db.session.add(user)
    #db.session.commit()
    # click.echo("created email recipients")


if __name__ == "__main__":
    cli()
