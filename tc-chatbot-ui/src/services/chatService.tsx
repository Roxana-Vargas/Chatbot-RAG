
export const sendQuestion = async (question: string) => {
  try {
    const url = `${import.meta.env.VITE_APP_HOST}/dev/chatbot`; // Usa VITE_ si trabajas con Vite

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ message: question }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Error en la solicitud: ${response.status} - ${errorText}`);
    }

    return await response.json();
  } catch (error: unknown) {
    console.error("Error en sendQuestion:", error);
    return { success: false, message: error instanceof Error ? error.message : "Error desconocido" };
  }
};

export const sendEvaluation = async (data: object) => {
  try {
    const url = `${import.meta.env.VITE_APP_HOST}/dev/metrics`;

    const response = await fetch(url, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(data),
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Error en la solicitud: ${response.status} - ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error("Error en sendEvaluation:", error);
    return { success: false, message: error instanceof Error ? error.message : "Error desconocido" };
  }
};