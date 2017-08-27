from imgurpython import ImgurClient
import base64

IMGUR_ALBUM_DESCRIPTIONS = dict(
    daltonized="Colors have been modified to enhance the originalimage" 
               " for colorblind users",
    simulated="Colors have been modified to simulate what colorblind users see")

def get_imgur_instance(imgur_credentials):
    return ImgurClient(imgur_credentials["client_id"], 
                       imgur_credentials["client_secret"],
                       imgur_credentials["access_token"],
                       imgur_credentials["refresh_token"])

def get_imgur_album_link(album_id):
    return "https://imgur.com/a/%s" % album_id

def generate_imgur_album_title(sim_or_dalt):
    if sim_or_dalt == "daltonized":
        return "Colorblind Enhanced Images"
    return "What Colour-blind Users See"

def generate_imgur_description(submission, cvd_type):
    return "\n".join((
        IMGUR_ALBUM_DESCRIPTIONS[cvd_type],
        "Original post by /u/%s" % submission.author,
        "Link to post : https://www.reddit.com/%s" % submission.id))

def get_image_title(sim_or_dalt, color_deficit):
    return "%s Image - %s" % (sim_or_dalt.title(), 
                              color_deficit.title())


def upload(imgur, temp_buffer, config=None, anon=True):
    contents = temp_buffer.getvalue()
    b64 = base64.b64encode(contents)
    data = {
        'image': b64,
        'type': 'base64',
    }
    data.update({meta: config[meta] for meta in set(imgur.allowed_image_fields).intersection(config.keys())})

    return imgur.make_request('POST', 'upload', data, anon)