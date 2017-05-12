from datetime import datetime

from z2_site.models import Detail, DETAIL_FEATURED
from z2_site.common import DEBUG


def museum_global(request):
    data = {"debug":DEBUG}

    # Server info
    data["HOST"] = request.get_host()
    if data["HOST"] in ["museum.pokyfriends.com", "beta.museumofzzt.com"]:
        data["ENV"] = "PRIVATE BETA"
    elif data["HOST"] in ["z2.pokyfriends.com", "museumofzzt.com"]:
        data["ENV"] = "PUBLIC BETA"
    else:
        data["ENV"] = "DEVELOPMENT SERVER"

    # Server date/time
    data["datetime"] = datetime.utcnow()
    if data["datetime"].day == 27:  # This is very important
        data["drupe"] = True

    # Featured Games
    featured = Detail.objects.get(pk=DETAIL_FEATURED)
    data["fg"] = featured.file_set.all().order_by("?")[0]


    return data
