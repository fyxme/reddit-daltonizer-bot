from imgurpython import ImgurClient
import webbrowser

imgur = dict(
    client_id="431d34de20a1576",
    client_secret="b6937c456003a82c90501b756f7b91187f9bf7e9")

client = ImgurClient(imgur['client_id'], imgur['client_secret'])

# Authorization flow, pin example (see docs for other auth types)
authorization_url = client.get_auth_url('pin')

print authorization_url
webbrowser.open(authorization_url)

pin = raw_input("Enter pin : ")

credentials = client.authorize(pin, "pin")
client.set_user_auth(credentials['access_token'], credentials['refresh_token'])

print credentials