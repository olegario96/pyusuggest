# pyusuggest

## Introduction

This package implements a simple class to integrate with amazing [Ubersuggest tool](https://neilpatel.com/ubersuggest/).

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

    - Keyword or prase that will be used in the query of Ubersuggest tool

  * `area`

  * `locale`

    - The region that will be used in the query. **Must** follow the padron `en-us`.

For use `look_up` method:

  * `results`

    - Quantity of results that will be returned by the query

## Documentation

Other methods and option params can be checked at documentation.
