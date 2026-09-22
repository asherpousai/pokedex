from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QLabel, QTableWidget, QTableWidgetItem,
    QComboBox, QTextEdit, QMessageBox, QHeaderView, QGroupBox
)
from PyQt5.QtCore import Qt

# Import custom data handling class from pokemon_data module
from pokemon_data import PokemonData

# Main GUI of Application 
class PokemonViewer(QMainWindow):    
    def __init__(self):
        # Initialise parent class and data
        super().__init__()
        self.pokemon_data = PokemonData()

        # General app QSS styling 
        self.setStyleSheet("""
        QScrollBar:vertical {
            width: 6px;
            background: #e0e0e0;
        }

        QScrollBar::handle:vertical {
            background: #888;
            min-height: 40px;
            border-radius: 40px;
        }

        QScrollBar::handle:vertical:hover {
            background: #adadad;
        }

        QScrollBar::add-line:vertical,
        QScrollBar::sub-line:vertical {
            height: 0px;  /* removes arrows */
        }

        QScrollBar::add-page:vertical,
        QScrollBar::sub-page:vertical {
            background: none;
                                
        QGroupBox::title {
            font-family: Segoe UI;
            font-size: 14pt;
            font-weight: bold;
            color: #2196F3;
        }
        }
                           """)
        self.init_ui()
        
    # Initialise the GUI interface
    def init_ui(self):
        # Set window presets 
        self.setWindowTitle("Pokemon CSV Viewer")
        self.setGeometry(100, 100, 1200, 700)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Add components
        main_layout.addWidget(self._create_load_section())
        main_layout.addWidget(self._create_filter_section())
        main_layout.addWidget(self._create_table_section())
        main_layout.addWidget(self._create_details_section())

    def _create_load_section(self):
        # Creates file loading section
        group = self._create_styled_group("Data Loading")
        layout = QHBoxLayout()
        
        self.file_path_input = QLineEdit()
        self.file_path_input.setPlaceholderText("Enter CSV file path...")
        self.file_path_input.setText(r"C:\Users\Asher\Projects\Pokedex\data\pokemon.csv") 
        
        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)
        load_button.setStyleSheet("background-color: #4CAF50; color: white;")
        
        self.status_label = QLabel("No data loaded")
        self.status_label.setStyleSheet("color: #666;")
        
        layout.addWidget(QLabel("File Path:"))
        layout.addWidget(self.file_path_input)
        layout.addWidget(load_button)
        layout.addWidget(self.status_label)
        
        group.setLayout(layout)
        return group
    
    def _create_filter_section(self):
        # Create search and filter controls

        group = self._create_styled_group("Search and Filters")
        layout = QVBoxLayout()
        
        # Search row
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search Pokemon name (supports regex: ^Char.* or Bulb)")
        self.search_input.textChanged.connect(self.apply_search)
        
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.apply_search)
        
        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        
        # Filter row
        filter_layout = QHBoxLayout()
        
        self.type_filter = QComboBox()
        self.type_filter.addItem("All Types")
        self.type_filter.currentTextChanged.connect(self.apply_type_filter)
        
        self.generation_filter = QComboBox()
        self.generation_filter.addItems(["All Generations", "1", "2", "3", "4", "5", "6", "7", "8"])
        self.generation_filter.currentTextChanged.connect(self.apply_generation_filter)
        
        self.sort_combo = QComboBox()
        self.sort_combo.addItems(["Name", "Number", "HP", "Attack", "Defense", "Total Stats"])
        
        sort_button = QPushButton("Sort Ascending")
        sort_button.clicked.connect(lambda: self.apply_sort(False))
        
        sort_desc_button = QPushButton("Sort Descending")
        sort_desc_button.clicked.connect(lambda: self.apply_sort(True))
        
        clear_button = QPushButton("Clear Filters")
        clear_button.clicked.connect(self.clear_filters)
        clear_button.setStyleSheet("background-color: #ff9800; color: white;")
        
        filter_layout.addWidget(QLabel("Type:"))
        filter_layout.addWidget(self.type_filter)
        filter_layout.addWidget(QLabel("Generation:"))
        filter_layout.addWidget(self.generation_filter)
        filter_layout.addWidget(QLabel("Sort by:"))
        filter_layout.addWidget(self.sort_combo)
        filter_layout.addWidget(sort_button)
        filter_layout.addWidget(sort_desc_button)
        filter_layout.addWidget(clear_button)
        
        layout.addLayout(search_layout)
        layout.addLayout(filter_layout)
        
        group.setLayout(layout)
        return group
    
    def _create_table_section(self):
        # Create data table display

        group = self._create_styled_group("Pokemon Data")
        layout = QVBoxLayout()
        
        self.result_count_label = QLabel("Results: 0")
        self.result_count_label.setStyleSheet("color: #2196F3;")
        
        self.table = QTableWidget()
        self.table.setColumnCount(10)
        self.table.setHorizontalHeaderLabels([
            'Branch No', 'Name', 'Type 1', 'Type 2', 'HP', 'Attack', 
            'Defense', 'Special Attack', 'Special Defence', 'Total'
        ])

        horizontal_header = self.table.horizontalHeader()
        assert horizontal_header is not None
        horizontal_header.setSectionResizeMode(QHeaderView.Stretch)

        vertical_header = self.table.verticalHeader()
        assert vertical_header is not None
        vertical_header.setSectionResizeMode(QHeaderView.Stretch)

        vertical_header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Allow for row selection 
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.itemClicked.connect(self.show_pokemon_details)
    
        layout.addWidget(self.result_count_label)
        layout.addWidget(self.table)
        
        group.setLayout(layout)
        return group
    
    def _create_details_section(self):
        # Create Pokemon details display section

        group = self._create_styled_group("Pokemon Details")
        layout = QVBoxLayout()
        
        self.details_text = QTextEdit()
        self.details_text.setReadOnly(True)
        self.details_text.setMaximumHeight(400)
        self.details_text.setStyleSheet("background-color: #ffffff; font-family: Segoe UI; font-size: 9pt")
        
        layout.addWidget(self.details_text)
        group.setLayout(layout)
        return group
    
    # Custom QSS for consistent styling of UI
    def _create_styled_group(self, title):
        group = QGroupBox(title)
        group.setStyleSheet("""
            QGroupBox {
                font-family: Segoe UI;
                font-size: 9pt;
                color: #000;
                            
                padding-top: 25px;
                margin-top: 5px;
            }
            QGroupBox::title {

            }
        """)
        return group
    
    def load_data(self):
        # Load CSV data file

        file_path = self.file_path_input.text()
        success, message = self.pokemon_data.load_csv(file_path)
        
        # Conditional: Handle success or failure
        if success:
            self.status_label.setText(message)
            self.status_label.setStyleSheet("color: #72c675;")
            
            # Populate type filter
            types = self.pokemon_data.get_all_types()
            self.type_filter.clear()
            self.type_filter.addItem("All Types")
            self.type_filter.addItems(types)
            
            # Display data
            self.update_table()
        else:
            self.status_label.setText(message)
            self.status_label.setStyleSheet("color: #c42b1c;")
            QMessageBox.warning(self, "Error", message)
    
    def apply_search(self):
        # Apply search filter using regex

        search_term = self.search_input.text()
        self.pokemon_data.search_by_name(search_term)
        self.update_table()
    
    def apply_type_filter(self):
        # Apply type filter

        type_filter = self.type_filter.currentText()
        self.pokemon_data.filter_by_type(type_filter)
        self.update_table()
    
    def apply_generation_filter(self):
        # Apply generation filter

        generation = self.generation_filter.currentText()
        self.pokemon_data.filter_by_generation(generation)
        self.update_table()
    
    def apply_sort(self, reverse):
        # Apply sorting to data

        sort_key = self.sort_combo.currentText()
        self.pokemon_data.sort_data(sort_key, reverse)
        self.update_table()
    
    def clear_filters(self):
        # Clear all filters and reset display
        self.search_input.clear()
        self.type_filter.setCurrentIndex(0)
        self.generation_filter.setCurrentIndex(0)
        self.pokemon_data.filtered_data = self.pokemon_data.pokemon_list.copy()
        self.update_table()
    
    def update_table(self):
        # Update table with filtered data
        data = self.pokemon_data.filtered_data
        self.table.setRowCount(len(data))
        
        # Update result count
        self.result_count_label.setText(f"Results: {len(data)} Pokemon")
        
        # Loop through filtered data and populate table
        for row, pokemon in enumerate(data):
            # Create table items for each column
            items = [
                QTableWidgetItem(pokemon['no']),
                QTableWidgetItem(pokemon['name']),
                QTableWidgetItem(pokemon['type1']),
                QTableWidgetItem(pokemon['type2']),
                QTableWidgetItem(pokemon['hp']),
                QTableWidgetItem(pokemon['attack']),
                QTableWidgetItem(pokemon['defense']),
                QTableWidgetItem(pokemon['sp_attack']),
                QTableWidgetItem(pokemon['sp_defense']),
                QTableWidgetItem(pokemon['total'])
            ]
            
            # Add items to table
            for col, item in enumerate(items):
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.table.setItem(row, col, item)

         
    
    def show_pokemon_details(self, item):
        # Show detailed Pokemon information when row is selected

        row = item.row()
        # Conditional: Ensure valid row selection
        if row < len(self.pokemon_data.filtered_data):
            pokemon = self.pokemon_data.filtered_data[row]
            
            # Format details text
            details = f"""
            No: {pokemon['no']}  |  Branch Code: {pokemon['branch_code']}
            Name: {pokemon['name']}  |  Original: {pokemon['original_name']}
            Generation: {pokemon['generation']}  |  Category: {pokemon['category']}
            
            Physical:
                Height: {pokemon['height']} m  |  Weight: {pokemon['weight']} kg
                Color: {pokemon['color']}
            
            Types:
                Primary: {pokemon['type1']}  |  Secondary: {pokemon['type2']}
            
            Abilities:
                Ability 1: {pokemon['ability1']}
                Ability 2: {pokemon['ability2']}
                Hidden: {pokemon['ability_hidden']}
            
            Base Stats:
                HP: {pokemon['hp']}  |  Attack: {pokemon['attack']}  |  Defense: {pokemon['defense']}
                Sp. Attack: {pokemon['sp_attack']}  |  Sp. Defense: {pokemon['sp_defense']}  |  Speed: {pokemon['speed']}
                TOTAL: {pokemon['total']}
            
                Mega Evolution: {pokemon['mega_evolution']}

                        """
            self.details_text.setPlainText(details)