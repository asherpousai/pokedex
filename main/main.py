import sys
from PyQt5.QtWidgets import QApplication

# Import the custom GUI class from pokemon_gui module
from pokemon_gui import PokemonViewer

def main():
    # Create Qt application
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show main window
    viewer = PokemonViewer()
    viewer.show()
    
    # Run application event loop
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()