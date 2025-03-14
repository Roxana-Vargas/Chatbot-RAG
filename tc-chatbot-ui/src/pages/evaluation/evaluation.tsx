import React, { useState } from "react";
import * as XLSX from "xlsx";
import { sendQuestion, sendEvaluation } from "@/services/chatService";
import { Header } from "@/components/custom/header";
import { Modal } from "@/components/custom/modal";
import { Skeleton } from "@/components/ui/skeleton";

export function Evaluation() {
  const [data, setData] = useState<any[]>([]);
  const [results, setResults] = useState<EvaluationResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [modalContent, setModalContent] = useState<Array<string>>([]);

  interface EvaluationResult {
    question: string;
    ground_truth: string;
    answer?: string;
    time?: number;
    contexts?: string[];
    metrics?: {
      faithfulness: number;
      answer_relevancy: number;
      context_recall: number;
      context_precision: number;
      semantic_similarity: number;
      answer_correctness: number;
    };
  }

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (!files) return;
    const file = files[0];
    const reader = new FileReader();
    reader.onload = (event) => {
      const binaryStr = event.target?.result;
      const workbook = XLSX.read(binaryStr, { type: "binary" });
      const sheetName = workbook.SheetNames[0];
      const sheet = workbook.Sheets[sheetName];
      const jsonData = XLSX.utils.sheet_to_json(sheet);
      setData(jsonData);
    };
    reader.readAsBinaryString(file);
  };

  const processEvaluation = async () => {
    setIsLoading(true);
    setResults([]);

    for (const item of data) {
      const { question, ground_truth } = item;
      const partialResult: EvaluationResult = { question, ground_truth };
      setResults((prev) => [...prev, partialResult]);

      try {
        const response = await sendQuestion(question);
        const pageContents = response.documents.map((doc: any) => doc.page_content);

        setResults((prev) => {
          const updatedResults = [...prev];
          const index = updatedResults.findIndex((r) => r.question === question);
          if (index !== -1) {
            updatedResults[index] = {
              ...updatedResults[index],
              answer: response.response.content,
              contexts: pageContents,
              time: Math.floor(response.response.processing_time),
            };
          }
          return updatedResults;
        });

        let evaluationData;
        let attempt = 0;
        let success = false;

        while (attempt < 2 && !success) {
          try {
            evaluationData = await sendEvaluation({
              question,
              ground_truth,
              answer: response.response.content,
              contexts: pageContents,
            });
            success = true;
          } catch (error) {
            console.error(`Intento ${attempt + 1} fallido en sendEvaluation:`, error);
            attempt++;
            if (attempt >= 2) {
              console.error("Fallo definitivo en sendEvaluation");
            }
          }
        }

        if (success && evaluationData) {
          setResults((prev) => {
            const updatedResults = [...prev];
            const index = updatedResults.findIndex((r) => r.question === question);
            if (index !== -1) {
              updatedResults[index] = { ...updatedResults[index], metrics: evaluationData.metrics };
            }
            return updatedResults;
          });
        }
      } catch (error) {
        console.error("Error procesando la pregunta:", error);
      }
    }

    setIsLoading(false);
  };


  const totalTime = results.reduce((sum, message) => sum + (message.time || 0), 0);
  const averageTime = results.length > 0 ? (totalTime / results.length).toFixed(2) : "0";

  const calculateAccuracy = (results: EvaluationResult[]) => {
    if (!results.length) return 0;
    const totalCorrectness = results.reduce((sum, r) => sum + (r.metrics?.['answer_correctness'] || 0), 0);
    return ((totalCorrectness / results.length) * 100).toFixed(2);
  };

  const EvaluationResults = ({ results }: { results: EvaluationResult[] }) => {
    return (
      <div>
          <span>📊 Precisión: {calculateAccuracy(results)}%</span>
      </div>
    );
  };
  


  return (
    <div className="flex flex-col min-h-screen bg-background">
      <Header />
      <div className="flex flex-col items-center justify-center p-4">
        <h1 className="text-2xl font-bold mb-4 text-center">Evaluación</h1>
        <input
          type="file"
          accept=".xlsx, .xls"
          onChange={handleFileUpload}
          className="mb-4 p-2 border border-gray-300 rounded"
        />
        <button
          onClick={processEvaluation}
          disabled={isLoading || data.length === 0}
          className="bg-blue-500 text-white px-4 py-2 rounded disabled:bg-gray-400"
        >
          {isLoading ? "Procesando..." : "Iniciar Evaluación"}
        </button>

        {results.length > 0 && (
          <div className="mt-6 w-full overflow-x-auto">
            <table className="min-w-full bg-white dark:bg-gray-800 text-sm shadow-md rounded-lg">
              <thead>
                <tr className="bg-gray-100 dark:bg-gray-700">
                  <th className="px-4 py-2 text-left">Pregunta</th>
                  <th className="px-4 py-2 text-left">Respuesta Esperada</th>
                  <th className="px-4 py-2 text-left">Respuesta del Chatbot</th>
                  <th className="px-4 py-2 text-left">Tiempo</th>
                  <th className="px-4 py-2 text-left">Recursos</th>
                  <th className="px-4 py-2 text-left">Faithfulness</th>
                  <th className="px-4 py-2 text-left">Answer Relevancy</th>
                  <th className="px-4 py-2 text-left">Context Recall</th>
                  <th className="px-4 py-2 text-left">Context Precision</th>
                  <th className="px-4 py-2 text-left">Semantic Similarity</th>
                  <th className="px-4 py-2 text-left">Answer Correctness</th>
                </tr>
              </thead>
              <tbody>
                {results.map((result, index) => (
                  <tr key={index} className="border-t hover:bg-gray-50 dark:hover:bg-gray-700">
                    <td className="px-4 py-2">{result.question}</td>
                    <td className="px-4 py-2">{result.ground_truth}</td>
                    <td className="px-4 py-2">{result.answer || <Skeleton className="w-32 h-4" />}</td>
                    <td className="px-4 py-2">{result.time || <Skeleton className="w-32 h-4" />}</td>
                    <td className="px-4 py-2">
                      {result.contexts ? (
                        <button
                          className="text-blue-500 underline hover:text-blue-700"
                          onClick={() => {
                            console.log(result.contexts);
                            setModalContent(result.contexts || []);
                            setIsModalOpen(true);
                          }}
                        >
                          Ver Recursos
                        </button>
                      ) : <Skeleton className="w-24 h-4" />}
                    </td>
                    {result.metrics ? (
                      Object.values(result.metrics).map((metric, i) => (
                        <td key={i} className="px-4 py-2">{metric}</td>
                      ))
                    ) : (
                      <td colSpan={6} className="px-4 py-2 text-center">
                        <Skeleton className="w-full h-4" />
                      </td>
                    )}
                  </tr>
                ))}
              </tbody>
            </table>
            <br/>
            <span className="bg-green-100 text-green-700 text-xs my-4 font-medium px-2 py-1 rounded">
              Tiempo de Respuesta Promedio: {averageTime}ms
            </span>
            <br/>
            <EvaluationResults results={results} />
          </div>
        )}
        {/* Modal */}
        {isModalOpen && (
          <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)}>
            <div className="flex flex-col gap-4 p-4">
              <h2 className="text-xl font-semibold text-black">Documentos</h2>
              <ul className="flex flex-col gap-4">
                {modalContent.map((document: any, index: number) => (
                  <li key={index} className="flex gap-4">
                    <p className="text-sm text-black">{document}</p>
                  </li>
                ))}
              </ul>
            </div>
          </Modal>
        )}
      </div>
    </div>
  );
}