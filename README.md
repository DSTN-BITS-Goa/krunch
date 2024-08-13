# README

1. `git clone --bare https://github.com/DSTN-BITS-Goa/krunch.git krunch-public-temp`
2. `cd krunch-public-temp`
3. `git push <YOUR_REPO_GIT_LINK> main`
4. `cd .. && rm -rf krunch-public-temp`
5. `git clone <YOUR_REPO_GIT_LINK>`
OPEN your repo
6. `git remote add public https://github.com/DSTN-BITS-Goa/krunch.git`
7. `git remote add origin <YOUR_REPO_GIT_LINK>`
8. `git remote -v`
9. `git pull public main`

Disable GhA