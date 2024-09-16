import unittest
from collections import defaultdict
from io import StringIO
import csv
from process_log import FlowLogProcessor


class TestFlowLogProcessor(unittest.TestCase):

    def setUp(self):
        # Initialize FlowLogProcessor instance
        self.processor = FlowLogProcessor()

        # Example CSV data for mappings
        self.mappings_csv = StringIO("""dstport,protocol,tag
                                    25,tcp,email
                                    443,tcp,web
                                    22,tcp,ssh
                                    """)

        # Example CSV data for logs
        self.log_csv = StringIO("""srcport,dstport,protocol,action
49152,25,6,ACCEPT
49200,443,6,ACCEPT
49300,22,6,ACCEPT
49400,80,6,ACCEPT
49500,21,6,ACCEPT
""")

        # Reader objects
        self.mapping_reader = csv.DictReader(self.mappings_csv)
        self.log_reader = csv.DictReader(self.log_csv)

    '''
    Test the mappings are built correctly
    '''
    def test_build_mappings(self):
        self.processor.build_mappings(self.mapping_reader)
        expected_mappings = {
            ('25', 'TCP'): 'email',
            ('443', 'TCP'): 'web',
            ('22', 'TCP'): 'ssh'
        }

        self.assertEqual(self.processor.mappings, expected_mappings)

    '''
    Test the counts for tags and port combos are correct
    '''
    def test_process_row(self):
        # Build the mappings first
        self.processor.build_mappings(self.mapping_reader)

        # Count dictionaries for testing
        count_tag = defaultdict(int)
        count_port_combo = defaultdict(int)

        # Sample row for testing
        sample_row = {'srcport': '49152', 'dstport': '25', 'protocol': '6', 'action': 'ACCEPT'}

        # Process the row
        self.processor.process_row(sample_row, count_tag, count_port_combo)

        # Assert the counts were incremented correctly
        self.assertEqual(count_tag['email'], 1)
        self.assertEqual(count_port_combo[('25', 'TCP')], 1)

    """
    Test that untagged items are counted correctly
    """
    def test_untagged_count(self):
        # Build the mappings first
        self.processor.build_mappings(self.mapping_reader)

        # Count dictionaries for testing
        count_tag = defaultdict(int)
        count_port_combo = defaultdict(int)

        # Example row that does not have a mapping (port 80 or 21)
        untagged_row = {'srcport': '49400', 'dstport': '80', 'protocol': '6', 'action': 'ACCEPT'}
        untagged_row2 = {'srcport': '49500', 'dstport': '21', 'protocol': '6', 'action': 'ACCEPT'}

        # Process untagged rows
        self.processor.process_row(untagged_row, count_tag, count_port_combo)
        self.processor.process_row(untagged_row2, count_tag, count_port_combo)

        # Assert that the untagged items are counted correctly
        self.assertEqual(count_tag['untagged'], 2)

    def tearDown(self):
        self.mappings_csv.close()
        self.log_csv.close()

if __name__ == '__main__':
    unittest.main()
