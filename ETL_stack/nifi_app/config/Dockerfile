FROM apache/nifi:latest


USER root

RUN apt-get update 

# Install Python3
RUN apt-get install -y python3 python3-pip
RUN apt-get install -y libpython3.11-stdlib


RUN pip3 install pandas
RUN pip3 install aiofiles
RUN pip3 install pyarrow
