# vidscramble

Makes a new video by randomly chopping up your MP4 into 1-2 second bits. Great for creating quick video remixes or montages.

Setup:
`pip install moviepy`

Use it:
`python video_chopper.py input.mp4 output.mp4`

Want different clip lengths?
`python video_chopper.py input.mp4 output.mp4 --min-duration 0.5 --max-duration 1.5`

