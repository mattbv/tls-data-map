# Include the Dropbox SDK
import dropbox

# Get your app key and secret from the Dropbox developer website
app_key = '3b6azqp69c222jt'
app_secret = '3cnzz2uq6vjzh9x'

flow = dropbox.DropboxOAuth2FlowNoRedirect(app_key, app_secret)

# Have the user sign in and authorize this token
authorize_url = flow.start()
print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'
code = raw_input("Enter the authorization code here: ").strip()

# This will fail if the user enters an invalid authorization code
access_token, user_id = flow.finish(code)

client = dropbox.client.DropboxClient(access_token)
print 'linked account: ', client.account_info()

#f = open('working-draft.txt', 'rb')
#response = client.put_file('/magnum-opus.txt', f)
#print 'uploaded: ', response
#
#folder_metadata = client.metadata('/')
#print 'metadata: ', folder_metadata
#
#f, metadata = client.get_file_and_metadata('/magnum-opus.txt')
#out = open('magnum-opus.txt', 'wb')
#out.write(f.read())
#out.close()
#print metadata