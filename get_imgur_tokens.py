from imgurpython import ImgurClient
import webbrowser
import credentials

client = ImgurClient(credentials.imgur['client_id'], credentials.imgur['client_secret'])

# Authorization flow, pin example (see docs for other auth types)
authorization_url = client.get_auth_url('pin')

print authorization_url
webbrowser.open(authorization_url)

pin = raw_input("Enter pin : ")

credentials = client.authorize(pin, "pin")

print "Imgur Access token : %s" % credentials["access_token"]
print "Imgur Refresh token : %s" % credentials["refresh_token"]