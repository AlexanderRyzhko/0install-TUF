'''
Script to add the target paths
Add the targets to unclaimed
'''
#from datetime import *
from tuf.libtuf import *
import distutils.core

# copy subdirectory example

path_to_server_root = raw_input("Enter the path to the server, or press enter for /var/www: ")
if(not(path_to_server_root)):
	path_to_server_root = "/var/www"

newMetaDir = path_to_server_root + "/metadata.staged"
metaDir = path_to_server_root + "/metadata"
targetsDirectory = path_to_server_root + "/targets"
path_to_f_targets = raw_input("Enter the path to futer targets, or press enter for /var/www: ")
if(not(path_to_f_targets)):
	path_to_f_targets = "/var/www"
futureTargetsDirectory = path_to_f_targets + "/future_targets"





#repo_path = "/var/www"
repo_path = path_to_server_root
#targets_path = "/var/www/targets/"
targets_path = targetsDirectory 

#keys should be off-line, example path to USB stick
path_to_target_key = "/root/keys/targets_key"
path_to_root_key = "/root/keys/root_key"
path_to_root_key2 = "/root/keys/root_key2"
path_to_release_key = "/root/keys/timestamp_key"
path_to_timestamp_key = "/root/keys/timestamp_key"

#finds current week
#week = datetime.date(datetime.now()).strftime("%U") 

#check key paths
def checkKey(path_to_key):
	temp = 1 
	key_type = path_to_key.split('/')[-1]
	while(temp):
		try:
			f = open(path_to_key)
			f.close()
			temp = 0
		except:
			print "Could not find " + key_type 
			path_to_key = raw_input("Please enter a absolute path to " + key_type  + " file: ")
	return path_to_key

path_to_target_key = checkKey(path_to_target_key)
path_to_root_key = checkKey(path_to_root_key)
path_to_root_key2 = checkKey(path_to_root_key2)
path_to_release_key = checkKey(path_to_release_key)
path_to_timestamp_key = checkKey(path_to_release_key)


#coppying new targets and metadata. Stop the service while creating new metadata!
distutils.dir_util.copy_tree(futureTargetsDirectory, targetsDirectory)


#there are 2 weeks, there 2 folders that get toggeled every week
#targets_path = targets_path + str(int(week) % 2) +'/'



# Load the repository created in the previous section.  This repository so far contains metadata for
# the top-level roles, but no targets.
repository = load_repository(repo_path)

# Get a list of file paths in a directory, even those in sub-directories.
# This must be relative to an existing directory in the repository, otherwise throw an
# error.
list_of_targets = repository.get_filepaths_in_directory(targets_path,
                                                        recursive_walk=True, followlinks=True) 

# Add the list of target paths to the metadata of the Targets role.  Any target file paths
# that may already exist are NOT replaced.  add_targets() does not create or move target files.
repository.targets.add_targets(list_of_targets)

# Individual target files may also be added.
#repository.targets.add_target("path/to/repository/targets/file3.txt")

# The private key of the updated targets metadata must be loaded before it can be signed and
# written (Note the load_repository() call above).
private_targets_key =  import_rsa_privatekey_from_file(path_to_target_key)

repository.targets.load_signing_key(private_targets_key)

# Due to the load_repository(), we must also load the private keys of the other top-level roles
# to generate a valid set of metadata.
private_root_key = import_rsa_privatekey_from_file(path_to_root_key)



private_root_key2 = import_rsa_privatekey_from_file(path_to_root_key2)

private_release_key = import_rsa_privatekey_from_file(path_to_release_key)

private_timestamp_key = import_rsa_privatekey_from_file(path_to_timestamp_key)


repository.root.load_signing_key(private_root_key)
repository.root.load_signing_key(private_root_key2)
repository.release.load_signing_key(private_timestamp_key)
repository.timestamp.load_signing_key(private_timestamp_key)

# Generate new versions of all the top-level metadata.
#coppying new targets and metadata. Stop the service while creating new metadata!
repository.write()
distutils.dir_util.copy_tree(newMetaDir, metaDir)

#comtinue the service




