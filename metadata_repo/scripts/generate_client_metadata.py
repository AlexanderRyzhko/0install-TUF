'''
Script to created the TUF client directory
'''

from tuf.libtuf import *

# The following function creates a directory structure that a client 
# downloading new software using TUF (via tuf/client/updater.py) will expect.
# The root.txt metadata file must exist, and also the directories that hold the metadata files
# downloaded from a repository.  Software updaters integrating with TUF may use this
# directory to store TUF updates saved on the client side.  create_tuf_client_directory()
# moves metadata from "path/to/repository/metadata" to "path/to/client/".  The repository
# in "path/to/repository/" is the repository created in the "Create TUF Repository" section.
create_tuf_client_directory("path/to/repository/", "path/to/client/")
