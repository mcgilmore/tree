# iTOL Tree Generator v0.1
Helps create phylogenetic tree showing distribution of a protein using [OrthoDB v12](https://www.orthodb.org/) by creating an [iTOL](https://itol.embl.de/)-compatible dataset for visualisation from a given OrthoDB group.

## Build
`cargo build --release`

## Usage
`tree [OrthoDB_group_id]`

Use `--help` or `-h` argument for usage instructions

## Instructions
1. Using OrthoDB v12, find your protein and the desired phylogenetic level to annotate. Copy the group identifier and paste it into the text box in the GUI.
	- For example, the group identifier for GroEL at the Bacteria level is **9766614at2**.
2. The script will produce an iTOL dataset (.txt).
3. Create an iTOL tree by uploading the included **"OrthoDBv12_tree"** file
4. Open the tree, and navigate to the "Datasets" tab. Select "Upload annotation file" and navigate to the dataset file created by the script. Upload it.
5. Adjust the tree and aesthetics to your preferences.

## Notes
- Tree is a little more limited than the full selection of species on OrthoDB. This happens because not every species has an NCBI taxonomy ID, so PhyloT will not include those on the tree. As a result there are some errors on importing the tree into iTOL, but these shouldn't result in an undue gap in the dataset coverage.
