#!/bin/bash
(./main.py) | (column -t) > README.md
rm filosofia.htm for_lang.htm names.html
cat README.md
