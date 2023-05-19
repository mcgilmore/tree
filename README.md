# tree.py
Helps create phylogenetic tree showing distribution of a protein in bacterial species, using [OrthoDB v11](https://www.orthodb.org/) and [iTOL](https://itol.embl.de/).

 1. Using OrthoDB v11, find your protein and the desired phylogenetic level to annotate. Copy the group identifier and paste it into the text box in the tree.py GUI.
	- For example, the group identifier for GroEL at the Bacteria level is **9766614at2**.
2. The script will produce an iTOL dataset. Save it somewhere for uploading to iTOL.
3. Create an iTOL tree using the included **"OrthoDBv11_tree.txt"** file.
4. Open the tree, and navigate to the "Datasets" tab. Select "Upload annotation file" and navigate to the dataset file created by the script.
5. Adjust the tree and aesthetics to your preferences.


 
