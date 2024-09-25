import subprocess

subprocess.run([
    "yt-dlp",
    "-q",
    "-o", "here.wav",
    "-f",
    "ba",
    "dQw4w9WgXcQ"
])