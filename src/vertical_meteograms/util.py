# Stdlib imports
from datetime import datetime, timedelta

# Third-party app imports
from dateutil.parser import ParserError
from dateutil.parser import parse as parse_date

# Core Django imports
from django.utils.timezone import make_aware

# Imports from my apps
from .models import VMDate


def _get_date(date_=None):
    """check date_ in argument, return datetime object"""
    if date_:
        try:
            # reformat dates to isoformat, use TIME_ZONE from settings
            dt = parse_date(date_)
        except ParserError as exc:
            raise ParserError(f"Invalid date. \n{exc}")
    else:
        dt = datetime.now()

    return dt


# https://stackoverflow.com/a/23580186
# to run daily or four times each day ??
def upload(date_=None):
    """upload and save station and margin"""

    dt = _get_date(date_)
    for hour in [0, 6, 12, 18]:
        dt = dt.replace(hour=hour, minute=0, second=0, microsecond=0)
        # create instance
        inst = VMDate(date=make_aware(dt))
        # save instance on db
        inst.save()


def clean(date_=None, step_=6):
    """clean, remove VMDate instance older than date_ - step_ days"""

    # get reference day
    dt = _get_date(date_)
    # compute date X days before reference day
    enddate = dt - timedelta(days=step_)
    # delete of instance with date lower than enddate
    VMDate.objects.filter(date__lt=enddate).delete()
