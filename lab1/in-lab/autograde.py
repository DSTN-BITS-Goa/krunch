import json
import unittest

# Import the Disk class from both implementations
from disk import Disk

scores = {"scores": {}}
class TestDiskClass(unittest.TestCase):

    def setUp(self):
        # Fixed parameters
        self.addr = "-1"
        self.lateAddr = "-1"
        self.lateAddrDesc = "0,-1,0"
        self.addrDesc = "5,-1,0"
        self.graphics = False
        self.compute = True
        self.skew = 0
        self.window = -1
        self.policy = "VR"
        self.seekSpeed = 1
        self.rotateSpeed = 1
        self.numTracks = 3
        self.armTrack = 0
        self.initialDir = 1
        self.zoning = "30,30,30"
        self.rValue = 0

    def get_fail_message(self, expected, actual):
        return "Expected: " + str(expected) + "\nActual: " + str(actual)

    def update_scores(self, test_case, score, expr1, expr2):
        if expr1 == expr2:
            scores["scores"][test_case] = score
        else:
            scores["scores"][test_case] = 0
    def test_case_1(self):
        # Test Case 1
        self.addr = "5,8,17,57,52,3"
        self.window = 3
        self.numTracks = 5
        self.rValue = 0.3
        self.zoning = "30" + ",30" * (self.numTracks - 1)
        answer = [
            (5, 0, 315, 30, 345),
            (8, 0, 60, 30, 90),
            (17, 40, 200, 30, 270),
            (3, 40, 230, 30, 300),
            (57, 160, 350, 30, 540),
            (52, 0, 180, 30, 210),
        ]
        # python disk.py -c -a 5,8,17,57,52,3 -w 3 -n 5 -p VR -r 0.3

        disk = Disk(
            self.addr,
            self.addrDesc,
            self.lateAddr,
            self.lateAddrDesc,
            self.policy,
            self.seekSpeed,
            self.rotateSpeed,
            self.skew,
            self.window,
            self.compute,
            self.graphics,
            self.zoning,
            self.armTrack,
            self.numTracks,
            self.initialDir,
            self.rValue,
        )

        disk.Go()

        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_1", 10, disk.getBlockStats(), answer)

        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 1 failed\n" + fail_message
        )

    def test_case_2(self):
        # Test Case 2
        self.addr = "15,41,31,50,11,23,8,13,44,7"
        self.numTracks = 5
        self.armTrack = 4
        self.zoning = "30" + ",30" * (self.numTracks - 1)
        answer = [
            (50, 0, 225, 30, 255),
            (41, 40, 20, 30, 90),
            (44, 0, 60, 30, 90),
            (31, 40, 260, 30, 330),
            (15, 40, 170, 30, 240),
            (23, 0, 210, 30, 240),
            (13, 0, 30, 30, 60),
            (11, 40, 230, 30, 300),
            (8, 0, 240, 30, 270),
            (7, 0, 300, 30, 330),
        ]
        # python disk.py -c -a 15,41,31,50,11,23,8,13,44,7 -n 5 -t 4 -p VR

        disk = Disk(
            self.addr,
            self.addrDesc,
            self.lateAddr,
            self.lateAddrDesc,
            self.policy,
            self.seekSpeed,
            self.rotateSpeed,
            self.skew,
            self.window,
            self.compute,
            self.graphics,
            self.zoning,
            self.armTrack,
            self.numTracks,
            self.initialDir,
            self.rValue,
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())
        self.update_scores("test_case_2", 10, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 2 failed\n" + fail_message
        )

    def test_case_3(self):
        # Test Case 3
        self.addr = "34,25,34,12,48,49,39,9,31,19"
        self.armTrack = 1
        self.numTracks = 5
        self.initialDir = 0
        self.rValue = 1
        self.zoning = "30" + ",30" * (self.numTracks - 1)

        answer = [
            (12, 0, 165, 30, 195),
            (19, 0, 180, 30, 210),
            (9, 40, 350, 30, 420),
            (34, 80, 280, 30, 390),
            (25, 0, 60, 30, 90),
            (34, 0, 240, 30, 270),
            (31, 0, 240, 30, 270),
            (39, 40, 170, 30, 240),
            (48, 40, 200, 30, 270),
            (49, 0, 0, 30, 30),
        ]
        # python disk.py -c -a 34,25,34,12,48,49,39,9,31,19 -r 1 -n 5 -t 1 -i 0 -p VR

        disk = Disk(
            self.addr,
            self.addrDesc,
            self.lateAddr,
            self.lateAddrDesc,
            self.policy,
            self.seekSpeed,
            self.rotateSpeed,
            self.skew,
            self.window,
            self.compute,
            self.graphics,
            self.zoning,
            self.armTrack,
            self.numTracks,
            self.initialDir,
            self.rValue,
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_3", 10, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 3 failed\n" + fail_message
        )

    def test_case_4(self):
        # Test Case 4
        self.addr = "33,26,9,62,20,36,64,5,39,44,2,27,50,32,52"
        self.window = 6
        self.numTracks = 6
        self.armTrack = 2
        self.rValue = 1
        self.zoning = "30" + ",30" * (self.numTracks - 1)

        answer = [
            (33, 0, 75, 30, 105),
            (26, 0, 120, 30, 150),
            (36, 40, 230, 30, 300),
            (62, 80, 310, 30, 420),
            (20, 160, 350, 30, 540),
            (9, 40, 320, 30, 390),
            (5, 0, 210, 30, 240),
            (2, 0, 240, 30, 270),
            (27, 80, 280, 30, 390),
            (39, 40, 290, 30, 360),
            (44, 0, 120, 30, 150),
            (64, 80, 130, 30, 240),
            (50, 40, 230, 30, 300),
            (52, 0, 30, 30, 60),
            (32, 80, 10, 30, 120),
        ]
        # python disk.py -c -a 33,26,9,62,20,36,64,5,39,44,2,27,50,32,52 -r 1 -n 6 -t 2 -w 6 -p VR

        disk = Disk(
            self.addr,
            self.addrDesc,
            self.lateAddr,
            self.lateAddrDesc,
            self.policy,
            self.seekSpeed,
            self.rotateSpeed,
            self.skew,
            self.window,
            self.compute,
            self.graphics,
            self.zoning,
            self.armTrack,
            self.numTracks,
            self.initialDir,
            self.rValue,
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_4", 20, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 4 failed\n" + fail_message
        )

    def test_case_5(self):
        # Test Case 5
        self.addr = "66,26,3,5,68,11,66,59,54,56,57,63,4,58,5"
        self.numTracks = 10
        self.armTrack = 3
        self.window = 6
        self.rValue = 0.4
        self.zoning = "30,30,30,60,60,60,90,90,90,90"

        answer = [
            (26, 40, 185, 30, 255),
            (3, 80, 280, 30, 390),
            (5, 0, 30, 30, 60),
            (11, 0, 150, 30, 180),
            (66, 360, 330, 90, 780),
            (68, 0, 90, 90, 180),
            (66, 0, 90, 90, 180),
            (63, 40, 320, 90, 450),
            (59, 40, 230, 90, 360),
            (54, 40, 140, 90, 270),
            (56, 0, 90, 90, 180),
            (57, 0, 0, 90, 90),
            (58, 40, 320, 90, 450),
            (4, 280, 140, 30, 450),
            (5, 0, 0, 30, 30),
        ]
        # python disk.py -c -a 66,26,3,5,68,11,66,59,54,56,57,63,4,58,5 -r 0.4 -n 10 -t 3 -w 6 -z 30,30,30,60,60,60,90,90,90,90 -p VR

        disk = Disk(
            self.addr,
            self.addrDesc,
            self.lateAddr,
            self.lateAddrDesc,
            self.policy,
            self.seekSpeed,
            self.rotateSpeed,
            self.skew,
            self.window,
            self.compute,
            self.graphics,
            self.zoning,
            self.armTrack,
            self.numTracks,
            self.initialDir,
            self.rValue,
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_5", 20, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 5 failed\n" + fail_message
        )

    def test_case_6(self):
        # Test Case 1
        self.addr = "1,90,25,71,61,48,9,36,57,17,70,60,33,90,84,30,109,117,97,56,37,87,107,21,56"
        self.window = 6
        self.numTracks = 10
        self.armTrack = 5
        self.zoning = "30" + ",30" * (self.numTracks - 1)
        # python disk.py -c -t 5 -n 10 -p VR -a 1,90,25,71,61,48,9,36,57,17,70,60,33,90,84,30,109,117,97,56,37,87,107,21,56 -w 6

        answer = [
            (71, 0, 135, 30, 165),
            (61, 0, 30, 30, 60),
            (48, 40, 260, 30, 330),
            (25, 80, 280, 30, 390),
            (1, 80, 250, 30, 360),
            (90, 280, 200, 30, 510),
            (70, 80, 10, 30, 120),
            (60, 0, 30, 30, 60),
            (57, 40, 200, 30, 270),
            (36, 40, 20, 30, 90),
            (17, 80, 40, 30, 150),
            (9, 40, 50, 30, 120),
            (33, 80, 250, 30, 360),
            (30, 0, 240, 30, 270),
            (90, 200, 130, 30, 360),
            (84, 0, 150, 30, 180),
            (109, 80, 280, 30, 390),
            (117, 0, 210, 30, 240),
            (97, 40, 50, 30, 120),
            (107, 0, 270, 30, 300),
            (87, 40, 50, 30, 120),
            (56, 120, 0, 30, 150),
            (37, 40, 80, 30, 150),
            (21, 80, 130, 30, 240),
            (56, 120, 180, 30, 330),
        ]

        disk = Disk(
            self.addr,
            self.addrDesc,
            self.lateAddr,
            self.lateAddrDesc,
            self.policy,
            self.seekSpeed,
            self.rotateSpeed,
            self.skew,
            self.window,
            self.compute,
            self.graphics,
            self.zoning,
            self.armTrack,
            self.numTracks,
            self.initialDir,
            self.rValue,
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_6", 20, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 1 failed\n" + fail_message
        )

    def test_case_7(self):
        # Test Case 2
        self.addr = (
            "56,78,79,17,1,44,32,97,82,72,66,79,17,52,19,108,7,98,8,82,40,48,101,2,7"
        )
        self.window = 7
        self.numTracks = 10
        self.armTrack = 9
        self.rValue = 1
        self.zoning = "30" + ",30" * (self.numTracks - 1)
        # python disk.py -c -t 9 -n 10 -p VR -r 1 -a 56,78,79,17,1,44,32,97,82,72,66,79,17,52,19,108,7,98,8,82,40,48,101,2,7 -w 7

        answer = [
            (78, 120, 225, 30, 375),
            (79, 0, 0, 30, 30),
            (56, 80, 280, 30, 390),
            (44, 40, 290, 30, 360),
            (32, 40, 290, 30, 360),
            (17, 40, 200, 30, 270),
            (1, 40, 170, 30, 240),
            (17, 40, 50, 30, 120),
            (52, 120, 180, 30, 330),
            (66, 40, 350, 30, 420),
            (82, 40, 50, 30, 120),
            (72, 0, 30, 30, 60),
            (79, 0, 180, 30, 210),
            (97, 80, 70, 30, 180),
            (98, 0, 0, 30, 30),
            (108, 40, 230, 30, 300),
            (82, 120, 150, 30, 300),
            (40, 120, 30, 30, 180),
            (19, 80, 340, 30, 450),
            (7, 40, 290, 30, 360),
            (8, 0, 0, 30, 30),
            (2, 0, 150, 30, 180),
            (7, 0, 120, 30, 150),
            (48, 160, 320, 30, 510),
            (101, 160, 320, 30, 510),
        ]

        disk = Disk(
            self.addr,
            self.addrDesc,
            self.lateAddr,
            self.lateAddrDesc,
            self.policy,
            self.seekSpeed,
            self.rotateSpeed,
            self.skew,
            self.window,
            self.compute,
            self.graphics,
            self.zoning,
            self.armTrack,
            self.numTracks,
            self.initialDir,
            self.rValue,
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_7", 30, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 2 failed\n" + fail_message
        )

    def test_case_8(self):
        # Test Case 3
        self.addr = "101,90,50,31,18,48,94,36,57,27,108,56,33,90,74,30,109,117,97,108,37,87,107,82,56"
        self.numTracks = 10
        self.armTrack = 0
        self.skew = 1
        self.initialDir = 0
        self.window = 5
        self.rValue = 0.6
        self.zoning = "30" + ",30" * (self.numTracks - 1)
        answer = [
            (18, 40, 335, 30, 405),
            (31, 40, 350, 30, 420),
            (50, 80, 160, 30, 270),
            (90, 120, 60, 30, 210),
            (101, 40, 290, 30, 360),
            (94, 40, 50, 30, 120),
            (48, 120, 180, 30, 330),
            (57, 0, 240, 30, 270),
            (36, 40, 350, 30, 420),
            (27, 40, 350, 30, 420),
            (33, 0, 150, 30, 180),
            (56, 80, 280, 30, 390),
            (74, 80, 130, 30, 240),
            (90, 40, 80, 30, 150),
            (108, 80, 130, 30, 240),
            (109, 0, 0, 30, 30),
            (117, 0, 210, 30, 240),
            (108, 0, 60, 30, 90),
            (97, 40, 290, 30, 360),
            (30, 240, 60, 30, 330),
            (37, 40, 170, 30, 240),
            (56, 40, 170, 30, 240),
            (82, 80, 10, 30, 120),
            (87, 40, 110, 30, 180),
            (107, 40, 200, 30, 270),
        ]
        # python disk.py -c -t 0 -n 10 -p VR -r 0.6 -a 101,90,50,31,18,48,94,36,57,27,108,56,33,90,74,30,109,117,97,108,37,87,107,82,56 -i 0 -o 1 -w 5

        disk = Disk(
            self.addr,
            self.addrDesc,
            self.lateAddr,
            self.lateAddrDesc,
            self.policy,
            self.seekSpeed,
            self.rotateSpeed,
            self.skew,
            self.window,
            self.compute,
            self.graphics,
            self.zoning,
            self.armTrack,
            self.numTracks,
            self.initialDir,
            self.rValue,
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_8", 30, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 3 failed\n" + fail_message
        )

    def test_case_9(self):
        # Test Case 4
        self.addr = (
            "26,59,40,66,68,7,1,92,28,25,109,51,92,52,70,16,69,95,57,81,73,7,83,65,33"
        )
        self.numTracks = 15
        self.window = 6
        self.armTrack = 5
        self.skew = 1
        self.rValue = 0.3
        self.zoning = "30,30,30,30,30,60,60,60,60,60,90,90,90,90,90"
        # python disk.py -c -t 5 -n 15 -p VR -r 0.3 -a 26,59,40,66,68,7,1,92,28,25,109,51,92,52,70,16,69,95,57,81,73,7,83,65,33 -o 1 -z 30,30,30,30,30,60,60,60,60,60,90,90,90,90,90 -w 6
        answer = [
            (66, 40, 110, 60, 210),
            (68, 0, 60, 60, 120),
            (59, 80, 205, 30, 315),
            (40, 40, 50, 30, 120),
            (26, 40, 200, 30, 270),
            (7, 80, 340, 30, 450),
            (1, 0, 150, 30, 180),
            (28, 80, 40, 30, 150),
            (25, 0, 240, 30, 270),
            (51, 80, 10, 30, 120),
            (92, 240, 210, 90, 540),
            (109, 160, 200, 90, 450),
            (95, 120, 60, 90, 270),
            (92, 40, 230, 90, 360),
            (70, 160, 5, 60, 225),
            (69, 0, 240, 60, 300),
            (52, 80, 295, 30, 405),
            (16, 120, 120, 30, 270),
            (7, 40, 350, 30, 420),
            (57, 160, 350, 30, 540),
            (65, 40, 125, 60, 225),
            (73, 80, 100, 60, 240),
            (81, 40, 80, 60, 180),
            (83, 0, 60, 60, 120),
            (33, 240, 345, 30, 615),
        ]

        disk = Disk(
            self.addr,
            self.addrDesc,
            self.lateAddr,
            self.lateAddrDesc,
            self.policy,
            self.seekSpeed,
            self.rotateSpeed,
            self.skew,
            self.window,
            self.compute,
            self.graphics,
            self.zoning,
            self.armTrack,
            self.numTracks,
            self.initialDir,
            self.rValue,
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_9", 50, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 4 failed\n" + fail_message
        )

    def test_case_10(self):
        # Test Case 5
        self.addr = "92,83,46,28,56,44,86,33,52,64,99,55,31,83,68,27,100,108,89,99,34,80,98,75,51,11,47,67,100,106,52,95,28,88,60,1,79,43,90,73"
        self.numTracks = 15
        self.window = 9
        self.armTrack = 9
        self.skew = 2
        self.initialDir = 0
        self.rValue = 0.1
        self.zoning = "30,30,30,30,30,60,60,60,60,60,90,90,90,90,90"
        # python disk.py -c -t 9 -n 15 -p VR -r 0.1 -a 92,83,46,28,56,44,86,33,52,64,99,55,31,83,68,27,100,108,89,99,34,80,98,75,51,11,47,67,100,106,52,95,28,88,60,1,79,43,90,73 -o 2 -z 30,30,30,30,30,60,60,60,60,60,90,90,90,90,90 -w 9 -i 0
        answer = [
            (86, 0, 270, 60, 330),
            (83, 40, 320, 60, 420),
            (92, 80, 205, 90, 375),
            (56, 240, 0, 30, 270),
            (52, 0, 210, 30, 240),
            (46, 40, 50, 30, 120),
            (44, 0, 270, 30, 300),
            (28, 40, 110, 30, 180),
            (33, 0, 120, 30, 150),
            (31, 0, 270, 30, 300),
            (27, 0, 210, 30, 240),
            (55, 80, 130, 30, 240),
            (64, 40, 305, 60, 405),
            (68, 40, 260, 60, 360),
            (83, 80, 280, 60, 420),
            (99, 160, 35, 90, 285),
            (100, 0, 0, 90, 90),
            (108, 80, 190, 90, 360),
            (99, 80, 100, 90, 270),
            (98, 0, 180, 90, 270),
            (89, 120, 105, 60, 285),
            (80, 40, 320, 60, 420),
            (75, 40, 200, 60, 300),
            (51, 120, 225, 30, 375),
            (47, 40, 110, 30, 180),
            (34, 40, 200, 30, 270),
            (11, 80, 160, 30, 270),
            (1, 0, 30, 30, 60),
            (28, 80, 100, 30, 210),
            (52, 80, 10, 30, 120),
            (60, 40, 155, 60, 255),
            (67, 40, 80, 60, 180),
            (88, 120, 0, 60, 180),
            (95, 80, 235, 90, 405),
            (100, 40, 140, 90, 270),
            (106, 80, 10, 90, 180),
            (90, 160, 110, 90, 360),
            (79, 80, 145, 60, 285),
            (73, 40, 140, 60, 240),
            (43, 160, 5, 30, 195),
        ]

        disk = Disk(
            self.addr,
            self.addrDesc,
            self.lateAddr,
            self.lateAddrDesc,
            self.policy,
            self.seekSpeed,
            self.rotateSpeed,
            self.skew,
            self.window,
            self.compute,
            self.graphics,
            self.zoning,
            self.armTrack,
            self.numTracks,
            self.initialDir,
            self.rValue,
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_10", 50, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 5 failed\n" + fail_message
        )


# If this script is executed directly, run the tests
if __name__ == "__main__":
    unittest.main(exit=False)

    # iterate from 1 to 10 and if test_case_i is not in scores, add it with 0
    for i in range(1, 11):
        if "test_case_" + str(i) not in scores["scores"]:
            scores["scores"]["test_case_" + str(i)] = 0

    print(json.dumps({"_presentation": "semantic"}, separators=(',', ': ')))
    print(json.dumps(scores, separators=(',', ': ')))
