# Converts track list into Adobe Audition's markers file
# Source file must be formatted as follows:
# ---
# TOTAL DURATION {[HH:]MM:SS}[,TIME FACTOR {FLOAT}]
# TRACK START TIME {[HH:]MM:SS},TRACK NAME {STRING}
# ...
# ---

import sys
import ntpath
import datetime


class Track:
    pass


def parse_time(s, factor):
    fmt = "%M:%S" if s.count(":") == 1 else "%H:%M:%S"
    time = datetime.datetime.strptime(s, fmt)
    return datetime.timedelta(hours=time.hour, minutes=time.minute, seconds=time.second) * factor


def format_time(t):
    seconds = abs(int(t.seconds))
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return "%d:%02d:%02d.000" % (hours, minutes, seconds)


def format_dst_filename(src):
    fn = ntpath.basename(src).split(".")[0] + ".csv"
    return ntpath.join(ntpath.dirname(src), "markers-" + fn)


def read_tracks(file):
    field_separator = ","
    line = file.readline().rstrip("\n")
    fields = line.split(field_separator)
    time_factor = float(fields[1]) if len(fields) > 1 else 1.0
    total_duration = parse_time(fields[0], time_factor)

    tracks = []
    while True:
        line = file.readline().rstrip("\n")
        if line == "":
            break
        fields = line.split(field_separator)

        track = Track()
        track.start = parse_time(fields[0], time_factor)
        track.name = fields[1]

        tracks.append(track)
    return tracks, total_duration


def update_tracks(tracks, total_duration):
    i = 0
    n = len(tracks) - 1
    while i <= n:
        track = tracks[i]
        end = tracks[i + 1].start if i < n else total_duration
        track.duration = end - track.start
        i += 1


def write_tracks(tracks, file):
    file.write("Name\tStart\tDuration\tTime Format\tType\tDescription\n")
    for i, track in enumerate(tracks):
        line = "%02d - %s\t%s\t%s\tdecimal\tCue\t" % (i + 1,
                                                      track.name,
                                                      format_time(track.start),
                                                      format_time(track.duration))
        file.write(line + "\n")


def main():
    src_filename = str(sys.argv[1])
    with open(src_filename, "r") as file:
        tracks, total_duration = read_tracks(file)

    update_tracks(tracks, total_duration)

    dst_filename = format_dst_filename(src_filename)
    with open(dst_filename, "w") as file:
        write_tracks(tracks, file)


main()
