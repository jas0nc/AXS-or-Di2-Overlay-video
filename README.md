This a python program for coverting the gear change event recorded by Garmin Edge computer to an transparent overlay video for use in editor software. 

![temp_gear_image](https://github.com/user-attachments/assets/3f72abc1-395c-4b2f-b40f-9019723a2fce)
![Screenshot 2025-02-28 at 3 42 11 PM](https://github.com/user-attachments/assets/4d7bddee-8fc3-4fa9-8633-71a4f651aecc)

**Requirements: **
1) python3
2) library like pandas, moviepy, PIL, packaging.
3) ffmpeg

This program has no ability to read fit file directly, so we still need to use third party app to extract the event file from the garmin fit file. 
**Method:**
1) go to https://www.fitfileviewer.com
![Screenshot 2025-02-28 at 3 29 12 PM](https://github.com/user-attachments/assets/4dd8a67a-f927-4e2a-aa0b-3b643aba415e)
2) open your fit file downloaded from garmin connect website
3) look into event tag, and the download the event file in csv.
![Screenshot 2025-02-28 at 3 18 39 PM](https://github.com/user-attachments/assets/9cf01900-4bf0-4dbd-976b-2422d337205b)
4) Select ISO time format during export.
![Screenshot 2025-02-28 at 3 19 29 PM](https://github.com/user-attachments/assets/5b3ba725-dc6b-4994-ab23-a534bf78e4de)
5) save the exported csv file as **input.csv**

**Usage:**
Finally we can use this app with below command

python3 gear_overlay.py input.csv -o output-gearbox.mov

**Contributor**
The program is mainly built by Perplexity AI, only minor fine tune was made. No worry, it works nicely.
