import click
import redis
from rq import Connection, Worker
from flask import current_app
from flask_migrate import upgrade
from flask.cli import FlaskGroup
from web import create_app, db
from web.models import catfile_to_db
from web.models import Paper, HpEvent

cli = FlaskGroup(create_app=create_app)


@cli.command("show_config")
def show_config():
    from pprint import pprint

    pprint(current_app.config)
    print(db.engine)


@cli.command("create_db")
def create_db():
    db.create_all()


@cli.command("upgrade_db")
def upgrade_db():
    """Upgrade running db with new structure

    - using flask-migrate alembic functionalities
    - upgrading db tables if necessary

    Here we use a (bad ?) hack to guess in what version the current code base is before applying some changes.
    """

    def hpevents_datetime_migrate():
        """Reparse catalogs txt files and fixe the hpevent datetime value

        the bug was fixed in the commit '6b38c89 Fix the missing hours in hpevent bug'
        """
        # delete all events
        for _e in HpEvent.query.all():
            db.session.delete(_e)
            db.session.commit()
        # then parse catalogs again
        for _p in Paper.query.all():
            _p.push_cat(force=True)
            db.session.commit()

    upgrade()
    if "0.4.0-pre-3" in current_app.config["VERSION"]:
        hpevents_datetime_migrate()


@cli.command("mock_papers")
def mock_papers():
    papers_list = [
        ["aa33199-18", "aa33199-18.pdf", None, None],
        [
            "2016GL069787",
            "2016GL069787.pdf",
            "2016GL069787/1010022016gl069787_bibheliotech_V1.txt",
            None,
        ],
        [
            "5.0067370",
            "5.0067370.pdf",
            "5.0067370/10106350067370_bibheliotech_V1.txt",
            None,
        ],
    ]
    for p_l in papers_list:
        paper = Paper(title=p_l[0], pdf_path=p_l[1], cat_path=p_l[2], task_id=p_l[3])
        db.session.add(paper)
    db.session.commit()


@cli.command("list_papers")
def list_papers():
    for p in Paper.query.all():
        print(p)


@cli.command("list_events")
@click.argument("mission_id", required=False)
def list_events(mission_id=None):
    if mission_id:
        events = HpEvent.query.filter_by(mission_id=mission_id)
    else:
        events = HpEvent.query.all()
    for e in events:
        print(e)


@cli.command("feed_catalog")
@click.argument("catalog_file")
def feed_catalog(catalog_file):
    """From a catalog file, feed db with events"""
    catfile_to_db(catalog_file)


@cli.command("run_worker")
def run_worker():
    redis_url = current_app.config["REDIS_URL"]
    redis_connection = redis.from_url(redis_url)
    with Connection(redis_connection):
        worker = Worker(current_app.config["QUEUES"])
        worker.work()


if __name__ == "__main__":
    cli()
