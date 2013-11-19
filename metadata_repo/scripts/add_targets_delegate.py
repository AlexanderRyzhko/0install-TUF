'''
Script to add the target paths
Create the delegated role 'unclaimed'
Add the targets to unclaimed
'''


from tuf.libtuf import *

# Load the repository created in the previous section.  This repository so far contains metadata for
# the top-level roles, but no targets.
repository = load_repository("path/to/repository/")

# Get a list of file paths in a directory, even those in sub-directories.
# This must be relative to an existing directory in the repository, otherwise throw an
# error.
list_of_targets = repository.get_filepaths_in_directory("path/to/repository/targets/",
                                                        recursive_walk=True, followlinks=True) 

# Add the list of target paths to the metadata of the Targets role.  Any target file paths
# that may already exist are NOT replaced.  add_targets() does not create or move target files.
repository.targets.add_targets(list_of_targets)

# The private key of the updated targets metadata must be loaded before it can be signed and
# written (Note the load_repository() call above).
private_targets_key =  import_rsa_privatekey_from_file("path/to/targets_key")

repository.targets.load_signing_key(private_targets_key)

# Due to the load_repository(), we must also load the private keys of the other top-level roles
# to generate a valid set of metadata.
private_root_key = import_rsa_privatekey_from_file("path/to/root_key")

private_root_key2 = import_rsa_privatekey_from_file("path/to/root_key2")

private_release_key = import_rsa_privatekey_from_file("path/to/release_key")

private_timestamp_key = import_rsa_privatekey_from_file("path/to/timestamp_key")


repository.root.load_signing_key(private_root_key)
repository.root.load_signing_key(private_root_key2)
repository.release.load_signing_key(private_release_key)
repository.timestamp.load_signing_key(private_timestamp_key)

# Generate new versions of all the top-level metadata.
repository.write()


generate_and_write_rsa_keypair("path/to/unclaimed_key", bits=2048, password="password")
public_unclaimed_key = import_rsa_publickey_from_file("path/to/unclaimed_key.pub")

repository.targets.delegate("unclaimed", [public_unclaimed_key], [])

# Load the private key of "targets/unclaimed" so that signatures are later added and valid
# metadata is created.
private_unclaimed_key = import_rsa_privatekey_from_file("path/to/unclaimed_key")

repository.targets.unclaimed.load_signing_key(private_unclaimed_key)


repository.targets.unclaimed.delegate("foo", [public_unclaimed_key], [],
                                      restricted_paths=["path/to/repository/targets/foo/"])
repository.targets.unclaimed.foo.load_signing_key(private_unclaimed_key)
repository.targets.unclaimed.foo.add_target("path/to/repository/targets/foo/foo.xml")
repository.targets.unclaimed.foo.add_target("path/to/repository/targets/foo/FooBar-0.1.tar.gz")
repository.targets.unclaimed.foo.add_target("path/to/repository/targets/foo/FooBar-0.2.tar.gz")
repository.targets.unclaimed.foo.add_target("path/to/repository/targets/foo/FooBar-0.3.tar.gz")


repository.targets.remove_target("path/to/repository/targets/foo/foo.xml")
repository.targets.remove_target("path/to/repository/targets/foo/FooBar-0.1.tar.gz")
repository.targets.remove_target("path/to/repository/targets/foo/FooBar-0.2.tar.gz")
repository.targets.remove_target("path/to/repository/targets/foo/FooBar-0.3.tar.gz")

repository.write()

