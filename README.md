0install-TUF
============


0install INTRODUCTION
---------------------

Zero Install is a decentralized cross-distribution software installation system
available under the LGPL. It allows software developers to publish programs
directly from their own web-sites, while supporting features familiar from
centralized distribution repositories such as shared libraries, automatic
updates and digital signatures. It is intended to complement, rather than
replace, the operating system's package management. 0install packages never
interfere with those provided by the distribution.

0install does not define a new packaging format; unmodified tarballs or zip
archives can be used. Instead, it defines an XML metadata format to describe
these packages and the dependencies between them. A single metadata file can be
used on multiple platforms (e.g. Ubuntu, Debian, Fedora, openSUSE, Mac OS X and
Windows), assuming binary or source archives are available that work on those
systems.

0install also has some interesting features not often found in traditional
package managers. For example, while it will share libraries whenever possible,
it can always install multiple versions of a package in parallel when there are
conflicting requirements. Installation is always side-effect-free (each package
is unpacked to its own directory and will not touch shared directories such as
/usr/bin), making it ideal for use with sandboxing technologies and
visualization.

The XML file describing the program's requirements can also be included in a
source-code repository, allowing full dependency handling for unreleased
developer versions. For example, a user can clone a Git repository and build
and test the program, automatically downloading newer versions of libraries
where necessary, without interfering with the versions of those libraries
installed by their distribution, which continue to be used for other software.

See [the 0install.net web-site](http://0install.net/) for full details.


0install INSTALLATION
---------------------

Zero Install uses the normal Python distutils method of installation. To
install system-wide, run setup.py like this:

    $ sudo python setup.py install

You can also install just to your home directory (this doesn't require root
access):

    $ python setup.py install --home ~ --install-data ~/.local
    $ export PATH=$HOME/bin:$PATH

Logging out and back in again will ensure $PATH and the Applications menu get
updated correctly, on Ubuntu at least.

A bash completion script is available in share/bash-completion. It can be
sourced from your .bashrc or added under /usr/share/bash-completion. Note that
you may have to install a separate "bash-completion" package on some systems.

For zsh users, copy the script in share/zsh/site-functions/ to a directory in
your $fpath (e.g. /usr/local/share/zsh/site-functions).

For fish-shell users, add the full path to share/fish/completions to
$fish_complete_path.

TUF THE UPDATE FRAMEWORK
========================

TUF INTRODUCTION
----------------

A Framework for Securing Software Update Systems

TUF (The Update Framework) helps developers secure their new or existing software update systems. Software update systems are vulnerable to many known attacks, including those that can result in clients being compromised or crashed. TUF helps solve this problem by providing a flexible security framework that can be added to software updater's.

What Is a Software Update System?

Generally, a software update system is an application (or part of an application) running on a client system that obtains and installs software. This can include updates to software that is already installed or even completely new software.

What does TUF protect against?

* Key revocation 
* External dependencies  
* Arbitrary package attacks 
* Slow retrieval attacks 
* Endless data attacks 
* Freeze attack 

TUF INSTALLATION
----------------

TUF Update framework can be installed through PIP.

    $ sudo apt-get install python-pip
    $ sudo pip install tuf


See [the TUF website](http://theupdateframework.com/projects/project/wiki/Docs/overview) for more details.


0install + TUF
==============

OVERVIEW
--------

We integrated TUF update framework with 0install. 

Check the following [wiki page] (https://github.com/AlexanderRyzhko/0install-TUF/wiki/Integration-of-TUF-with-0install) for more details on how TUF was integrated with 0install.

A brief description on how 0install + TUF works.

The following diagram shows how the roles handled by TUF and how the keys are managed. 

![0install+TUF](/Images/TUF_metadata.jpg)



More information about the roles:

1. Root: The root role signs for itself here
2. Target: The target role signs for xml feed files
3. Release:  The release role signs a metadata file that provides information about the
   latest version of all of the other metadata on the repository(0install + TUF don't actually use this; it maintains by    xml. But we don't want to update TUF framework)
4. Timestamp: To prevent an adversary from replaying an out-of-date signed metadata file
   whose signature has not yet expired


THREAT MODEL
------------

The main threats that is associated with 0install are:

1. Attacker can compromise and act on behalf of a developer
2. Attacker can modify packages
3. Attacker can compromise 0install servers
4. Attacker can host his own feed files 

Please visit the [wiki page] (https://github.com/AlexanderRyzhko/0install-TUF/wiki/0install-Security-With-and-Without-TUF) for more details of each attack. 


KEY MANAGEMENT
--------------

1. Offline keys
The root and the target roles are going to be signed by the offline keys, so that an attacker will not be able to compromise and push updates as the developer. 

2. Online keys
The timestamp and the release roles are signed by the online keys. These keys are stored on the 0install server. If 0install is compromised, then the attacker will be able to read the online keys. 

3. Developer keys
The developer keys are generated by 0install or provided by developers when the developer uses the 0publish application to create and publish packages (gpg keys). All the keys are registered to a particular email address. These keys need to be kept offline as they are used to sign the packages and the XML feed file. A single developer can have multiple keys as he can be the contributor for multiple packages. 

Currently, Zero Install also maintains a list of trusted keys, and aids the user's decision of whether to trust a key using its database service of known keys. The default database service can be susceptible to attacks. Successful attack puts signature verifications into risk allowing attacker’s malicious keys appear as valid. Users / organizations may wish to provide their own database and perform real verification checks on authors. This would verify developers to packages that they have developed.

Note: In the diagram the release role is a dummy role as the XML feed file takes care of what the release role was intended for, so the release role which is signed by the online key does not perform any function but is kept offline to protect from old targets.txt in case of online key compromise. For this reason if release role is removed timestamp role has to become offline.   


METADATA MANAGEMENT
-------------------

The TUF metadata is going to be hosted on the 0install feed website. The user will be downloading both the XML and the TUF metadata for downloading the packages on 0install. 

We have given the metadata management to 0install as its as its a safe and efficient way of generating and distributing the metadata to the users. 

The metadata for each XML is calculated to be not more then 3 KB. 

Expiry of the metadata:
The metadata will have to be regenerated by 0install every fort night (15 days). If the metadata is not generated periodically it will expire after a month. If the metadata expires the users will not be able to download the packages. 


GENERATING METADATA FOR 0install + TUF
--------------------------------------

Generating of TUF metadata is a simple procedure which has to be done every fortnight by 0install. 

Please follow the steps given on the [wiki page] (https://github.com/AlexanderRyzhko/0install-TUF/wiki) for generating TUF metadata for all the XML feed files. 


MODIFICATIONS TO 0install
-------------------------

We have to make some changes to 0install with the integration of TUF, the changes are mentioned below:

1. Endless data attack
TUF was not able to protect from this attack as only the XML was downloaded through TUF and not the whole package. So to protect from this attack we modified the download code so that it terminates the download after 100% and does not proceed after that. 

2. Key revocation
Currently TUF does not hander the download of the package so the only keys that are currently in use are the developer keys used to sign the XML feed files. 
There are a few ways in which we can handle the key revocation 
The developer would have to regenerate the developer key after a fixed period of time, with his original credential that he registered with 0install 
The developer can be provided new keys every time he revokes his existing key by 0install.

3. Generating TUF metadata
When 0install wants to make an update of all the XML feed files the TUF metadata will have to be regenerate for the XML feed files. This is a fairly simple procedure. Once the metadata is generated, the TUF metadata can be upload on to the server so that when a user what's to download a package and gives the XML feed URI, he downloads the XML TUF metadata as well.

4. Hosting TUF metadata
Along with the present XML feed files that 0install hosts currently, 0install will also have to host the metadata for all the XML feed files. The TUF metadata which is generated for all the XML feed files is not that large and will not occupy much space on the server. 

5. Validation of developers 
At present the developers are not validated by 0install. There is no way to find out who has developed the package, which means an attacker can create a vulnerable package, host and distribute the package to users. 

There must be a quick and efficient way to validate developers. When 0install is able to validate developers, users can be sure that the packages are downloaded from a valid place. 

Also, there is no process where a developer claims a package. In the future, when a developer creates a new package for 0install he claims the rights for that package, which mean that no other group or developer who can create the same package. By doing this we can be rest assured that an attacker will not be able to develop vulnerable packages that have been hosted by 0install. 


Note: The reason we have suggested the changes here is because, there is no validation done for who has created the package, and to validate developers as well. 


CHNAGES IN THE DEVELOPER END
----------------------------

Developer's now will have to register with 0install before developing package. 

Developer's will also have to claim package that are are currently building. There by only that developer or group of developer will have the rights to make and push changes to the packages they have claimed. 

Developer's will have to regenerate the developer keys after a fixed period of time. 

The rest of the process is just the same for the developer's. 


CHANGES IN THE USER END
-----------------------

The user does not have to do much with the new implementations of 0install + TUF. The user will have to follow the installation instruction for both 0install and TUF. The rest of the process is more or less the same. 

INSTALLATION OF ROX

Sample installation procedure is given for rox-edit

To install [Edit](http://rox.sourceforge.net/2005/interfaces/Edit) and name it 'rox-edit':

    $ 0install add rox-edit http://rox.sourceforge.net/2005/interfaces/Edit

To run it (use the name you chose above):

    $ rox-edit

When you run it, 0install will check how long it has been since it checked
for updates and will run a check in the background if it has been too long.
To check for updates manually:

    $ 0install update rox-edit
    http://rox.sourceforge.net/2005/interfaces/ROX-Lib: 2.0.5 -> 2.0.6

This shows that ROX-Lib, a library rox-edit uses, was upgraded.

If an upgrade stops a program from working, use "0install whatchanged".
This will tell you when the application was last upgraded and what changed, and
tell you how to revert to the previous version:

    $ 0install whatchanged rox-edit
    Last checked    : Tue Sep 25 09:45:19 2012
    Last update     : 2012-09-25
    Previous update : 2012-08-25
    
    http://rox.sourceforge.net/2005/interfaces/ROX-Lib: 2.0.5 -> 2.0.6
    
    To run using the previous selections, use:
    0install run /home/tal/.config/0install.net/apps/rox-edit/selections-2012-08-25.xml

To see where things have been stored:

    $ 0install select rox-edit
    - URI: http://rox.sourceforge.net/2005/interfaces/Edit
      Version: 2.2
      Path: /home/tal/.cache/0install.net/implementations/sha256=ba3b4953...c8ce3177f08c926bebafcf16b9
      - URI: http://rox.sourceforge.net/2005/interfaces/ROX-Lib
        Version: 2.0.6
        Path: /home/tal/.cache/0install.net/implementations/sha256=ccefa7b187...16b6d0ad67c4df6d0c06243e
      - URI: http://repo.roscidus.com/python/python
        Version: 2.7.3-4
        Path: (package:deb:python2.7:2.7.3-4:x86_64)

To view or change configuration settings:

    $ 0install config


CONSISTENCY OF 0install + TUF
-----------------------------

There are two main problems that arise here with the implementation of 0install and TUF

1. How do files get updated?
Developer uploads the new xml files to a secure folder on 0install. Every fortnight when the update needs to be pushed the TUF metadata is generated and pushed to production from dev environment.

2. What happens if a client downloads files during an update?
New propose is 0install tries to download again after a fixed period of time (e.g. 10 sec), so if the metadata is being updated the user does not get a bad hash error and updates successfully


SECURITY OF 0install + TUF 
--------------------------

Since the download is going through TUF, we can safely assume that 0install applications are protected against attacks like arbitrary package attacks, key compromise and replay & freeze attacks. 

With the architecture of 0install being completely distributed in nature. Only the XML retrieval is through TUF and not the retrieval of the packages. Although there is no metadata configured for the packages the download still goes through TUF. We were not able to generate TUF metadata for the packages as well because of the distributed architecture of 0install. Even if we have not generate the metadata for the packages its still safe as the download goes through TUF and the targets file has the link of where the packages are hosted. 


PERFORMANCE OF 0install + TUF        
-----------------------------

One of the important aspects that we need to look at is how well TUF and 0install work together. 

Initial results are good. 0install + TUF works well. 

The overhead that is created by implementing 0install with TUF is very negligible, we generated the metadata for the 79 applications and the size of the files is around 22.31KB. 

In the future: With greater number of application targets (XMLs) can be splitted into bins (path_hashed) to lower amount of metadata needed for downloading (considering scalability).
