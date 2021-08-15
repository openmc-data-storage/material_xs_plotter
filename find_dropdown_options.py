import json
import os
import re

xml_file = os.getenv("OPENMC_CROSS_SECTIONS")

import xml.etree.ElementTree as ET

tree = ET.parse(xml_file)

root = tree.getroot()

all_isotopes = []
all_elements = []

for child in root:
    entry = child.attrib
    if entry["type"] == "neutron":
        symbol_mass_number = re.split("(\d+)", entry["materials"])[0:2]
        all_isotopes.append(symbol_mass_number)
        all_elements.append(symbol_mass_number[0])

all_elements = list(set(all_elements))

ELEMENT_SYMBOL = {
    "hydrogen": "H",
    "helium": "He",
    "lithium": "Li",
    "beryllium": "Be",
    "boron": "B",
    "carbon": "C",
    "nitrogen": "N",
    "oxygen": "O",
    "fluorine": "F",
    "neon": "Ne",
    "sodium": "Na",
    "magnesium": "Mg",
    "aluminium": "Al",
    "silicon": "Si",
    "phosphorus": "P",
    "sulfur": "S",
    "sulphur": "S",
    "chlorine": "Cl",
    "argon": "Ar",
    "potassium": "K",
    "calcium": "Ca",
    "scandium": "Sc",
    "titanium": "Ti",
    "vanadium": "V",
    "chromium": "Cr",
    "manganese": "Mn",
    "iron": "Fe",
    "cobalt": "Co",
    "nickel": "Ni",
    "copper": "Cu",
    "zinc": "Zn",
    "gallium": "Ga",
    "germanium": "Ge",
    "arsenic": "As",
    "selenium": "Se",
    "bromine": "Br",
    "krypton": "Kr",
    "rubidium": "Rb",
    "strontium": "Sr",
    "yttrium": "Y",
    "zirconium": "Zr",
    "niobium": "Nb",
    "molybdenum": "Mo",
    "technetium": "Tc",
    "ruthenium": "Ru",
    "rhodium": "Rh",
    "palladium": "Pd",
    "silver": "Ag",
    "cadmium": "Cd",
    "indium": "In",
    "tin": "Sn",
    "antimony": "Sb",
    "tellurium": "Te",
    "iodine": "I",
    "xenon": "Xe",
    "caesium": "Cs",
    "cesium": "Cs",
    "barium": "Ba",
    "lanthanum": "La",
    "cerium": "Ce",
    "praseodymium": "Pr",
    "neodymium": "Nd",
    "promethium": "Pm",
    "samarium": "Sm",
    "europium": "Eu",
    "gadolinium": "Gd",
    "terbium": "Tb",
    "dysprosium": "Dy",
    "holmium": "Ho",
    "erbium": "Er",
    "thulium": "Tm",
    "ytterbium": "Yb",
    "lutetium": "Lu",
    "hafnium": "Hf",
    "tantalum": "Ta",
    "tungsten": "W",
    "wolfram": "W",
    "rhenium": "Re",
    "osmium": "Os",
    "iridium": "Ir",
    "platinum": "Pt",
    "gold": "Au",
    "mercury": "Hg",
    "thallium": "Tl",
    "lead": "Pb",
    "bismuth": "Bi",
    "polonium": "Po",
    "astatine": "At",
    "radon": "Rn",
    "francium": "Fr",
    "radium": "Ra",
    "actinium": "Ac",
    "thorium": "Th",
    "protactinium": "Pa",
    "uranium": "U",
    "neptunium": "Np",
    "plutonium": "Pu",
    "americium": "Am",
    "curium": "Cm",
    "berkelium": "Bk",
    "californium": "Cf",
    "einsteinium": "Es",
    "fermium": "Fm",
    "mendelevium": "Md",
    "nobelium": "No",
    "lawrencium": "Lr",
    "rutherfordium": "Rf",
    "dubnium": "Db",
    "seaborgium": "Sg",
    "bohrium": "Bh",
    "hassium": "Hs",
    "meitnerium": "Mt",
    "darmstadtium": "Ds",
    "roentgenium": "Rg",
    "copernicium": "Cn",
    "nihonium": "Nh",
    "flerovium": "Fl",
    "moscovium": "Mc",
    "livermorium": "Lv",
    "tennessine": "Ts",
    "oganesson": "Og",
}

ELEMENT_NAMES = {value: key for (key, value) in ELEMENT_SYMBOL.items()}

options = []

for isotope in all_isotopes:
    isotope_and_mass_number = isotope[0] + isotope[1]
    options.append(
        {
            "label": ELEMENT_NAMES[isotope[0]] + " " + isotope[1],
            "value": isotope[0] + isotope[1],
        }
    )

for element in all_elements:
    options.append(
        {
            "label": ELEMENT_NAMES[element],
            "value": element,
        }
    )

print(options)
sorted_options = sorted(options, key=lambda k: k['label'])

with open("options.json", "w") as outfile:
    json.dump(sorted_options, outfile)
