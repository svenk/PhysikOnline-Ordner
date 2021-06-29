#!/bin/bash
# POTT-Daten runterladen

wget -O"pott_num_edits.csv" "https://elearning.physik.uni-frankfurt.de/projekt/report/15?asc=1&format=tab"

wget -O"pott_all_edits.csv" "https://elearning.physik.uni-frankfurt.de/projekt/report/16?asc=1&max=6000&page=1&format=tab"
