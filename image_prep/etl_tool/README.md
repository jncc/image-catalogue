# ETL TOOL

### Survey Analysis to Metadata Sheet.py

- Requirements:
    - 're' and 'string' from python builtins
    - 'yaml' library (available on pip)
    - 'openpyxl' library (available on pip)
    - 'gdal' (python library) includes 'osgeo' download a wheel from https://www.lfd.uci.edu/~gohlke/pythonlibs/

Creates an Excel sheet as specified in config.yaml, some fields from a given survey sheet and others just static values

### Format of config.yaml

Each item in the 'Fields' dictionary of the config specifies a Field name in the final sheet:
E.g.
  "XMP-JNCCMarineSurvey:stationCode":
Then any functions that need to be run to produce the data for the field
E.g.
    - [Get Data from Field, Mandatory Check]
Then the argument(s) for the first function
E.g.
    - Station code

So overall:
"XMP-JNCCMarineSurvey:stationCode":
    - [Get Data from Field, Mandatory Check]
    - Station code

This takes the field 'Station code', checks it's not empty and puts that in the field "XMP-JNCCMarineSurvey:stationCode"


### Adding a New Function

To add a new function, define it in the code and ensure it takes in as parameters the return from the previous function or the argument from the config.
If you are adding a prebuilt or inbuilt function such as math.round, say, be aware that all arguments are passed between the functions as lists so you will have to run the decorator 'turn_data_to_args' to break up these lists.
Once it is coded you must add it to the 'NAME_TO_FUNCTION' dictionary:
E.g.
'Round Number':  check_all_arguments_are_floats(turn_data_to_args(math.round))
Then add it to the config, referring to it by the name in the key section of NAME_TO__FUNCTION


### Make Config From Proforma.py

Simply takes the blueprint for a config file and creates it without any data filled in.
The field names are taken from the proforma.