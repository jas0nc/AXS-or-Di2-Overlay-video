import pandas as pd
from moviepy import *
from moviepy.video.tools.drawing import color_gradient
from PIL import Image, ImageDraw, ImageFont
import argparse
import os

def generate_gear_overlay(csv_filepath, output_filepath="gear_overlay.mov"):
    """
    Generates a transparent .mov video overlay showing gear changes from a cycling CSV.

    Args:
        csv_filepath (str): Path to the CSV file.
        output_filepath (str, optional): Path to the output .mov file. Defaults to "gear_overlay.mov".
    """

    try:
        df = pd.read_csv(csv_filepath)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_filepath}")
        return

    # Extract start time from 'timer' event
    start_timer_event = df[(df['event'] == 'timer') & (df['event type'] == 'start')]
    if not start_timer_event.empty:
        start_timecode = pd.to_datetime(start_timer_event['timestamp'].iloc[0])
    else:
        print("Warning: No 'timer start' event found. Using first gear change event as start time.")
        gear_changes = df[df['event'].isin(['frontGearChange', 'rearGearChange'])].copy()
        if gear_changes.empty:
            print("No gear change events found in the CSV.")
            return
        gear_changes['timestamp'] = pd.to_datetime(gear_changes['timestamp'])
        start_timecode = gear_changes['timestamp'].iloc[0] #use the first gear change event

    # Filter relevant events
    gear_changes = df[df['event'].isin(['frontGearChange', 'rearGearChange'])].copy()
    gear_changes['timestamp'] = pd.to_datetime(gear_changes['timestamp'])

    if gear_changes.empty:
        print("No gear change events found in the CSV.")
        return

    # Determine end time (not strictly needed anymore, but good to have)
    end_time = gear_changes['timestamp'].iloc[-1]
    total_duration = (end_time - start_timecode).total_seconds()

    # Prepare video clip list
    clips = []

    # Function to create a gear frame as a PIL image
    def create_gear_frame(front_gear, rear_gear):
        width, height = 250, 150  # Adjust as needed
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)

        # Choose a font and size that works on your system
        try:
            font = ImageFont.truetype("/Library/Fonts/NCLMonsterBeast-Demo.ttf", size=50)  # Replace with path to a font on your system
        except IOError:
            font = ImageFont.load_default()  # Use a default font if Arial is not found

        text = f"{int(front_gear) if pd.notna(front_gear) else '-'}x{int(rear_gear) if pd.notna(rear_gear) else '-'}"  # display gear, change gear to int and replace nan with -

        # Use textbbox to get text size
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        x = (width - text_width) / 2
        y = (height - text_height) / 2


        # Draw black outline
        outline_color = (0, 0, 0, 255)  # Black, fully opaque
        for i in range(-2, 3):
            for j in range(-1, 2):
                draw.text((x + i, y + j), text, font=font, fill=outline_color)
	# Draw white text
        text_color = (255, 255, 255, 255)  # White, fully opaque
        draw.text((x, y), text, font=font, fill=text_color)

        return image

    # Iterate through gear changes to create clips
    for i in range(len(gear_changes)):
        event = gear_changes.iloc[i]
        front_gear = event['front gear']
        rear_gear = event['rear gear']

        # Calculate clip start time relative to start_timecode
        clip_start_time = (event['timestamp'] - start_timecode).total_seconds()

        # Determine duration of the clip
        if i < len(gear_changes) - 1:
            next_time = gear_changes['timestamp'].iloc[i + 1]
            duration = (next_time - event['timestamp']).total_seconds()
        else:
            duration = 1  # Small duration for the last clip to be displayed

        # Create the gear frame
        img = create_gear_frame(front_gear, rear_gear)
        img.save("temp_gear_image.png")  # Save as a temporary file

        # Create the clip from the image
        clip = ImageClip("temp_gear_image.png", duration=duration)
        clip = clip.with_position(("center", "bottom")).with_opacity(1).with_start(clip_start_time)  # Adjust position as needed
        clips.append(clip)

    # Concatenate clips
    final_clip = concatenate_videoclips(clips, method="compose")

    # Set audio to none
    final_clip = final_clip.without_audio()

    # Ensure the background is transparent when saving
    final_clip.write_videofile(output_filepath,
                               codec="png",  # Use PNG codec for transparency
                               audio=False,
                               fps=1,
                               ffmpeg_params=["-pix_fmt", "yuva420p"]) # Ensure transparency is preserved
    # Clean up temporary file
    os.remove("temp_gear_image.png")

    print(f"Gear overlay video created: {output_filepath}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a transparent gear overlay video from a cycling CSV.")
    parser.add_argument("csv_filepath", help="Path to the input CSV file.")
    parser.add_argument("-o", "--output_filepath", help="Path to the output .mov file (optional, default: gear_overlay.mov)", default="gear_overlay.mov")

    args = parser.parse_args()

    generate_gear_overlay(args.csv_filepath, args.output_filepath)
