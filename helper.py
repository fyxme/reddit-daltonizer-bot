#!/usr/bin/env python
import os
import praw
import daltonizer
from imgurpython import ImgurClient

SECONDS_PER_MINUTE = 60

IMGUR_ALBUM_DESCRIPTIONS = dict(
    daltonized="Colors have been modified to enhance the image for colorblind users",
    simulated="Colors have been modified to simulate what colorblind users see")

def folder_exists(path):
    return os.path.isdir(path)

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)

def get_reddit_instance(reddit_credentials):
    return praw.Reddit(
        client_id=reddit_credentials["client_id"],
        client_secret=reddit_credentials["client_secret"],
        password=reddit_credentials["password"],
        username=reddit_credentials["username"],
        user_agent=reddit_credentials["user_agent"])

def get_imgur_instance(imgur_credentials):
    return ImgurClient(imgur_credentials["client_id"], 
                       imgur_credentials["client_secret"],
                       imgur_credentials["access_token"],
                       imgur_credentials["refresh_token"])

def print_skip(submission, reason):
    print "Skipping submission : [%s] %s" % (submission.id, reason)

def print_valid(submission):
    print "> Valid submission : [%s] %s" % (submission.id, submission.url)

def get_imgur_album_link(album_id):
    return "https://imgur.com/a/%s" % album_id

def get_formated_links(name, converted_imgs):
    temp = ""
    for col in converted_imgs[name]:
        temp += " [%s](%s) |" % (daltonizer.deficit_to_fullname(col), 
                                 converted_imgs[name][col]["link"])
    return temp[1:-1]

def get_reply_message(converted_imgs,imgur_albums):
    return "\n\n".join((
        " | ".join((
            "**[Colorblind Enhanced Images](%s)**" % imgur_albums["daltonized"],
            "**[What colorblind users see](%s)**" % imgur_albums["simulated"])),
        "----",
        "^( | )".join((
            "^(*I adjust colors of an image submission to accomodate users with colorblindness*)",
            "[^Contact](https://www.reddit.com/message/compose/?to=daltonicbot)",
            "[^FAQ](https://www.reddit.com/user/DaltonicBot/comments/6v1omy/faq/)",
            "^v%s" % BOT_VERSION))))

def get_long_reply_message(converted_imgs):
    return "\n\n".join((
        "**Colorblind Enhanced Images:**",
        helper.get_formated_links("daltonized",converted_imgs),
        "----",
        "**What Colour-blind Users See:**",
        helper.get_formated_links("simulated",converted_imgs),
        "----",
        "^( | )".join(
            "*I'm a bot that adjusts the colors of an image post to accommodate redditors with color blindness*",
            "[^Contact](https://www.reddit.com/message/compose/?to=daltonicbot)",
            "[^FAQ](https://www.reddit.com/user/DaltonicBot/comments/6v1omy/faq/)",
            "v%s" % BOT_VERSION)))

def get_converted_img_ids(converted_imgs, cvd_type):
    return [converted_imgs[cvd_type][color_deficit]["link"][19:-4] for color_deficit in converted_imgs[cvd_type]]

def generate_imgur_description(submission, cvd_type):
    return "\n".join((
        IMGUR_ALBUM_DESCRIPTIONS[cvd_type],
        "Original post by /u/%s" % submission.author,
        "Link to post : https://www.reddit.com/%s" % submission.id))

def get_image_title(sim_or_dalt, color_deficit):
    return "%s Image - %s" % (sim_or_dalt.title(), 
                      daltonizer.COLOR_DEFICITS[color_deficit].title())

def difference_between_images(img1_path,img2_path):
    """
        Returns the percentage difference between 2 images
    """
    i1 = Image.open(img1_path)
    i2 = Image.open(img2_path)

    pairs = izip(i1.getdata(), i2.getdata())

    if len(i1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1-p2) for p1,p2 in pairs)
    else:
        dif = sum(abs(c1-c2) for p1,p2 in pairs for c1,c2 in zip(p1,p2))
     
    ncomponents = i1.size[0] * i1.size[1] * 3
    return (dif / 255.0 * 100) / ncomponents
