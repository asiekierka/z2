import json
import os
import random
import sys
import zipfile
from datetime import datetime

import django
import pytumblr
import requests
from twitter import *
from PIL import Image

sys.path.append("/var/projects/museum")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "museum.settings")
django.setup()

from museum_site.models import (
    File, DETAIL_ZZT, DETAIL_SZZT, DETAIL_UPLOADED, DETAIL_GFX
)

import zookeeper

from private import (
    CONSUMER, SECRET, OAUTH_TOKEN, OAUTH_SECRET, TWITTER_CONSUMER_KEY,
    TWITTER_CONSUMER_SECRET, TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET,
    WEBHOOK_URL
)


def main():
    POST = True if "NOPOST" not in sys.argv else False
    CRON_ROOT = "/var/projects/museum/tools/crons/"
    ROOT = "/var/projects/museum"
    QUEUE = os.path.join(CRON_ROOT, "woz_queue.txt")
    APRIL = True if datetime.now().strftime("%m-%d") == "04-01" else False

    BLACKLISTED_FILES = [
        951,  # G**g J*****n And STK Revealed
        1779,  # 1**9 T*o
        1577,  # 9**1: A Z*T M******l
        1927,  # N**e E*****n
        1811,  # B*N L***N!!
        1852,  # M*****a R***s
        2064,  # M*****a R***s SE
        1496,  # B******! (Author's request)
        2542,  # E**e K****e M****m-M***k! (Author's request)
        493,  # G***D P**t 1! (Author's request)
        494,  # G***D P**t 2! (Author's request)
        494,  # G***D S********k! (Author's request)
        2242,  # M*****'s Z*T T*******s (Author's request)
        2242,  # P******l (Author's request)
        1197,  # P******l B* (Author's request)
        925,  # T*e P****e F***s I* (Author's request)
        1723,  # T***h (Author's request)
        1801,  # Z*TV 8 (Author's request TEMPORARY UNTIL BOARDS ARE HANDLED)
        1901,  # Z*TV 9 (Author's request TEMPORARY UNTIL BOARDS ARE HANDLED)
        2059,  #M****m B***s A*******y (Harassing)
        2095,  #M****m B***s 3 (Harassing)
        2540,  #M****m B***s 4 (Harassing)
        2087,  #M****m B***s 1 (Harassing)
        2084,  #M****m B***s 2 (Harassing)

    ]

    BOARD_TITLE_BLACKLIST = [
        "!;MadTom's ColorKit", "!;MadTom's ZZToolKit", "!The NOC Color Kit", "$ **.**Tripping Color Kit**.**", "$- == (( ( paramach ) )) == -", "$ K Z T - Color Kit",
        "$ ZZT Palette Plus v1.1", "$-( Blend Box )-", "$(( ( Paranoid Machinations ) ))", "$() Dude Scott This is Josh ()", "$({[/-=+Colors R' Us 2.25 +=-\]})",
        "$(= SGP ColorKit v1.0 =)", "$)][( dexter's pepsi-kit )][(", "$*)|(* dexscam! *)|(*", "$*-*-* Mega Color Box '98 *-*-*", "$**GameMstr1's MegaShades Board**",
        "$*-< CorPuS HeRmetIcUm >-*", "$*-=yllek's kewl color board=-*", "$:: hm's wonkeriffic toolkit ::", "$::<< BenKit >>::", "$:[ dexkit ]:", "$:{*pisces~iscariot*}  version 666",
        "$:-BesTK-:", "$[[[ [  suburbiaTRiUMPHANT  ] ]]]", "$[] DarkMage ColorKit []", "$[=- textures by eJECTION13 -=]", "$[glt-kit by tboT]", "$[Jacob Hammond's Colorkit]",
        "$_/\" VisuoFunctional Spectrum _/\"", "$_Underscore_", "$+*=-{[ULTIMA COLOR BOARD]}-=*+", "$-+=Flame, Inc. Color Kit=+-", "$-+-The-Shaft-tool-kit-+-", "$<(divided)>",
        "$<> FutureWare Blending Kit <>", "$-= Raichu's Circuitbox v6.28 =-", "$-=([ <3\/|$|0/\/ ])=-", "$-=(MRFLOYDS COLOR BOX)=-",
        "$-=* * * 3 Palette * * *=-", "$-=\EM's Damn ZZT-Kit/=-", "$-=|DirrCo Krazie Kitt 3|=-", "$-=+*PARASITE'S TOOL KIT*+=-",
        "$--==::Noboyuki's ToolSet::==--", "$--==<<BenKit 2 (or BQKiT)>>==--", "$==--Magical Mystical ColorBox--==", "$-=Mondo SaxxonPike ToolBox=-",
        "$-=SNACK 4.0 (board 1)=-", "$-=SNACK 4.0 (Board 2)=-", "$>>COLOR TOOLBOX<<", "$3d vFINAL - Josh Microwave", "$A.I.Z.I Advanced with ZOP", "$AKWare Tool-Kit",
        "$AKWare Tool-Kit V2.0", "$ALL v1.0 for ZZT", "$barrel 'o fun kit", "$Bocco11's ZZToolkit v1.10", "$Creemy Chock n' Cheez Froot Lumps", "$DGE Color Kit",
        "$DrCrab's Crammed Board", "$Dude Scott This is Josh V3.0", "$Ed's Colorkit", "$Embassy Games Color Center", "$Headache- Inducing- Evil.",
        "$HGSI Coloring Kit (v4)", "$JM's All Purpose ZZT Toolbox", "$KPCK V. 1.0", "$MIG toolkit", "$Misteroo Rebellion/AKWare Toolkit", "$MNMZ Soft Toolkit v1.3",
        "$Mystical Winds TK - Art Set Adv.", "$Mystickcal Color Toolkit", "$Newt's Toolbox", "$packboard.v1.aetsch.if.2000", "$playing this board will kill you",
        "$Ra/\/|)()/\/\ I/\/C TK V. NUTS", "$ROOKIT 2", "$Shades Toolbox", "$SIMBA SEZ ROAR", "$Spectracolor", "$StreamLineSTK versionArr", "$Terrain Toolbox - Ice",
        "$The KjKit!   Board 3", "$The KjKit!  Board 2", "$The KjKit! Board 1", "$The KjKit! Board 2", "$The KjKit! Board 3", "$The ZZT First Aid Kit", "$Ultra Colour",
        "$Vecchio's Toolkit", "$vin3y $hades Toolbo><", "$VINEY80X", "$vstk - v. peter gabriel", "$wtog", "$ZZT First Aid Kit", "$ZZTek Color Board - by kev carter",
        "$ZZTek Colour Kit", "::   - ZZT Rainbow v3.7 -   ::", ":: NMZmaster Toolkit v3.0", "::/\/omo(7) update!", "::z.nadir's palace of bullet::", ":; 2z + t",
        ":; Compressed Textkit", ":; Friday Night Fever", ":; UseLESSS ReDUNDAncYYYYy", ":;.silverspectrum v.karma", ":;[ the draco toolkit ]", ":;_-=(EarthquakeTK)=-_",
        ":;_-=+X(ETK 2)X+=-_", ":;-=( beef's ultra funky tool kit", ":;-=*Raptorian's Toolbox v2.1*=-", ":;Dave's ARG! PG Tool-kit", ":;dexmono vthe fly",
        ":;lemmer toolkit: v100", ":;lemmer's ascii chart on fire", ":;Quantum's Toolkit (1)", ":;Quantum's Toolkit (3)", ":;rom v. hall of heads2k",
        ":WinS Toolbox v2.5", "Quantum's Toolkit (2)", "Quantum's Toolkit (4)", "*NEW STK--Objects", "*NEW STK--Objects, Blinking", "*NEW STK--Boulders, Both", "*NEW STK--N/S Sliders, Both",
        "*NEW STK--E/W Sliders, Both", "*NEW STK--Gems, Both", "*NEW STK--Keys, Both", "*NEW STK--Normal Walls, Both", "*NEW STK--Breakable Walls, Both", "*NEW STK--Invisible Walls, Both",
        "*NEW STK--Fake Walls, Both", "*NEW STK--Water, Both", "*NEW STK--Bombs", "*NEW STK--Bombs, Blinking", "*NEW STK--Pushers", "*NEW STK--Pushers, Blinking", "*NEW STK--Spinning Guns",
        "*NEW STK--Spinning Guns, Blinking", "*NEW STK--CounterClockwise", "*NEW STK--CounterCl., Blinking", "*NEW STK--Clockwise", "*NEW STK--Clockwise, Blinking", "*NEW STK--Transporters",
        "*NEW STK--Transporters, Blinking", "*NEW STK--Blink Walls", "*NEW STK--Blink Walls, Blinking", "*NEW STK--Centipede Heads", "*NEW STK--Centip. Heads, Blinking",
        "*NEW STK--Line Walls, Both", "*NEW STK--Solid Walls, Both", "*NEW STK--Pre Activated Bombs", "*NEW STK--Bullets", "*NEW STK--Ammo, Torches, more",
        "*NEW STK--Doors, Passages, Floors", "*NEW STK--Ricochet", "*NEW STK--Strange Stuff", "*NEW STK--More Strange Stuff", "*MORESTK--Ammo, Both",
        "*MORESTK--Torches, Both", "*MORESTK--Doors, Both", "*MORESTK--Star, Bl enemies, etc.", "*MORESTK--More Passages", "*MORESTK--Duplicators", "*MORESTK--Dupes, Blinking",
        "*MORESTK--In-process Dupes", "*MORESTK--PreActivatedBombs1", "*MORESTK--PreActivatedBombs2", "*MORESTK--PreActivatedBombs3", "*MORESTK--Energizers, Both",
        "*MORESTK--Forests, Both", "*MORESTK--Horiz. BWall Rays", "*MORESTK--All Bullets", "*MORESTK--Ricochets, Both", "*MORESTK--Text: B, G, Cy, R",
        "*MORESTK--Text: P, Y, W", "*MORESTK--Still Bullets, Both", "*MORESTK--Empties, Both", "*WEIRDSTK--Crosses", "*WEIRDSTK--Passages",
        "*WEIRDSTK--Carrots", "*WEIRDSTK--Dead pushers", "*WEIRDSTK--Smilies", "*WEIRDSTK--Dead bears", "*WEIRDSTK--Dead ruffians", "*WEIRDSTK--Dead lions",
        "*WEIRDSTK--Dead tigers", "*WEIRDSTK--Dead heads", "*WEIRDSTK--Dead segments", "*WEIRDSTK--Breakables", "*WEIRDSTK--Breakables, blinking",
        "*WIL STK--MONITORs w/o stats", "*WIL STK--Monitors", "*WIL STK--Monitors, Blinking", "*WIL STK--Slimes", "*WIL STK--Slimes, Blinking",
        "*WIL STK--Slimes w/o stats", "*WIL STK--Hyper Enemies", "*WIL STK--More Hyper Enemies", "*WIL STK--Faster/Slower Bombs",
        "*WIL STK--Scroll to Fakes", "*WIL STK--Scroll to Fakes, Blinkin"
    ]

    # Check if there's anything in the manual queue
    """ Queue Format: YYYY-MM-DD:HOUR:PK:FILENAME:BOARD
        Use * for wildcards in dates/hours
        Keep wildcard dates/hours below specific ones to allow first match
         1:45 AM == 9
         5:45 AM == 12
         8:45 AM == 15
        11:45 AM == 18
         2:45 PM == 21
         5:45 PM == 0
         8:45 PM == 3
        11:45 PM == 6
    """
    source = "RANDOM"
    queue_data = {}
    output = ""
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_hour = datetime.now().strftime("%H")
    print("DATE/HOUR", current_date, current_hour)
    with open(QUEUE) as fh:
        lines = fh.readlines()

    for line in lines:
        line = line.strip()
        print("LINE", line)

        date, hour, pk, filename, board = line.split(":")
        # Do we use this?
        if (source == "RANDOM") and ((date == "*" or date == current_date) and (hour == "*" or hour == current_hour)):
            source = "QUEUE"
            queue_data = {"pk":int(pk), "filename":filename, "board":int(board)}
        else: # if we don't use it, add it to the output text file
            output += line + "\n"
    print("---")

    # Write the new queue
    output = output[:-1]
    with open(QUEUE, "w") as fh:
        fh.write(output)

    print("SOURCE IS", source)
    print("DATA IS", queue_data)

    if source == "RANDOM":
        # Select a random zip
        # - Zip must have a ZZT World in it and be published
        # - Zip must not have modified graphics
        qs = File.objects.filter(details__in=[DETAIL_ZZT]).exclude(details__in=[DETAIL_UPLOADED, DETAIL_GFX]).order_by("?")

        # Filter out blacklisted files
        for file_obj in qs:
            data = file_obj
            if data.id not in BLACKLISTED_FILES:
                break

        # Pull related articles in preparation of linking them later
        related_articles = data.articles.filter(published=True).order_by("-date")

        # Select a random ZZT file in the zip
        zip = zipfile.ZipFile(ROOT + data.download_url())
        files = zip.namelist()
        files.sort()

        world_choices = []
        for file in files:
            filename = file.lower()
            if filename.endswith(".zzt"):
                world_choices.append(file)

        if not world_choices:
            abort("ERROR: World choices was empty for", file.id)

        selected = random.choice(world_choices)
        print(selected)

        # Extract it
        zip.extract(selected, CRON_ROOT)

        # Figure out if it's Title Screen Tuesday
        now = datetime.now()
        if int(now.strftime("%w")) == 2:
            tuesday = True
        else:
            tuesday = False

        # Parse the world with Zookeeper
        z = zookeeper.Zookeeper(os.path.join(CRON_ROOT, selected))

        # Select a random board (unless it's Tuesday)
        processing = True
        board_name = ""
        while processing:
            if tuesday:
                board_num = 0
                processing = False
            else:
                board_num = random.randint(0, len(z.boards) - 1)

            # Verify the board isn't a common toolkit
            if processing and z.boards[board_num].title in BOARD_TITLE_BLACKLIST:
                continue

            z.boards[board_num].screenshot(CRON_ROOT + "temp", title_screen=(board_num == 0), format="RGBA")
            board_name = z.boards[board_num].title
            processing = False
    elif source == "QUEUE":
        tuesday = False

        # Pull the zip
        data = File.objects.get(pk=queue_data["pk"])
        selected = queue_data["filename"]
        board_num = queue_data["board"]

        # Select the ZZT file in the zip
        zip = zipfile.ZipFile(ROOT + data.download_url())

        # Extract it
        zip.extract(queue_data["filename"], CRON_ROOT)

        # Parse the world with Zookeeper
        z = zookeeper.Zookeeper(os.path.join(CRON_ROOT, queue_data["filename"]))

        # Render
        z.boards[queue_data["board"]].screenshot(CRON_ROOT + "temp", title_screen=(queue_data["board"] == 0), format="RGBA", dark=APRIL)
        board_name = z.boards[queue_data["board"]].title

    # Remove the ZZT file. We're done with it.
    try:
        os.remove(os.path.join(CRON_ROOT, selected))
    except:
        abort("Couldn't remove:", selected)

    # Prepare the posts
    # Tumblr
    tumblr_post = "<b>{title}</b> by <i>{author}</i>"
    if data.release_date:
        tumblr_post += " ({year})"
    if data.company:
        tumblr_post += "<br>\nPublished by: {company}"
    tumblr_post += "<br>\n"
    tumblr_post += "[{zzt_file}] - {board_title}<br>\n"
    tumblr_post += "<a href='https://museumofzzt.com{file_url}"
    tumblr_post += "?file={zzt_file}&board={board_idx}'>Download / Explore {zip_file} "
    tumblr_post += "on the Museum of ZZT</a><br>\n"
    if data.archive_name:
        tumblr_post += "<a href='https://archive.org/details/{archive_name}'>Play on Archive.org</a><br>\n"

    tumblr_post = tumblr_post.format(
        title=data.title,
        author=data.author,
        year=str(data.release_date)[:4],
        company=data.company,
        zzt_file=selected,
        board_title=z.boards[board_num].title,
        file_url=data.file_url(),
        board_idx=board_num,
        zip_file=data.filename,
        archive_name=data.archive_name
    )

    # Tumblr - Related Articles
    if len(related_articles) > 0:
        article_text = "<br>"
        for article in related_articles[:3]:
            article_text += "<a href='https://museumofzzt.com{url}'>{text}</a><br>\n"
            article_text = article_text.format(
                url=article.url(),
                text=article.title
            )
        tumblr_post += article_text

    # Tumblr - Tags
    tags = ["ZZT", data.author, data.title, data.filename]

    if tuesday:
        tags.append("title screen tuesday")
    print(tumblr_post)

    client = pytumblr.TumblrRestClient(CONSUMER, SECRET, OAUTH_TOKEN, OAUTH_SECRET)

    if POST:
        print("Posting to tumblr...")
        print(tags)
        resp = client.create_photo("worldsofzzt", state="published", tags=tags, caption=tumblr_post, data=(CRON_ROOT + "temp.png"))
        print(resp)

        # Twitter
        twitter_post = "https://museumofzzt.com{file_url}"
        twitter_post += "?file={zzt_file}&board={board_idx}\n"
        twitter_post += "{title} by {author}"
        if data.release_date:
            twitter_post += " ({year})"
        if data.company:
            twitter_post += "\nPublished by: {company}"
        twitter_post += "\n[{zzt_file}] - \"{board_title}\""
        if data.archive_name:
            twitter_post += "\nhttps://archive.org/details/{archive_name}"

        twitter_post = twitter_post.format(
            file_url=data.file_url(),
            zzt_file=selected,
            board_idx=board_num,
            board_title=z.boards[board_num].title,
            title=data.title,
            author=data.author,
            year=str(data.release_date)[:4],
            company=data.company,
            archive_name=data.archive_name,
        )


        print(twitter_post)
        print("Posting to twitter...")

        # Fix the image
        orig = Image.open(CRON_ROOT + "temp.png")
        temp = orig.load()
        temp[0,0] = (temp[0,0][0], temp[0,0][1], temp[0,0][2], 254)
        orig.save(CRON_ROOT + "twitter.png")

        # April
        if APRIL:
            twitter_post = "Room is dark - you need to light a torch!\n" + twitter_post

        with open(CRON_ROOT + "twitter.png", "rb") as imagefile:
            imagedata = imagefile.read()

            t_up = Twitter(domain='upload.twitter.com', auth=OAuth(TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET))
            img1 = t_up.media.upload(media=imagedata)["media_id_string"]
            t = Twitter(auth=OAuth(TWITTER_OAUTH_TOKEN, TWITTER_OAUTH_SECRET, TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET))
            resp = t.statuses.update(status=twitter_post, media_ids=img1)
            print(resp)
            twitter_id = resp.get("id")
            twitter_img = resp["entities"]["media"][0]["media_url"]

        # Twitter - Related Articles
        if len(related_articles) > 0:
            article_text = "For more \"{title}\" content, check out:\n".format(title=data.title)
            for article in related_articles[:3]:
                article_text += "https://museumofzzt.com" + article.url() + "\n"

            resp = t.statuses.update(status=article_text, in_reply_to_status_id=twitter_id)

        # Discord webhook
        discord_post = "https://twitter.com/worldsofzzt/status/{}\n**{}** by {} ({})\n"
        if data.company:
            discord_post += "Published by: {}\n".format(data.company)
        discord_post += "`[{}] - \"{}\"` \n"
        discord_post += "Explore: https://museumofzzt.com" + data.file_url() + "?file=" + selected + "&board=" + str(board_num) + "\n"
        if data.archive_name:
            discord_post += "Play: https://archive.org/details/" + data.archive_name

        discord_post = discord_post.format(twitter_id, data.title, data.author, str(data.release_date)[:4], selected, z.boards[board_num].title)

        discord_data = {
            "content": discord_post,
            "embeds": [
                {"image": {"url": twitter_img}}
            ]
        }
        resp = requests.post(WEBHOOK_URL, headers={"Content-Type": "application/json"}, data=json.dumps(discord_data))
        print(resp)
        print(resp.content)

    else:
        print("DID NOT POST")

    return True

def abort(msg):
    print(msg)
    sys.exit()

if __name__ == "__main__":
    main()
