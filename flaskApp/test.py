import unittest
import main_algorithm


class TestMainAlgorithm(unittest.TestCase):

    def setUp(self):
        self.raw_availabilities = [0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0]
        self.slots_to_fill = {
            2019: {4: {23: {"9am": None, "10am": None}, 24: {"9am": None, "10am": None}}}}
        self.max_slots = 2
        self.total_shifts = 4
        self.employees = ["Luke", "George", "Zac"]
        self.target_shifts = [2, 1, 1]
        self.result = main_algorithm.make_schedule(
            self.raw_availabilities, self.slots_to_fill, self.max_slots, self.total_shifts, self.employees, self.target_shifts)

    def test_not_none(self):
        self.assertNotEqual(self.result, None)

    def test_db_queries(self):
        # check db query equal to expected

    def test_data_processed(self):
        # check db queries properly transformed into necessary inputs for algorithm

    def test_unschedulable(self):
        # check if unschedulable list in result is equal to expected

    def test_scheduled(self):
        # check result slots_to_fill dict is equal to expected

    def test_db_update(self):
        # check if the db updates to reflect the output of the algorithm
        # basically test_scheduled combined with test_db_queries


if __name__ == '__main__':
    unittest.main()
