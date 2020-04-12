package com.bopr;

import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.text.ParseException;
import java.time.Duration;
import java.util.Scanner;

public class Markers {

    public static void main(String[] args) throws IOException, ParseException {
        File src = new File(args[0]);
        File dst = new File(src.getParentFile(), "~" + src.getName());

//        PrintWriter writer = new PrintWriter(System.out);
        PrintWriter writer = new PrintWriter(dst);
        Scanner scanner = new Scanner(new FileInputStream(src)).useDelimiter("\\t");

        try {
            writer.println(scanner.nextLine()); /* header line */

            Duration prev = Duration.ZERO;
            while (scanner.hasNext()) {
                String name = scanner.next();
                Duration start = parseTime(scanner.next());
                String duration = scanner.next();
                String timeType = scanner.next();
                String type = scanner.next();

                writer.println(name + "\t"
                        + formatTime(prev) + "\t"
                        + formatTime(start.minus(prev)) + "\t"
                        + timeType + "\t" + type + "\t");

                prev = start;
                scanner.nextLine();
            }
        } finally {
            scanner.close();
            writer.close();
        }
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
