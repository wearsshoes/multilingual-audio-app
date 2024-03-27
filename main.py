import os
from dotenv import load_dotenv
from audio_processing import *

def main(audio_file, output_file):
    """
    Main function to perform speaker diarization on an audio file.

    Args:
        audio_file (str): Path to the input audio file.
        output_file (str): Path to save the diarization output as an RTTM file.
    """
    # Perform diarization and save the results to the specified output file
    diarization_result = diarize_pyannote(audio_file, output_file)

    # Optionally, print the diarization result or further process it
    print(f"Diarization result saved to {output_file}")


if __name__ == "__main__":
    # Example usage: python main.py input_audio.wav diarization_output.rttm
    import sys
    load_dotenv()

    if len(sys.argv) != 3:
        print("Usage: python main.py <audio_file> <output_file>")
        sys.exit(1)

    audio_file = sys.argv[1]
    output_file = sys.argv[2]

    main(audio_file, output_file)