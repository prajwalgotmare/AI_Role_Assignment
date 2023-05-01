# Project Description

I have referred this file to complete this project: https://docs.google.com/document/d/1APypjaN3nmU1Pey_dxJcfPkQHqdOERwLzO02N0BXiIE/edit

This project involves taking an input video file in mp4 format and performing computer vision techniques which will result in generating an output video file that incorporates ball tracking with color, overlay text “Entry or Exit” & timestamp at the time of entry/exit of a numbered quadrant, and a text file with records in the format as requested (Time, Quadrant Number, Ball Colour, Event Type (Entry or Exit)).

<div align="center">
<img src="https://i.imgur.com/oCZ9bxN.png" width="400">
</div>

## Video Conversion

The provided input video was labeled as "AI Assignment video" and had a variable frame rate mode of 30.043 fps as found in the metadata of the video. Therefore, the video was first converted to a constant frame rate mode with a dimension of width = 1280 , height = 720 and 30 fps. I have used OpenShot video editor to convert "Ai assignment video.mp4" to the required video format labeled as "original formatted.mp4" to acheive best results (For more file comparison, you can check Videos_Metadata_comparison.txt above - To check difference between AI Assignment video.mp4 and original formatted.mp4 )

## Code Execution

To determine the region of interest coordinates and color ranges, I utilized the Jupyter notebook "ROI_Coordinates_and_color_ranges.ipynb". Then, I incorporated the identified region of interest coordinates and color ranges into a Python file named "main.py". Before executing the code, I have set the input file path as "original formated.mp4" and the output file path as "processed_video.mp4" which must be present in local folder which you can get from below media files link.

All the media files related to this project can be found on this link:

https://drive.google.com/drive/folders/18ABPey2TltEyoVhKjKlyxEbJIULpW3vW?usp=share_link

## Files Included

The following files are included in the repository:

0. ROI_Coordinates_and_color_ranges.ipynb
1. Videos_Metadata_comparison.txt
2. Ball_info.txt
3. README.md
4. main.py

## Requirements

The following requirements were used for this project:

- Python version: 3.10.9 
- OpenCV version: 4.7.0
- imutils version: 0.5.4
- pandas version: 2.0.1
