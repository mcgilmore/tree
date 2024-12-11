import tree
import sys

guiMode = False
group = None

if len(sys.argv) > 2:
	print("Too many arguments, I am confused")
	exit()
elif len(sys.argv) < 2:
	print("No arguments provided, running in GUI mode")
	guiMode = True
elif len(sys.argv) == 2:
	print(f"Using {sys.argv[1]} as input")
	guiMode = False
	group = sys.argv[1]

if guiMode == False:
	organism_names = tree.retrieve_organism_names(group)
	tree.writeiTol(f'./{group}.txt', organism_names, group)
elif guiMode == True:
	from PyQt5.QtWidgets import QApplication
	import gui
	app = QApplication(sys.argv)
	window = gui.OrthoDBGUI()
	window.show()
	sys.exit(app.exec_())

#if __name__ == "__main__":
