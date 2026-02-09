import { useState } from "react";

function App() {
  const [gene, setGene] = useState("");
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [requestId, setRequestId] = useState(null);

  const searchVariants = async () => {
    if (!gene) {
      setError("Please enter a gene name");
      return;
    }

    setLoading(true);
    setError(null);
    setResults([]);
    setRequestId(null);

    try {
      const response = await fetch(
        `http://localhost:8000/variants?gene=${gene}`
      );

      if (!response.ok) {
        throw new Error("API request failed");
      }

      const data = await response.json();
      setResults(data.results || []);
      setRequestId(data.request_id || null);
    } catch (err) {
      setError("Failed to fetch variants");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>Mutation Browser</h1>

      <div style={{ marginBottom: "1rem" }}>
        <input
          type="text"
          value={gene}
          placeholder="Enter gene (e.g. TP53)"
          onChange={(e) => setGene(e.target.value)}
          style={{ padding: "0.5rem", marginRight: "0.5rem" }}
        />
        <button onClick={searchVariants}>Search</button>
      </div>

      {loading && <p>Loading…</p>}
      {error && <p style={{ color: "red" }}>{error}</p>}
      {requestId && (
        <p style={{ fontSize: "0.9rem", color: "#555" }}>
          Request ID: {requestId}
        </p>
      )}

      {results.length > 0 && (
  <>
    <p>
      <strong>{results.length}</strong> samples found
    </p>

    <table border="1" cellPadding="5">
      <thead>
        <tr>
          <th>Sample ID</th>
          <th>Gene</th>
          <th>Variant</th>
          <th>VAF</th>
          <th>Tumor Type</th>
        </tr>
      </thead>
      <tbody>
        {results.map((row, idx) => (
          <tr key={idx}>
            <td>{row.sample_id}</td>
            <td>{row.gene}</td>
            <td>{row.variant}</td>
            <td>{row.vaf}</td>
            <td>{row.tumor_type}</td>
          </tr>
        ))}
      </tbody>
    </table>
  </>
)}

      {results.length === 0 && !loading && !error && (
        <p>No results to display</p>
      )}
    </div>
  );
}

export default App;
