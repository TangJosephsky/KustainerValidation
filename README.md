# KustainerValidation
A demo repository, showing how one could validate detections against an ADX emulator to catch KQL runtime errors.

# Setup
This repository has three main folders: detections, pipelines and sampledata. 

The **pipelines** folder contains the python scripts used to ingest data and query against the ADX emulator (kustainer). The validate.yml file contains the main logic for our KQL validation stage: It runs the kustainer image, installs any python dependencies and runs the python scripts.

The **sampledata** folder contains a folder per Table that you want to ingest. If you want to add another table as sample data, simply add a folder with the name of your table and provide a schema.json file and a data.json file. Both can easily be generated by running ```<tablename> | getschema | project ColumnName, ColumnType``` or by running ```<tablename> | take 3``` and exporting the results as csv. You can then use powershell's ```convertfrom-csv | convertto-json``` commands to easily get the json daa you need.

The **detections** folder contains a couple of Sentinel and Defender detections, based on the "ARM API" format or the "Graph Create custom detectionrule" format. You're free to store your detections in whatever IAC format that you want, but keep in mind that you might need to update some of the python scripts to navigate your object correctly.
