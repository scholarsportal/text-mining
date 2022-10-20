# Text Mining Scholars Portal Journals

This repository is intended to document the APIs on [Scholars Portal Journals](https://journals.scholarsportal.info/) that will enable you to build datasets. 

The python scripts found here are intended for demonstration purposes and make use of the [pandas library](https://pandas.pydata.org).

**To access any of the API links, you'll need to be within your university's IP ranges.** 

## Building a corpus file

Using the [search form](https://journals.scholarsportal.info/) on the site you can fine tune your query parameters and then copy the string from the top of the results page and add it to the query variable in the `corpus-builder.py` script like so:

    query = '((covid 19) AND TITLE:(taste OR smell)) AND YEAR GE 2020-01-01 AND YEAR LE 2022-12-31 sort:date'

There are a few other user defined variables that you should be aware of. 

    pageLength = 20

This is the number of results to grab at a time. The larger the number, the slower the response will be, so feel free to play around with this one to determine what works best. The default is 20.

    datatype = 'id'

This defines the amount of metadata that is returned for each result. The three options are:

 1. **id** - this only returns URIs and URLs for each of the results. If you have a lot of data to harvest, this is probably your best option. You can grab tens of thousands of results at a time if you set the `pageLength` accordingly.

 2. **bib** - includes all of the bibliographic data about the article, like title, authors, journal, doi and date. This is useful if you want to filter or clean up the results list before harvesting.
 
 3. **full** - includes all of the above plus abstract, keywords and search snippet text. This can be a lot of data and the extra fields need to be added to the data structure in the script.

Once all your variables are entered, run `python3 corpus-builder.py` in your terminal. The script will generate a CSV in the same directory.

If you want to write your own script, you just need to append the parameters `page_length`, `data`, and `format=json` to the search results url like so:

https://journals.scholarsportal.info/search?q=covid+19&search_in=anywhere&op=AND&q=taste+OR+smell&search_in=TITLE&date_from=2020&date_to=2022&sort=date&page_length=20&data=bib&format=json

## Harvesting

Now that you have a CSV file of all the data you'd like to harvest, run the harvester script: `python harvester.py`

This script will loop through the CSV file and harvest the full metadata along with the extracted full text of the article into a [json lines](https://jsonlines.org/) file. These files can grow quite large very fast so make sure you have the appropriate disk space!

For each record the harvester hits a data view page like this:

https://journals.scholarsportal.info/data/08878994/v136icomplete/28_satdippwsi.xml

This page has entitlement information and links to JSON, XML (JATS), and PDF files. The included harvesting script uses the JSON data and generates a separate log file if there are issues with entitlements are the full text is missing. 

### Entitlements

If you're not entitled to an article based on your libraries subscriptions, then the full text links will not appear. To access entitled content, you will need to harvest from within your university's IP ranges. If you try to harvest through a proxy, you might run into rate limiting and if you're not within any known IP ranges, it will return a "not authenticated" error.

### Formats

**JSON**

https://journals.scholarsportal.info/data/json/08878994/v136icomplete/28_satdippwsi.xml

The full text here is extracted directly from the PDF file on the fly or from the XML. 

**XML**

https://journals.scholarsportal.info/data/xml/08878994/v136icomplete/28_satdippwsi.xml

If `xml_available = true`, that means we have the full text in JATS XML format, which includes markup tags. If `xml_available = false`, then the full text will be absent in the xml view. 

**PDF**

https://journals.scholarsportal.info/data/pdf/08878994/v136icomplete/28_satdippwsi.xml

If there's a PDF file, this will get it.

## Feedback

We always want to improve our services so please let us know what works and what doesn't. Are there any features you'd like to see? We'd love to hear about your text mining endeavors!

journals@scholarsportal.info




