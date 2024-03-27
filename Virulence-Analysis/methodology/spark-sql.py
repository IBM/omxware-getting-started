#! /usr/bin/env python

import argparse
import importlib
import re
import sys
import time
from typing import List

from pyspark.sql import SparkSession


def parse(file_name: str) -> List[str]:
    stmts = []
    stmt_buffer = []

    with open(file_name, 'r') as sql_file:
        block_comment = False
        for line in sql_file:
            if line.startswith('/*') and not line.endswith('*/'):
                block_comment = True
                stmts.append(line.rstrip())
            elif line.startswith('*/'):
                block_comment = False
                stmts.append(line.rstrip())
            elif not block_comment and not line.startswith('--'):
                if line.startswith('@'):
                    stmts.extend(parse(re.sub(r'[@;]', '', line.rstrip())))
                elif not line.rstrip().endswith(';'):
                    stmt_buffer.append(line)
                else:
                    stmt_buffer.append(line.replace(';', ''))
                    stmt = ''.join(stmt_buffer)
                    stmts.append(stmt)
                    stmt_buffer = []
            else:
                stmts.append(line.rstrip())

    return stmts


def parse_sql_file(file_name: str) -> List[str]:
    return parse(file_name)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--sql-file', dest='sql_file', type=str, required=True,
                        help='file containing spark sql commands to execute')
    parser.add_argument('--udf-mods', dest='udf_mods', type=str, required=False,
                        help='file containing python code for Spark User Defined Functions')
    args = parser.parse_args()

    with SparkSession.builder.appName('spark-sql.py').enableHiveSupport().getOrCreate() as spark:
        if args.udf_mods:
            udf_mods = importlib.import_module(args.udf_mods, package=__name__)
            importlib.invalidate_caches()
            udf_mods.register(spark)

        in_comment = False
        stmts = parse_sql_file(args.sql_file)
        for stmt in stmts:
            try:
                if stmt.startswith('--') or stmt.startswith('/*'):
                    in_comment = True
                elif stmt.startswith('*/'):
                    in_comment = False

                print(stmt)

                if not in_comment:
                    start_time = time.time()
                    df = spark.sql(stmt)
                    if stmt.strip().lower().startswith('select'):
                        df.show(truncate=False)
                    print('completed in {:.2f} seconds\n'.format(time.time() - start_time))

                if stmt.startswith('--') or stmt.endswith('*/'):
                    in_comment = False
            except Exception as e:
                print(str(e))
                sys.exit(1)


if __name__ == '__main__':
    main()
