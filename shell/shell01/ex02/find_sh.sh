#!/usr/bin/bash
find . -iname "*.sh" -printf "%f\n" | sed 's/\.sh$//'
 
