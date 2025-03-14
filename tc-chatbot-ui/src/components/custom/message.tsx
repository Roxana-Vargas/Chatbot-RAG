import { useState} from 'react';
import { motion } from 'framer-motion';
import { cx } from 'classix';
import { SparklesIcon } from './icons';
import { Markdown } from './markdown';
import { MessageActions } from '@/components/custom/actions';
import { Modal } from './modal';

export const PreviewMessage = ({ message, docs, }: { message: any; docs: Array<object> }) => {
  console.log('message', message);

  const [isModalOpen, setIsModalOpen] = useState(false);

  const openModal = () => setIsModalOpen(true);
  const closeModal = () => setIsModalOpen(false);
  return (
    <motion.div
      className="w-full mx-auto max-w-3xl px-4 group/message"
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      data-role={message.role}
    >
      <div
        className={cx(
          'group-data-[role=user]/message:bg-zinc-700 dark:group-data-[role=user]/message:bg-muted group-data-[role=user]/message:text-white flex gap-4 group-data-[role=user]/message:px-3 w-full group-data-[role=user]/message:w-fit group-data-[role=user]/message:ml-auto group-data-[role=user]/message:max-w-2xl group-data-[role=user]/message:py-2 rounded-xl'
        )}
      >
        {message.role === 'assistant' && (
          <div className="size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border">
            <SparklesIcon size={14} />
          </div>
        )}

        <div className="flex flex-col w-full">
          {message.content && (
            <div className="flex flex-col gap-4 text-left">
              <Markdown>{message.content}</Markdown>
              {message.role === 'bot' && (
                <div className="flex flex-row gap-4 text-left">
                  <button
                    onClick={() => openModal()}
                    className="text-sm text-gray-600 border border-gray-300 rounded px-2 py-1 self-start hover:bg-gray-50 transition-colors"
                  >
                    Ver Recursos
                  </button>
                  <div className="flex gap-2">
                    <span className="bg-blue-100 text-blue-700 text-xs font-medium px-2 py-1 rounded">
                      Confianza: {message.confidence}%
                    </span>
                    <span className="bg-green-100 text-green-700 text-xs font-medium px-2 py-1 rounded">
                      Tiempo de Respuesta: {message.time}ms
                    </span>
                  </div>


                </div>
              )}
            </div>
          )}

          {message.role === 'assistant' && (
            <><MessageActions message={message} /></>
          )}
        </div>
        {/* Modal para mostrar los documentos */}
        {
          isModalOpen && (
            <Modal isOpen={isModalOpen} onClose={closeModal}>
              <div className="flex flex-col gap-4">
                <h2 className="text-xl font-semibold" style={{ color: "black" }}>Documentos</h2>
                <ul className="flex flex-col gap-4">
                  {docs.map((document: any, index: number) => (
                    <li key={index} className="flex gap-4">
                      <p style={{ color: "black" }} className="text-sm">{document.page_content}</p>
                    </li>
                  ))}
                </ul>
              </div>
            </Modal>
          )
        }
      </div>
    </motion.div>
  );
};

export const ThinkingMessage = () => {
  const role = 'assistant';

  return (
    <motion.div
      className="w-full mx-auto max-w-3xl px-4 group/message "
      initial={{ y: 5, opacity: 0 }}
      animate={{ y: 0, opacity: 1, transition: { delay: 0.2 } }}
      data-role={role}
    >
      <div
        className={cx(
          'flex gap-4 group-data-[role=user]/message:px-3 w-full group-data-[role=user]/message:w-fit group-data-[role=user]/message:ml-auto group-data-[role=user]/message:max-w-2xl group-data-[role=user]/message:py-2 rounded-xl',
          'group-data-[role=user]/message:bg-muted'
        )}
      >
        <div className="size-8 flex items-center rounded-full justify-center ring-1 shrink-0 ring-border">
          <SparklesIcon size={14} />
        </div>
      </div>
    </motion.div>
  );
};
