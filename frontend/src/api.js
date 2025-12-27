const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function uploadFile(file) {
  const formData = new FormData();
  formData.append("file", file);

  const res = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || "Failed to upload file");
  }

  return res.json();
}

export async function generateNotes(fileId) {
  const res = await fetch(`${API_BASE_URL}/notes/${encodeURIComponent(fileId)}`, {
    method: "POST"
  });

  if (!res.ok) {
    const data = await res.json().catch(() => ({}));
    throw new Error(data.detail || "Failed to generate notes");
  }

  return res.json();
}

export function getFileUrl(fileId) {
  return `${API_BASE_URL}/file/${encodeURIComponent(fileId)}`;
}


