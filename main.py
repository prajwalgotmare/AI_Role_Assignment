import cv2
import imutils
import time
from tqdm import tqdm
import pandas as pd
import os
from datetime import datetime, timedelta

# Set the input file path and output file path (original formatted.mp4 must be in local folder)
Input_file = "original formatted.mp4"
Output_file = "processed_video.mp4"

# Define the lower and upper bounds for the colors you want to detect
yellowLower = (20, 100, 100)
yellowUpper = (30, 255, 255)
redOrangeLower = (0, 100, 160)
redOrangeUpper = (10, 255, 255)
blueLower = (55, 55, 20)
blueUpper = (95, 100, 100)
whiteLower = (18, 15, 170)
whiteUpper = (180, 25, 245)

# Define the ROI for each quadrant
roi = {
    '1': [835, 360, 350, 320],
    '2': [500, 360, 320, 320],
    '3': [480, 10, 320, 360],
    '4': [840, 0, 345, 360],
}

# Open the video file
vs = cv2.VideoCapture(Input_file)
time.sleep(2.0)

# Create an empty dataframe with the desired columns
df = pd.DataFrame(columns=['Time', 'Quadrant Number', 'Ball Colour', 'Type'])

total_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(vs.get(cv2.CAP_PROP_FPS))

print(f"Total frames: {total_frames}")

with open('yellow.txt', 'w') as yellow_file:
    yellow_file.write('Frame_number,Time,Quadrant Number,Ball Colour\n') # Add first row to the file

with open('red-orange.txt', 'w') as red_orange_file:
    red_orange_file.write('Frame_number,Time,Quadrant Number,Ball Colour\n') # Add first row to the file

with open('blue.txt', 'w') as blue_file:
    blue_file.write('Frame_number,Time,Quadrant Number,Ball Colour\n') # Add first row to the file

with open('white.txt', 'w') as white_file:
    white_file.write('Frame_number,Time,Quadrant Number,Ball Colour\n') # Add first row to the file

for i in tqdm(range(0, total_frames, fps)):
    vs.set(cv2.CAP_PROP_POS_FRAMES, i)
    ret, frame = vs.read()

    if not ret:
        break
    # Get the current time in the format mm:ss.ss from the start of video

    current_time = time.strftime('%M:%S', time.gmtime(i / fps)) + '.' + str(i % fps).zfill(2)
    
    # Apply Gaussian blur to the frame
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    # Threshold the image for yellow color only
    yellowMask = cv2.inRange(hsv, yellowLower, yellowUpper)

    # Perform morphological operations to clean up the thresholded image
    yellowMask = cv2.erode(yellowMask, None, iterations=2)
    yellowMask = cv2.dilate(yellowMask, None, iterations=2)

    # Find contours in the thresholded image
    yellowCnts = cv2.findContours(yellowMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellowCnts = imutils.grab_contours(yellowCnts)
    
    for c in yellowCnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 10:
            # Check which quadrant the ball is in
            quadrant = None
            for key, value in roi.items():
                if x > value[0] and x < value[0] + value[2] and y > value[1] and y < value[1] + value[3]:
                    quadrant = key
                    break
            if quadrant is not None:

                with open('yellow.txt', 'a') as file:
                    file.write(f"{i},{current_time}, {quadrant},yellow\n")

    # Threshold the image for red-orange color only
    redOrangeMask = cv2.inRange(hsv, redOrangeLower, redOrangeUpper)

    # Perform morphological operations to clean up the thresholded image
    redOrangeMask = cv2.erode(redOrangeMask, None, iterations=2)
    redOrangeMask = cv2.dilate(redOrangeMask, None, iterations=2)

    # Find contours in the thresholded image
    redOrangeCnts = cv2.findContours(redOrangeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    redOrangeCnts = imutils.grab_contours(redOrangeCnts)
    
    for c in redOrangeCnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 10:
            # Check which quadrant the ball is in
            quadrant = None
            for key, value in roi.items():
                if x > value[0] and x < value[0] + value[2] and y > value[1] and y < value[1] + value[3]:
                    quadrant = key
                    break
            if quadrant is not None:
                with open('red-orange.txt', 'a') as red_orange_file:
                    red_orange_file.write(f"{i},{current_time}, {quadrant},red-orange\n")

    # Threshold the image for blue color only
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)

    # Perform morphological operations to clean up the thresholded image
    blueMask = cv2.erode(blueMask, None, iterations=2)
    blueMask = cv2.dilate(blueMask, None, iterations=2)

    # Find contours in the thresholded image
    blueCnts = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blueCnts = imutils.grab_contours(blueCnts)

    for c in blueCnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 25:
            # Check which quadrant the ball is in
            quadrant = None
            for key, value in roi.items():
                if x > value[0] and x < value[0] + value[2] and y > value[1] and y < value[1] + value[3]:
                    quadrant = key
                    break
            if quadrant is not None:
                with open('blue.txt', 'a') as blue_file:
                    blue_file.write(f"{i},{current_time}, {quadrant},blue\n")

    # Threshold the image for white color only
    whiteMask = cv2.inRange(hsv, whiteLower, whiteUpper)

    # Perform morphological operations to clean up the thresholded image
    whiteMask = cv2.erode(whiteMask, None, iterations=2)
    whiteMask = cv2.dilate(whiteMask, None, iterations=2)

    # Find contours in the thresholded image
    whiteCnts = cv2.findContours(whiteMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    whiteCnts = imutils.grab_contours(whiteCnts)
    
    for c in whiteCnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 30:
            # Check which quadrant the ball is in
            quadrant = None
            for key, value in roi.items():
                if x > value[0] and x < value[0] + value[2] and y > value[1] and y < value[1] + value[3]:
                    quadrant = key
                    break
            if quadrant is not None:

                with open('white.txt', 'a') as file:
                    file.write(f"{i},{current_time}, {quadrant},white\n")

    # out.write(frame) 

vs.release()

# read in all three text files
df_yellow = pd.read_csv('yellow.txt', header=0)
df_red_orange = pd.read_csv('red-orange.txt', header=0)
df_blue = pd.read_csv('blue.txt', header=0)
df_white = pd.read_csv('white.txt', header=0)

# create multiple dataframes based on quadrant number for each color
df_dict_yellow = {}
for quadrant in df_yellow['Quadrant Number'].unique():
    indices = df_yellow.index[df_yellow['Quadrant Number'] == quadrant].tolist()
    dfs = []
    temp = [indices[0]]
    for i in range(1, len(indices)):
        if indices[i] == indices[i-1]+1:
            temp.append(indices[i])
        else:
            dfs.append(df_yellow.iloc[temp].copy())
            temp = [indices[i]]
    dfs.append(df_yellow.iloc[temp].copy())
    df_dict_yellow[quadrant] = dfs

df_dict_red_orange = {}
for quadrant in df_red_orange['Quadrant Number'].unique():
    indices = df_red_orange.index[df_red_orange['Quadrant Number'] == quadrant].tolist()
    dfs = []
    temp = [indices[0]]
    for i in range(1, len(indices)):
        if indices[i] == indices[i-1]+1:
            temp.append(indices[i])
        else:
            dfs.append(df_red_orange.iloc[temp].copy())
            temp = [indices[i]]
    dfs.append(df_red_orange.iloc[temp].copy())
    df_dict_red_orange[quadrant] = dfs

df_dict_blue = {}
for quadrant in df_blue['Quadrant Number'].unique():
    indices = df_blue.index[df_blue['Quadrant Number'] == quadrant].tolist()
    dfs = []
    temp = [indices[0]]
    for i in range(1, len(indices)):
        if indices[i] == indices[i-1]+1:
            temp.append(indices[i])
        else:
            dfs.append(df_blue.iloc[temp].copy())
            temp = [indices[i]]
    dfs.append(df_blue.iloc[temp].copy())
    df_dict_blue[quadrant] = dfs

df_dict_white = {}
for quadrant in df_white['Quadrant Number'].unique():
    indices = df_white.index[df_white['Quadrant Number'] == quadrant].tolist()
    dfs = []
    temp = [indices[0]]
    for i in range(1, len(indices)):
        if indices[i] == indices[i-1]+1:
            temp.append(indices[i])
        else:
            dfs.append(df_white.iloc[temp].copy())
            temp = [indices[i]]
    dfs.append(df_white.iloc[temp].copy())
    df_dict_white[quadrant] = dfs

# create an empty list to store the dataframes
dfs = []
# loop through the dataframes in df_dict_yellow
for key in df_dict_yellow:
    for df in df_dict_yellow[key]:
        if len(df) == 1:
            df['Type'] = 'Entry'
        else:
            df.loc[df.index[0], 'Type'] = 'Entry'
            df.loc[df.index[-1], 'Type'] = 'Exit'
            new_df = pd.concat([df.iloc[[0]], df.iloc[[-1]]])
            new_df = new_df.sort_values(by=['Time'])
            dfs.append(new_df)
# loop through the dataframes in df_dict_red_orange
for key in df_dict_red_orange:
    for df in df_dict_red_orange[key]:
        if len(df) == 1:
            df['Type'] = 'Entry'
        else:
            df.loc[df.index[0], 'Type'] = 'Entry'
            df.loc[df.index[-1], 'Type'] = 'Exit'
            new_df = pd.concat([df.iloc[[0]], df.iloc[[-1]]])
            new_df = new_df.sort_values(by=['Time'])
            dfs.append(new_df)
# loop through the dataframes in df_dict_blue
for key in df_dict_blue:
    for df in df_dict_blue[key]:
        if len(df) == 1:
            df['Type'] = 'Entry'
        else:
            df.loc[df.index[0], 'Type'] = 'Entry'
            df.loc[df.index[-1], 'Type'] = 'Exit'
            new_df = pd.concat([df.iloc[[0]], df.iloc[[-1]]])
            new_df = new_df.sort_values(by=['Time'])
            dfs.append(new_df)

# loop through the dataframes in df_dict_blue
for key in df_dict_white:
    for df in df_dict_white[key]:
        if len(df) == 1:
            df['Type'] = 'Entry'
        else:
            df.loc[df.index[0], 'Type'] = 'Entry'
            df.loc[df.index[-1], 'Type'] = 'Exit'
            new_df = pd.concat([df.iloc[[0]], df.iloc[[-1]]])
            new_df = new_df.sort_values(by=['Time'])
            dfs.append(new_df)

# concatenate all the dataframes in the list

final_df = pd.concat(dfs)
# sort the rows by the 2nd column
final_df = final_df.sort_values(by=final_df.columns[1])

# reset the index to make it serial
final_df = final_df.reset_index(drop=True)

# print(final_df.head(10))

# Create a new text file with column names and file name as final.txt
final_df.to_csv('final.txt', sep=',', index=False)

# Create a new text file with column names and file name as final.txt
print("--------------------------------------------------------")

# Load video file
cap = cv2.VideoCapture(Input_file)

# Get total number of frames in the video
num_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

# Get frames per second (FPS) of the video
fps = cap.get(cv2.CAP_PROP_FPS)

# Calculate the length of the video in seconds
video_length = num_frames // fps
video_length_formatted = "{:02d}:{:05.2f}".format(
    int(video_length // 60),
    video_length % 60
)

# Release the video capture object
cap.release()

new_df1 = pd.read_csv('final.txt').iloc[:, 1:]

# remove rows where time is equal to length of video
new_df1 = new_df1[new_df1['Time'] != str(video_length_formatted)]

new_df1.to_csv('Ball_info.txt', sep=',', index=False)

# os._exit(1)

print("--------------------------------------------------------")

vs = cv2.VideoCapture(Input_file)
time.sleep(2.0)

# Create a VideoWriter object to write the output video
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(Output_file, fourcc, 30.0, (int(vs.get(3)), int(vs.get(4))))

# set the font and color for the text
font = cv2.FONT_HERSHEY_SIMPLEX
thickness = 2

ee_list = []

for index, row in final_df.iterrows():
    frame_list = []
    # Check if the Type is Entry
    if row['Type'] == 'Entry':
        # Get the quadrant number
        quadrant = row['Quadrant Number']
        # Get the frame number
        frame_num = row['Frame_number']
        # Check if there is another row with the same quadrant number and Type Exit
        if (final_df['Quadrant Number'] == quadrant).any() and (final_df['Type'] == 'Exit').any():
            # Get the frame number of the Exit row
            exit_frame_num = final_df.loc[(final_df['Quadrant Number'] == quadrant) & (final_df['Type'] == 'Exit') & (final_df['Frame_number'] > frame_num), 'Frame_number'].values[0]
            # Get the exit time from the df
            exit_time = final_df.loc[(final_df['Quadrant Number'] == quadrant) & (final_df['Type'] == 'Exit') & (final_df['Frame_number'] > frame_num), 'Time'].values[0]
            # Add the frame numbers to the list
            frame_list.append({'Color': row['Ball Colour'], 'Entry': (frame_num, frame_num + 90), 'Exit': (exit_frame_num - 60, exit_frame_num)})
            # Add another dict in frame_list with entry time and exit time form final_df
            frame_list.append({'Entry Time': row['Time'], 'Exit Time': exit_time})
            # print(frame_list)
            ee_list.append(frame_list)
            # Loop through the frames in the video

# print(ee_list)

total_frames = int(vs.get(cv2.CAP_PROP_FRAME_COUNT))
fps = int(vs.get(cv2.CAP_PROP_FPS))

for i in tqdm(range(0, total_frames)):
    # Set the video stream to the current frame
    vs.set(cv2.CAP_PROP_POS_FRAMES, i)
    # Read the current frame
    ret, frame = vs.read()

    if not ret:
        break
    # Get the current time in the format mm:ss.ss from the start of video
    # current_time = time.strftime('%M:%S.%S', time.gmtime(i // fps))

    current_time = time.strftime('%M:%S', time.gmtime(i / fps)) + '.' + str(i % fps).zfill(2)
    
    # Apply Gaussian blur to the frame
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)

    # Convert the frame to the HSV color space
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    yellowMask = cv2.inRange(hsv, yellowLower, yellowUpper)
    redorangeMask = cv2.inRange(hsv, redOrangeLower, redOrangeUpper)
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    whiteMask = cv2.inRange(hsv, whiteLower, whiteUpper)

    # Perform morphological operations to clean up the thresholded image
    yellowMask = cv2.erode(yellowMask, None, iterations=2)
    yellowMask = cv2.dilate(yellowMask, None, iterations=2)
    redorangeMask = cv2.erode(redorangeMask, None, iterations=2)
    redorangeMask = cv2.dilate(redorangeMask, None, iterations=2)
    blueMask = cv2.erode(blueMask, None, iterations=2)
    blueMask = cv2.dilate(blueMask, None, iterations=2)
    whiteMask = cv2.erode(whiteMask, None, iterations=2)
    whiteMask = cv2.dilate(whiteMask, None, iterations=2)

    # Find contours in the thresholded image
    yellowCnts = cv2.findContours(yellowMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    yellowCnts = imutils.grab_contours(yellowCnts)
    redorangeCnts = cv2.findContours(redorangeMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    redorangeCnts = imutils.grab_contours(redorangeCnts)
    blueCnts = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blueCnts = imutils.grab_contours(blueCnts)
    whiteCnts = cv2.findContours(whiteMask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    whiteCnts = imutils.grab_contours(whiteCnts)
    
    for c in yellowCnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 10:
            # Check which quadrant the ball is in
            quadrant = None
            for key, value in roi.items():
                if x > value[0] and x < value[0] + value[2] and y > value[1] and y < value[1] + value[3]:
                    quadrant = key
                    break
            if quadrant is not None:
                # Draw yellow circle
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 5)
                # Label yellow circle
                cv2.putText(frame, "yellow", (int(x-radius), int(y-radius)-10), font, 1, (0, 255, 255), thickness)
                # Draw yellow star at centroid of yellow ball
                cv2.drawMarker(frame, (int(x), int(y)), (0, 255, 255), cv2.MARKER_STAR, 20, 2)

                for color_dict in ee_list:
                    if color_dict[0]['Color'] == 'yellow':
                        yellow_range = color_dict[0]
                        yellow_times = color_dict[1]
                        if i in range(yellow_range['Entry'][0], yellow_range['Entry'][1]):
                            if 'Entry Time' in yellow_times:
                                cv2.putText(frame, "Entry -" + yellow_times['Entry Time'], (int(x-radius-50), int(y-radius)-50), font, 1, (0, 0, 0), thickness)
                        elif i in range(yellow_range['Exit'][0], yellow_range['Exit'][1]):
                            if 'Exit Time' in yellow_times:
                                if total_frames - yellow_range['Exit'][1] > 30 :
                                    cv2.putText(frame, "Exit -" + yellow_times['Exit Time'], (int(x-radius-50), int(y-radius)-30), font, 1, (0, 0, 0), thickness)

    
    for c in redorangeCnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 10:
            # Check which quadrant the ball is in
            quadrant = None
            for key, value in roi.items():
                if x > value[0] and x < value[0] + value[2] and y > value[1] and y < value[1] + value[3]:
                    quadrant = key
                    break
            if quadrant is not None:
                # Draw redorange circle
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 165, 255), 5)
                # Label redorange circle
                cv2.putText(frame, "red-orange", (int(x-radius), int(y-radius)-10), font, 1, (0, 165, 255), thickness)
                # Draw redorange star at centroid of redorange ball
                cv2.drawMarker(frame, (int(x), int(y)), (0, 165, 255), cv2.MARKER_STAR, 20, 2)

                for color_dict in ee_list:
                    if color_dict[0]['Color'] == 'red-orange':
                        redorange_range = color_dict[0]
                        redorange_times = color_dict[1]
                        if i in range(redorange_range['Entry'][0], redorange_range['Entry'][1]):
                            if 'Entry Time' in redorange_times:
                                cv2.putText(frame, "Entry -" + redorange_times['Entry Time'], (int(x-radius-50), int(y-radius)-50), font, 1, (0, 0, 0), thickness)
                        elif i in range(redorange_range['Exit'][0], redorange_range['Exit'][1]):
                            if 'Exit Time' in redorange_times:
                                if total_frames - redorange_range['Exit'][1] > 30 :
                                    cv2.putText(frame, "Exit -" + redorange_times['Exit Time'], (int(x-radius-50), int(y-radius)-30), font, 1, (0, 0, 0), thickness)
    for c in blueCnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 25 :
            # Check which quadrant the ball is in
            quadrant = None
            for key, value in roi.items():
                if x > value[0] and x < value[0] + value[2] and y > value[1] and y < value[1] + value[3]:
                    quadrant = key
                    break
            if quadrant is not None:
                # Draw blue circle
                cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0), 5)
                # Label blue circle
                cv2.putText(frame, "blue", (int(x-radius), int(y-radius)-10), font, 1, (255, 0, 0), thickness)
                # Draw blue star at centroid of blue ball
                cv2.drawMarker(frame, (int(x), int(y)), (255, 0, 0), cv2.MARKER_STAR, 20, 2)

                for color_dict in ee_list:
                    if color_dict[0]['Color'] == 'blue':
                        blue_range = color_dict[0]
                        blue_times = color_dict[1]
                        if i in range(blue_range['Entry'][0], blue_range['Entry'][1]):
                            if 'Entry Time' in blue_times:
                                cv2.putText(frame, "Entry -" + blue_times['Entry Time'], (int(x-radius-50), int(y-radius)-50), font, 1, (0, 0, 0), thickness)
                        elif i in range(blue_range['Exit'][0], blue_range['Exit'][1]):
                            if 'Exit Time' in blue_times:
                                if total_frames - blue_range['Exit'][1] > 30 :
                                    cv2.putText(frame, "Exit -" + blue_times['Exit Time'], (int(x-radius-50), int(y-radius)-30), font, 1, (0, 0, 0), thickness)
    
    for c in whiteCnts:
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        if radius > 30:
            # Check which quadrant the ball is in
            quadrant = None
            for key, value in roi.items():
                if x > value[0] and x < value[0] + value[2] and y > value[1] and y < value[1] + value[3]:
                    quadrant = key
                    break
            if quadrant is not None:
                # Draw white circle
                cv2.circle(frame, (int(x), int(y)), int(radius), (255, 255, 255), 5)
                # Label white circle
                cv2.putText(frame, "white", (int(x-radius), int(y-radius)-10), font, 1, (255, 255, 255), thickness)
                # Draw white star at centroid of blue ball
                cv2.drawMarker(frame, (int(x), int(y)), (255, 255, 255), cv2.MARKER_STAR, 20, 2)

                for color_dict in ee_list:
                    if color_dict[0]['Color'] == 'white':
                        white_range = color_dict[0]
                        white_times = color_dict[1]
                        if i in range(white_range['Entry'][0], white_range['Entry'][1]):
                            if 'Entry Time' in white_times:
                                cv2.putText(frame, "Entry -" + white_times['Entry Time'], (int(x-radius-50), int(y-radius)-50), font, 1, (0, 0, 0), thickness)
                        elif i in range(white_range['Exit'][0], white_range['Exit'][1]):
                            if 'Exit Time' in white_times:
                                if total_frames - white_range['Exit'][1] > 30 :
                                    cv2.putText(frame, "Exit -" + white_times['Exit Time'], (int(x-radius-50), int(y-radius)-30), font, 1, (0, 0, 0), thickness)
    
    out.write(frame) 

# Release the video stream and output video file
vs.release()
out.release()

# Use the os.startfile() method to play the video
if os.path.exists(Output_file):
    os.startfile(Output_file)
else:
    print("Error: File not found or unable to play.")
