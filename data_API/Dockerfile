FROM ubuntu:18.04
RUN apt-get update
RUN apt-get install -y vim 
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt-get update
RUN apt install -y python3.9
RUN apt-get install -y curl
RUN apt install -y python3.9-distutils
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.9 get-pip.py
COPY / /data_API
RUN pip install tornado scikit-learn flashtext rdflib pandas numpy requests
WORKDIR "/data_API"
CMD python3.9 api_server.py
