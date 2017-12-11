# Copy this file to config.py
INSTA_APP_ID = 'YOUR INSTAGRAM APP ID'
INSTA_APP_SECRET = 'YOUR INSTAGRAM APP SECRET'
CLARIFAI_APP_ID = 'CLARIFAI APP ID'
REDIRECT_URI = "REDIRECT URL REGISTERED WITH INSTA"
URL = "https://api.instagram.com/oauth/authorize/?client_id={0}&redirect_uri={1}&response_type=code".format(INSTA_APP_ID, REDIRECT_URI)
MEDIA_URL = "https://api.instagram.com/v1/users/self/media/recent/?access_token={0}&count=19"
