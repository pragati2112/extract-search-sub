import subprocess


# extract subtitle via cc-extractor
# Read and save in key-value based DB afterwards---
def extract_subtitles(file_path="uploads/sample2.mp4", out_path="uploads/srts/out.srt"):
    subprocess.Popen(["/usr/bin/ccextractor", file_path, "-o", out_path])
