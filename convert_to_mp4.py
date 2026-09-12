import ffmpeg
import sys
import os

def convert_mkv_to_mp4(mkv_file_path, mp4_file_path):
    """
    Converts an MKV video file to MP4 format using ffmpeg-python.

    Args:
        mkv_file_path (str): The path to the input MKV file.
        mp4_file_path (str): The path to the output MP4 file.
    """
    # Check if the input MKV file exists
    if not os.path.exists(mkv_file_path):
        print(f"Error: MKV file not found at {mkv_file_path}")
        sys.exit(1)

    # Check if the output directory is writable
    output_dir = os.path.dirname(mp4_file_path)
    if output_dir and not os.path.isdir(output_dir):
        print(f"Error: Output directory is not a valid directory: {output_dir}")
        sys.exit(1)

    try:
        # Use ffmpeg-python to convert the file
        ffmpeg.input(mkv_file_path).output(mp4_file_path, codec="copy").run(overwrite_output=True)  # Added overwrite_output
        print(f"Successfully converted {mkv_file_path} to {mp4_file_path}")
    except ffmpeg.Error as e:
        print(f"Error during conversion: {e.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    # Specify the path to your MKV file
    mkv_file_path = "CitiesSkylines2_Data.mkv"  # Replace with the actual path to your MKV file

    # Specify the path to where you want to save the MP4 file
    mp4_file_path = "CitiesSkylines2_Data.mp4"  # Replace with the desired output path

    convert_mkv_to_mp4(mkv_file_path, mp4_file_path)
