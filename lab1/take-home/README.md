# Lab 1: Take Home

## Usage

To test your solution:

```bash
python test.py
```

## Question

### Question 1

- Modify disk.py to implement the C-LOOK algorithm. The set of requests should be able to run with -p CLOOK option. In case two requests are on the same track (tie) preserve the original request ordering.
- For example python disk.py -c -a 30,18,13,17,1,16 -w 3 -p CLOOK. The requests should be processed in the order 18,13,30,1,17,16
- Make sure the code works with the various options available

### Question 2

- For the set of requests: 10,11,12,13, the default setup performs poorly. Try adding track skew to improve the performance (\-o skew), where skew is an integer.
- You are not required to submit this. This will be tested during the lab session.

1. Given the default seek rate, what should the track skew be to maximize performance?  
2. Try the same thing for different seek rates (e.g., \-S 2, \-S 4)? In general, write a mathematical formula to figure out the track skew for a given disk, if you are provided with the seek rate, rotational latency, and sectors per track? Use any additional information if required.
