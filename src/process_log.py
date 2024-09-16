import csv
from collections import defaultdict

'''
This class reads a csv file containing network traffic logs and a mapping file that maps port and protocol to a tag.
'''

class FlowLogProcessor:
    '''
    Constructor that initializes the flowlog protocol number mapping
    '''

    def __init__(self):
        self.flowlog_protocol_mapping = {
            '1': 'ICMP',
            '6': 'TCP',
            '17': 'UDP',
            '41': 'IPv6',
            '50': 'ESP',
            '51': 'AH',
            '58': 'ICMPv6',
            '115': 'L2TP'
        }
        self.mappings = {}

    def print_count(self, count):
        for key, value in count.items():
            if isinstance(key, tuple):
                print(f"{key[0]},{key[1]},{value}")
            else:
                print(f"{key},{value}")

    '''
    process_row function processes a row from the csv file and updates the count_tag and count_port_combo dictionaries
    @param row: a row from the csv file
    @param count_tag: a dictionary that maps tag to count
    @param count_port_combo: a dictionary that maps port and protocol to count
    @return None
    '''

    def process_row(self, row, count_tag, count_port_combo):
        key = (row['dstport'], self.flowlog_protocol_mapping[row['protocol']])
        if key in self.mappings:
            tag = self.mappings[key]
            count_tag[tag] += 1
        else:
            count_tag['untagged'] += 1
        count_port_combo[key] += 1

    '''
    process_log function reads the csv file and processes each row
    @param log_file: the csv file containing network traffic logs
    '''

    def process_log(self, log_file):
        count_tag = defaultdict(int)
        count_port_combo = defaultdict(int)
        with open(log_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.process_row(row, count_tag, count_port_combo)
        print("Tag, Count")
        self.print_count(count_tag)
        print("Port,Protocol,Count")
        self.print_count(count_port_combo)

    '''
    build_mappings function reads the mapping file and builds the mappings dictionary  (dtsport, protocol) -> tag  
    @param reader: a csv reader object
    '''

    def build_mappings(self, reader):
        for row in reader:
            key = (row['dstport'], row['protocol'].upper())
            self.mappings[key] = row['tag'].lower()

    def run(self, mapping_file, log_file):
        with open(mapping_file, 'r') as f:
            reader = csv.DictReader(f)
            self.build_mappings(reader)
        self.process_log(log_file)


processor = FlowLogProcessor()
processor.run("../resource/mapping.csv", "../resource/network_traffic.csv")
