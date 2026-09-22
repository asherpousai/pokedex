import csv
import re

class PokemonData:
    # Class to handle Pokemon data loading and processing
    
    def __init__(self):
        self.pokemon_list = []  # List to store all Pokemon data
        self.filtered_data = []  # List to store filtered results
        
    def load_csv(self, filename):
        # Load Pokemon data from CSV file, handling syntax irregularities
        
        try:
            with open(filename, 'r', encoding='utf-8-sig') as file:  # Handle BOM character
                csv_reader = csv.DictReader(file)  
                
                
                # Loop through each row in CSV
                for row in csv_reader:
                    # Conditional: Clean and validate data
                    pokemon = self._clean_pokemon_data(row)
                    if pokemon:  # Only add valid entries
                        self.pokemon_list.append(pokemon)
            
            self.filtered_data = self.pokemon_list.copy()
            return True, f"Loaded {len(self.pokemon_list)} Pokemon successfully!"
            
        except FileNotFoundError:
            return False, f"Error: File '{filename}' not found!"
        except Exception as e:
            return False, f"Error loading file: {str(e)}"
    
    def _clean_pokemon_data(self, row):
        # Clean and validate Pokemon data, handling irregularities
        # Demonstrates: Conditional statements, data validation
        
        # Args: row (dict): Raw CSV row data
        # Returns: dict: Cleaned Pokemon data or None if invalid

        try:
            # Handle empty fields by replacing with defaults
            pokemon = {
                'no': row.get('No', '0'),
                'branch_code': row.get('Branch_Code', ''),
                'name': row.get('Name', 'Unknown'),
                'original_name': row.get('Original_Name', ''),
                'generation': row.get('Generation', '0'),
                'height': row.get('Height', '0'),
                'weight': row.get('Weight', '0'),
                'type1': row.get('Type1', 'Normal'),
                'type2': row.get('Type2', '').strip() or 'None',  # Handle empty Type2 Dark   
                'ability1': row.get('Ability1', '').strip() or 'None',
                'ability2': row.get('Ability2', '').strip() or 'None',
                'ability_hidden': row.get('Ability_Hidden', '').strip() or 'None',
                'color': row.get('Color', 'Unknown'),
                'hp': row.get('HP', '0'),
                'attack': row.get('Attack', '0'),
                'defense': row.get('Defense', '0'),
                'sp_attack': row.get('SP_Attack', '0'),
                'sp_defense': row.get('SP_Defense', '0'),
                'speed': row.get('Speed', '0'),
                'total': row.get('Total', '0'),
                'category': row.get('Category', 'Ordinary'),
                'mega_evolution': row.get('Mega_Evolution_Flag', '').strip() or 'No'
            }
            return pokemon
        except Exception:
            return None
    
    def search_by_name(self, search_term):
        # Search Pokemon by name using regular expressions
        # Demonstrates: Regular expressions, Loops, Lists
        
        # Args: search_term (str): Search pattern (supports regex)

        if not search_term:
            self.filtered_data = self.pokemon_list.copy()
            return
        
        # Use regex for case-insensitive pattern matching
        try:
            pattern = re.compile(search_term, re.IGNORECASE)
            self.filtered_data = []
            
            # Loop through all Pokemon
            for pokemon in self.pokemon_list:
                # Conditional: Check if name matches pattern
                if pattern.search(pokemon['name']) or pattern.search(pokemon['original_name']):
                    self.filtered_data.append(pokemon)
        except re.error:
            # Handle invalid regex patterns
            self.filtered_data = self.pokemon_list.copy()
    
    def filter_by_type(self, type_filter):
        # Filter Pokemon by type
        # Demonstrates: Loops, Conditional statements, Lists
        
        # Args: type_filter (str): Type to filter by (e.g., "Fire", "Water")
        
        if type_filter == "All Types":
            self.filtered_data = self.pokemon_list.copy()
            return
        
        self.filtered_data = []
        # Loop through all Pokemon
        for pokemon in self.pokemon_list:
            # Conditional: Check if either type matches
            if pokemon['type1'] == type_filter or pokemon['type2'] == type_filter:
                self.filtered_data.append(pokemon)
    
    def filter_by_generation(self, generation):
        # Filter Pokemon by generation
        # Demonstrates: Loops, Conditional statements
        
        # Args: generation (str): Generation number to filter by

        if generation == "All Generations":
            self.filtered_data = self.pokemon_list.copy()
            return
        
        self.filtered_data = []
        for pokemon in self.pokemon_list:
            if pokemon['generation'] == generation:
                self.filtered_data.append(pokemon)
    
    def sort_data(self, sort_key, reverse=False):
        # Sort filtered data by specified attribute
        # Demonstrates: Loops, Conditional statements

        # Args: sort_key (str): Display name of attribute to sort by || reverse (bool): Sort in descending order if True

        # Map display names to data keys
        sort_mapping = {
            'Name': 'name',
            'Number': 'no',
            'HP': 'hp',
            'Attack': 'attack',
            'Defense': 'defense',
            'Total Stats': 'total'
        }
        
        key = sort_mapping.get(sort_key, 'name')
        
        # Conditional: Use numeric or string sorting
        if key in ['no', 'hp', 'attack', 'defense', 'total']:
            # Numeric sorting
            self.filtered_data.sort(key=lambda x: int(x[key]) if x[key].isdigit() else 0, reverse=reverse)
        else:
            # String sorting
            self.filtered_data.sort(key=lambda x: x[key].lower(), reverse=reverse)
    
    def get_all_types(self):
        # Extract unique types from dataset
        # Demonstrates: Loops, Lists, Conditional statements
        
        # Returns: list: Sorted list of unique Pokemon types
        
        types = set()
        for pokemon in self.pokemon_list:
            types.add(pokemon['type1'])
            # Conditional: Only add Type2 if it exists
            if pokemon['type2'] != 'None':
                types.add(pokemon['type2'])
        return sorted(list(types))
    
    def validate_stat_range(self, stat_value, min_val, max_val):
        # Validate if stat is within range using regex
        # Demonstrates: Regular expressions, Conditional statements
        
        # Args: stat_value: Value to validate , min_val (int): Minimum allowed value , max_val (int): Maximum allowed value
            
        # Returns: bool: True if valid, False otherwise

        # Use regex to validate numeric input
        if not re.match(r'^\d+$', str(stat_value)): 
            return False
        
        value = int(stat_value)
        return min_val <= value <= max_val
