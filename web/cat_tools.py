import csv

from web import db
from web.models import HpEvent


def catfile_to_rows(catfile):
    """Get all rows of a catalog file as  dict

       -  read each line, rid of comments
       -  create a hp_event_dict
    :return: hpevent_dict list
    """
    hpeventdict_list = []
    with open(catfile, newline="") as csvfile:
        reader = csv.reader(
            filter(lambda r: r[0] != "#", csvfile), delimiter=" ", quotechar='"'
        )
        for row in reader:
            hpevent_dict = {
                "start_date": row[0],
                "stop_date": row[1],
                "doi": row[2],
                "mission": row[3],
                "instrument": row[4],
                "region": row[5],
            }

            hpeventdict_list.append(hpevent_dict)
    return hpeventdict_list


def catfile_to_db(catfile):
    """Save a catalog file's content to db as hpevents

    :return: nothing
    """
    for hpevent_dict in catfile_to_rows(catfile):
        hpevent = HpEvent(**hpevent_dict)
        db.session.add(hpevent)
    db.session.commit()
