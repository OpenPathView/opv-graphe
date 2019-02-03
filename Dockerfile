FROM python:3.6

ENV OPV_GRAPHE_WORKER 8
ENV OPV_GRAPHE_PORT 5015

COPY . /source/opv-graphe

WORKDIR /source/opv-graphe

RUN pip3 install -r requirements.txt && \
python3 setup.py install

EXPOSE ${OPV_GRAPHE_PORT}:${OPV_GRAPHE_PORT}

CMD ["sh", "-c", "gunicorn --bind 0.0.0.0:${OPV_GRAPHE_PORT} opv.graphe.__main__:app -w ${OPV_GRAPHE_WORKER}"]
