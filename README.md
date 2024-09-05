# Krunch

## Students

1. \<John Doe\> (2021A7PS1234G)
2. \<Jane Doe\> (2022A7PS4321G)

**WARNING: IF YOU ARE A STUDENT IN THE CLASS, DO NOT DIRECTLY FORK THIS REPO. DO NOT PUSH PROJECT SOLUTIONS PUBLICLY. THIS IS AN ACADEMIC INTEGRITY VIOLATION AND APPROPRIATE ACTION WILL BE TAKEN.**

Starring this repo may or may not affect your grades :)

## Cloning this Repository

1. Go [here](https://github.com/new) to create a new repository under your account. The name should be `CSF446_DSTN_2024_PairX` where `X` is your Pair number. Select **Private** for the repository visibility level. Skip this step if you already have created a private repo named `CSF446_DSTN_2024_PairX`. Add the instructor and the TAs as collaborators to your private repo.

2. On your development machine, create a bare clone of the [public Krunch repository](https://github.com/DSTN-BITS-Goa/krunch):

   ```console
   git clone --bare https://github.com/DSTN-BITS-Goa/krunch.git krunch-public-temp
   ```

3. Next, [mirror](https://git-scm.com/docs/git-push#Documentation/git-push.txt---mirror) the [public Krunch repository](https://github.com/DSTN-BITS-Goa/krunch) to your own private repository. The procedure for mirroring the repository is then:

   ```console
   $ cd krunch-public-temp

   # If you pull / push over HTTPS
   $ git push https://github.com/<USERNAME>/CSF446_DSTN_2024_Pair<X>.git main

   # If you pull / push over SSH
   $ git push git@github.com:<USERNAME>/CSF446_DSTN_2024_Pair<X>.git main
   ```

   This copies everything in the [public Krunch repository](https://github.com/DSTN-BITS-Goa/krunch) to your own private repository. You can now delete your local clone of the public repository:

   ```console
   cd .. && rm -rf krunch-public-temp
   ```

4. Clone your private repository to your development machine:

   ```console
   # If you pull / push over HTTPS
   $ git clone https://github.com/<USERNAME>/CSF446_DSTN_2024_Pair<X>.git

   # If you pull / push over SSH
   $ git clone git@github.com:<USERNAME>/CSF446_DSTN_2024_Pair<X>.git
   ```

5. Add the [public Krunch repository](https://github.com/DSTN-BITS-Goa/krunch) as a second remote. This allows you to retrieve changes from the Krunch repository and merge them with your solution throughout the semester:

   ```console
   git remote add public https://github.com/DSTN-BITS-Goa/krunch.git
   git remote add origin https://github.com/<USERNAME>/CSF446_DSTN_2024_Pair<X>.git
   ```

   You can verify that the remote was added with the following command:

   ```console
   $ git remote -v
   origin https://github.com/<USERNAME>/CSF446_DSTN_2024_Pair<X>.git (fetch)
   origin https://github.com/<USERNAME>/CSF446_DSTN_2024_Pair<X>.git (push)
   public https://github.com/DSTN-BITS-Goa/krunch.git (fetch)
   public https://github.com/DSTN-BITS-Goa/krunch.git (push)
   ```

6. You can now pull in changes from the [public Krunch repository](https://github.com/DSTN-BITS-Goa/krunch) as needed with:

   ```console
   git pull public main
   ```

7. **Disable GitHub Actions** from the project settings of your private repository, otherwise you may run out of GitHub Actions quota.

   ```text
   Settings > Actions > General > Actions permissions > Disable actions.
   ```
