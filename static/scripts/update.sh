#!/bin/sh

git rebase master


#!/bin/sh

# Check if params are enough to go ahead.
remoteBranch=$1
test -z "$remoteBranch" && echo "ERROR: Please provide the source remote branch." 1>&2 && exit 1

# Find which is your current branch
if currentBranch=$(git symbolic-ref --short -q HEAD)
then
    echo On branch "$currentBranch"
    echo "Pulling updates from the remote branch $remoteBranch ..."

    # Stash current changes
    git stash
    # Checkout remote branch from where you want to update.
    git checkout "$remoteBranch"
    # Pull the branch to update it
    git pull --rebase origin "$remoteBranch"
    # Checkout current branch which you were on before.
    git checkout "$currentBranch"
    # Rebase the changes
    git rebase "$remoteBranch"
    # Apply the stashed changes
    git stash apply

    echo "Updated the $currentBranch with changes from $remoteBranch"
else
    echo ERROR: Cannot find the current branch!
fi