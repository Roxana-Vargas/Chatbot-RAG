

export function Skeleton({ width = "100%", height = "20px", className = "" }) {
  return (
    <div
      className={`bg-gray-300 dark:bg-gray-600 animate-pulse rounded ${className}`}
      style={{ width, height }}
    ></div>
  );
}