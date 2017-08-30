# RedditDaltonizerBot
The Reddit Daltonizer Bot ([/u/DaltonicBot](https://www.reddit.com/user/DaltonicBot)) aims to help Colorblind reddit users by providing them with color enhanced images.


## How does it work?
1. The bot gets mentionned by a redditor on a post __This is to reduce spam__
2. It check if the summon is valid and ignores the invalid ones
    - The mention must be a top level comment (a direct reply to the submission)
    - The submission must be an image
    - This is the first time it has been mentionned in this post
3. It stores the image's data
4. It converts the image's colors to enhance it for colorblind users and simulate what colorblinds see
5. It uploads all the converted images to imgur
6. To reduce spam and minize the size of it's comments, it then creates two imgur albums (Enhanced images, Simulated images) and replies with direct links to both


### Upcoming changes & improvements
- **To reduce spam:**
    - Calculate the percentage difference between images to see if a conversion is required

- **To improve code performance & readability:**
    - Refactor `bot.process_submission()` method
    - Account for API Exceptions for both reddit and Imgur

- **To improve it's capabilities:**
    - Allow for multiple images
    - Add commands:
        - Simulated Images only
        - Enhanced Images only
        - Long reply mode (direct links to images), check `helpers.get_long_reply_message()` for more info
            - Add album link in superscript too
    - Attempt (*if possible*) to improve transformation matrices using machine learning and a user voting system (**long term goal**)
        - colors
        - color saturation
        - brightness

## Requirements

- PRAW
- imgurpython
- Pillow
- numpy

*Run `setup.sh` to install all the requirements*


## Contribution

*The bot is still in development and the code that powers it may be sloppy, undocumented and inefficient.*

**You are more than welcome to open issues and to contribute to the bot if you wish**


## Credits
- Credit to [/u/ghostfivenine](https://www.reddit.com/u/ghostfivenine) for the [idea](https://www.reddit.com/r/RequestABot/comments/6tvpvq/request_a_bot_that_adjusts_the_colors_of_an_image/)
- Credit to [/u/vortigernup](https://www.reddit.com/user/vortigernup) for many improvement suggestions
- Special thanks to the [/r/colorblind](reddit.com/r/colorBlind/) community for helping test this bot
