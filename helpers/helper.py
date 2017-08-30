#!/usr/bin/env python
import os
import praw
import collections

def get_reddit_instance(reddit_credentials):
    return praw.Reddit(
        client_id=reddit_credentials["client_id"],
        client_secret=reddit_credentials["client_secret"],
        password=reddit_credentials["password"],
        username=reddit_credentials["username"],
        user_agent=reddit_credentials["user_agent"])

def _get_formated_links(name, converted_imgs):
    temp = ""
    for col in converted_imgs[name]:
        temp += " [%s](%s) |" % (daltonizer.deficit_to_fullname(col),
                                 converted_imgs[name][col]["link"])
    return temp[1:-1]

def _get_reply_footer(version):
    return "^( | )".join((
            "^(*Helping redditors with colorblindness*)",
            "[^Contact](https://www.reddit.com/message/compose/?to=offdutyhuman)",
            "[^FAQ](https://www.reddit.com/user/DaltonicBot/comments/6v1omy/faq/)",
            "[^Source](https://github.com/hexagonist/RedditDaltonizerBot)",
            "^v%s" % version))

def get_reply_message(imgur_album_links,version):
    return "\n\n".join((
        " | ".join((
            "**[Colorblind Enhanced Images](%s)**" % imgur_album_links["daltonized"],
            "**[What colorblind users see](%s)**" % imgur_album_links["simulated"])),
        "----",
        _get_reply_footer(version)))

def get_long_reply_message(converted_imgs, version):
    return "\n\n".join((
        "**Colorblind Enhanced Images:**",
        helper._get_formated_links("daltonized",converted_imgs),
        "----",
        "**What Colour-blind Users See:**",
        helper._get_formated_links("simulated",converted_imgs),
        "----",
        _get_reply_footer(version)))

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
