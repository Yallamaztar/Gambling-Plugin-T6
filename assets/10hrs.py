from pydub import AudioSegment
import random

kiss = AudioSegment.from_file("kissya.mp3")
print("loaded kissya")

# 10 hours in ms
ten_hours_ms = 10 * 60 * 60 * 1000

# Build track
output = AudioSegment.silent(duration=0)
current_time = 0

while current_time < ten_hours_ms:
    # Random gap between 2 and 10 minutes
    gap = random.randint(2, 10) * 60 * 1000
    if current_time + gap > ten_hours_ms:
        print("breaking")
        break
    output += AudioSegment.silent(duration=gap)
    output += kiss
    current_time += gap + len(kiss)
    print("doing shit")

# Pad to exactly 10 hours
if len(output) < ten_hours_ms:
    output += AudioSegment.silent(duration=(ten_hours_ms - len(output)))
    print("yemane")

# Export result
output.export("10_hours_of_silence_with_kissya.mp3", format="mp3")
