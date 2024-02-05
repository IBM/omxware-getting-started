#! /usr/bin/env python

import argparse
import os
import shutil

from pyspark.sql import SparkSession

EXPORT_DIR = '.export_tmp'


def export(spark: SparkSession, stmt: str, path: str) -> None:
    df = spark.sql(stmt)
    df.write.mode('overwrite').csv(EXPORT_DIR)
    csv_files = sorted([file_name for file_name in os.listdir(EXPORT_DIR) if file_name.endswith('.csv')])

    output_dir = os.path.dirname(path)
    if not output_dir:
        output_dir = 'outputs'
    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, os.path.basename(path))
    with open(output_file, 'w') as out_file:
        columns = ','.join(df.columns)
        out_file.write(f'{columns}\n')
        for csv_file in csv_files:
            with open(os.path.join(EXPORT_DIR, csv_file), 'r') as in_file:
                shutil.copyfileobj(in_file, out_file)

    shutil.rmtree(EXPORT_DIR)
    print(f'exported {df.count()} records')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--stmt', dest='stmt', type=str, required=True, help='Spark SQL statement to run')
    parser.add_argument('--path', dest='path', type=str, required=True, help='File path to store results')
    args = parser.parse_args()

    with SparkSession.builder.appName('export.py').enableHiveSupport().getOrCreate() as spark:
        export(spark, args.stmt, args.path)


if __name__ == '__main__':
    main()
