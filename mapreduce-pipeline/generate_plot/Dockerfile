FROM python:3.8-buster

RUN pip install matplotlib

COPY compile_plot.py /compile_plot.py
RUN chmod a+x /compile_plot.py

ENTRYPOINT ["python", "./compile_plot.py"]
