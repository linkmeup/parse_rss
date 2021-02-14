This set of scripts allows you to render podcast episode and upload it to YouTube in Private mode.

The next steps are performed to do the task:
- Parse [linkmeup RSS](https://linkmeup.ru/rss/podcasts)
- Download media files, like mp3 and img
- Generates episode cover
- Add Recording Dates and desired Publication Dates
- Render video for episode by ffmpeg
- Upload this video to yourube channel in Private mode and add it to proper Playlist


Run the scripts in the following sequence:
- `get_podcasts.py`. Result will be saved to *all_podcasts.json*.
- `download_files.py`. Result will be saved to *all_podcasts_w_files.json*.
- `gen_cover.py`. Result will be saved to *all_podcasts_w_covers.json*.
- `render_video_norm.py`. Result will be saved to *all_podcasts_w_mp4.json*.
- `get_pub_dates.py`. Result will be saved to *all_podcasts_w_pd.json*.
- `upload_videos.py`. Result will be saved to *all_podcasts_w_ytid.json*.

You also can run `check_files.py` with filename and item to check as arguments to check if all the files exist.  
For example. 
`./check_files.py all_podcasts_w_files.json img` will check if key 'img' exists for each podcast episode, if there is file named after 'img' and what is filesize.

To bring the environment please install poetry and run `poetry install`. Than you can run scripts inside virtual env: `poetry run python get_podcasts.py`.

To be able to upload vidoes to YouTube via YouTube developer API you need to download *client_secret.json* from you google account.