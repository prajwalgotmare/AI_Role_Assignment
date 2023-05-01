# Project Description

I have referred this file to complete this project: https://docs.google.com/document/d/1APypjaN3nmU1Pey_dxJcfPkQHqdOERwLzO02N0BXiIE/edit

This project involves taking an input video file of a task (regarding ball detection) solved using OpenCV in Python and generating an output video file that incorporates ball tracking with color, overlay text “Entry or Exit” & timestamp at the time of entry/exit of a numbered quadrant, and a text file with records in the format provided above (Time, Quadrant Number, Ball Colour, Event Type (Entry or Exit)).

<div align="center">
<img src="https://i.imgur.com/oCZ9bxN.png" width="400">
</div>

## Video Conversion

The provided input video was labeled as "AI Assignment video" and had a variable frame rate mode of 30.043 fps as found in the metadata of the video. Therefore, the video was first converted to a constant frame rate mode with a dimension of 1280 * 720 and fps = 30. I have used OpenShot video editor to convert "Ai assignment video.mp4" to a video named as "original formatted.mp4". (For more file comparison, you can check Videos_Metadata_comparison.txt above)

All the media files related to this project can be found on this link:

https://drive.google.com/drive/folders/18ABPey2TltEyoVhKjKlyxEbJIULpW3vW?usp=share_link

## Code Execution

The code can be executed in the Jupyter notebook named "ROI_Coordinates_and_color_ranges.ipynb". Before executing the code, ensure that the required text file named "Ball_info.txt" is saved in the local folder.

## Files Included

The following files are included in the repository:

0. ROI_Coordinates_and_color_ranges.ipynb
1. Videos_Metadata_comparison.txt
2. Ball_info.txt
3. README.md

## Requirements

The following requirements were used for this project:

- Python version: 3.10.9 (tags/v3.10.9:1dd9be6, Dec 6 2022, 20:01:21) [MSC v.1934 64 bit (AMD64)]
- OpenCV version: 4.7.0
- imutils version: 0.5.4
- pandas version: 2.0.1
