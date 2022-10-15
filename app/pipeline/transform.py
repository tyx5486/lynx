from utils.helper_functions import execute

# wiki_info is a table of basic metadata for every wiki page:
# - Page title
# - Categories of the page
# - Date of last modification
sql_drop_wiki_info = """
    DROP TABLE IF EXISTS wiki_info;
"""

sql_create_wiki_info = """
    CREATE TABLE wiki_info (
       KEY page_id (page_id)
       , KEY category (category)
    ) AS
    SELECT p.page_id
    , p.page_namespace
    , CAST(p.page_title AS CHAR(255))               page_title
    , CAST(cl.cl_to AS CHAR(255))                   category
    , CAST(p.page_touched AS DATETIME)              last_modification_date
    FROM page p
    LEFT JOIN categorylinks cl ON p.page_id = cl.cl_from;
"""

# wiki_page_links records the links between the wiki pages, defined by the following:
# - The page which refers to another page
# - The referred page
sql_drop_wiki_page_links = """
    DROP TABLE IF EXISTS wiki_page_links;
"""

sql_create_wiki_page_links = """
	CREATE TABLE wiki_page_links AS
    SELECT CAST(cl.cl_to AS CHAR(255))              page_category
    , p1.page_id 
    , p1.page_namespace 
    , CAST(p1.page_title AS CHAR(255))              page_title
    , CAST(p1.page_touched AS DATETIME)             page_last_modification_date
    , p2.page_id                                    link_page_id
    , p2.page_namespace                             link_page_namespace
    , CAST(p2.page_title AS CHAR(255))              link_page_title
    , CAST(p2.page_touched AS DATETIME)             link_last_modification_date
    , TIMESTAMPDIFF(
        SECOND
        , p2.page_touched
        , p1.page_touched
    )                                               page_outdated_duration
    FROM page p1
	LEFT JOIN pagelinks pl ON p1.page_id = pl.pl_from
    LEFT JOIN page p2 ON p2.page_namespace = pl.pl_namespace AND p2.page_title = pl.pl_title
    LEFT JOIN categorylinks cl ON pl.pl_from = cl.cl_from
"""

sql_alter_unique_key_wiki_page_links = """
    ALTER TABLE wiki_page_links ADD UNIQUE KEY page_category_id_link_id (page_category, page_id, link_page_id);
"""

sql_alter_key1_wiki_page_links = """
    ALTER TABLE wiki_page_links ADD KEY page_namespace_last_modification_date (page_namespace, page_last_modification_date)
"""

sql_alter_key2_wiki_page_links = """
    ALTER TABLE wiki_page_links ADD KEY link_namespace_link_last_modification_date (link_page_namespace, link_last_modification_date)
"""

sql_alter_key3_wiki_page_links = """
    ALTER TABLE wiki_page_links ADD KEY page_outdated_duration (page_outdated_duration)
"""


def curate():

    commands = [
        "sql_drop_wiki_info",
        "sql_create_wiki_info",
        "sql_drop_wiki_page_links",
        "sql_create_wiki_page_links",
        "sql_alter_unique_key_wiki_page_links",
        "sql_alter_key1_wiki_page_links",
        "sql_alter_key2_wiki_page_links",
        "sql_alter_key3_wiki_page_links"
    ]

    for command in commands:

        # creates the tables in the database
        execute(eval(command))

        # logs
        print(f"{command} done!")

