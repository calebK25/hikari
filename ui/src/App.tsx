import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import axios from "axios";

function App() {
  const [q, setQ] = useState("");
  const [result, setResult] = useState<any>(null);
  const [job, setJob] = useState<string | null>(null);

  const { getRootProps, getInputProps } = useDropzone({
    accept: { "application/pdf": [] },
    maxFiles: 1,
    onDrop: async ([file]) => {
      const form = new FormData();
      form.append("file", file);
      const { data } = await axios.post("http://localhost:8000/upload", form);
      setJob(data.job_id);
    },
  });

  const ask = async () => {
    const res = await axios.post("http://localhost:8000/query", { q });
    setResult(res.data);
  };

  return (
    <div className="p-4 max-w-xl">
      <h1 className="text-2xl font-bold mb-2">Dark-Docs RAG</h1>

      {/* Upload */}
      <div 
        {...getRootProps({ 
          className: "border-2 border-dashed border-gray-300 rounded-lg p-8 mb-4 cursor-pointer hover:border-gray-400 transition-colors text-center bg-gray-50 hover:bg-gray-100" 
        })}
      >
        <input {...getInputProps()} />
        <div className="space-y-2">
          <svg className="mx-auto h-12 w-12 text-gray-400" stroke="currentColor" fill="none" viewBox="0 0 48 48">
            <path d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <p className="text-lg font-medium text-gray-900">Drop PDF here or click to select</p>
          <p className="text-sm text-gray-500">Supports PDF files only</p>
        </div>
      </div>
      {job && <p className="text-sm text-gray-500">Job id: {job}</p>}

      {/* Query */}
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        className="border p-2 w-full"
        placeholder="Ask a question..."
      />
      <button onClick={ask} className="mt-2 bg-blue-500 text-white px-4 py-2">
        Ask
      </button>

      {result && (
        <div className="mt-4">
          <p className="font-semibold">Answer:</p>
          <p className="mb-2">{result.answer}</p>
          <p className="font-semibold text-sm">Citations:</p>
          <ul className="text-xs list-disc list-inside">
            {result.citations.map((c: string) => <li key={c}>{c}</li>)}
          </ul>
        </div>
      )}
    </div>
  );
}
export default App;