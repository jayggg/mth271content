import os
from git import Repo

# Put your local folder name here: 

coursefolder = '/Users/Jay/tmpdir/'

# Update or Clone:

mth271 = os.path.join(os.path.abspath(coursefolder), 'mth271content')
if os.path.isdir(mth271):       # if repo exists, pull newest data 
    print('Checking if there are recent changes and updating')
    repo = Repo(mth271) 
    repo.remotes.origin.pull()
else:                           # otherwise, clone from remote
    print('Cloning a fresh local copy')
    repo = Repo.clone_from('https://github.com/jayggg/mth271content', mth271)

