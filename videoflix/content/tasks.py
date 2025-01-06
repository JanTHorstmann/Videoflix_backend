import subprocess

# 120p Converting
def convert_120p(source):
    new_file_name = source[:-4]
    target = new_file_name + '_120p.mp4'

    source_linux = source
    target_linux = target

    cmd = f'ffmpeg -i "{source_linux}" -vf scale=160:120 -c:v libx264 -preset ultrafast -crf 23 -c:a aac -strict -2 "{target_linux}"'
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# 360p Converting
def convert_360p(source):
    new_file_name = source[:-4]
    target = new_file_name + '_360p.mp4'

    source_linux = source
    target_linux = target

    cmd = f'ffmpeg -i "{source_linux}" -vf scale=480:360 -c:v libx264 -preset ultrafast -crf 23 -c:a aac -strict -2 "{target_linux}"'
    subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

# 720p Converting
def convert_720p(source):
    new_file_name = source[:-4]
    target = new_file_name + '_720p.mp4'

    source_linux = source
    target_linux = target

    cmd = f'ffmpeg -i "{source_linux}" -vf scale=1280:720 -c:v libx264 -preset ultrafast -crf 23 -c:a aac -strict -2 "{target_linux}"'
    subprocess.run(cmd, capture_output=True, shell=True)

# 1080p Converting
def convert_1080p(source):
    new_file_name = source[:-4]
    target = new_file_name + '_1080p.mp4'

    source_linux = source
    target_linux = target

    cmd = f'ffmpeg -i "{source_linux}" -vf scale=1920:1080 -c:v libx264 -preset ultrafast -crf 23 -c:a aac -strict -2 "{target_linux}"'
    subprocess.run(cmd, capture_output=True, shell=True)
