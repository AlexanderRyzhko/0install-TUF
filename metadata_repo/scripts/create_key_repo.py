'''
Script for creating the RSA keys and creating a new repository
'''

from tuf.libtuf import *
import time
import datetime

repo_path = "/var/www"
#targets_path = "/var/www/targets/"



keys = {
"path_to_target_key" : "/root/keys/targets_key",
"path_to_root_key" : "/root/keys/root_key",
"path_to_root_key2" : "/root/keys/root_key2",
"path_to_release_key" : "/root/keys/timestamp_key",
"path_to_timestamp_key" : "/root/keys/timestamp_key",
"path_to_root_key_public" : "/root/keys/root_key.pub"
"path_to_root_key_public2" : "/root/keys/root_key2.pub"
"path_to_release_key_public" :  "/root/keys/timestamp_key.pub"
"path_to_target_key_public" : "/root/keys/targets_key.pub"
"path_to_timestamp_key_public" : "/root/keys/timestamp_key.pub"
}

passw = "password"
exp_piriod = 1*2628000 # 1 month (in seconds)


#generate expiration time
current_time = time.time() 
timestamp_exp_date = str(datetime.datetime.fromtimestamp(int(current_time) + exp_piriod )


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

for key in keys:
	 keys[key] = checkKey(keys[key])



# Generate and write the first of two root keys for the TUF repository.
# The following function creates an RSA key pair, where the private key is saved to
# "path/to/root_key" and the public key to "path/to/root_key.pub".
generate_and_write_rsa_keypair(keys[path_to_root_key], bits=2048, password=passw )

# If the key length is unspecified, it defaults to 3072 bits. A length of less 
# than 2048 bits raises an exception. A password may be supplied as an 
# argument, otherwise a user prompt is presented.
generate_and_write_rsa_keypair(keys[path_to_root_key2])

# Import an existing public key.
public_root_key = import_rsa_publickey_from_file(keys[path_to_root_key_public])

# Import an existing private key.  Importing a private key requires a password, whereas
# importing a public key does not.
private_root_key = import_rsa_privatekey_from_file(keys[path_to_root_key])

# Create a new Repository object that holds the file path to the repository and the four
# top-level role objects (Root, Targets, Release, Timestamp). Metadata files are created when
# repository.write() is called.  The repository directory is created if it does not exist.
repository = create_new_repository(repo_path)

# The Repository instance, 'repository', initially contains top-level Metadata objects.
# Add one of the public keys, created in the previous section, to the root role.  Metadata is
# considered valid if it is signed by the public key's corresponding private key.
repository.root.add_key(public_root_key)

# Add a second public key to the root role.  Although previously generated and saved to a file,
# the second public key must be imported before it can added to a role.
public_root_key2 = import_rsa_publickey_from_file()
repository.root.add_key(public_root_key2)

# Threshold of each role defaults to 1.   Users may change the threshold value, but libtuf.py
# validates thresholds and warns users.  Set the threshold of the root role to 2,
# which means the root metadata file is considered valid if it contains at least two valid 
# signatures.
repository.root.threshold = 2
private_root_key2 = import_rsa_privatekey_from_file(keys[path_to_root_key2] , password=passw )

# Load the root signing keys to the repository, which write() uses to sign the root metadata.
# The load_signing_key() method SHOULD warn when the key is NOT explicitly allowed to
# sign for it.
repository.root.load_signing_key(private_root_key)
repository.root.load_signing_key(private_root_key2)

# Print the number of valid signatures and public/private keys of the repository's metadata.
repository.status()

try:
  repository.write()

# An exception is raised here by write() because the other top-level roles (targets, release,
# and timestamp) have not been configured with keys.
except tuf.Error, e:
  print e 

# Import an existing public key.
public_root_key = import_rsa_publickey_from_file(keys[path_to_root_key_public])

# Import an existing private key.  Importing a private key requires a password, whereas
# importing a public key does not.
private_root_key = import_rsa_privatekey_from_file(keys[path_to_root_key])


# Create a new Repository object that holds the file path to the repository and the four
# top-level role objects (Root, Targets, Release, Timestamp). Metadata files are created when
# repository.write() is called.  The repository directory is created if it does not exist.
repository = create_new_repository(repo_path)

# The Repository instance, 'repository', initially contains top-level Metadata objects.
# Add one of the public keys, created in the previous section, to the root role.  Metadata is
# considered valid if it is signed by the public key's corresponding private key.
repository.root.add_key(public_root_key)


# Add a second public key to the root role.  Although previously generated and saved to a file,
# the second public key must be imported before it can added to a role.
public_root_key2 = import_rsa_publickey_from_file(keys[path_to_root_key_public2])
repository.root.add_key(public_root_key2)

# Threshold of each role defaults to 1.   Users may change the threshold value, but libtuf.py
# validates thresholds and warns users.  Set the threshold of the root role to 2,
# which means the root metadata file is considered valid if it contains at least two valid 
# signatures.
repository.root.threshold = 2
private_root_key2 = import_rsa_privatekey_from_file(keys[path_to_root_key2], password=passw )

# Load the root signing keys to the repository, which write() uses to sign the root metadata.
# The load_signing_key() method SHOULD warn when the key is NOT explicitly allowed to
# sign for it.
repository.root.load_signing_key(private_root_key)
repository.root.load_signing_key(private_root_key2)

# Print the number of valid signatures and public/private keys of the repository's metadata.
repository.status()


try:
  repository.write()

# An exception is raised here by write() because the other top-level roles (targets, release,
# and timestamp) have not been configured with keys.
except tuf.Error, e:
  print e 


generate_and_write_rsa_keypair(keys[path_to_target_key], password=passw )
#generate_and_write_rsa_keypair("path/to/release_key", password="password")
generate_and_write_rsa_keypair(keys[path_to_timestamp_key], password=passw )

# Add the public keys of the remaining top-level roles.
repository.targets.add_key(import_rsa_publickey_from_file(keys[path_to_target_key_public]))
repository.release.add_key(import_rsa_publickey_from_file(keys[path_to_timestamp_key_public] ))
repository.timestamp.add_key(import_rsa_publickey_from_file(keys[path_to_release_key_public] ))

# Import the signing keys of the remaining top-level roles.  Prompt for passwords.
private_targets_key = import_rsa_privatekey_from_file(keys[path_to_target_key])

private_release_key = import_rsa_privatekey_from_file(keys[path_to_release_key])

private_timestamp_key = import_rsa_privatekey_from_file(keys[path_to_timestamp_key])


# Load the signing keys of the remaining roles so that valid signatures are generated when
# repository.write() is called.
repository.targets.load_signing_key(private_targets_key)
repository.release.load_signing_key(private_timestamp_key)
repository.timestamp.load_signing_key(private_timestamp_key)

# Optionally set the expiration date of the timestamp role.  By default, roles are set to expire
# as follows:  root(1 year), targets(3 months), release(1 week), timestamp(1 day).
repository.timestamp.expiration = timestamp_exp_date 

# Write all metadata to "path/to/repository/metadata.staged/".  The common case is to crawl the
# filesystem for all delegated roles in "path/to/repository/metadata.staged/targets/".
repository.write()
