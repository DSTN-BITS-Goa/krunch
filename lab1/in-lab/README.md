# Lab 1: In Lab

## Usage

To test your solution:

```bash
python test.py
```

To run the eval script:

```bash
python autograde.py
```

## Question

Add an implementation of the [$V(R)$](https://dl.acm.org/doi/pdf/10.1145/7351.8929) algorithm to [`disk.py`](disk.py)
Ensure that the code works with the various options available

### V(R) Algorithm Explained

- V(R) maintains the current direction of the disk head (inwards/outwards).
- V(R) services the next known request with the smallest effective distance.
- **Effective distance**:
  1. The effective distance of a request that lies in the current head direction is its physical distance (in tracks) from the current position of the read/write head (in tracks).
  2. The effective distance of a request that does NOT lie in the current head direction is its $\text{Physical distance} + R * (\text{Total number of tracks on the disk})$
- $R$ is a real number between $0$ and $1$ (inclusive).
- In case two requests are located on the same track preserve the original request ordering.

> **Note**
>
> For $R = 0$, V(R) behaves identically to $SSTF$.
> For $R = 1$, V(R) behaves identically to $LOOK$.

### Command-line Options

The program should be able to run with the following command line options:

- `-p VR` to select the V(R) policy
- `-r R` to specify the R value for the V(R) policy. This has already been implemented as a part of `parser` in [`disk.py`](disk.py)

### Example

For the following command:

```console
python disk.py -c -a 5,8,17,57,52,3 -w 3 -n 5 -p VR -r 0.3
```

The requests should be processed in the order $[5,8,17,3,57,52]$.

`initialDir` is $1$ (inward) and the starting track is $0$ by default.

- The first window which consists of $[5, 8, 17]$:
  - the effective distance of $d(5) = 0 = d(8)$, so they are processed first.
  - After this the effective distance of $d(17) = 1$ because $17$ is in the same direction as the initial direction (inwards).
- The second window which consists of $[57,52,3]$:
  - The effective distance of $d(57) = 3 = d(52)$ whereas the effective distance of $d(3) = 2.5$ because its in the opposite direction.
  - Since $3$ has the smaller effective distance its processed first which is then followed by $57, 52$.

> **Note**
>
> $d(x) = y$ means the effective distance of sector $x$ is $y$.
