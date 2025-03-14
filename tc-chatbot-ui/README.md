# Chatbot Frontend

Este es el frontend de un chatbot que permite a los usuarios realizar preguntas y recibir respuestas del modelo de IA. Además, cuenta con una funcionalidad de evaluación que permite subir un archivo de Excel con preguntas y respuestas esperadas para medir el desempeño del chatbot.

## 📌 Características

- Permite realizar preguntas al chatbot.
- Muestra respuestas generadas por el modelo.
- Permite cargar archivos Excel con preguntas y respuestas esperadas para evaluar el rendimiento del chatbot.
- Calcula métricas como relevancia de respuesta, precisión del contexto y similitud semántica.

## 🚀 Instalación

### 1️⃣ Requisitos Previos

Asegúrate de tener instalado:

- [Node.js](https://nodejs.org/)
- [npm](https://www.npmjs.com/) o [yarn](https://yarnpkg.com/)

### 2️⃣ Clonar el repositorio

```sh
git clone https://RoxVargas@bitbucket.org/roxvargas/tc-chatbot-ui.git
```

### 3️⃣ Instalar dependencias

```sh
yarn install
# o
npm install
```

### 4️⃣ Ejecutar el proyecto

```sh
yarn dev
# o
npm run dev
```

El frontend estará disponible en `http://localhost:8501/`.

## 📌 Uso

### 1️⃣ Interactuar con el chatbot

Accede a la raíz del frontend (`/`) y escribe preguntas en el campo de texto. El chatbot procesará la consulta y devolverá una respuesta.

### 2️⃣ Evaluación del chatbot

Dirígete a la ruta `/evaluacion` y carga un archivo de Excel con dos columnas:

- `answer` (respuesta generada por el modelo)
- `ground_truth` (respuesta esperada)

Tras procesar el archivo, se mostrarán métricas de evaluación como:

- **Faithfulness**
- **Answer Relevancy**
- **Context Recall**
- **Context Precision**
- **Semantic Similarity**
- **Answer Correctness**

📂 Archivo de prueba

Para facilitar la evaluación, puedes descargar un archivo de prueba en el siguiente enlace:

[Archivo de prueba en Google Drive](https://docs.google.com/spreadsheets/d/14ZQD9tNqsihnAlvVRPx0VrOP-R8Bq2smp66ofONYUUA/edit?gid=0#gid=0)

## 📂 Estructura del Proyecto

```
📦 chatbot-frontend
 ┣ 📂 components
 ┃ ┣ 📂 custom
 ┃ ┃ ┣ 📜 chatinput.tsx
 ┃ ┃ ┣ 📜 header.tsx
 ┃ ┃ ┣ 📜 message.tsx
 ┃ ┃ ┣ 📜 modal.tsx
 ┃ ┃ ┗ 📜 overview.tsx
 ┣ 📂 services
 ┃ ┗ 📜 chatService.ts
 ┣ 📂 pages
 ┃ ┣ 📜 chat.tsx  (Página principal del chatbot)
 ┃ ┣ 📜 evaluation.tsx (Página de evaluación)
 ┣ 📜 package.json
 ┣ 📜 tsconfig.json
 ┣ 📜 .gitignore
 ┗ 📜 README.md
```

## 🛠 Tecnologías Utilizadas

- React
- TypeScript
- XLSX.js (para procesamiento de archivos Excel)

