import subprocess
from server.read_srt import read_srt_file


# extract subtitle via cc-extractor
# Read and save in key-value based DB afterwards---
def extract_subtitles(file_path="uploads/sample2.mp4",
                      out_path="uploads/srts/out.srt",
                      video_id=''):
    p = subprocess.Popen(["/usr/bin/ccextractor", file_path, "-o", out_path])
    (output, err) = p.communicate()

    # This makes the wait possible
    p_status = p.wait()
    print('process status', p_status)
    # read srt file and save subtitles to dynamodb
    read_srt_file(out_path, video_id=video_id)
    return True
