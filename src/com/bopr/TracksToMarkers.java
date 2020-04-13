package com.bopr;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.time.Duration;
import java.util.Scanner;

public class TracksToMarkers {

    public static void main(String[] args) throws IOException {
        File tracks = new File(args[0]);
        File markers = new File(tracks.getParentFile(), formatFilename(tracks));

        Scanner scanner = new Scanner(new FileInputStream(tracks));
        PrintWriter writer = new PrintWriter(markers);

        try(scanner; writer) {
            writer.println("Name\tStart\tDuration\tTime Format\tType\tDescription");

            String[] firstLine = readLine(scanner);
            Duration start = parseTime(firstLine[0]);
            String name = firstLine[1];
            int trackNo = 1;
            Duration end;

            while (scanner.hasNext()) {
                String[] line = readLine(scanner);
                end = parseTime(line[0]);

                writeLine(writer, trackNo, start, end.minus(start), name);

                name = line[1];
                start = end;
                trackNo++;
            }

            writeLine(writer, trackNo, start, Duration.ofSeconds(10), name);
        }
    }

    private static String[] readLine(Scanner scanner) {
        return scanner.nextLine().split("\\t");
    }

    private static String formatFilename(File tracks) {
        return "markers-" + tracks.getName().split("\\.")[0] + ".csv";
    }

    private static void writeLine(PrintWriter writer, int trackNo, Duration start, Duration duration, String name) {
        writer.format("%02d - %s\t%s\t%s\tdecimal\tCue\t\r\n",
                trackNo,
                name,
                formatTime(start),
                formatTime(duration)
        );
    }

    private static Duration parseTime(String s) {
        String[] parts = s.split(":");
        if (parts.length == 3) {
            return Duration.parse("PT" + parts[0] + "H" + parts[1] + "M" + parts[2] + "S");
        } else {
            return Duration.parse("PT" + parts[0] + "M" + parts[1] + "S");
        }
    }

    private static String formatTime(Duration time) {
        return String.format("%d:%02d:%02d.%03d",
                time.toHoursPart(),
                time.toMinutesPart(),
                time.toSecondsPart(),
                time.toMillisPart());
    }

}
