# pyusuggest

## Introduction

This package implements a simple class to integrate with amazing
[Ubersuggest tool](https://neilpatel.com/ubersuggest/). But what is the Ubersuggest tool anyway?
It's a powerfull engine that can give statistics about keywords choosed by the user, taking as
params the locale. Unfortanelly, this
tool doesn't have a native API, so I decide to contribute. Home made.

## Index
* [Installation](#installation)
* [Dependencies](#dependencies)
* [API](#api)
  * [Look up method](#request-data-from-uberssugest)
  * [Get monthly statistics method](#look-up-method)
  * [Download search result in CSV format](#download-results-as-csv)
* [Documentation](#documentation)

## Installation

    pip install pyusuggest

## Dependencies

* `requests`
* `pytest`

## API

### Instancing the Ubersuggest

    from pyusuggest import Ubersuggest
    keyword = 'algorithm'
    ubersuggest = Ubersuggest(keyword)

### Request data from Uberssugest

    ubersuggest.look_up()

#### Params

For instancing `Ubersuggest`:

  * `keyword`

    - Keyword or prase that will be used in the query of Ubersuggest tool.

  * `locale`

    - The region that will be used in the query. **Must** follow the padron `en-us`.
    Default locale is `en-us`.

For use `look_up` method:

  * `results`

    - Quantity of results that will be returned by the query. The default number is 50.

### Get monthly statistics
You can get monthly statistics for the keyword searched and the related searches. The monthly statics show how many times that keyword was searched for each month.

```
ubersuggest.set_keyword('databases')
ubersuggest.look_up()
ubersuggest.get_monthly_statistics()
```

#### Params
For use the `get_monthly_statistics` method:

* `period`: number of months that the user wants to track. If no period is passed as
argument, every month will be returned.

### Download results as CSV
You can also download the results from each keyword in CSV format. It will write
a CSV file in the current working directory with the Search Volume, CPC and
Competition info.

```
ubersuggest.set_keyword('java')
ubersuggest.look_up()
ubersuggest.download_results_as_csv()
```

#### Params
For use the `get_monthly_statistics` method:

* No params are required for this method.

## Documentation

Other methods and option params can be checked at documentation.

