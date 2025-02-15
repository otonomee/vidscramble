from moviepy.editor import VideoFileClip, concatenate_videoclips
import random
import argparse

def create_random_cuts(input_file, output_file, min_duration=1, max_duration=2, total_output_duration=None):
    """
    Creates a new video from random segments of the input video.
    
    Args:
        input_file (str): Path to input MP4 file
        output_file (str): Path for output MP4 file
        min_duration (float): Minimum duration for each clip in seconds
        max_duration (float): Maximum duration for each clip in seconds
        total_output_duration (float): Optional total duration for output video in seconds
    """
    # Load the video file
    print(f"Loading video: {input_file}")
    video = VideoFileClip(input_file)
    
    # Get video duration
    duration = video.duration
    clips = []
    current_duration = 0
    
    # If total_output_duration is not specified, use the original video length
    if total_output_duration is None:
        total_output_duration = duration
    
    print("Generating random clips...")
    while current_duration < total_output_duration:
        # Generate random start time and clip duration
        start_time = random.uniform(0, duration - max_duration)
        clip_duration = random.uniform(min_duration, max_duration)
        
        # Ensure we don't exceed the desired total duration
        if current_duration + clip_duration > total_output_duration:
            clip_duration = total_output_duration - current_duration
        
        # Extract the clip
        clip = video.subclip(start_time, start_time + clip_duration)
        clips.append(clip)
        current_duration += clip_duration
        
        print(f"Added clip: {len(clips)} (Duration: {clip_duration:.2f}s, Total: {current_duration:.2f}s)")
    
    # Concatenate all clips
    print("Concatenating clips...")
    final_video = concatenate_videoclips(clips)
    
    # Write the output file
    print(f"Writing output to: {output_file}")
    final_video.write_videofile(output_file, codec='libx264')
    
    # Close all clips
    final_video.close()
    for clip in clips:
        clip.close()
    video.close()
    
    print("Done!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a video with random segments from input video")
    parser.add_argument("input_file", help="Input MP4 file path")
    parser.add_argument("output_file", help="Output MP4 file path")
    parser.add_argument("--min-duration", type=float, default=1, help="Minimum duration for each clip (seconds)")
    parser.add_argument("--max-duration", type=float, default=2, help="Maximum duration for each clip (seconds)")
    parser.add_argument("--total-duration", type=float, help="Total duration of output video (seconds)")
    
    args = parser.parse_args()
    
    create_random_cuts(
        args.input_file,
        args.output_file,
        args.min_duration,
        args.max_duration,
        args.total_duration
    )
