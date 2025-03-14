
# Chatbot RAG con evaluaci��n de m��tricas �0�6

Este repositorio contiene el c��digo y la configuraci��n necesaria para desplegar un chatbot basado en el modelo RAG (Retrieval-Augmented Generation) utilizando servicios de AWS. El chatbot est�� dise�0�9ado para responder preguntas basadas en un conjunto de datos predefinido y validar la calidad de las respuestas mediante m��tricas espec��ficas. A continuaci��n, se detalla la informaci��n necesaria para interactuar con los endpoints, las validaciones realizadas y los requisitos del proyecto.

---

# Instalaci��n y Configuraci��n

## Requisitos Previos 
- **Python** 3.11 o superior  
- **AWS CLI** configurado con credenciales v��lidas  
- **Docker** (opcional, para pruebas locales con AWS Lambda)  
- **Serverless Framework** instalado globalmente:  
  ```sh
  npm install -g serverless
  ```

## Clonar el repositorio:
```sh
git clone git@bitbucket.org:roxvargas/tc-backend-python.git
```

## Crear un entorno virtual e instalar dependencias:
```sh
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```
## Ejecuci��n Local con Serverless Offline

Para probar el chatbot en local usando Serverless Framework, ejecuta:
```sh
serverless offline
```

Para desplegar
```sh
serverless deploy
```

## Endpoints del proyecto

### 1. **Chatbot (`/chatbot`)**
Este endpoint recibe las pregunta del usuario y devuelve respuestas generadas por el modelo RAG.

#### **Par��metros de entrada:**
- **`message`** (string): La pregunta que el usuario desea hacer al chatbot.

#### **Respuesta:**
- **`response`** (object): Contiene la respuesta generada por el modelo RAG y metadatos adicionales.
  - **`content`** (string): La respuesta generada por el modelo RAG, en formato de texto.
  - **`confidence`** (float): Nivel de confianza de la respuesta, calculado a partir de los logprobs del modelo. Un valor cercano a 1 indica alta confianza.
  - **`processing_time`** (float): Tiempo en segundos que tom�� procesar la pregunta y generar la respuesta.
- **`documents`** (list): Lista de documentos o fragmentos de texto utilizados para generar la respuesta. Cada documento incluye:
  - **`page_content`** (string): Texto extra��do del documento.
  - **`metadata`** (object): Metadatos asociados al documento, como:
    - **`doc_id`** (string): Identificador ��nico del documento.
    - **`filename`** (string): Nombre del archivo de origen.
    - **`filetype`** (string): Tipo de archivo (por ejemplo, `application/pdf`).
    - **`page_number`** (int): N��mero de p��gina del documento.
    - **`orig_elements`** (list): Elementos originales del documento, como texto y metadatos adicionales.

---

### 2. **M��tricas (`/metrics`)**
Este endpoint genera las m��tricas de evaluaci��n de las respuestas generadas por el chatbot.

#### **Par��metros de entrada:**
- **`question`** (string): La pregunta original enviada al chatbot.
- **`answer`** (string): La respuesta generada por el chatbot.
- **`ground_truth`** (string): La respuesta esperada
- **`contexts`** (list): Lista de documentos rescuperados que se enviaron al LLM para generar la respuesta

#### **Respuesta:**

A continuaci��n, se muestra un ejemplo de la estructura de la respuesta que incluye los datos de entrada y las m��tricas calculadas:

```json
{
  "input_data": {
    "question": "cuales son los beneficios de la tarjeta diners",
    "ground_truth": "Acceso a salas vip",
    "answer": "acceso a salas vip",
    "contexts": ["salas vip"]
  },
  "metrics": {
    "faithfulness": 0.0,
    "answer_relevancy": 0.74,
    "context_recall": 1.0,
    "context_precision": 1.0,
    "semantic_similarity": 0.98,
    "answer_correctness": 1.0
  }
}
```
---

## Validaciones y Procesos

1. **Sanitizaci��n de Entrada:**
   - Se eliminan caracteres especiales no permitidos.
   - Se verifica que la pregunta no est�� vac��a.
   - Se valida que la pregunta no exceda un l��mite de longitud.

2. **Validaci��n de Preguntas con NLP:**
   - Se utiliza un modelo de NLP para asegurar que la pregunta est�� bien formulada.
   - Se rechazan preguntas incoherentes o mal estructuradas.

3. **Detecci��n de Lenguaje Da�0�9ino:**
   - Se emplea un modelo de detecci��n de lenguaje inapropiado para filtrar preguntas ofensivas o da�0�9inas.

4. **C��lculo de Confianza:**
   - La confianza de la respuesta se calcula utilizando los logprobs del LLM.

---

## Checklist de Requerimientos
- [X] ChatBot para consultas sobre facturaci��n y actividad sospechosa.
- [X] Respuestas limitadas al contexto
- [X] Uso de Python
- [X] Sanitizaci��n de entradas
- [X] La respuesta incluye los documentos recuperados
- [X] Tiempo de respuesta promedio < 10s.
- [X] Desplegar el chatbot en AWS utilizando servicios como Lambda, API Gateway y ECR.
- [x] Implementar el endpoint `/chatbot` para recibir preguntas y devolver respuestas.
- [x] Implementar el endpoint `/metrics` para evaluar las respuestas.
- [x] Validar preguntas bien formuladas con la integraci��n de  un modelo de NLP.
- [x] Detecci��n de lenguaje da�0�9ino.
- [x] Calcular la confianza de las respuestas utilizando logprobs.
- [x] Documentar el proceso de despliegue y uso del chatbot.
- [x] Probar el sistema con un conjunto de datos de prueba.


---

## Ejemplo de Uso

### Env��o de Pregunta al Chatbot:
```json
POST /chatbot
{
  "message": "�0�7C��mo detectar un consumo fraudulento?",
}
```

## Requisitos T��cnicos
- Lenguaje de Programaci��n: Python
- Frameworks: Serverless
- Servicios de AWS: Lambda, API Gateway, S3, ECR, Secrets Manager.
- Modelos: RAG para generaci��n de respuestas, modelo de NLP para validaci��n de preguntas, modelo de detecci��n de lenguaje da�0�9ino
