import json
import os
import unittest

from .task_runner import TaskRunner
from deepdiff import DeepDiff



class TestWebserver(unittest.TestCase):
    
    def setUp(self):
        self.fucntion = TaskRunner(None,None)

    
    
    def test_states_mean(self):
        self.helper_test_endpoint("states_mean")

    def test_state_mean(self):
        self.helper_test_endpoint("state_mean")

    def test_best5(self):
        self.helper_test_endpoint("best5")

    def test_worst5(self):
        self.helper_test_endpoint("worst5")

    def test_global_mean(self):
        self.helper_test_endpoint("global_mean")

    def test_diff_from_mean(self):
        self.helper_test_endpoint("diff_from_mean")

    def test_state_diff_from_mean(self):
        self.helper_test_endpoint("state_diff_from_mean")

    def test_mean_by_category(self):
        self.helper_test_endpoint("mean_by_category")

    def test_state_mean_by_category(self):
        self.helper_test_endpoint("state_mean_by_category")
    
    def helper_test_endpoint(self, endpoint):
        

        output_dir = f"unittests/{endpoint}/output/"
        input_dir = f"unittests/{endpoint}/input/"
        input_files = os.listdir(input_dir)
        


        for input_file in input_files:

            idx = input_file.split('-')[1]
            idx = int(idx.split('.')[0])
        
            with open(f"{input_dir}/{input_file}", "r") as fin:
                if fin is None:
                    print("File not found")
                req_data = json.load(fin)
            
            with open(f"{output_dir}/out-{idx}.json", "r") as fout:
                ref_result = json.load(fout)

            if(endpoint == 'states_mean'):
                rez = self.fucntion.states_mean(req_data)
            elif(endpoint == 'state_mean'):
                rez = self.fucntion.state_mean(req_data,"Timis")
            elif(endpoint == 'best5'):
                rez = self.fucntion.best5(req_data)
            elif(endpoint == 'worst5'):
                rez = self.fucntion.worst5(req_data)
            elif(endpoint == 'global_mean'):
                rez = self.fucntion.global_mean(req_data)
            elif(endpoint == 'diff_from_mean'):
                rez = self.fucntion.diff_from_mean(req_data)
            elif(endpoint == 'state_diff_from_mean'):
                rez = self.fucntion.state_diff_from_mean(req_data,"Bucuresti")
            elif(endpoint == 'mean_by_category'):
                rez = self.fucntion.mean_by_category(req_data)
            elif(endpoint == 'state_mean_by_category'):
                rez = self.fucntion.state_mean_by_category(req_data,"Alabama")
                
                
        
            diff = DeepDiff(ref_result, rez)
            self.assertEqual(diff, {}, "Test failed")
            print("Test passed")
            

    
if __name__ == '__main__':
    try:
        unittest.main()
    except:
        SystemExit