"""This is a sample Python script."""
import os
import csv
from typing import Optional, Any

import psycopg2
import psycopg2.extras

from monitoring import profile
from string_iterator_io import StringIteratorIO


def sum_to_n(number):
    """Sum of the number given."""
    total = 0
    for num in range(0, number):
        total += num
    return total


def get_data_from_csv_files(directory):
    """ get data from all csv files in the specific folder and its children.
    :param directory: root folder path
    :return: contents of all csv files found
    """
    print("main director: " + directory)
    contents = []
    for root, dirs, files in os.walk(directory):
        print(f'files: {files}')
        print(f'dirs: {dirs}')
        print(f'root: {root}')
        for file in files:
            file_path = os.path.join(root, file)
            print(f'filePath: {file_path}')
            if file.endswith(".csv"):
                print('=====================================')
                with open(file_path, 'r', encoding="utf-8") as __file__:
                    reader = csv.reader(__file__)
                    index = 0
                    for row in reader:
                        # Remove first line as title
                        if index == 0:
                            index = index + 1
                            continue
                        contents.append([row[0], row[1], row[2],
                                         row[3], row[4], row[5], row[6]])
                        index = index + 1
    return contents


def connect_to_pg():
    """
    Connect to postgres DB.
    :return: the connection
    """
    conn = psycopg2.connect(database="demo",
                            host="localhost",
                            user="hieubui",
                            password="12345678",
                            port="5432")
    conn.autocommit = True
    return conn


def create_dump_table(cursor):
    """
    Run Script to create table in db.
    :param cursor: cursor of the connection
    :return: None
    """
    cursor.execute("""
        DROP TABLE IF EXISTS public.user_profile;
        CREATE UNLOGGED TABLE public.user_profile
        (
            id uuid,
            user_name text,
            email text,
            domain_name text,
            birthday text,
            job_area text,
            country text
        )

        TABLESPACE pg_default;

        ALTER TABLE IF EXISTS public.user_profile OWNER to hieubui;
    """)


@profile
def insert_datadump_to_db(cursor, obj):
    """
    Insert data dump to Db by method execute_batch.
    :param cursor: cursor of the connection
    :param obj: data insert
    :return: None
    """
    psycopg2.extras.execute_batch(cursor, """
                    INSERT INTO public.user_profile(
                        id, user_name, email,
                        domain_name, birthday, job_area, country
                    ) VALUES (
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s,
                        %s
                    );
                """, obj)


@profile
def insert_datadump_to_db2(cursor, obj: [], table_name):
    """
    Insert data dump to Db by method copy_from.
    :param cursor: cursor of the connection
    :param obj: data insert
    :param table_name: the target table for inserting
    :return: None
    """
    csv_file_like_object = StringIteratorIO((
        '|'.join(map(clean_csv_value, (
            profile[0],
            profile[1],
            profile[2],
            profile[3],
            profile[4],
            profile[5],
            profile[6],
        ))) + '\n'
        for profile in obj
    ))
    cursor.copy_from(csv_file_like_object, table_name, sep='|')


def clean_csv_value(value: Optional[Any]) -> str:
    """
    Make data look like a csv data.
    :param value: data
    :return: csv data like
    """
    if value is None:
        return r'\N'
    return str(value).replace('\n', '\\n')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print(f'sum of 5 is: {sum_to_n(5)}')
    path = os.path.abspath(os.path.join(os.getcwd(), os.pardir)) + '/data'
    profiles = get_data_from_csv_files(path)
    try:
        connect = connect_to_pg()
        cur = connect.cursor()
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)
        create_dump_table(cur)
        insert_datadump_to_db2(cur, profiles, 'user_profile')
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if connect is not None:
            connect.close()
