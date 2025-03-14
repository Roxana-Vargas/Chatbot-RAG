import { ThemeToggle } from "./theme-toggle";
import { Link, useLocation } from "react-router-dom";
import { FaChartLine } from "react-icons/fa"; // Icono de evaluación
import { FaRobot } from "react-icons/fa";

export const Header = () => {
  const location = useLocation();
  const isEvaluation = location.pathname === "/evaluation";
  return (
    <>
      <header className="flex items-center justify-between px-2 sm:px-4 py-2 bg-background text-black dark:text-white w-full">
        <div className="flex items-center space-x-1 sm:space-x-2">
          <ThemeToggle />
        </div>
        <div className="flex items-center space-x-1 sm:space-x-2">
          {
            !isEvaluation ? (
              <Link
                to="/evaluation"
                className="flex items-center p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
              >
                <FaChartLine className="w-5 h-5" />
                <span className="ml-2 hidden sm:inline">Evaluación</span>
              </Link>
            ) : (
              <Link
                to="/"
                className="flex items-center p-2 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
              >
                <FaRobot className="w-5 h-5" />
                <span className="ml-2 hidden sm:inline">Probar Chatbot</span>
              </Link>
            )
          }
        </div>
      </header>
    </>
  );
};