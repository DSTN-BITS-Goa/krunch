import unittest

# Import the Disk class from both implementations
from disk import Disk


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
        self.assertEqual(
            disk.getBlockStats(), answer, "Test Case 5 failed\n" + fail_message
        )


# If this script is executed directly, run the tests
if __name__ == "__main__":
    unittest.main()
