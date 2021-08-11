
# build with the following command
# sudo docker build -t material_xs_plotter .

# run with 
# docker run --network host -t material_xs_plotter



FROM ghcr.io/openmc-data-storage/nuclear_data_base_docker:h5_base


COPY requirements.txt .
RUN pip install -r requirements.txt

RUN pip install gunicorn==20.0.4

ENV OPENMC_CROSS_SECTIONS=/TENDL-2019/cross_sections.xml
# COPY assets assets
COPY options.py .
COPY app.py .

ENV PORT 8080

EXPOSE 8080

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run
# to handle instance scaling. For more details see
# https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 app:server
