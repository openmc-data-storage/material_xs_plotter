import os

import numpy as np
import openmc
import streamlit as st
import plotly.graph_objects as go

key = 1

number_of_elements = st.selectbox(key = key,
                label='Number of different elements',
                options=range(0, 10))

element_names = ['Hydrogen', 'Helium', 'Lithium',
                 'Beryllium', 'Boron', 'Carbon', 'Nitrogen',
                 'Oxygen', 'Fluorine', 'Neon', 'Sodium',
                 'Magnesium', 'Aluminium', 'Silicon',
                 'Phosphorus', 'Sulfur', 'Chlorine',
                 'Argon', 'Potassium', 'Calcium',
                 'Scandium', 'Titanium', 'Vanadium',
                 'Chromium', 'Manganese', 'Iron',
                 'Cobalt', 'Nickel', 'Copper', 'Zinc',
                 'Gallium', 'Germanium', 'Arsenic',
                 'Selenium', 'Bromine', 'Krypton',
                 'Rubidium', 'Strontium', 'Yttrium',
                 'Zirconium', 'Niobium', 'Molybdenum',
                 'Technetium', 'Ruthenium', 'Rhodium',
                 'Palladium', 'Silver', 'Cadmium', 'Indium',
                 'Tin', 'Antimony', 'Tellurium', 'Iodine',
                 'Xenon', 'Caesium', 'Barium', 'Lanthanum',
                 'Cerium', 'Praseodymium', 'Neodymium',
                 'Promethium', 'Samarium', 'Europium', 
                 'Gadolinium', 'Terbium', 'Dysprosium',
                 'Holmium', 'Erbium', 'Thulium',
                 'Ytterbium', 'Lutetium', 'Hafnium',
                 'Tantalum', 'Tungsten', 'Rhenium',
                 'Osmium', 'Iridium', 'Platinum',
                 'Gold', 'Mercury', 'Thallium',
                 'Lead', 'Bismuth', 'Polonium',
                 'Astatine', 'Radon', 'Francium',
                 'Radium', 'Actinium', 'Thorium',
                 'Protactinium', 'Uranium', 'Neptunium',
                 'Plutonium', 'Americium', 'Curium',
                 'Berkelium', 'Californium', 'Einsteinium',
                 'Fermium', 'Mendelevium', 'Nobelium',
                 'Lawrencium', 'Rutherfordium', 'Dubnium',
                 'Seaborgium', 'Bohrium', 'Hassium',
                 'Meitnerium', 'Darmstadtium', 'Roentgenium',
                 'Copernicium', 'Nihonium', 'Flerovium',
                 'Moscovium', 'Livermorium', 'Tennessine',
                 'Oganesson']


REACTION_NAME = ['MT 1 (n,total)', 
                'MT 2 (n,elastic)',
                'MT 3 (n,nonelastic)', 
                'MT 4 (n,level)',
                'MT 5 (n,misc)', 
                'MT 11 (n,2nd)', 
                'MT 16 (n,2n)', 
                'MT 17 (n,3n)',
                'MT 18 (n,fission)', 
                'MT 19 (n,f)', 
                'MT 20 (n,nf)', 
                'MT 21 (n,2nf)',
                'MT 22 (n,na)', 
                'MT 23 (n,n3a)', 
                'MT 24 (n,2na)', 
                'MT 25 (n,3na)',
                'MT 27 (n,absorption)', 
                'MT 28 (n,np)', 
                'MT 29 (n,n2a)',
                'MT 30 (n,2n2a)', 
                'MT 32 (n,nd)', 
                'MT 33 (n,nt)', 
                'MT 34 (n,nHe-3)',
                'MT 35 (n,nd2a)', 
                'MT 36 (n,nt2a)', 
                'MT 37 (n,4n)', 
                'MT 38 (n,3nf)',
                'MT 41 (n,2np)', 
                'MT 42 (n,3np)', 
                'MT 44 (n,n2p)', 
                'MT 45 (n,npa)',
                'MT 91 (n,nc)', 
                'MT 101 (n,disappear)', 
                'MT 102 (n,gamma)',
                'MT 103 (n,p)', 
                'MT 104 (n,d)', 
                'MT 105 (n,t)', 
                'MT 106 (n,3He)',
                'MT 107 (n,a)', 
                'MT 108 (n,2a)', 
                'MT 109 (n,3a)', 
                'MT 111 (n,2p)',
                'MT 112 (n,pa)', 
                'MT 113 (n,t2a)', 
                'MT 114 (n,d2a)', 
                'MT 115 (n,pd)',
                'MT 116 (n,pt)', 
                'MT 117 (n,da)', 
                'MT 152 (n,5n)', 
                'MT 153 (n,6n)',
                'MT 154 (n,2nt)', 
                'MT 155 (n,ta)', 
                'MT 156 (n,4np)', 
                'MT 157 (n,3nd)',
                'MT 158 (n,nda)', 
                'MT 159 (n,2npa)', 
                'MT 160 (n,7n)', 
                'MT 161 (n,8n)',
                'MT 162 (n,5np)', 
                'MT 163 (n,6np)', 
                'MT 164 (n,7np)', 
                'MT 165 (n,4na)',
                'MT 166 (n,5na)', 
                'MT 167 (n,6na)', 
                'MT 168 (n,7na)', 
                'MT 169 (n,4nd)',
                'MT 170 (n,5nd)', 
                'MT 171 (n,6nd)', 
                'MT 172 (n,3nt)', 
                'MT 173 (n,4nt)',
                'MT 174 (n,5nt)', 
                'MT 175 (n,6nt)', 
                'MT 176 (n,2n3He)',
                'MT 177 (n,3n3He)', 
                'MT 178 (n,4n3He)', 
                'MT 179 (n,3n2p)',
                'MT 180 (n,3n3a)', 
                'MT 181 (n,3npa)', 
                'MT 182 (n,dt)',
                'MT 183 (n,npd)', 
                'MT 184 (n,npt)', 
                'MT 185 (n,ndt)',
                'MT 186 (n,np3He)', 
                'MT 187 (n,nd3He)', 
                'MT 188 (n,nt3He)',
                'MT 189 (n,nta)', 
                'MT 190 (n,2n2p)', 
                'MT 191 (n,p3He)',
                'MT 192 (n,d3He)', 
                'MT 193 (n,3Hea)', 
                'MT 194 (n,4n2p)',
                'MT 195 (n,4n2a)', 
                'MT 196 (n,4npa)', 
                'MT 197 (n,3p)',
                'MT 198 (n,n3p)', 
                'MT 199 (n,3n2pa)', 
                'MT 200 (n,5n2p)', 
                'MT 203 (n,Xp)',
                'MT 204 (n,Xd)',
                'MT 205 (n,Xt)',
                'MT 206 (n,3He)',
                'MT 207 (n,Xa)',
                'MT 301 (n,heat)',
                'MT 444 (n,damage)',
                'MT 649 (n,pc)', 
                'MT 699 (n,dc)', 
                'MT 749 (n,tc)', 
                'MT 799 (n,3Hec)',
                'MT 849 (n,ac)', 
                'MT 891 (n,2nc)',
                'MT 901 (n,displacement NRT)']+ \
                ['MT '+str(i)+' (n,n{})'.format(i - 50) for i in range(50, 91)] + \
                ['MT '+str(i)+' (n,p{})'.format(i - 600) for i in range(600, 649)] + \
                ['MT '+str(i)+' (n,d{})'.format(i - 650) for i in range(650, 699)] + \
                ['MT '+str(i)+' (n,t{})'.format(i - 700) for i in range(700, 749)] + \
                ['MT '+str(i)+' (n,3He{})'.format(i - 750) for i in range(750, 799)] + \
                ['MT '+str(i)+' (n,a{})'.format(i - 800) for i in range(800, 849)] + \
                ['MT '+str(i)+' (n,2n{})'.format(i - 875) for i in range(875, 891)]


element_symbols_and_values = []
element_values = []
for i in range(number_of_elements):
    key = key + 1
    element_symbol = st.selectbox(key = key,
                label='Element ' + str(i+1) +' symbol',
                options=element_names)

    key = key + 1
    element_value = st.number_input(key = key,
                min_value=0.,
                label='Element ' + str(i+1) + ' mass fraction')

    # if element_value 
    element_values.append(element_value)
    element_symbols_and_values.append((element_symbol, element_value))

density_value = st.number_input(key = key+2,
            min_value=0.,
            label='density g/cm3')


reaction_descriptions = st.multiselect(key = key+3,
            label='MT reaction number',
            options= REACTION_NAME)

axis_scales = st.selectbox(key = key+4,
            label='Axis scale',
            options= ['linear-linear', 'log-linear', 'linear-log', 'log-log'])

percent_type = st.selectbox(key = key+4,
            label='Axis scale',
            options= ['atom fraction', 'weight fraction'])

if percent_type == 'atom fraction':
    percent_type_symbol = 'ao'
elif percent_type == 'weight fraction':
    percent_type_symbol = 'wo'

fig = go.Figure()

if 0 in element_values:
    st.write("elements can't have zero values")

# if st.button('update graph'):
elif number_of_elements == 0:
    st.write('Selecte the number of elements')

elif density_value == 0:
    st.write('set the density value first')

elif len(reaction_descriptions)==0:
    st.write('select some reactions')

else:

    openmc_material = openmc.Material()
    for element_symbol_and_value in element_symbols_and_values:
        element_symbol = element_symbol_and_value[0]
        element_value = element_symbol_and_value[1]

        if element_value == 0:
            st.write('The element mass fraction is zero for', element_symbol)

        openmc_material.add_element(element_symbol, element_value, percent_type_symbol)

    openmc_material.set_density('g/cm3', density_value)

    mt_numbers = []
    for entry in reaction_descriptions:
        # print(entry)
        mt_number = int(entry.split(" ")[1])
        if mt_number == 1:
            mt_number='total'
        mt_numbers.append(mt_number)
        #mt_numbers.append(entry.split(" ")[-1])

    # print(openmc_material)

        # print(mt_number)
    x_data, y_datas = openmc.calculate_cexs(openmc_material,
                                            'material',
                                            mt_numbers)
    for reaction_description, y_data in zip(reaction_descriptions, y_datas):
        if not np.any(y_data):
            # print('all zero' , reaction_description)
            st.write(reaction_description, ' cross section not found in material')
        # print(y_data)
        else:

            fig.add_trace(go.Scatter(y=y_data,
                                    x=x_data,
                                    name= reaction_description,
                                    mode='lines'
                                    )
                            )

    xaxis_scale = axis_scales.split('-')[0]
    yaxis_scale = axis_scales.split('-')[1]

    fig.update_layout(
        title='Material cross sections',
        showlegend=True,
        xaxis={'title': 'Energy (eV)', 'type': xaxis_scale},
        yaxis={'title': 'Macroscopic Cross Section (1/cm)', 'type': yaxis_scale}
    )

    fig.update_traces(opacity=0.4)

    st.write(fig)
