import os
import datetime
import ffmpeg
import requests
import json
import random
import csv
from pydub import AudioSegment

OUTPUT_DIR = "RadioStream-30_Public_AM_FM"
METADATA_FILE = os.path.join(OUTPUT_DIR, "metadata.csv")

# Online radio stations
RADIO_STATIONS = {
    "BBC World Service": "http://stream.live.vc.bbcmedia.co.uk/bbc_world_service",
    "Jazz FM": "http://media-ice.musicradio.com/JazzFMMP3",
    "NPR News": "https://npr-ice.streamguys1.com/live.mp3"
}


def record_stream(station_name, url, duration):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{station_name}_{timestamp}.mp3"
    output_file = os.path.join(OUTPUT_DIR, filename)

    print(f"Recording {station_name} for {duration} seconds...")

    try:
        (
            ffmpeg
            .input(url, t=duration)
            .output(output_file, format="mp3", acodec="libmp3lame", audio_bitrate="128k")
            .run(quiet=True)
        )
        print(f"Recording saved to {output_file}")
        return output_file
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def convert_to_wav(mp3_file):
    try:
        wav_filepath = mp3_file.replace(".mp3", ".wav")
        audio = AudioSegment.from_mp3(mp3_file)
        audio.export(wav_filepath, format="wav")
        print(f"Converted {mp3_file} to {wav_filepath}")
        return wav_filepath
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def save_metadata(station_name, url, duration, wav_filepath):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    data = [station_name, url, duration, wav_filepath, timestamp]

    file_exists = os.path.exists(METADATA_FILE)
    with open(METADATA_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Station Name", "URL", "Duration", "Filepath", "Timestamp"])
        writer.writerow(data)

    print(f"Metadata saved to {METADATA_FILE}")


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for station_name, url in RADIO_STATIONS.items():
        duration = random.randint(30, 90)  
        mp3_file = record_stream(station_name, url, duration)
        if mp3_file:
            wav_file = convert_to_wav(mp3_file)
            if wav_file:
                save_metadata(station_name, url, duration, wav_file)


if __name__ == "__main__":
    main()
