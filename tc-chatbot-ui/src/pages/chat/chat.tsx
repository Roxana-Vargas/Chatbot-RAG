import { useState } from "react";
import { ChatInput } from "@/components/custom/chatinput";
import { PreviewMessage, ThinkingMessage } from "../../components/custom/message";
import { useScrollToBottom } from '@/components/custom/use-scroll-to-bottom';
import { message } from "../../interfaces/interfaces";
import { Overview } from "@/components/custom/overview";
import { Header } from "@/components/custom/header";
import { v4 as uuidv4 } from 'uuid';
import { sendQuestion } from "@/services/chatService";


export function Chat() {
  const [messagesContainerRef, messagesEndRef] = useScrollToBottom<HTMLDivElement>();
  const [messages, setMessages] = useState<message[]>([]);
  const [question, setQuestion] = useState<string>("");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [documents, setDocuments] = useState<any[]>([]); // Estado para almacenar los documentos


  async function handleSubmit(text?: string) {
    const userMessage: message = {
      id: uuidv4(),
      content: text || question,
      role: 'user',
      confidence: 0,
      time: 0,
    };

    setMessages((prevMessages) => [...prevMessages, userMessage]);
    setQuestion("");
    setIsLoading(true);

    try {
      const response = await sendQuestion(text || question);

      const botMessage: message = {
        id: uuidv4(),
        content: response.response.content,
        role: 'bot',
        confidence: response.response.confidence,
        time: Math.floor(response.response.processing_time),
      };

      setMessages((prevMessages) => [...prevMessages, botMessage]);

      // Almacenar los documentos en el estado
      if (response.documents && response.documents.length > 0) {
        setDocuments(response.documents);
      }
    } catch (error) {
      console.error("Error:", error);

      const errorMessage: message = {
        id: uuidv4(),
        content: "Hubo un error al procesar tu solicitud. Inténtalo de nuevo.",
        role: 'bot',
        confidence: 0,
        time: 0,
      };

      setMessages((prevMessages) => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex flex-col min-w-0 h-dvh bg-background">
      <Header />
      <div className="flex flex-col min-w-0 gap-6 flex-1 overflow-y-scroll pt-4" ref={messagesContainerRef}>
        {messages.length == 0 && <Overview />}
        {messages.map((message) => (
          <PreviewMessage key={message.id} message={message} docs={documents} />
        ))}
        {isLoading && (
          <div className="w-full mx-auto max-w-3xl px-4 flex items-center justify-start">
            <ThinkingMessage />
            <p className="ml-2">Procesando...</p>
          </div>
        )}

        <div ref={messagesEndRef} className="shrink-0 min-w-[24px] min-h-[24px]" />
      </div>
      <div className="flex mx-auto px-4 bg-background pb-4 md:pb-6 gap-2 w-full md:max-w-3xl">
        <ChatInput
          question={question}
          setQuestion={setQuestion}
          onSubmit={handleSubmit}
          isLoading={isLoading}
        />
      </div>


    </div>
  );
}