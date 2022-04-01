# Stdlib imports
from pathlib import Path

# Third-party app imports
from dateutil.parser import parse as parse_date

# Core Django imports
from django.conf import settings
from django.core.management import BaseCommand
from django.utils.timezone import make_aware

# Imports from my apps
from src.vertical_meteograms.models import VMDate


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

    help = "Update plots"

    def handle(self, *args, **options):
        """ """
        gfx = Path(settings.MEDIA_ROOT) / "gfx"
        # List date in gfx directory
        list_date = [path.stem for path in gfx.glob(("[0-9]" * 10)) if path.is_dir()]

        # Remove date not listed anymore
        for obj in VMDate.objects.all():
            _date = obj.date.strftime("%Y%m%d%H")
            if _date not in list_date:
                self.stdout.write(f"Removing date {obj}")
                obj.delete()

        # create new date
        for _date in list_date:
            dt = parse_date(_date[:8] + "T" + _date[8:])
            dt = dt.replace(minute=0, second=0, microsecond=0)
            obj, created = VMDate.objects.get_or_create(date=make_aware(dt))
            if created:
                self.stdout.write(f"Adding date {obj}")
