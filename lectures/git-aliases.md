### Git shortcuts

You can add the following into your `~/.gitconfig` file and after that you can use
`git co` to do `git checkout` and so on.

```text
[alias]
  co = checkout
  ci = commit
  st = status
  br = branch
  hist = log --pretty=format:\"%h %ad | %s%d [%an]\" --graph --date=short
  type = cat-file -t
  dump = cat-file -p
```
**Or**, you can add the following to your `~/.bash_aliases` file.
I do both to get double advantage!

```bash
# git shortcuts
alias gpull="git pull"
alias gpu="git pull --rebase"
alias gpush="git push"
alias glog="git log"
alias gst="git status"
alias gdf="git diff"
alias gct="git checkout"
```


#### Add git branch to your bash prompt.
Add this to your `~/.bashrc` file.

```bash

function git-branch-name {
  git symbolic-ref HEAD 2>/dev/null | cut -d"/" -f 3
}

function git-branch-prompt {
  local branch=`git-branch-name`
  if [ $branch ]; then printf " [%s]" $branch; fi
}
if [ "$PS1" ]; then
    set -o notify # Report change in job status
    export PS2="---> "
    # export PS1="[\u@\h] (\#)\$ " # Set our prompt (man bash for more info)
    # the line below will generate a very colorful prompt for those who
    # like such things
    export PS1="\[\033[01;31m\][\u@\h: \[\033[1;33m\]\$(PWD)]\[\033[0;32m\]\$(git-branch-prompt)\$ \[\033[00m\]"
fi;

```