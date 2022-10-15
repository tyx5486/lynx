import time
# quick fix so that app does not hit the db before it is ready during initial docker built
time.sleep(10)

from pipeline.ingest import ingest_files
from pipeline.transform import curate
from pipeline.aggregate import aggregate

def main():

    # logs
    print("main()..")

    # the tables to be ingested
    tables = [
        "page",
        "categorylinks",
        "pagelinks",
    ]

    # runs the pipeline
    print("ingest_files()..")
    ingest_files(tables)

    print("curate()..")
    curate()
    
    print("aggregate()..")
    aggregate()

    # logs
    print("Done!")


main()
