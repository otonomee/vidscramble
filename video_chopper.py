from moviepy.editor import VideoFileClip, concatenate_videoclips
import random
import argparse
import numpy as np

def fragment_and_shuffle(input_file, output_file, min_duration=1, max_duration=2):
    """
    Divides video into unique fragments and shuffles them.
    Each fragment is used exactly once.
    """
    print(f"Loading video: {input_file}")
    video = VideoFileClip(input_file)
    duration = video.duration
    
    # Generate fragment start times
    fragments = []
    current_time = 0
    
    # Create fragments of random lengths that cover the entire video
    while current_time < duration:
        # For the last fragment, adjust to not exceed video length
        remaining_time = duration - current_time
        if remaining_time < min_duration:
            if fragments:  # If we have previous fragments
                # Merge with previous fragment
                fragments[-1][1] = duration
            break
            
        possible_duration = min(max_duration, remaining_time)
        frag_duration = random.uniform(min_duration, possible_duration)
        
        fragments.append([current_time, current_time + frag_duration])
        current_time += frag_duration
    
    # Shuffle the fragments
    random.shuffle(fragments)
    
    # Create clips from fragments
    print("Creating clips from fragments...")
    clips = []
    for start, end in fragments:
        clip = video.subclip(start, end)
        clips.append(clip)
        print(f"Added fragment {len(clips)}: {start:.2f}s - {end:.2f}s")
    
    # Concatenate all clips
    print("Concatenating fragments...")
    final_video = concatenate_videoclips(clips)
    
    # Write the output file
    print(f"Writing output to: {output_file}")
    final_video.write_videofile(output_file, codec='libx264')
    
    # Clean up
    final_video.close()
    for clip in clips:
        clip.close()
    video.close()
    
    print(f"Done! Created video with {len(fragments)} unique fragments")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shuffle unique video fragments")
    parser.add_argument("input_file", help="Input MP4 file path")
    parser.add_argument("output_file", help="Output MP4 file path")
    parser.add_argument("--min-duration", type=float, default=1, help="Minimum duration for each fragment (seconds)")
    parser.add_argument("--max-duration", type=float, default=2, help="Maximum duration for each fragment (seconds)")
    
    args = parser.parse_args()
    
    fragment_and_shuffle(
        args.input_file,
        args.output_file,
        args.min_duration,
        args.max_duration
    )
