# Assumptions:

## CSV File Structure:

The mappings CSV file contains columns: dstport, protocol, and tag.
The log CSV file contains columns: srcport, dstport, protocol, and action.
It is assumed that both files will be well-formed with consistent headers.

## Protocol Mapping Completeness:

It assumes that the flowlog_protocol_mapping dictionary is complete for all possible numeric protocol codes in the log file. If a protocol appears in the log that is not mapped, this could lead to errors or unexpected behavior.

## Tag Processing

The program processes tags and keeps them in memory, assuming the mapping dict won't run out of memory
The tag values in the mappings CSV are converted to lowercase. This assumes that the tags are case-insensitive, and converting them to lowercase will not lose important information.

## Edge-cases

The program doesn't handle cases where the CSV files are empty, which could result in exceptions or no output.


# Execution

Place the network flow log and tag mappings in the resource directory, following the current naming convention.

run the application --> python3 src/process_log.py
run tests --> python3 -m unittest src/test_process_log.py  
