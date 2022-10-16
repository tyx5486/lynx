# Wikipedia Assistant

A simple application that pulls the ```page```, ```pagelinks``` and ```categorylinks``` tables from the [simple wiki data dumps](https://dumps.wikimedia.org/simplewiki/).

We have 3 separate services
 - [**db**](https://github.com/tyx5486/lynx/tree/main/db): a mysql database
 - [**app**](https://github.com/tyx5486/lynx/tree/main/app): the data pipelines
 - [**api**](https://github.com/tyx5486/lynx/tree/main/api): the web application to receive request

Each service runs in their own `docker` container and we use `docker-compose` to configure all the services.

## Getting Started

Set a `DB_PASSWORD` environment variable. 

```
export DB_PASSWORD="mySecretPassword"
```

Spin up the docker containers. 
```
docker-compose up
```
This will take a while (1 hour plus on a Ryzen 5600X) since the dump files are pretty large. 

## 1. Database & Pipelines

The pipelines are orchestrated in `app/app.py` and can be found in [here](https://github.com/tyx5486/lynx/tree/main/app/pipeline). 

All transformations are done in `SQL` and everything else is done in `python`. 

Here is a rough idea of what the code does:

1. Downloads the dump files, extract the sql files and creates the the tables
    * **page**
    * **categorylinks**
    * **pagelinks**

2. Cleans the above tables to get
    * **wiki_info** -> de-normalized page and category info
    * **wiki_page_links** -> de-normalized page and link info

3. Aggregates the above tables to get 
    * **wiki_category_rank** -> a rank of all categories by number of pages
    * **wiki_most_outdated_top_ten** -> the top ten categories and their most outdated page

We do the transformations across 3 steps to allow for easier data auditing and bug tracking.

## 2. API Usage
The 2 endpoints are as follows. 

You can use `your_domain = host.docker.internal` if the containers are on your local machine.

---

An endpoint that receives an arbitrary SQL query and returns the result of
executing the query on the database.

#### Request
```curl -H "query: SELECT * FROM page LIMIT 10" http://[your_domian]:5000/query```

#### Response
```
{
  "page_content_model": {
    "0": "wikitext",
    "1": "wikitext"
  },
  "page_id": {
    "0": 1,
    "1": 2
  },
  "page_is_new": {
    "0": 0,
    "1": 0
  },
  "page_is_redirect": {
    "0": 0,
    "1": 0
  },
  "page_lang": {
    "0": null,
    "1": null
  },
  "page_latest": {
    "0": 8446859,
    "1": 8346993
  },
  "page_len": {
    "0": 22188,
    "1": 13247
  },
  "page_links_updated": {
    "0": "20220918033749",
    "1": "20220912214014"
  },
  "page_namespace": {
    "0": 0,
    "1": 0
  },
  "page_random": {
    "0": 0.778582929065,
    "1": 0.123830928525
  },
  "page_title": {
    "0": "April",
    "1": "August"
  },
  "page_touched": {
    "0": "20220918033748",
    "1": "20220912214121"
  }
}
```

---

An endpoint that receives a category and returns the most outdated page for that
category.

> A page is called outdated if at least one of the pages it refers to was modified
later than the page itself. The measure of this outdatedness is the biggest
difference between the last modification of a referred page and the last
modification of the page.
#### Request
```curl http://[your_domain]/most_outdated?category=Coordinates_on_Wikidata```

#### Response
```
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <title>wiki data</title>
  </head>
  <body>
    Most Oudated Page for top ten category: Coordinates_on_Wikidata
    <br><br>

    <table border="1" class="dataframe">
      <thead>
        <tr style="text-align: right;">
          <th></th>
          <th>0</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <th>page_id</th>
          <td>16316</td>
        </tr>
        <tr>
          <th>page_namespace</th>
          <td>0</td>
        </tr>
        <tr>
          <th>page_title</th>
          <td>Wake_Island</td>
        </tr>
        <tr>
```

## 3. Scheduling
The pipelines need to run twice a month, this is done via `app`'s `Dockerfile` and a `crontab` to keep things as simple as possible.

## 4. Sharing
Docker is build 

## 5. Submit Code and Documentation
This git repo is the code and you are reading the documentation!