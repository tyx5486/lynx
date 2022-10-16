from config.secret import host_args

import gzip
import urllib.request 
import shutil
import mysql.connector


def download_dump(table_name):
    """
    Downloads a sql.gz file from https://dumps.wikimedia.org/simplewiki/latest

    Parameters
    ----------
    table_name: string
        The name of the table to be downloaded
    """

    urllib.request.urlretrieve(
        f"https://dumps.wikimedia.org/simplewiki/latest/simplewiki-latest-{table_name}.sql.gz",
        f"data/{table_name}.gz",
    )


def extract_dump(table_name):
    """
    Extracts the sql dump file

    Parameters
    ----------
    table_name: string
        The name of the .gz file
    """

    with gzip.open(f"data/{table_name}.gz", 'rb') as f_in:
        with open(f'data/{table_name}.sql', 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def get_commands(table_name):
    """
    Pulls out the sql commands from the dump file

    Parameters
    ----------
    table_name: string
        The name of the .sql file

    Returns
    -------
    list
        A list of commands to create the table and insert rows.
        The list is ordered in the sequence the commands should be executed.

    """

    file_name = f"data/{table_name}.sql"

    fd = open(file_name, 'r', encoding="utf8")
    sql_file = fd.read()
    fd.close()

    # get the DROP and CREATE commands
    ddl_commands = sql_file.split('-- Dumping data')[0].split(';')
    commands = ["DROP", "CREATE"]
    ddl_commands = [ddl_command for ddl_command in ddl_commands if any(c in ddl_command for c in commands)]

    # get the INSERT commands
    dml_commands = sql_file.split('-- Dumping data')[1].split('\n')
    dml_commands = [dml_command for dml_command in dml_commands if "INSERT" in dml_command]

    return ddl_commands + dml_commands


def execute(command):
    """
    Initialized the connection and cursor, runs the command, closes the connection and cursor

    Parameters
    ----------
    command: string
        The query to be executed
    """

    conn = mysql.connector.connect(**host_args)
    cur = conn.cursor(dictionary=True, buffered=True)

    # logs
    print(f"Running : {command[0:50]}..")

    cur.execute(command, multi=True)
    conn.commit()

    cur.close()
    conn.close()


