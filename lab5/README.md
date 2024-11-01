# Lab 5:

## Background
- Great [tutorial](https://www.youtube.com/watch?v=WfV-3B27nPU) on getting started with nfs
- [Blog](https://www.admin-magazine.com/HPC/Articles/Useful-NFS-Options-for-Tuning-and-Management) on tuning nfs for performance
- Nfs man [page](https://linux.die.net/man/5/nfs)
- How to setup nfs [cache](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/storage_administration_guide/fscachenfs)

## Question
- Setup a nfs server and 2 nfs clients among 3 different machines
- To measure the latency of receiving a file you can time it using the `time` command in linux
- Client1 should ask for a 100-500 MB text file from the server, note down the latency
- Now client1 and client2 should simultaneously ask for the same text file from the server, note down the latency
- Repeat the above steps for a 10-50 MB image and 100-500 MB video file
- Try to tune the nfs server for better performance
  - change `wsize` and `rsize` parameters
  - change between sync and async
  - setup `FS-cache`
  - note down latency changes
- Now repeat the same for a 1-10 KB text file and 10-50 KB image file.
- What were the differences in parameter values for performance tuning between the MBs and KBs files?
- Set `lookupcache=none` (does not use cache) in the configuration for clients and observe performance difference for the files. Make sure to drop the existing caches before doing this to see a difference

## Cleanup After Viva
- Make sure you re-enable firewalls and other security measures that may have been needed to be disabled for this
- Remove the nfs server and client configs