
# build with the following command
# sudo docker build -t material_xs_plotter .

# run with 
# docker run material_xs_plotter


# build with the following command
# sudo docker build -f Dockerfile_openmc -t openmcworkshop/openmc

FROM ghcr.io/openmc-data-storage/nuclear_data_base_docker:h5_base


RUN pip3 install streamlit
RUN pip3 install plotly


ENV OPENMC_CROSS_SECTIONS=/tendl-2019-hdf5/cross_sections.xml
COPY index.py .

EXPOSE 8080

ENTRYPOINT ["streamlit", "run", "index.py"]

