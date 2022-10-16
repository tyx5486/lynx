from utils.helper_functions import execute

# wiki_catagory_rank ranks catagories by number of pages. 
# the category with the most pages is ranked 1
sql_drop_wiki_catagory_rank = """
    DROP TABLE IF EXISTS wiki_category_rank;
"""

sql_create_wiki_category_rank = """
    CREATE TABLE IF NOT EXISTS wiki_category_rank AS
    WITH wi AS (
        SELECT category
        , COUNT(*) pages
        FROM wiki_info
        GROUP BY 1
    )
    SELECT category
    , pages
    , RANK() OVER (ORDER BY pages DESC) category_rank
    FROM wi
"""

# wiki_most_outdated a records the most outdated page for each category
# A page is called outdated if at least one of the pages it refers to was modified
# later than the page itself. If more than 1 page in a category are outdated by
# the same number of seconds, we take the page with the smallest page_id
sql_drop_wiki_most_outdated_top_ten = """
    DROP TABLE IF EXISTS wiki_most_outdated_top_ten
"""

sql_create_wiki_most_outdated_top_ten = """
    CREATE TABLE IF NOT EXISTS wiki_most_outdated_top_ten AS
    SELECT DISTINCT page_category
    , FIRST_VALUE(page_id) OVER (PARTITION BY page_category ORDER BY page_outdated_duration DESC) most_outdated_page
    FROM wiki_page_links
    WHERE page_category IN (
      SELECT category 
      FROM wiki_category_rank 
      WHERE category_rank <= 11
    );
"""

def aggregate():

    commands = [
        "sql_drop_wiki_catagory_rank",
        "sql_create_wiki_category_rank",
        "sql_drop_wiki_most_outdated_top_ten",
        "sql_create_wiki_most_outdated_top_ten"
    ]

    for command in commands:

        # creates the tables in the database
        execute(eval(command))

        # logs
        print(f"{command[command.find('wiki'):]} created")

