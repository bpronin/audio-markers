import sys
import ntpath
import datetime

TIME_FACTOR = 1.002


def parse_duration(s):
    t = datetime.datetime.strptime(s, "%H:%M:%S")
    return datetime.timedelta(hours=t.hour, minutes=t.minute, seconds=t.second) * TIME_FACTOR


def format_duration(t):
    seconds = t.seconds
    hours, seconds = divmod(seconds, 3600)
    minutes, seconds = divmod(seconds, 60)
    return "%d:%02d:%02d.000" % (hours, minutes, seconds)


def write_line(file, no, start, dur, name):
    ln = "%02d - %s\t%s\t%s\tdecimal\tCue\t\n" % (no, name, format_duration(start), format_duration(dur))
    file.write(ln)


src_filename = str(sys.argv[1])
dst_filename = ntpath.join(ntpath.dirname(src_filename), "markers.csv")
src_file = open(src_filename, "r")
dst_file = open(dst_filename, "w")


def parse_track_no(s):
    return int(s.split(".")[0])


try:
    dst_file.write("Name\tStart\tDuration\tTime Format\tType\tDescription\n")

    line = src_file.readline().strip()
    fields = line.split("\t")
    track_name = fields[2]
    start_time = parse_duration(fields[1])
    track_no = 1

    while True:
        line = src_file.readline().strip()
        if not line:
            break

        fields = line.split("\t")
        end_time = parse_duration(fields[1])

        write_line(dst_file, track_no, start_time, end_time - start_time, track_name)

        track_name = fields[2]
        start_time = end_time
        track_no += 1

    write_line(dst_file, track_no, start_time, datetime.timedelta(seconds=10), track_name)
finally:
    src_file.close()
    dst_file.close()
