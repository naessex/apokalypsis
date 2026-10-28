# Contributing to Apokalypsis

Thank you for helping. This page covers the three rules every pull request follows.

## 1. Sign off every commit (DCO)

Apokalypsis uses the [Developer Certificate of Origin](https://developercertificate.org/)
instead of a contributor license agreement. A sign-off states that you wrote the change,
or have the right to submit it, under the project's Apache 2.0 license.

Add the sign-off with the `-s` flag:

```
git commit -s -m "Describe the change"
```

That adds a line like `Signed-off-by: Your Name <you@example.com>` to the commit message.
The email must match the commit's author email. The `dco` check fails any pull request
that has a commit without it.

To fix a commit you already made:

```
git commit --amend -s          # the last commit
git rebase --signoff main      # every commit on your branch
```

Then push again with `git push --force-with-lease`.

## 2. Keep the clean room

Apokalypsis is influenced by another learning method that is licensed under the AGPL.
Never copy code, text or files from another project into this one. Write from the idea,
not from the source. `CLEAN-ROOM.md` gives the full rules once it is added.

## 3. One change per pull request

Keep each pull request to one change, describe what it does, and make sure the
`pr-check` and `dco` checks pass. Write in U.S. English.
