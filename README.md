# **async-ptt-crawler**

This project scrapes/crawls post content and comments from [PTT](https://term.ptt.cc/) website, and implements [neural CKIP Chinese NLP tools](https://github.com/ckiplab/ckip-transformers) on the scraped data asynchronously.

## **Documentation**
### 1. Installation

1. Python version
   * `python == 3.7.5`

2. Clone repository
    ```bash
    git@github.com:Taiwan-Social-Media-Corpus/async-scraptt.git
    ```

3. Install Requirement
* pip

    ```bash
    cd async-scraptt && pip install -r requirements.txt      
    ```
* pipenv

    ```bash
    cd async-scraptt && pipenv install -r requirements.txt    
    ```

### 2. Usage

1. Commands
```
scrapy crawl ptt -a boards=BOARDS [-a scrap_all=BOOLEAN] 
            [-a index_from=NUMBER -a index_to=NUMBER]   
            [-a since=YEAR] [-a data_dir=PATH]

positional arguments:
-a boards=BOARDS                          ptt board name (e.g. Soft_Job)
-a index_from=NUMBER -a index_to=NUMBER   html index number from a ptt board
-a scrap_all=BOOLEAN                      scrap all posts if true
-a since=YEAR                             scrap all posts from a given year
-a data_dir=PATH                          output file path (default: ./data)
```

* Crawl all the posts of a board:
  ```bash
  scrapy crawl ptt -a boards=Soft_Job -a scrap_all=True
  ```

* Crawl all the posts of a board from a year in the past:
  ```bash
  scrapy crawl ptt -a boards=Soft_Job -a since=2022
  ```

* Crawl the posts of a board based on html indexes:
  ```bash
  scrapy crawl ptt -a boards=Soft_Job -a index_from=1722 -a index_to=1723
  ```

  > Please make sure the number of `index_from` is greater than `index_to`.

* Crawl the posts of multiple boards. For example:
  ```bash
  scrapy crawl ptt -a boards=Soft_Job,Gossiping -a index_from=1722 -a index_to=1723
  ```

  >Note: the comma in the argument `boards` cannot have spaces. It cannot be `boards=Soft_Job, Baseball` or  `boards=["Soft_Job", "Baseball"]`.


## Contact
If you have any suggestion or question, please do not hesitate to email us at shukai@gmail.com or philcoke35@gmail.com
