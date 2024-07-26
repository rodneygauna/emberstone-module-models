'''
This script is used to convert the NFIRS nodules to models.
Using the "nfirs_modules.csv" file, the script will create the beginning
of mongooseJS models for each module.
'''
import pandas as pd


# Module No. dictionary
module_dict = {
    1: 'BasicModule',
    2: 'FireModule',
    3: 'StructureFileModule',
    4: 'CivilianFireCasualtyModule',
    5: 'FireServiceCasualtyModule',
    6: 'EmergencyMedicalServicesModule',
    7: 'HazardousMaterialsModule',
    8: 'WildlandFireModule',
    9: 'ApparatusModule',
    10: 'PersonnelModule',
    11: 'ArsonModule',
}

# Read in the modules
modules = pd.read_csv('nfirs_modules.csv')

# Create the models for each module
# Loop through each module and create a unique model for each module number
# Generate a .js file for each module's line
# CSV columns:
# 1. "Module No." - Module number
# 2. "Line" - Module section
# 3. "Element" - Field name

# Track processed (Module No., Line) pairs to avoid duplicate files
processed = set()

for i in range(len(modules)):
    module = modules.iloc[i]
    module_no = module['Module No.']
    line = module['Line']

    # Skip if this (Module No., Line) pair has already been processed
    if (module_no, line) in processed:
        continue

    # Mark this (Module No., Line) pair as processed
    processed.add((module_no, line))

    # Create a new file for each module by line
    # Populate the moduel_no with the module_dict discription (e.g. 1 -> Basic Module)
    with open(f'models/{module_dict[module_no]}_{line}_Model.js', 'w', encoding='utf-8') as f:
        f.write('import mongoose from "mongoose";\n\n')
        f.write(f'const {module_dict[module_no]}_{line}_Schema = new mongoose.Schema({{\n')
        # For loop to add each element to the schema
        for j in range(len(modules)):
            if modules.iloc[j]['Module No.'] == module_no and modules.iloc[j]['Line'] == line:
                # Add the element to the schema
                # Make the element a string for now
                # format the element to be lowercase and replace spaces or special characters with underscores
                element = modules.iloc[j]['Element'] \
                    .replace(' ', '_') \
                    .replace('(', '') \
                    .replace(')', '') \
                    .replace('/', '_') \
                    .replace('-', '_') \
                    .replace('.', '_') \
                    .replace(',', '_') \
                    .replace(';', '_') \
                    .replace(':', '_') \
                    .replace('?', '_') \
                    .replace('!', '_') \
                    .replace('&', '_') \
                    .replace('@', '_') \
                    .replace('#', '_') \
                    .replace('$', '_') \
                    .replace('%', '_') \
                    .replace('^', '_') \
                    .replace('*', '_') \
                    .replace('+', '_') \
                    .replace('=', '_') \
                    .replace('<', '_') \
                    .replace('>', '_') \
                    .replace('{', '_') \
                    .replace('}', '_') \
                    .replace('[', '_') \
                    .replace(']', '_') \
                    .replace('|', '_') \
                    .replace('\\', '_') \
                    .replace('`', '_') \
                    .replace('~', '_') \
                    .replace('\'', '_') \
                    .replace('"', '_') \
                    .replace(' ', '_') \
                    .lower()
                f.write(f'    {element}: String,\n')
        f.write('});\n\n')
        # Populate the module_no with the module_dict discription (e.g. 1 -> Basic Module)
        f.write(f'export default mongoose.model("{module_dict[module_no]}_{line}", {module_dict[module_no]}_{line}_Schema);\n')
