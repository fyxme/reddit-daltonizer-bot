#!/usr/bin/env python

import time
import credentials
import daltonizer
import helper

BOT_VERSION = "0.3.1"

SUBREDDITS = ["colorblind", "test"]
BANNED_FROM_SUBS = ["pics", "pic"]

def process_submission(reddit, imgur, submission):
    folder_path = "img/%s" % submission.id

    img = daltonizer.Img(submission.id, submission.url, folder_path)

    img.daltonize()
    img.save_converted()

    converted_imgs = img.get_converted_paths()

    # Upload images to imgur
    for clv_type in converted_imgs:
        print clv_type
        for col_def in converted_imgs[clv_type]:
            to_up = "%s/%s" % (folder_path, 
                               converted_imgs[clv_type][col_def])
            
            converted_imgs[clv_type][col_def] = (
                imgur.upload_from_path(to_up, 
                    config={"title":helper.get_image_title(clv_type, col_def)},
                    anon=False))

            print " Type [%s] - Uploaded imgur : %s" % (col_def, 
                converted_imgs[clv_type][col_def]["link"])

    # Create 2 albums (simulated, daltonised) with all the images
    conv_dalt_img_ids = helper.get_converted_img_ids(converted_imgs, "daltonized")
    daltonized_album = imgur.create_album({
        "ids":",".join(conv_dalt_img_ids),
        "title":"Colorblind Enhanced Images",
        "description":helper.generate_imgur_description(submission, "daltonized")})

    conv_sim_img_ids = helper.get_converted_img_ids(converted_imgs, "simulated")
    simulated_album = imgur.create_album({
        "ids":",".join(conv_sim_img_ids),
        "title":"What Colour-blind Users See",
        "description":helper.generate_imgur_description(submission, "simulated")})
                    
    submission.reply(helper.get_reply_message(converted_imgs,{
        "simulated":helper.get_imgur_album_link(simulated_album["id"]),
        "daltonized":helper.get_imgur_album_link(daltonized_album["id"])}))
        

def hot_submissions_only(reddit, imgur, started_at, limit=25):
    for submission in reddit.subreddit("+".join(SUBREDDITS)).hot(limit=limit):
        if submission.created_utc < started_at:
            helper.print_skip(submission, "Old submission")
            continue

        if helper.folder_exists(folder_path):
            helper.print_skip(submission, "Already daltonised")
        elif not hasattr(submission, "post_hint") or submission.post_hint != "image":
            helper.print_skip(submission, "Not an image post")
        else:
            helper.print_valid(submission)

            # submission is valid process it
            process_submission(reddit, imgur, submission) 

def test_process(reddit, imgur):
    submission_id = "6waxn2"

    submission = reddit.submission(submission_id)

    print "Testing submission : %s" % submission.shortlink

    process_submission(reddit, imgur, submission)

def main():
    started_at = time.time()
    reddit = helper.get_reddit_instance(credentials.reddit)
    imgur = helper.get_imgur_instance(credentials.imgur)

    count = interval = 1

    test_process(reddit, imgur)

    exit()

    while True:
        hot_submissions_only(reddit, imgur, started_at, 50)

        print "%s minutes since start - sleep(%s)" % (
            count,
            helper.SECONDS_PER_MINUTE * interval)

        time.sleep(helper.SECONDS_PER_MINUTE * interval)
        count += 1

if __name__ == '__main__':
    main()


