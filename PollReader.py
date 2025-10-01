import csv
import unittest

class PollReader:
    def __init__(self, filename):
        self.filename = filename
        self.data_dict = {
            'month': [],
            'date': [],
            'sample': [],
            'sample type': [],
            'Harris result': [],
            'Trump result': []
        }

    def build_data_dict(self):
        with open(self.filename, 'r') as file:
            reader = csv.reader(file)
            header = next(reader)  # skip header row
            for row in reader:
                if len(row) < 5:
                    continue
                self.data_dict['month'].append(row[0])
                self.data_dict['date'].append(int(row[1]))
                # split sample into number + type
                sample_parts = row[2].split()
                if len(sample_parts) == 2:
                    self.data_dict['sample'].append(int(sample_parts[0]))
                    self.data_dict['sample type'].append(sample_parts[1])
                else:
                    self.data_dict['sample'].append(0)
                    self.data_dict['sample type'].append("UNK")
                self.data_dict['Harris result'].append(float(row[3]))
                self.data_dict['Trump result'].append(float(row[4]))

    def highest_polling_candidate(self):
        if not self.data_dict['Harris result'] or not self.data_dict['Trump result']:
            return None

        avg_harris = sum(self.data_dict['Harris result']) / len(self.data_dict['Harris result'])
        avg_trump = sum(self.data_dict['Trump result']) / len(self.data_dict['Trump result'])

        if avg_harris > avg_trump:
            return f"Harris {avg_harris*100:.1f}%"
        elif avg_trump > avg_harris:
            return f"Trump {avg_trump*100:.1f}%"
        else:
            return f"Tie {avg_harris*100:.1f}%"

    def likely_voter_polling_average(self):
        harris_scores = []
        trump_scores = []

        for i in range(len(self.data_dict['sample type'])):
            if self.data_dict['sample type'][i] == "LV":  # only LV rows
                harris_scores.append(self.data_dict['Harris result'][i])
                trump_scores.append(self.data_dict['Trump result'][i])

        if not harris_scores or not trump_scores:
            return 0.0, 0.0

        harris_avg = sum(harris_scores) / len(harris_scores)
        trump_avg = sum(trump_scores) / len(trump_scores)

        return harris_avg, trump_avg

    def polling_history_change(self):
        """
        Compare earliest 30 polls vs latest 30 polls and return net change.
        """
        harris = self.data_dict['Harris result']
        trump = self.data_dict['Trump result']

        if len(harris) < 60:
            return 0.0, 0.0

        earliest_harris = sum(harris[:30]) / 30
        latest_harris = sum(harris[-30:]) / 30
        earliest_trump = sum(trump[:30]) / 30
        latest_trump = sum(trump[-30:]) / 30

        return (latest_harris - earliest_harris,
                latest_trump - earliest_trump)


class TestPollReader(unittest.TestCase):
    def setUp(self):
        self.poll_reader = PollReader('polling_data.csv')
        self.poll_reader.build_data_dict()

    def test_build_data_dict(self):
        self.assertEqual(len(self.poll_reader.data_dict['date']), len(self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['date']))
        self.assertTrue(all(isinstance(x, int) for x in self.poll_reader.data_dict['sample']))
        self.assertTrue(all(isinstance(x, str) for x in self.poll_reader.data_dict['sample type']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Harris result']))
        self.assertTrue(all(isinstance(x, float) for x in self.poll_reader.data_dict['Trump result']))

    def test_highest_polling_candidate(self):
        result = self.poll_reader.highest_polling_candidate()
        self.assertTrue(isinstance(result, str))
        self.assertTrue("Harris" in result)
        self.assertTrue("57.0%" in result)

    def test_likely_voter_polling_average(self):
        harris_avg, trump_avg = self.poll_reader.likely_voter_polling_average()
        self.assertTrue(isinstance(harris_avg, float))
        self.assertTrue(isinstance(trump_avg, float))
        self.assertTrue(f"{harris_avg:.2%}" == "49.34%")
        self.assertTrue(f"{trump_avg:.2%}" == "46.04%")

    def test_polling_history_change(self):
        harris_change, trump_change = self.poll_reader.polling_history_change()
        self.assertTrue(isinstance(harris_change, float))
        self.assertTrue(isinstance(trump_change, float))
        self.assertTrue(f"{harris_change:+.2%}" == "+1.53%")
        self.assertTrue(f"{trump_change:+.2%}" == "+2.07%")


def main():
    poll_reader = PollReader('/Users/annakerhoulas/SI201/DISCUSSION/dicussion-6-kerhoula/polling_data.csv')
    poll_reader.build_data_dict()

    highest_polling = poll_reader.highest_polling_candidate()
    print(f"Highest Polling Candidate: {highest_polling}")
    
    harris_avg, trump_avg = poll_reader.likely_voter_polling_average()
    print(f"Likely Voter Polling Average:")
    print(f"  Harris: {harris_avg:.2%}")
    print(f"  Trump: {trump_avg:.2%}")
    
    harris_change, trump_change = poll_reader.polling_history_change()
    print(f"Polling History Change:")
    print(f"  Harris: {harris_change:+.2%}")
    print(f"  Trump: {trump_change:+.2%}")
    
if __name__ == '__main__':
    main()
    unittest.main(verbosity=2)