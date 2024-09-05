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
        self.policy = "CLOOK"
        self.seekSpeed = 1
        self.rotateSpeed = 1
        self.numTracks = 3
        self.armTrack = 0
        self.initialDir = 1
        self.zoning = "30,30,30"

    def get_fail_message(self, expected, actual):
        return "Expected: " + str(expected) + "\nActual: " + str(actual)

    def update_scores(self, test_case, score, expr1, expr2):
        if expr1 == expr2:
            scores["scores"][test_case] = score
        else:
            scores["scores"][test_case] = 0

    def test_case_1(self):
        # Test Case 1
        self.addr = "3,34,18,17,1,30,19"
        answer = [
            (3, 0, 255, 30, 285),
            (1, 0, 270, 30, 300),
            (18, 40, 80, 30, 150),
            (17, 0, 300, 30, 330),
            (19, 0, 30, 30, 60),
            (34, 40, 20, 30, 90),
            (30, 0, 210, 30, 240),
        ]
        # python disk.py -c -a 3,34,18,17,1,30,19 -p CLOOK

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
        )

        disk.Go()

        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_1", 10, disk.getBlockStats(), answer)

        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 1 failed\n" + fail_message
        )

    def test_case_2(self):
        # Test Case 2
        self.addr = "30,18,13,17,1,16"
        self.window = 3
        answer = [
            (18, 40, 305, 30, 375),
            (13, 0, 180, 30, 210),
            (30, 40, 80, 30, 150),
            (1, 80, 100, 30, 210),
            (17, 40, 50, 30, 120),
            (16, 0, 300, 30, 330),
        ]
        # python disk.py -c -a 30,18,13,17,1,16 -w 3 -p CLOOK

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
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_2", 10, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 2 failed\n" + fail_message
        )

    def test_case_3(self):
        # Test Case 3
        self.addr = "50,40,1,10,23,36,28,13,8,4"
        self.armTrack = 2
        self.numTracks = 5
        self.initialDir = 0
        self.seekSpeed = 0.5
        self.rotateSpeed = 4
        self.zoning = "30" + ",30" * (self.numTracks - 1)
        answer = [
            (28, 0, 71, 7, 78),
            (23, 80, 55, 8, 143),
            (13, 0, 7, 8, 15),
            (1, 80, 2, 8, 90),
            (10, 0, 60, 7, 67),
            (8, 0, 68, 7, 75),
            (4, 0, 53, 7, 60),
            (50, 320, 18, 7, 345),
            (40, 80, 18, 7, 105),
            (36, 0, 53, 7, 60),
        ]
        # python disk.py -c -a 50,40,1,10,23,36,28,13,8,4 -t 2 -n 5 -i 0 -p CLOOK -S 0.5 -R 4

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
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_3", 10, disk.getBlockStats(), answer)

        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 3 failed\n" + fail_message
        )

    def test_case_4(self):
        # Test Case 4
        self.addr = "16,40,37,9,38,28,1,41,11,13,18,25"
        self.window = 5
        self.numTracks = 6
        self.armTrack = 5
        self.zoning = "30,30,60,60,90,90"
        # python disk.py -c -t 5 -n 6 -p CLOOK -z 30,30,60,60,90,90 -a 16,40,37,9,38,28,1,41,11,13,18,25 -w 5

        answer = [
            (40, 0, 135, 90, 225),
            (9, 200, 10, 30, 240),
            (16, 40, 140, 30, 210),
            (37, 120, 150, 90, 360),
            (38, 0, 0, 90, 90),
            (41, 40, 140, 90, 270),
            (1, 200, 40, 30, 270),
            (11, 0, 270, 30, 300),
            (13, 40, 350, 30, 420),
            (28, 40, 125, 60, 225),
            (25, 0, 120, 60, 180),
            (18, 40, 35, 30, 105),
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
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_4", 10, disk.getBlockStats(), answer)

        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 4 failed\n" + fail_message
        )

    def test_case_5(self):
        # Test Case 5
        self.addr = "17,39,26,43,45,4,0,60,18,16"
        self.numTracks = 6
        self.armTrack = 1
        self.skew = 1
        self.initialDir = 0
        self.zoning = "30" + ",30" * (self.numTracks - 1)
        answer = [
            (17, 0, 345, 30, 375),
            (18, 0, 0, 30, 30),
            (16, 0, 270, 30, 300),
            (4, 40, 260, 30, 330),
            (0, 0, 210, 30, 240),
            (60, 200, 280, 30, 510),
            (39, 80, 280, 30, 390),
            (43, 0, 90, 30, 120),
            (45, 0, 30, 30, 60),
            (26, 40, 50, 30, 120),
        ]
        # python disk.py -c -t 1 -n 6 -p CLOOK -a 17,39,26,43,45,4,0,60,18,16 -i 0 -o 1

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
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_5", 20, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 5 failed\n" + fail_message
        )

    def test_case_6(self):
        # Test Case 6
        self.addr = "43,51,25,65,11,64,2,32,66,45,63,7,32,17"
        self.numTracks = 10
        self.window = 6
        self.armTrack = 3
        self.skew = 1
        self.zoning = "30,30,30,60,60,60,90,90,90,90"
        # python disk.py -c -t 3 -n 10 -p CLOOK -a 43,51,25,65,11,64,2,32,66,45,63,7,32,17 -o 1 -z 30,30,30,60,60,60,90,90,90,90 -w 6
        answer = [
            (43, 40, 50, 60, 150),
            (51, 40, 80, 60, 180),
            (65, 120, 315, 90, 525),
            (64, 0, 180, 90, 270),
            (11, 320, 130, 30, 480),
            (25, 80, 10, 30, 120),
            (32, 0, 180, 30, 210),
            (45, 80, 355, 60, 495),
            (63, 160, 155, 90, 405),
            (66, 40, 230, 90, 360),
            (2, 360, 270, 30, 660),
            (7, 0, 120, 30, 150),
            (17, 40, 260, 30, 330),
            (32, 40, 50, 30, 120),
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
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_6", 20, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 6 failed\n" + fail_message
        )

    def test_case_7(self):
        # Test Case 7
        self.addr = "1,90,25,71,61,48,9,36,57,17,70,60,33,90,84,30,109,117,97,56,37,87,107,21,56"
        self.window = 6
        self.numTracks = 10
        self.armTrack = 5
        self.zoning = "30" + ",30" * (self.numTracks - 1)
        # python disk.py -c -t 5 -n 10 -p CLOOK -a 1,90,25,71,61,48,9,36,57,17,70,60,33,90,84,30,109,117,97,56,37,87,107,21,56 -w 6

        answer = [
            (71, 0, 135, 30, 165),
            (61, 0, 30, 30, 60),
            (90, 80, 40, 30, 150),
            (1, 280, 260, 30, 570),
            (25, 80, 250, 30, 360),
            (48, 80, 220, 30, 330),
            (57, 0, 240, 30, 270),
            (70, 40, 320, 30, 390),
            (60, 0, 30, 30, 60),
            (9, 200, 40, 30, 270),
            (17, 40, 170, 30, 240),
            (36, 80, 100, 30, 210),
            (90, 160, 350, 30, 540),
            (84, 0, 150, 30, 180),
            (109, 80, 280, 30, 390),
            (117, 0, 210, 30, 240),
            (33, 280, 50, 30, 360),
            (30, 0, 240, 30, 270),
            (37, 40, 140, 30, 210),
            (56, 40, 140, 30, 210),
            (87, 120, 60, 30, 210),
            (97, 40, 230, 30, 300),
            (107, 0, 270, 30, 300),
            (21, 280, 350, 30, 660),
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
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())
        self.update_scores("test_case_7", 20, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 7 failed\n" + fail_message
        )

    def test_case_8(self):
        # Test Case 8
        self.addr = (
            "56,78,79,17,1,44,32,97,82,72,66,79,17,52,19,108,7,98,8,82,40,48,101,2,7"
        )
        self.window = 7
        self.numTracks = 10
        self.armTrack = 9
        self.zoning = "30" + ",30" * (self.numTracks - 1)
        # python disk.py -c -t 9 -n 10 -p CLOOK -a 56,78,79,17,1,44,32,97,82,72,66,79,17,52,19,108,7,98,8,82,40,48,101,2,7 -w 7

        answer = [
            (1, 360, 195, 30, 585),
            (17, 40, 50, 30, 120),
            (32, 40, 20, 30, 90),
            (44, 40, 290, 30, 360),
            (56, 40, 290, 30, 360),
            (78, 80, 190, 30, 300),
            (79, 0, 0, 30, 30),
            (82, 0, 60, 30, 90),
            (72, 0, 30, 30, 60),
            (79, 0, 180, 30, 210),
            (97, 80, 70, 30, 180),
            (17, 280, 170, 30, 480),
            (52, 120, 180, 30, 330),
            (66, 40, 350, 30, 420),
            (82, 40, 50, 30, 120),
            (98, 80, 10, 30, 120),
            (108, 40, 230, 30, 300),
            (7, 360, 180, 30, 570),
            (8, 0, 0, 30, 30),
            (19, 40, 260, 30, 330),
            (40, 80, 160, 30, 270),
            (48, 40, 170, 30, 240),
            (101, 160, 320, 30, 510),
            (2, 320, 280, 30, 630),
            (7, 0, 120, 30, 150),
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
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_8", 30, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 8 failed\n" + fail_message
        )

    def test_case_9(self):
        # Test Case 9
        self.addr = "101,90,50,31,18,48,94,36,57,27,108,56,33,90,74,30,109,117,97,108,37,87,107,82,56"
        self.numTracks = 10
        self.armTrack = 0
        self.skew = 1
        self.initialDir = 0
        self.window = 5
        self.zoning = "30" + ",30" * (self.numTracks - 1)
        answer = [
            (101, 320, 235, 30, 585),
            (90, 40, 290, 30, 360),
            (50, 120, 0, 30, 150),
            (31, 80, 340, 30, 450),
            (18, 40, 230, 30, 300),
            (94, 240, 30, 30, 300),
            (48, 120, 180, 30, 330),
            (57, 0, 240, 30, 270),
            (36, 40, 350, 30, 420),
            (27, 40, 350, 30, 420),
            (33, 0, 150, 30, 180),
            (108, 280, 350, 30, 660),
            (90, 80, 10, 30, 120),
            (74, 40, 140, 30, 210),
            (56, 80, 10, 30, 120),
            (30, 80, 130, 30, 240),
            (109, 280, 110, 30, 420),
            (117, 0, 210, 30, 240),
            (108, 0, 60, 30, 90),
            (97, 40, 290, 30, 360),
            (107, 0, 270, 30, 300),
            (87, 40, 20, 30, 90),
            (82, 40, 110, 30, 180),
            (56, 80, 130, 30, 240),
            (37, 40, 50, 30, 120),
        ]
        # python disk.py -c -t 0 -n 10 -p CLOOK -a 101,90,50,31,18,48,94,36,57,27,108,56,33,90,74,30,109,117,97,108,37,87,107,82,56 -i 0 -o 1 -w 5

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
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_9", 30, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 9 failed\n" + fail_message
        )

    def test_case_10(self):
        # Test Case 10
        self.addr = (
            "26,59,40,66,68,7,1,92,28,25,109,51,92,52,70,16,69,95,57,81,73,7,83,65,33"
        )
        self.numTracks = 15
        self.window = 6
        self.armTrack = 5
        self.skew = 1
        self.zoning = "30,30,30,30,30,60,60,60,60,60,90,90,90,90,90"
        # python disk.py -c -t 5 -n 15 -p CLOOK -a 26,59,40,66,68,7,1,92,28,25,109,51,92,52,70,16,69,95,57,81,73,7,83,65,33 -o 1 -z 30,30,30,30,30,60,60,60,60,60,90,90,90,90,90 -w 6
        answer = [
            (66, 40, 110, 60, 210),
            (68, 0, 60, 60, 120),
            (7, 240, 165, 30, 435),
            (26, 80, 160, 30, 270),
            (40, 40, 20, 30, 90),
            (59, 40, 170, 30, 240),
            (51, 0, 90, 30, 120),
            (92, 240, 210, 90, 540),
            (109, 160, 200, 90, 450),
            (1, 560, 40, 30, 630),
            (28, 80, 40, 30, 150),
            (25, 0, 240, 30, 270),
            (52, 80, 40, 30, 150),
            (70, 80, 235, 60, 375),
            (69, 0, 240, 60, 300),
            (92, 160, 305, 90, 555),
            (95, 40, 230, 90, 360),
            (16, 400, 50, 30, 480),
            (57, 120, 90, 30, 240),
            (65, 40, 125, 60, 225),
            (73, 80, 100, 60, 240),
            (81, 40, 80, 60, 180),
            (83, 0, 60, 60, 120),
            (7, 320, 145, 30, 495),
            (33, 80, 10, 30, 120),
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
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_10", 50, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 10 failed\n" + fail_message
        )

    def test_case_11(self):
        # Test Case 11
        self.addr = "92,83,46,28,56,44,86,33,52,64,99,55,31,83,68,27,100,108,89,99,34,80,98,75,51,11,47,67,100,106,52,95,28,88,60,1,79,43,90,73"
        self.numTracks = 15
        self.window = 9
        self.armTrack = 9
        self.skew = 2
        self.initialDir = 0
        self.zoning = "30,30,30,30,30,60,60,60,60,60,90,90,90,90,90"
        # python disk.py -c -t 9 -n 15 -p CLOOK -a 92,83,46,28,56,44,86,33,52,64,99,55,31,83,68,27,100,108,89,99,34,80,98,75,51,11,47,67,100,106,52,95,28,88,60,1,79,43,90,73 -o 2 -z 30,30,30,30,30,60,60,60,60,60,90,90,90,90,90 -w 9 -i 0
        answer = [
            (86, 0, 270, 60, 330),
            (83, 40, 320, 60, 420),
            (56, 160, 95, 30, 285),
            (52, 0, 210, 30, 240),
            (46, 40, 50, 30, 120),
            (44, 0, 270, 30, 300),
            (28, 40, 110, 30, 180),
            (33, 0, 120, 30, 150),
            (92, 320, 130, 90, 540),
            (83, 80, 205, 60, 345),
            (68, 80, 160, 60, 300),
            (64, 40, 260, 60, 360),
            (55, 40, 245, 30, 315),
            (31, 80, 130, 30, 240),
            (27, 0, 210, 30, 240),
            (108, 480, 150, 90, 720),
            (99, 80, 100, 90, 270),
            (100, 0, 0, 90, 90),
            (99, 0, 180, 90, 270),
            (98, 0, 180, 90, 270),
            (89, 120, 105, 60, 285),
            (80, 40, 320, 60, 420),
            (75, 40, 200, 60, 300),
            (51, 120, 225, 30, 375),
            (47, 40, 110, 30, 180),
            (34, 40, 200, 30, 270),
            (11, 80, 160, 30, 270),
            (1, 0, 30, 30, 60),
            (106, 560, 70, 90, 720),
            (100, 80, 10, 90, 180),
            (95, 40, 320, 90, 450),
            (88, 80, 175, 60, 315),
            (67, 120, 0, 60, 180),
            (60, 40, 80, 60, 180),
            (52, 40, 35, 30, 105),
            (28, 80, 130, 30, 240),
            (90, 320, 100, 90, 510),
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
        )

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())

        self.update_scores("test_case_11", 50, disk.getBlockStats(), answer)
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 11 failed\n" + fail_message
        )

# If this script is executed directly, run the tests
if __name__ == "__main__":
    unittest.main(exit=False)
    # iterate from 1 to 10 and if test_case_i is not in scores, add it with 0
    for i in range(1, 12):
        if "test_case_" + str(i) not in scores["scores"]:
            scores["scores"]["test_case_" + str(i)] = 0

    print(json.dumps({"_presentation": "semantic"}, separators=(',', ': ')))
    print(json.dumps(scores, separators=(',', ': ')))
