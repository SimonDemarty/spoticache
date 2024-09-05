# spoticache

spotify musics downloader

# Set up

For this tool to work, you need to set up an app on the [Spotify Dashboard](https://developer.spotify.com/dashboard) :
1. Click on ```Create app```.
2. Complete the form (```Redirect Url``` should be set to ```http://localhost:8888/callback```) and tick the ```Web API``` option.

Then in the root of this repo, create a ```.env``` file according to this template:

```bash
SPOTIFY_CLIENT_ID = "YOUR CLIENT ID HERE"
SPOTIFY_CLIENT_SECRET = "YOUR CLIENT SECRET HERE"
SPOTIFY_REDIRECT_URI = "http://localhost:8888/callback"
```
Both the client id and the client secret can be found in the newly created spotify app.
