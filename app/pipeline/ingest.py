
from utils.helper_functions import download_dump, extract_dump, get_commands, execute

def ingest_files(tables):

    for table in tables:

        # pulls the wiki dump files from https://dumps.wikimedia.org/simplewiki/
        download_dump(table)

        # extract to get the sql file
        extract_dump(table)

        # pulls out individual sql commands from sql file
        commands = get_commands(table)

        # creates the table in the database and insert rows
        for command in commands:
            execute(command)

        # logs
        print(f'{table} created')
