# pyusuggest

## Introduction

This package implements a simple class to integrate with amazing
[Ubersuggest tool](https://neilpatel.com/ubersuggest/). But what is the Ubersuggest tool anyway?
It's a powerfull engine that can give statistics about keywords choosed by the user, taking as
params the locale and the target of the search (i.e. web, YouTube, images). Unfortanelly, this
tool doesn't have a native API, so I decide to contribute. Home made.

## Index
* [Installation](#installation)
* [Dependencies](#dependencies)
* [API](#api)
  * [Params](#params)
  * [Look up method](#look-up-method)
* [Documentation](#documentation)

## Installation

    pip install pyusuggest

## Dependencies

* requests
* pytest

## API

### Instancing the Ubersuggest

    from pyusuggest import Ubersuggest
    keyword = 'algorithm'
    ubersuggest = Ubersuggest(keyword)

### Request data from Uberssugest

    ubersuggest.look_up()

## Params

For instancing `Ubersuggest`:

  * `keyword`

    - Keyword or prase that will be used in the query of Ubersuggest tool.

  * `area`

    - The targe area that query should aim (i.e. general web, YouTube, images). More options
    can be found at the [Ubersuggest](https://neilpatel.com/ubersuggest/) site or at the API class.

  * `locale`

    - The region that will be used in the query. **Must** follow the padron `en-us`. Default
    locale is `en-us`.

For use `look_up` method:

  * `results`

    - Quantity of results that will be returned by the query. The default number is 50.

## Documentation

Other methods and option params can be checked at documentation.
