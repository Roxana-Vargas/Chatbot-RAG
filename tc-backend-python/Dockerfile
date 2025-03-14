# Usa la imagen base de Lambda con Python 3.11
FROM public.ecr.aws/lambda/python:3.11

# Instala Git y otras dependencias necesarias
RUN yum update -y && yum install -y git

# Copia y instala dependencias
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Descargar el modelo de spaCy manualmente
RUN python -m spacy download es_core_news_sm  

# Copia el código de la aplicación
COPY src/ ./src/

# Especifica el manejador de Lambda
# Punto de entrada
ENTRYPOINT [ "/lambda-entrypoint.sh" ]
