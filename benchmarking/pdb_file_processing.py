## Functions related to processing of structure files

import numpy as np
import pandas as pd
from Bio import PDB
import os, argparse, re, subprocess

def get_two_chains(name, filepath, ext, chains, name_to_save='standard'):

    """ Isolate two desired chains from a PDB file, intended for use in interface alignment. Helps alignment tools to focus only on the target interface within a deposited complex. The new structures will be deposited in a 'two_chains/' subfolder within the provided filepath.
    
    Expected input: name|str = Name of structure, string
                    filepath|str = Path to folder containing original structure, named '<name>.pdb, string'
                    chains|list[str] = List of chains to extract, expecting only 2
                    name_to_save|str *optional = Desired name to save new file, if not provided, new file will be named <name>.pdb; .pdb extension will always be added to whatever new name is provided """

    # Parse provided structure
    if ext == 'pdb':
        parser = PDB.PDBParser(QUIET=True)
        io = PDB.PDBIO()
    if ext == 'cif':
        parser = PDB.MMCIFParser(QUIET=True)
        io = PDB.MMCIFIO()
    filename = filepath+'/'+name+'.'+ext
    structure = parser.get_structure(name, filename)
    model_ids = [x.get_id() for x in structure.get_models()]
    io.set_structure(structure)

    # Define selection class
    class ChainSelect(PDB.Select):
        # Obtain first model - structures usually only have one, but NMR data often has more than one
        # Multiple models are not supported by Foldseek-IF so we must retain only the first one
        def accept_model(self, model):
            if model.get_id() == model_ids[0]:
                return True
            else:
                return False
        # Obtain only the target chains (those participating in the interface)
        def accept_chain(self, chain):
            if chain.get_id()==chains[0] or chain.get_id()==chains[1]:
                return True
            else:
                return False
        # Obtain only residues which are part of the protein chains (i.e. remove waters, ligands, etc.)
        # Use logic for denoting heteroatoms within the residue id: the first part of the id will not be empty if heteroatom
        # These need to be removed because a) they are not relevant and b) there has been one instance where ligands caused Foldseek-IF to fault during the createdb module (see 7b0n author chains o and l)
        def accept_residue(self, residue):
            res = residue.id[0]
            if res != " ":
                return False
            else:
                return True

    # Set output parameters and save new file with only the defined selection       
    if name_to_save == 'standard':
        name_to_save = name   
    io.save(f'{filepath}/{name_to_save}.{ext}', ChainSelect())

#Use the following command in ChimeraX to select interface residues
## select (#2/A@CB/A:gly@CA @<8 & #2/B@CB/B:gly@CA) | (#2/B@CB/B:gly@CA @<8 & #2/A@CB/A:gly@CA) residues true

def get_CA_only(name, filepath, savepath, parser, io):
    """
    Reduce structure file to C-alpha only. For tests with PULCHRA reconstruction. 'ca_' is prepended to input file name when saving output file.
    
    Input:
    name|str: Name of structure file
    filepath|str: Path to directory where structure file is located
    savepath|str: Path to directory of desired output file location
    parser|Bio.PDB.Parser: Parser object from Biopython PDB module (to avoid loading with every run of function)
    io|Bio.PDB.IO: IO object from Biopython PDB module (to avoid loading with every run of function)
    
    """
    filepath = filepath + name
    structure = parser.get_structure(name.strip(".pdb"), filepath)
    class CASelect(PDB.Select):
        def accept_atom(self, atom):
            return atom.get_id() == 'CA'
    name_to_save = name
    io.set_structure(structure)   
    io.save(f'{savepath}/{name_to_save}', CASelect())

def get_interface_residues(name, filepath, mode='CB', cutoff=8.0):

    """ Extract interface residues from a desired structure based on Foldseek-IF definition (Cbeta-Cbeta less than 8.0 Angstroms apart). Returns the ids of each chain, the number of interface residues on each chain, and the full length of each chain.
    
    Expected input: name|str = Name of structure for extraction
                    filepath|str = Path to folder containing original structure, including trailing backslash
                    mode|str = Interface definition mode; expected value either 'CB' for Beta-carbon - Beta-carbon distances or 'CA' for Alpha-carbon - Alpha-carbon distances
                    cutoff|float = Distance, in Angstroms, by which to determine if two nearby residues are interface contacts; default 8.0 """
    
    # Parse structure
    ext = name.split(".")[-1]
    if ext == 'pdb':
        parser = PDB.PDBParser(QUIET=True)
        io = PDB.PDBIO()
    if ext == 'cif':
        parser = PDB.MMCIFParser(QUIET=True)
        io = PDB.MMCIFIO()
    filename = filepath+name
    structure = parser.get_structure(name.strip(ext), filename)

    # Iterate through structural elements to test distance between all CB atoms (or CA for GLY residues)
    # Append residues that meet distance cutoff to list
    chains = []
    for chain in structure.get_chains():
        chains+=[chain]
    chainalen = len(chains[0])
    chainblen = len(chains[1])
    interface_residues=[]
    if mode == 'CB':
        for res1 in chains[0]:
            for res2 in chains[1]:
                #Atom-atom distance
                #print (res1,res2)
                test = False
                for a in res1.get_atoms():
                    if test:break
                    if a.get_name() == 'CB' or (res1.get_resname() == 'GLY' and a.get_name() == 'CA'):
                        for b in res2.get_atoms():
                            if b.get_name() == 'CB' or (res2.get_resname() == 'GLY' and b.get_name() == 'CA'):
                                dist = (a.coord[0]-b.coord[0])**2 + (a.coord[1]-b.coord[1])**2 + (a.coord[2]-b.coord[2])**2
                                dist = dist**(1/2)
                                if dist < cutoff:
                                    #Save residues
                                    #print ("Appending",res1,res2)
                                    interface_residues.append(res1.get_full_id())
                                    interface_residues.append(res2.get_full_id())
                                    test=True
                                    break
    elif mode == 'CA':
        for res1 in chains[0]:
            for res2 in chains[1]:
                #Atom-atom distance
                #print (res1,res2)
                test = False
                for a in res1.get_atoms():
                    if test:break
                    if a.get_name() == 'CA':
                        for b in res2.get_atoms():
                            if b.get_name() == 'CA':
                                dist = (a.coord[0]-b.coord[0])**2 + (a.coord[1]-b.coord[1])**2 + (a.coord[2]-b.coord[2])**2
                                dist = dist**(1/2)
                                if dist < cutoff:
                                    #Save residues
                                    #print ("Appending",res1,res2)
                                    interface_residues.append(res1.get_full_id())
                                    interface_residues.append(res2.get_full_id())
                                    test=True
                                    break   

    # Set PDB Select class that will keep only those residues in list
    # Residues are identified by their FULL Bio.PDB identifier to retain correct chain context                   
    class ResSelect(PDB.Select):
        def accept_residue(self, residue):
            if residue.get_full_id() in interface_residues:
                return True
            else:
                return False
    
    # Write information for each residue to dataframe
    chainids = [chains[0].get_id(), chains[1].get_id()]
    chaina = [str(x[3][1]) for x in interface_residues if x[2] == chainids[0]]
    chaina = list(set(chaina))
    lenifa = len(chaina)
    chainb = [str(x[3][1]) for x in interface_residues if x[2] == chainids[1]]
    chainb = list(set(chainb))
    lenifb = len(chainb)
    return chainids[0], chainids[1], lenifa, lenifb, chainalen, chainblen

def use_pulchra(input_filename, input_filepath):

    # Call PULCHRA (adjust the executable path if necessary)
    result = subprocess.run(["/Users/stromjoe/Documents/GitHub/pulchra/pulchra", f"{input_filepath}/{input_filename}", "-q"],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            check=True)
    try:
        result.stdout.decode() 
    except subprocess.CalledProcessError as e:
        print("PULCHRA failed with error:")
        print(e.stderr.decode())

def reconstruct_multimer(input_id, input_filepath):
    use_pulchra(f"{input_id}-A.pdb", input_filepath)
    use_pulchra(f"{input_id}-B.pdb", input_filepath)
    full_contents = []
    with open(f"{input_filepath}/{input_id}-A.rebuilt.pdb", 'r') as f:
        contents = f.readlines()
    for i in range(0,len(contents)):
        if re.match("ATOM",contents[i]):
            contents[i] = contents[i][0:21] + "A" + contents[i][22:]
    contents.pop()
    full_contents+=contents
    with open(f"{input_filepath}/{input_id}-B.rebuilt.pdb", 'r') as f:
        contents = f.readlines()
    for i in range(0,len(contents)):
        if re.match("ATOM",contents[i]):
            contents[i] = contents[i][0:21] + "B" + contents[i][22:]
    full_contents+=contents
    with open(f"{input_filepath}/{input_id}.rebuilt.pdb",'w+') as f:
        f.writelines(full_contents)