import unittest
import requests
import json

URL = "http://localhost:5500"


class ResponseTester(unittest.TestCase):
    def test_get_response(self):
        gold_answers = "What's up?"
        data = {
            "history": "So nice to meet you. <|endoftext|>[DA_2]"
        }
        j_data = json.dumps(data)
        r = requests.post(f"{URL}/respond", data=j_data)
        tmp_answer = json.loads(r.text)
        self.assertEqual(gold_answers, tmp_answer["data"])


class BatchResponseTester(unittest.TestCase):
    def test_get_batch_response(self):
        gold_answers = [
            'Morning, Mary .  What can I do for you?', 'Yes, it is.']
        data = {
            "histories": ["Good morning! <|endoftext|>[DA_2]", "It's such a nice day.<|endoftext|>[DA_1]"]
        }
        j_data = json.dumps(data)
        r = requests.post(f"{URL}/respond_batch", data=j_data)
        tmp_answer = json.loads(r.text)
        self.assertEqual(gold_answers, tmp_answer["data"])


if __name__ == "__main__":
    unittest.main()
