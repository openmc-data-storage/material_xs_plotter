
def zaid_to_isotope(zaid: str) -> str:
    """converts an isotope into a zaid e.g. 003006 -> Li6"""
    a = str(zaid)[-3:]
    z = str(zaid)[:-3]
    symbol = ATOMIC_SYMBOL[int(z)]
    mass_number = str(int(a))
    if mass_number == '0':
        return symbol
    else:
        return symbol + mass_number

def convert_strings_to_numbers(input_string: str) -> float:
    """Converts a number represented as a string into a float. Handels special
    case formatting that is used in fotran inputs"""

    processed_string = input_string.split(".")
    if len(processed_string) == 1 : # in case there is no decimal point
        return float(input_string)

    # the string is a normal number
    if any(item in processed_string[1].lower() for item in ["e+","e", "e-"]):
        return float(input_string)

    # the string is a fortran formatted number
    processed_string[1] = processed_string[1].replace("+","e+")
    processed_string[1] = processed_string[1].replace("-","e-")
    combined_string = f"{processed_string[0]}.{processed_string[1]}"

    return float(combined_string)

ATOMIC_SYMBOL = {
    # 0: 'n', 
    1: 'H', 2: 'He', 3: 'Li', 4: 'Be', 5: 'B', 6: 'C',
    7: 'N', 8: 'O', 9: 'F', 10: 'Ne', 11: 'Na', 12: 'Mg', 13: 'Al',
    14: 'Si', 15: 'P', 16: 'S', 17: 'Cl', 18: 'Ar', 19: 'K',
    20: 'Ca', 21: 'Sc', 22: 'Ti', 23: 'V', 24: 'Cr', 25: 'Mn',
    26: 'Fe', 27: 'Co', 28: 'Ni', 29: 'Cu', 30: 'Zn', 31: 'Ga',
    32: 'Ge', 33: 'As', 34: 'Se', 35: 'Br', 36: 'Kr', 37: 'Rb',
    38: 'Sr', 39: 'Y', 40: 'Zr', 41: 'Nb', 42: 'Mo', 43: 'Tc',
    44: 'Ru', 45: 'Rh', 46: 'Pd', 47: 'Ag', 48: 'Cd', 49: 'In',
    50: 'Sn', 51: 'Sb', 52: 'Te', 53: 'I', 54: 'Xe', 55: 'Cs',
    56: 'Ba', 57: 'La', 58: 'Ce', 59: 'Pr', 60: 'Nd', 61: 'Pm',
    62: 'Sm', 63: 'Eu', 64: 'Gd', 65: 'Tb', 66: 'Dy', 67: 'Ho',
    68: 'Er', 69: 'Tm', 70: 'Yb', 71: 'Lu', 72: 'Hf', 73: 'Ta',
    74: 'W', 75: 'Re', 76: 'Os', 77: 'Ir', 78: 'Pt', 79: 'Au',
    80: 'Hg', 81: 'Tl', 82: 'Pb', 83: 'Bi', 84: 'Po', 85: 'At',
    86: 'Rn', 87: 'Fr', 88: 'Ra', 89: 'Ac', 90: 'Th', 91: 'Pa',
    92: 'U', 93: 'Np', 94: 'Pu', 95: 'Am', 96: 'Cm', 97: 'Bk',
    98: 'Cf', 99: 'Es', 100: 'Fm', 101: 'Md', 102: 'No',
    103: 'Lr', 104: 'Rf', 105: 'Db', 106: 'Sg', 107: 'Bh',
    108: 'Hs', 109: 'Mt', 110: 'Ds', 111: 'Rg', 112: 'Cn',
    113: 'Nh', 114: 'Fl', 115: 'Mc', 116: 'Lv', 117: 'Ts',
    118: 'Og'
}

reaction_names = [
    {"label": "MT 1 (n,total)", "value": "total"},
    {"label": "MT 2 (n,elastic)", "value": 2},
    {"label": "MT 3 (n,nonelastic)", "value": 3},
    {"label": "MT 4 (n,level)", "value": 4},
    {"label": "MT 5 (n,misc)", "value": 5},
    {"label": "MT 11 (n,2nd)", "value": 11},
    {"label": "MT 16 (n,2n)", "value": 16},
    {"label": "MT 17 (n,3n)", "value": 17},
    {"label": "MT 18 (n,fission)", "value": 18},
    {"label": "MT 19 (n,f)", "value": 19},
    {"label": "MT 20 (n,nf)", "value": 20},
    {"label": "MT 21 (n,2nf)", "value": 21},
    {"label": "MT 22 (n,na)", "value": 22},
    {"label": "MT 23 (n,n3a)", "value": 23},
    {"label": "MT 24 (n,2na)", "value": 24},
    {"label": "MT 25 (n,3na)", "value": 25},
    {"label": "MT 27 (n,absorption)", "value": 27},
    {"label": "MT 28 (n,np)", "value": 28},
    {"label": "MT 29 (n,n2a)", "value": 29},
    {"label": "MT 30 (n,2n2a)", "value": 30},
    {"label": "MT 32 (n,nd)", "value": 32},
    {"label": "MT 33 (n,nt)", "value": 33},
    {"label": "MT 34 (n,nHe-3)", "value": 34},
    {"label": "MT 35 (n,nd2a)", "value": 35},
    {"label": "MT 36 (n,nt2a)", "value": 36},
    {"label": "MT 37 (n,4n)", "value": 37},
    {"label": "MT 38 (n,3nf)", "value": 38},
    {"label": "MT 41 (n,2np)", "value": 41},
    {"label": "MT 42 (n,3np)", "value": 42},
    {"label": "MT 44 (n,n2p)", "value": 44},
    {"label": "MT 45 (n,npa)", "value": 45},
    {"label": "MT 91 (n,nc)", "value": 91},
    {"label": "MT 101 (n,disappear)", "value": 101},
    {"label": "MT 102 (n,gamma)", "value": 102},
    {"label": "MT 103 (n,p)", "value": 103},
    {"label": "MT 104 (n,d)", "value": 104},
    {"label": "MT 105 (n,t)", "value": 105},
    {"label": "MT 106 (n,3He)", "value": 106},
    {"label": "MT 107 (n,a)", "value": 107},
    {"label": "MT 108 (n,2a)", "value": 108},
    {"label": "MT 109 (n,3a)", "value": 109},
    {"label": "MT 111 (n,2p)", "value": 111},
    {"label": "MT 112 (n,pa)", "value": 112},
    {"label": "MT 113 (n,t2a)", "value": 113},
    {"label": "MT 114 (n,d2a)", "value": 114},
    {"label": "MT 115 (n,pd)", "value": 115},
    {"label": "MT 116 (n,pt)", "value": 116},
    {"label": "MT 117 (n,da)", "value": 117},
    {"label": "MT 152 (n,5n)", "value": 152},
    {"label": "MT 153 (n,6n)", "value": 153},
    {"label": "MT 154 (n,2nt)", "value": 154},
    {"label": "MT 155 (n,ta)", "value": 155},
    {"label": "MT 156 (n,4np)", "value": 156},
    {"label": "MT 157 (n,3nd)", "value": 157},
    {"label": "MT 158 (n,nda)", "value": 158},
    {"label": "MT 159 (n,2npa)", "value": 159},
    {"label": "MT 160 (n,7n)", "value": 160},
    {"label": "MT 161 (n,8n)", "value": 161},
    {"label": "MT 162 (n,5np)", "value": 162},
    {"label": "MT 163 (n,6np)", "value": 163},
    {"label": "MT 164 (n,7np)", "value": 164},
    {"label": "MT 165 (n,4na)", "value": 165},
    {"label": "MT 166 (n,5na)", "value": 166},
    {"label": "MT 167 (n,6na)", "value": 167},
    {"label": "MT 168 (n,7na)", "value": 168},
    {"label": "MT 169 (n,4nd)", "value": 169},
    {"label": "MT 170 (n,5nd)", "value": 170},
    {"label": "MT 171 (n,6nd)", "value": 171},
    {"label": "MT 172 (n,3nt)", "value": 172},
    {"label": "MT 173 (n,4nt)", "value": 173},
    {"label": "MT 174 (n,5nt)", "value": 174},
    {"label": "MT 175 (n,6nt)", "value": 175},
    {"label": "MT 176 (n,2n3He)", "value": 176},
    {"label": "MT 177 (n,3n3He)", "value": 177},
    {"label": "MT 178 (n,4n3He)", "value": 178},
    {"label": "MT 179 (n,3n2p)", "value": 179},
    {"label": "MT 180 (n,3n3a)", "value": 180},
    {"label": "MT 181 (n,3npa)", "value": 181},
    {"label": "MT 182 (n,dt)", "value": 182},
    {"label": "MT 183 (n,npd)", "value": 183},
    {"label": "MT 184 (n,npt)", "value": 184},
    {"label": "MT 185 (n,ndt)", "value": 185},
    {"label": "MT 186 (n,np3He)", "value": 186},
    {"label": "MT 187 (n,nd3He)", "value": 187},
    {"label": "MT 188 (n,nt3He)", "value": 188},
    {"label": "MT 189 (n,nta)", "value": 189},
    {"label": "MT 190 (n,2n2p)", "value": 190},
    {"label": "MT 191 (n,p3He)", "value": 191},
    {"label": "MT 192 (n,d3He)", "value": 192},
    {"label": "MT 193 (n,3Hea)", "value": 193},
    {"label": "MT 194 (n,4n2p)", "value": 194},
    {"label": "MT 195 (n,4n2a)", "value": 195},
    {"label": "MT 196 (n,4npa)", "value": 196},
    {"label": "MT 197 (n,3p)", "value": 197},
    {"label": "MT 198 (n,n3p)", "value": 198},
    {"label": "MT 199 (n,3n2pa)", "value": 199},
    {"label": "MT 200 (n,5n2p)", "value": 200},
    {"label": "MT 203 (n,Xp)", "value": 203},
    {"label": "MT 204 (n,Xd)", "value": 204},
    {"label": "MT 205 (n,Xt)", "value": 205},
    {"label": "MT 206 (n,3He)", "value": 206},
    {"label": "MT 207 (n,Xa)", "value": 207},
    {"label": "MT 301 (n,heat)", "value": 301},
    {"label": "MT 444 (n,damage)", "value": 444},
    {"label": "MT 649 (n,pc)", "value": 649},
    {"label": "MT 699 (n,dc)", "value": 699},
    {"label": "MT 749 (n,tc)", "value": 749},
    {"label": "MT 799 (n,3Hec)", "value": 799},
    {"label": "MT 849 (n,ac)", "value": 849},
    {"label": "MT 891 (n,2nc)", "value": 891},
    {"label": "MT 901 (n,displacement NRT)", "value": 901},
]

for i in range(50, 91):
    reaction_names.append({"label": f"MT {i} (n,n{i-50})", "value": i})

    # {'label[, ''MT '+str(i)+' (n,p{})'.format(i - 600) for i in range(600, 649)] +  'value':\  '+},
    # {'label[, ''MT '+str(i)+' (n,d{})'.format(i - 650) for i in range(650, 699)] +  'value':\  '+},
    # {'label[, ''MT '+str(i)+' (n,t{})'.format(i - 700) for i in range(700, 749)] +  'value':\  '+},
    # {'label[, ''MT '+str(i)+' (n,3He{})'.format(i - 750) for i in range(750, 799)] +  'value':\  '+},
    # {'label[, ''MT '+str(i)+' (n,a{})'.format(i - 800) for i in range(800, 849)] +  'value':\  '+},
    # {'label[, ''MT '+str(i)+' (n,2n{})'.format(i - 875) for i in range(875, 891) 'value':]  '+},
