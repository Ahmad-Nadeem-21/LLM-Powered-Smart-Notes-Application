import React, { useState } from "react";
import { uploadFile, generateNotes, getFileUrl } from "./api.js";

function App() {
  const [file, setFile] = useState(null);
  const [backendFile, setBackendFile] = useState(null);
  const [notes, setNotes] = useState("");
  const [cached, setCached] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files?.[0] ?? null);
    setNotes("");
    setCached(false);
    setError("");
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please choose a file first.");
      return;
    }
    setError("");
    setIsUploading(true);
    setNotes("");
    setCached(false);

    try {
      const res = await uploadFile(file);
      setBackendFile({ fileId: res.file_id, filename: res.filename });
    } catch (err) {
      setError(err.message);
    } finally {
      setIsUploading(false);
    }
  };

  const handleGenerateNotes = async () => {
    if (!backendFile?.fileId) {
      setError("Upload a file first.");
      return;
    }
    setError("");
    setIsGenerating(true);

    try {
      const res = await generateNotes(backendFile.fileId);
      setNotes(res.notes);
      setCached(!!res.cached);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsGenerating(false);
    }
  };

  return (
    <div className="app-root">
      <div className="app-shell">
        <header className="app-header">
          <div>
            <h1>Smart Notes</h1>
            <p className="subtitle">
              Upload a PDF, DOCX, or TXT file and turn it into clean study notes.
            </p>
          </div>
        </header>

        <main className="app-main">
          <section className="panel left">
            <h2>1. Upload your file</h2>
            <p className="helper-text">
              Supported formats: <strong>PDF</strong>, <strong>DOCX</strong>, <strong>TXT</strong>.
            </p>
            <label className="file-input-label">
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleFileChange}
              />
              <span className="file-input-visual">
                <span className="file-icon">📄</span>
                <span>
                  {file ? (
                    <>
                      <span className="file-name">{file.name}</span>
                      <span className="file-size">
                        {(file.size / 1024 / 1024).toFixed(2)} MB
                      </span>
                    </>
                  ) : (
                    <>
                      <span className="file-name">Choose a file</span>
                      <span className="file-size">or drag & drop here</span>
                    </>
                  )}
                </span>
              </span>
            </label>

            <button
              className="primary-btn"
              onClick={handleUpload}
              disabled={isUploading || !file}
            >
              {isUploading ? "Uploading..." : "Upload to server"}
            </button>

            {backendFile && (
              <div className="upload-summary card">
                <h3>Uploaded file</h3>
                <p className="file-title">{backendFile.filename}</p>
                <p className="file-id">ID: {backendFile.fileId}</p>
                <a
                  href={getFileUrl(backendFile.fileId)}
                  target="_blank"
                  rel="noreferrer"
                  className="ghost-link"
                >
                  View raw file
                </a>
              </div>
            )}
          </section>

          <section className="panel right">
            <h2>2. Generate notes</h2>
            <p className="helper-text">
              We&apos;ll send your text to your local LLM (Ollama) and build structured notes.
            </p>

            <button
              className="secondary-btn"
              onClick={handleGenerateNotes}
              disabled={isGenerating || !backendFile}
            >
              {isGenerating ? "Generating..." : "Generate notes"}
            </button>

            {error && <div className="error-banner">{error}</div>}

            {notes && (
              <div className="notes-card">
                <div className="notes-header">
                  <h3>Study notes</h3>
                  {cached && (
                    <span className="badge badge-soft">From cache</span>
                  )}
                </div>
                <pre className="notes-content">{notes}</pre>
              </div>
            )}

            {!notes && !error && backendFile && !isGenerating && (
              <p className="empty-state">
                Click <strong>Generate notes</strong> to create notes for this file.
              </p>
            )}
          </section>
        </main>

        <footer className="app-footer">
          <span>Backend:</span>
          <code>FastAPI @ http://localhost:8000</code>
        </footer>
      </div>
    </div>
  );
}

export default App;


