#!/usr/bin/env python

import time
import credentials
from daltonize import DaltonizableImageFromURL
from helpers import helper, imgur_helper
from praw.models import Comment
import StringIO

import collections

BOT_VERSION = "0.3.6"

SUBREDDITS = ["colorblind","test"]

SECONDS_PER_MIN = 60

# Number of times per minute to run
RUN_EVERY_X = 5

COLOR_DEFICITS = collections.OrderedDict([
    ("d", "deuteranopia"),
    ("p", "protanopia"),
    ("t", "tritanopia"),
    ("m", "monochromacy")])

def log(line):
    # append to file
    with open('out.log','a') as out:
        out.write(line)

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
        log(key)
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

            log(" Type [%s] - Uploaded imgur : %s" % (cvd_type,
            uploaded_imgs[key][cvd_type]["link"]))

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

    return (helper.get_reply_message(
            {"simulated":imgur_helper.get_imgur_album_link(
                imgur_albums["simulated"]["id"]),
            "daltonized":imgur_helper.get_imgur_album_link(
                imgur_albums["daltonized"]["id"])},
            BOT_VERSION))

def is_valid_mention(mention):
    return isinstance(mention, Comment) and mention.new and mention.is_root

def is_valid_submission(submission):
    return (not submission.saved
            and hasattr(submission, "post_hint")
            and submission.post_hint == "image")

def daltonize_submission(reddit, imgur, submission, replyable=None):
    if not replyable:
        replyable = submission

    log("Processing submssion [id : {}]".format(submission.id))
    reply_msg = process_submission(reddit, imgur, submission)
    replyable.reply(reply_msg)
    submission.save()

def check_mentions(reddit, imgur):
    valid_mentions = [mention for mention in reddit.inbox.mentions() if is_valid_mention(mention)]

    for valid_mention in valid_mentions:
        submission = valid_mention.submission
        # check if the submission is an image
        # and that we haven't replied to it yet
        if is_valid_submission(submission):
            daltonize_submission(
                reddit,
                imgur,
                submission,
                replyable=valid_mention)

    # mark all new mentions as red
    if valid_mentions:
        reddit.inbox.mark_read(valid_mentions)

def check_submissions(reddit, imgur, subs, start_time):
    for submission in reddit.subreddit("+".join(subs)).new():
        if (submission.created_utc > start_time
            and is_valid_submission(submission)):
            daltonize_submission(reddit, imgur, submission)

def main():
    reddit = helper.get_reddit_instance(credentials.reddit)
    imgur = imgur_helper.get_imgur_instance(credentials.imgur)
    start_time = time.time()

    while True:
        # current number of minutes the program has been running
        current_mins = (time.time() - start_time) // 60
        log("[Elapsed minutes : {}]".format(current_mins))

        # Check for mentions every minute
        log("Checking mentions")
        check_mentions(reddit, imgur)

        # run once every x minutes
        if current_mins % RUN_EVERY_X == 0:
            try:
                # Check for submission every X minutes
                log("Checking submissions")
                check_submissions(reddit, imgur, SUBREDDITS, start_time)
            except KeyboardInterrupt:
                raise
            except Exception, e:
                log(str(e))

        log("Sleeping {} seconds".format(SECONDS_PER_MIN))
        time.sleep(SECONDS_PER_MIN)

if __name__ == '__main__':
    main()
