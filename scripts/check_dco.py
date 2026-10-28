"""Fail when a commit in a range has no DCO sign-off. Standard library only.

Usage: python scripts/check_dco.py <base-ref> [<head-ref>]

Every commit between base and head (merge commits excepted) must carry a line
  Signed-off-by: Name <email>
whose email matches the commit author's email. See CONTRIBUTING.md.
Exit 0 when every commit is signed off, 1 when any is not (each one named).
"""
import re
import subprocess
import sys


def git(*args):
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    base = sys.argv[1]
    head = sys.argv[2] if len(sys.argv) > 2 else "HEAD"
    shas = git("rev-list", "--no-merges", f"{base}..{head}").split()
    missing = []
    for sha in shas:
        email = git("show", "-s", "--format=%ae", sha).strip().lower()
        body = git("show", "-s", "--format=%B", sha)
        signers = [e.lower() for e in re.findall(r"^Signed-off-by: .+ <([^>]+)>\s*$", body, re.M)]
        if email not in signers:
            subject = git("show", "-s", "--format=%s", sha).strip()
            missing.append(f"{sha[:7]} {subject} (author {email})")
    if missing:
        print(f"DCO CHECK FAILED: {len(missing)} of {len(shas)} commit(s) not signed off")
        for line in missing:
            print("  x " + line)
        print("Fix: git commit --amend -s (last commit) or git rebase --signoff <base> (several), then push again.")
        sys.exit(1)
    print(f"DCO check passed: {len(shas)} commit(s) signed off.")


if __name__ == "__main__":
    main()
