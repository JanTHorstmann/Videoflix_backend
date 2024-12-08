import subprocess

def convert_120p(source):
    new_file_name = source[:-4]
    target = new_file_name + '_120p.mp4'
    source_linux = "/mnt/" + source.replace("\\", "/").replace("C:", "c")
    target_linux = "/mnt/" + target.replace("\\", "/").replace("C:", "c")
    cmd = 'ffmpeg -i "{}" -s hd120 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source_linux, target_linux)
    subprocess.run(cmd, capture_output=True, shell=True)

def convert_360p(source):
    new_file_name = source[:-4]
    target = new_file_name + '_360p.mp4'
    source_linux = "/mnt/" + source.replace("\\", "/").replace("C:", "c")
    target_linux = "/mnt/" + target.replace("\\", "/").replace("C:", "c")
    cmd = 'ffmpeg -i "{}" -s hd360 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source_linux, target_linux)
    subprocess.run(cmd, capture_output=True, shell=True)

def convert_720p(source):
    new_file_name = source[:-4]
    target = new_file_name + '_720p.mp4'
    source_linux = "/mnt/" + source.replace("\\", "/").replace("C:", "c")
    target_linux = "/mnt/" + target.replace("\\", "/").replace("C:", "c")
    cmd = 'ffmpeg -i "{}" -s hd720 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source_linux, target_linux)
    subprocess.run(cmd, capture_output=True, shell=True)

def convert_1080p(source):
    new_file_name = source[:-4]
    target = new_file_name + '_1080p.mp4'
    source_linux = "/mnt/" + source.replace("\\", "/").replace("C:", "c")
    target_linux = "/mnt/" + target.replace("\\", "/").replace("C:", "c")
    cmd = 'ffmpeg -i "{}" -s hd1080 -c:v libx264 -crf 23 -c:a aac -strict -2 "{}"'.format(source_linux, target_linux)
    subprocess.run(cmd, capture_output=True, shell=True)