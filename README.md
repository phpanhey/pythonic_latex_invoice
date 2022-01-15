# Pythonic invoice

A pythonic way to create your invoices.


## Usage
first make your config file. a example config is provided (`invoice_doe_olsen_inc.json.example`). place your logo called `logo.pdf`  here `/src/img/`. a example logo is provided (`logo.pdf.example`).

```sh
python3 pythonic_latex_invoice.py --config invoice_doe_olsen_inc.json
```
will compile to this invoice_doe_olsen_inc.pdf:

![alt text](https://github.com/phpanhey/pythonic_latex_invoice/blob/master/src/img/invoice_example.jpg?raw=true)