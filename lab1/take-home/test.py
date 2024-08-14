import unittest

# Import the Disk class from both implementations
from disk import Disk

class TestDiskClass(unittest.TestCase):

    def setUp(self):
        # Fixed parameters
        self.addr = '-1'
        self.lateAddr = '-1'
        self.lateAddrDesc = '0,-1,0'
        self.addrDesc = '5,-1,0'
        self.graphics = False
        self.compute = True
        self.skew = 0
        self.window = -1
        self.policy = 'CLOOK'
        self.seekSpeed = 1
        self.rotateSpeed = 1
        self.numTracks = 3
        self.armTrack = 0
        self.initialDir = 1
        self.zoning = '30,30,30'

    def get_fail_message(self, expected, actual):
        return "Expected: " + str(expected) + "\nActual: " + str(actual)
    
    def test_case_1(self):
        # Test Case 1
        self.addr = '3,34,18,17,1,30,19'
        answer = [(3, 0, 255, 30, 285), (1, 0, 270, 30, 300), (18, 40, 80, 30, 150), (17, 0, 300, 30, 330), (19, 0, 30, 30, 60), (34, 40, 20, 30, 90), (30, 0, 210, 30, 240)]
        # python disk.py -c -a 3,34,18,17,1,30,19 -p CLOOK

        disk = Disk(self.addr, self.addrDesc, self.lateAddr, self.lateAddrDesc,
                      self.policy, self.seekSpeed, self.rotateSpeed, self.skew, self.window, 
                      self.compute, self.graphics, self.zoning, self.armTrack, 
                      self.numTracks, self.initialDir)

        disk.Go()

        fail_message = self.get_fail_message(answer, disk.getBlockStats())
        self.assertEqual(disk.getBlockStats(), answer, 
                         "Test Case 1 failed\n" + fail_message)

    def test_case_2(self):
        # Test Case 2
        self.addr = '30,18,13,17,1,16'
        self.window = 3
        answer = [(18, 40, 305, 30, 375), (13, 0, 180, 30, 210), (30, 40, 80, 30, 150), (1, 80, 100, 30, 210), (17, 40, 50, 30, 120), (16, 0, 300, 30, 330)]
        # python disk.py -c -a 30,18,13,17,1,16 -w 3 -p CLOOK

        disk = Disk(self.addr, self.addrDesc, self.lateAddr, self.lateAddrDesc,
                      self.policy, self.seekSpeed, self.rotateSpeed, self.skew, self.window, 
                      self.compute, self.graphics, self.zoning, self.armTrack, 
                      self.numTracks, self.initialDir)

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())
        self.assertEqual(disk.getBlockStats(), answer, 
                         "Test Case 2 failed\n" + fail_message)

    def test_case_3(self):
        # Test Case 3
        self.addr = '50,40,1,10,23,36,28,13,8,4'
        self.armTrack = 2
        self.numTracks = 5
        self.initialDir = 0
        self.seekSpeed = 0.5
        self.rotateSpeed = 4
        self.zoning = '30' + ',30' * (self.numTracks - 1)
        answer = [(28, 0, 71, 7, 78), (23, 80, 55, 8, 143), (13, 0, 7, 8, 15), (1, 80, 2, 8, 90), (10, 0, 60, 7, 67), (8, 0, 68, 7, 75), (4, 0, 53, 7, 60), (50, 320, 18, 7, 345), (40, 80, 18, 7, 105), (36, 0, 53, 7, 60)]
        # python disk.py -c -a 50,40,1,10,23,36,28,13,8,4 -t 2 -n 5 -i 0 -p CLOOK -S 0.5 -R 4

        disk = Disk(self.addr, self.addrDesc, self.lateAddr, self.lateAddrDesc,
                      self.policy, self.seekSpeed, self.rotateSpeed, self.skew, self.window, 
                      self.compute, self.graphics, self.zoning, self.armTrack, 
                      self.numTracks, self.initialDir)

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())
        self.assertEqual(disk.getBlockStats(), answer, 
                         "Test Case 3 failed\n" + fail_message)

    def test_case_4(self):
        # Test Case 4
        self.addr = '16,40,37,9,38,28,1,41,11,13,18,25'
        self.window = 5
        self.numTracks = 6
        self.armTrack = 5
        self.zoning = '30,30,60,60,90,90'
        # python disk.py -c -t 5 -n 6 -p CLOOK -z 30,30,60,60,90,90 -a 16,40,37,9,38,28,1,41,11,13,18,25 -w 5

        print(self.addr)
        answer = [(40, 0, 135, 90, 225), (9, 200, 10, 30, 240), (16, 40, 140, 30, 210), (37, 120, 150, 90, 360), (38, 0, 0, 90, 90), (41, 40, 140, 90, 270), (1, 200, 40, 30, 270), (11, 0, 270, 30, 300), (13, 40, 350, 30, 420), (28, 40, 125, 60, 225), (25, 0, 120, 60, 180), (18, 40, 35, 30, 105)]

        disk = Disk(self.addr, self.addrDesc, self.lateAddr, self.lateAddrDesc,
                      self.policy, self.seekSpeed, self.rotateSpeed, self.skew, self.window, 
                      self.compute, self.graphics, self.zoning, self.armTrack, 
                      self.numTracks, self.initialDir)

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())
        self.assertEqual(disk.getBlockStats(), answer, 
                         "Test Case 4 failed\n" + fail_message)

    def test_case_5(self):
        # Test Case 5
        self.addr = '17,39,26,43,45,4,0,60,18,16'
        self.numTracks = 6
        self.armTrack = 1
        self.skew = 1
        self.initialDir = 0
        self.zoning = '30' + ',30' * (self.numTracks - 1)
        answer = [(17, 0, 345, 30, 375), (18, 0, 0, 30, 30), (16, 0, 270, 30, 300), (4, 40, 260, 30, 330), (0, 0, 210, 30, 240), (60, 200, 280, 30, 510), (39, 80, 280, 30, 390), (43, 0, 90, 30, 120), (45, 0, 30, 30, 60), (26, 40, 50, 30, 120)]
        # python disk.py -c -t 1 -n 6 -p CLOOK -a 17,39,26,43,45,4,0,60,18,16 -i 0 -o 1

        disk = Disk(self.addr, self.addrDesc, self.lateAddr, self.lateAddrDesc,
                      self.policy, self.seekSpeed, self.rotateSpeed, self.skew, self.window, 
                      self.compute, self.graphics, self.zoning, self.armTrack, 
                      self.numTracks, self.initialDir)

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())
        self.assertEqual(disk.getBlockStats(), answer, 
                         "Test Case 5 failed\n" + fail_message)

    def test_case_6(self):
        # Test Case 6
        self.addr = '43,51,25,65,11,64,2,32,66,45,63,7,32,17'
        self.numTracks = 10
        self.window = 6
        self.armTrack = 3
        self.skew = 1
        self.zoning = '30,30,30,60,60,60,90,90,90,90'
        # python disk.py -c -t 3 -n 10 -p CLOOK -a 43,51,25,65,11,64,2,32,66,45,63,7,32,17 -o 1 -z 30,30,30,60,60,60,90,90,90,90 -w 6
        answer = [(43, 40, 50, 60, 150), (51, 40, 80, 60, 180), (65, 120, 315, 90, 525), (64, 0, 180, 90, 270), (11, 320, 130, 30, 480), (25, 80, 10, 30, 120), (32, 0, 180, 30, 210), (45, 80, 355, 60, 495), (63, 160, 155, 90, 405), (66, 40, 230, 90, 360), (2, 360, 270, 30, 660), (7, 0, 120, 30, 150), (17, 40, 260, 30, 330), (32, 40, 50, 30, 120)]

        disk = Disk(self.addr, self.addrDesc, self.lateAddr, self.lateAddrDesc,
                      self.policy, self.seekSpeed, self.rotateSpeed, self.skew, self.window, 
                      self.compute, self.graphics, self.zoning, self.armTrack, 
                      self.numTracks, self.initialDir)

        disk.Go()
        fail_message = self.get_fail_message(answer, disk.getBlockStats())
        self.assertEqual(disk.getBlockStats(), answer, 
                         "Test Case 6 failed\n" + fail_message)

# If this script is executed directly, run the tests
if __name__ == '__main__':
    unittest.main()
