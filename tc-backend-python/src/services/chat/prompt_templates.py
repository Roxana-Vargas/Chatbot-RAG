from langchain.prompts import PromptTemplate

# Prompt for general questions on procedures
general_query_prompt = PromptTemplate.from_template(
    """
    Eres un asistente para asesores de soporte de una plataforma de streaming.
    Responde usando únicamente la información del siguiente contexto extraído de la documentación interna.

    **Contexto:**
    {context}

    **Pregunta del asesor:**
    {user_message}

    **Respuesta basada en la documentación:**
    """
)

# Prompt for billing and payment questions
billing_query_prompt = PromptTemplate.from_template(
    """
    Eres un asistente especializado en facturación para asesores de soporte en una plataforma de streaming.
    Responde basándote únicamente en la información del contexto extraído de la documentación interna.

    **Contexto:**
    {context}

    **Pregunta del asesor:**
    {user_message}

    **Instrucciones precisas según la documentación:**
    """
)

# Prompt for fraud and suspicious activity detection
fraud_detection_prompt = PromptTemplate.from_template(
    """
    Eres un asistente experto en seguridad para asesores de soporte de una plataforma de streaming.
    Ayuda a identificar y responder sobre actividad sospechosa según la documentación interna.

    **Contexto:**
    {context}

    **Caso reportado por el asesor:**
    {user_message}

    **Pasos recomendados según los procedimientos internos:**
    """
)

# Prompt to summarize long procedures
procedure_summary_prompt = PromptTemplate.from_template(
    """
    Eres un asistente de soporte técnico. Simplifica y resume los procedimientos detallados en la documentación.

    **Procedimiento original:**
    {context}

    **Resumen en pasos claros para el asesor de soporte:**
    """
)

# Export prompts

PROMPT_TEMPLATES = {
    "general_query": general_query_prompt,
    "billing_query": billing_query_prompt,
    "fraud_detection": fraud_detection_prompt,
    "procedure_summary": procedure_summary_prompt,
}