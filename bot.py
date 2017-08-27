#!/usr/bin/env python

import time
import credentials
from daltonize import DaltonizableImageFromURL
from helpers import helper, imgur_helper
import StringIO

import collections

BOT_VERSION = "0.3.3"

SUBREDDITS = ["colorblind", "test"]

COLOR_DEFICITS = collections.OrderedDict([
    ("d", "deuteranopia"),
    ("p", "protanopia"),
    ("t", "tritanopia"),
    ("m", "monochromacy")])

def process_submission(reddit, imgur, submission):
    folder_path = "img/%s" % submission.id

    img = DaltonizableImageFromURL(submission.url)

    converted_imgs = dict(
        daltonized=img.daltonize("dpt"),
        simulated=img.simulate("dptm"))

    uploaded_imgs = dict(
        daltonized=dict(),
        simulated=dict())

    for key in converted_imgs:
        print key
        for converted_img in converted_imgs[key]:
            cvd_type = converted_img.color_deficit

            # open temp file object
            temp = StringIO.StringIO()

            # save img to temp file object
            converted_img.save(temp, format="jpeg")
        
            # upload to imgur
            uploaded_imgs[key][cvd_type] = imgur_helper.upload(
                imgur,
                temp,
                config={"title":imgur_helper.get_image_title(
                    key,
                    COLOR_DEFICITS[cvd_type])},
                anon=False)

            print " Type [%s] - Uploaded imgur : %s" % (cvd_type, 
            uploaded_imgs[key][cvd_type]["link"])

            temp.close()

    imgur_albums = dict()

    # Create 2 albums (simulated, daltonised) with all the images
    for key in uploaded_imgs:
        temp_imgs = uploaded_imgs[key]

        # list of imgur image ids for converted "key"
        conv_img_ids = [temp_imgs[cvd_type]["id"] 
            for cvd_type in COLOR_DEFICITS.keys() 
            if cvd_type in temp_imgs]

        # create album with images
        imgur_albums[key] = imgur.create_album({
            "ids":",".join(conv_img_ids),
            "title":imgur_helper.generate_imgur_album_title(key),
            "description":
                imgur_helper.generate_imgur_description(
                    submission, 
                    key)})

    submission.reply(
        helper.get_reply_message({
            "simulated":imgur_helper.get_imgur_album_link(
                imgur_albums["simulated"]["id"]),
            "daltonized":imgur_helper.get_imgur_album_link(
                imgur_albums["daltonized"]["id"])},
            BOT_VERSION))

def test():
    reddit = helper.get_reddit_instance(credentials.reddit)
    imgur = imgur_helper.get_imgur_instance(credentials.imgur)

    submission_id = "6waxn2"

    submission = reddit.submission(submission_id)

    print "Testing submission : %s" % submission.shortlink

    process_submission(reddit, imgur, submission)


def main():
    started_at = time.time()
    reddit = helper.get_reddit_instance(credentials.reddit)
    imgur = imgur_helper.get_imgur_instance(credentials.imgur)

    for submission in reddit.subreddit("+".join(SUBREDDITS)).stream.submissions():
        if submission.created_utc < started_at:
            continue

        if (hasattr(submission, "post_hint") 
            and submission.post_hint == "image"):
            process_submission(reddit, imgur, submission)


if __name__ == '__main__':
    main()