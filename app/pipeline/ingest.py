
from utils.helper_functions import download_dump, extract_dump, get_commands, execute

def ingest_files(tables):

    for table in tables:

        download_dump(table)
        extract_dump(table)
        commands = get_commands(table)

        # creates the table in the database and insert rows
        for command in commands:
            execute(command)

        # logs
        print(f'{table} created')
