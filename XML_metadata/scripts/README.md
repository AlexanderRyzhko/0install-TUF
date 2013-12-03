Those are three scripts for generating TUF metadata: 

create_key_repo.py – creates main repository. On top of the script is specified the root folder for metadata.

add_tagets_delegate.py – adds targets to tagets.txt and signs appropriate files with keys that first check on 
Specified directory when not found asks user to provide valid part to keys. Script automatically adds new and updated targets into targets folder and updates metadata

generate_client_metadata.py – generates clients’ metadata. Clients metadata should be already generated and packaged with 0install
