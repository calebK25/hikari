import React, { useState } from "react";
function App() {
  const [q, setQ] = useState("");
  const [ans, setAns] = useState("");
  const ask = () =>
    fetch("/query", { method: "POST", body: JSON.stringify({ q }), headers: { "Content-Type": "application/json" } })
      .then(r => r.json())
      .then(r => setAns(r.answer));
  return (
    <div className="p-4">
      <input value={q} onChange={e => setQ(e.target.value)} className="border p-2" />
      <button onClick={ask} className="ml-2 bg-blue-500 text-white px-4 py-2">Ask</button>
      <p className="mt-4">{ans}</p>
    </div>
  );
}
export default App;