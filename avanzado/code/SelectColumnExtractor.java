package org.apache.hadoop.examples;

import java.io.IOException;

import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;

import org.apache.hadoop.io.LongWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.io.Text;

import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;

import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

public class SelectColumnExtractor extends Configured implements Tool {

    public static class ColumnMapper extends Mapper<LongWritable, Text, NullWritable, Text> {
        private int selectColumn = -1;

        @Override
        protected void setup(Context context) {
            Configuration conf = context.getConfiguration();
            selectColumn = conf.getInt("select.column", -1);
        }

        @Override
        protected void map(LongWritable key, Text value, Context context) throws IOException, InterruptedException {
            String line = value.toString();
            String[] rawColumns = line.split(" (?=\")"); // espacio antes de comillas dobles
            int totalColumns = rawColumns.length;

            if (selectColumn >= totalColumns || selectColumn < 0) {
                context.write(NullWritable.get(), new Text(line));
                return;
            }

            String column = rawColumns[selectColumn].trim();
            if (column.startsWith("\"") && column.endsWith("\"") && column.length() >= 2) {
                column = column.substring(1, column.length() - 1);
            }

            context.write(NullWritable.get(), new Text(column));
        }
    }

    @Override
    public int run(String[] args) throws Exception {
        if (args.length != 3) {
            System.err.println("Usage: SelectColumnExtractor <input> <output> <columnIndex>");
            return -1;
        }

        Configuration conf = getConf();
        conf.setInt("select.column", Integer.parseInt(args[2]));

        Job job = Job.getInstance(conf, "Select Column Extractor");
        job.setJarByClass(SelectColumnExtractor.class);

        job.setMapperClass(ColumnMapper.class);
        job.setNumReduceTasks(0); // solo mapper

        job.setOutputKeyClass(NullWritable.class);
        job.setOutputValueClass(Text.class);

        FileInputFormat.setInputPaths(job, new Path(args[0]));
        FileOutputFormat.setOutputPath(job, new Path(args[1]));

        return job.waitForCompletion(true) ? 0 : 1;
    }

    public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new SelectColumnExtractor(), args);
        System.exit(exitCode);
    }
}
