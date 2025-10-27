# Chatbot RAG con evaluación de métricas

Este repositorio contiene el código y la configuración necesaria para desplegar un chatbot basado en el modelo RAG (Retrieval-Augmented Generation) utilizando servicios de AWS. El chatbot está diseñado para responder preguntas basadas en un conjunto de datos predefinido y validar la calidad de las respuestas mediante métricas específicas. A continuación, se detalla la información necesaria para interactuar con los endpoints, las validaciones realizadas y los requisitos del proyecto.

---

# Instalación y Configuración

## Requisitos Previos

* **Python** 3.11 o superior
* **AWS CLI** configurado con credenciales válidas
* **Docker** (opcional, para pruebas locales con AWS Lambda)
* **Serverless Framework** instalado globalmente:

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

## Ejecución Local con Serverless Offline

Para probar el chatbot en local usando Serverless Framework, ejecuta:

```sh
serverless offline
```

Para desplegar:

```sh
serverless deploy
```

---

## Endpoints del proyecto

### 1. **Chatbot (`/chatbot`)**

Este endpoint recibe las preguntas del usuario y devuelve respuestas generadas por el modelo RAG.

#### **Parámetros de entrada:**

* **`message`** (string): La pregunta que el usuario desea hacer al chatbot.

#### **Respuesta:**

* **`response`** (object): Contiene la respuesta generada por el modelo RAG y metadatos adicionales.

  * **`content`** (string): La respuesta generada por el modelo RAG, en formato de texto.
  * **`confidence`** (float): Nivel de confianza de la respuesta, calculado a partir de los logprobs del modelo. Un valor cercano a 1 indica alta confianza.
  * **`processing_time`** (float): Tiempo en segundos que tomó procesar la pregunta y generar la respuesta.
* **`documents`** (list): Lista de documentos o fragmentos de texto utilizados para generar la respuesta. Cada documento incluye:

  * **`page_content`** (string): Texto extraído del documento.
  * **`metadata`** (object): Metadatos asociados al documento, como:

    * **`doc_id`** (string): Identificador único del documento.
    * **`filename`** (string): Nombre del archivo de origen.
    * **`filetype`** (string): Tipo de archivo (por ejemplo, `application/pdf`).
    * **`page_number`** (int): Número de página del documento.
    * **`orig_elements`** (list): Elementos originales del documento, como texto y metadatos adicionales.

---

### 2. **Métricas (`/metrics`)**

Este endpoint genera las métricas de evaluación de las respuestas generadas por el chatbot.

#### **Parámetros de entrada:**

* **`question`** (string): La pregunta original enviada al chatbot.
* **`answer`** (string): La respuesta generada por el chatbot.
* **`ground_truth`** (string): La respuesta esperada.
* **`contexts`** (list): Lista de documentos recuperados que se enviaron al LLM para generar la respuesta.

#### **Respuesta:**

A continuación, se muestra un ejemplo de la estructura de la respuesta que incluye los datos de entrada y las métricas calculadas:

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

1. **Sanitización de Entrada:**

   * Se eliminan caracteres especiales no permitidos.
   * Se verifica que la pregunta no esté vacía.
   * Se valida que la pregunta no exceda un límite de longitud.

2. **Validación de Preguntas con NLP:**

   * Se utiliza un modelo de NLP para asegurar que la pregunta esté bien formulada.
   * Se rechazan preguntas incoherentes o mal estructuradas.

3. **Detección de Lenguaje Dañino:**

   * Se emplea un modelo de detección de lenguaje inapropiado para filtrar preguntas ofensivas o dañinas.

4. **Cálculo de Confianza:**

   * La confianza de la respuesta se calcula utilizando los logprobs del LLM.

---

## Checklist de Requerimientos

* [x] ChatBot para consultas sobre facturación y actividad sospechosa.
* [x] Respuestas limitadas al contexto.
* [x] Uso de Python.
* [x] Sanitización de entradas.
* [x] La respuesta incluye los documentos recuperados.
* [x] Tiempo de respuesta promedio < 10s.
* [x] Desplegar el chatbot en AWS utilizando servicios como Lambda, API Gateway y ECR.
* [x] Implementar el endpoint `/chatbot` para recibir preguntas y devolver respuestas.
* [x] Implementar el endpoint `/metrics` para evaluar las respuestas.
* [x] Validar preguntas bien formuladas con la integración de un modelo de NLP.
* [x] Detección de lenguaje dañino.
* [x] Calcular la confianza de las respuestas utilizando logprobs.
* [x] Documentar el proceso de despliegue y uso del chatbot.
* [x] Probar el sistema con un conjunto de datos de prueba.

---

## Ejemplo de Uso

### Envío de Pregunta al Chatbot:

```json
POST /chatbot
{
  "message": "¿Cómo detectar un consumo fraudulento?"
}
```

---

## Requisitos Técnicos

* Lenguaje de Programación: Python
* Frameworks: Serverless
* Servicios de AWS: Lambda, API Gateway, S3, ECR, Secrets Manager.
* Modelos: RAG para generación de respuestas, modelo de NLP para validación de preguntas, modelo de detección de lenguaje dañino.


