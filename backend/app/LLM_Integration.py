import requests
import textwrap
import logging

# ----------------------------
# Configuration
# ----------------------------

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3"   

MAX_CHUNK_SIZE = 3000     
REQUEST_TIMEOUT = 120  # Increased for first request/model loading    

logger = logging.getLogger(__name__)


# ----------------------------
# Ollama Client
# ----------------------------

def ollama_chat(prompt: str) -> str:
    """
    Send a prompt to the local Ollama model and return the response text.
    """
    print(f"[DEBUG] Sending request to Ollama at {OLLAMA_URL}")
    print(f"[DEBUG] Prompt length: {len(prompt)} characters")
    
    # First, check if Ollama is reachable
    try:
        health_check = requests.get("http://localhost:11434/api/tags", timeout=5)
        if health_check.status_code != 200:
            raise RuntimeError(f"Ollama health check failed with status {health_check.status_code}")
        print(f"[DEBUG] Ollama is reachable")
    except requests.exceptions.ConnectionError:
        raise RuntimeError(f"Cannot connect to Ollama at http://localhost:11434. Make sure Ollama is running.") from None
    except Exception as e:
        print(f"[WARNING] Health check failed: {e}, proceeding anyway...")
    
    try:
        print(f"[DEBUG] Sending chat request (this may take 30-60s for first request)...")
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that creates clear, structured study notes."
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "stream": False
            },
            timeout=REQUEST_TIMEOUT
        )
        print(f"[DEBUG] Ollama response status: {response.status_code}")
    except requests.exceptions.Timeout:
        print(f"[ERROR] Ollama request timed out after {REQUEST_TIMEOUT} seconds")
        raise RuntimeError(f"Ollama request timed out after {REQUEST_TIMEOUT} seconds. The model may be loading or Ollama may be stuck. Try restarting Ollama.") from None
    except requests.exceptions.ConnectionError as exc:
        print(f"[ERROR] Cannot connect to Ollama: {exc}")
        raise RuntimeError(f"Cannot connect to Ollama at {OLLAMA_URL}. Is Ollama running?") from exc
    except requests.RequestException as exc:
        print(f"[ERROR] Ollama request failed: {exc}")
        raise RuntimeError(f"Ollama request failed: {exc}") from exc

    if response.status_code != 200:
        print(f"[ERROR] Ollama returned status {response.status_code}: {response.text}")
        raise RuntimeError(f"Ollama request failed: {response.text}")

    result = response.json()["message"]["content"].strip()
    print(f"[DEBUG] Ollama response received, length: {len(result)} characters")
    return result


# ----------------------------
# Text Chunking
# ----------------------------

def chunk_text(text: str, max_chunk_size: int = MAX_CHUNK_SIZE) -> list[str]:
    """
    Split large text into smaller chunks for LLM processing.
    """
    clean_text = text.replace("\n", " ")
    return textwrap.wrap(clean_text, max_chunk_size)


# ----------------------------
# Summarization Logic
# ----------------------------

def summarize_chunk(chunk: str) -> str:
    """
    Summarize a single text chunk.
    """
    prompt = f"""
    Summarize the following text clearly and concisely.
    Focus on key insights, main arguments, and core ideas.

    Text:
    {chunk}
    """

    return ollama_chat(prompt)



def generate_notes(full_text: str) -> str:
    """
    Generate structured notes from a full document using
    map-reduce summarization.
    """
    print(f"[DEBUG] generate_notes called with text length: {len(full_text)}")
    
    # For very short texts, skip map-reduce and go straight to notes generation
    if len(full_text.strip()) < 500:
        print(f"[DEBUG] Text is short ({len(full_text)} chars), skipping chunking")
        prompt = f"""
        Create well-structured study notes from the following text.

        Requirements:
        - Start with a short overview paragraph
        - Then provide 3-5 concise bullet-point notes
        - Use clear, student-friendly language

        Text:
        {full_text}
        """
        print(f"[DEBUG] Sending direct prompt to Ollama (length: {len(prompt)})")
        result = ollama_chat(prompt)
        print(f"[DEBUG] Notes generated, length: {len(result)}")
        return result
    
    chunks = chunk_text(full_text)
    print(f"[DEBUG] Text split into {len(chunks)} chunks")

    if not chunks:
        raise ValueError("No text available for summarization.")

    summaries = []

    for i, chunk in enumerate(chunks):
        print(f"[DEBUG] Processing chunk {i + 1} / {len(chunks)} (length: {len(chunk)})")
        logger.info(f"Summarizing chunk {i + 1} / {len(chunks)}")
        summary = summarize_chunk(chunk)
        print(f"[DEBUG] Chunk {i + 1} summarized, length: {len(summary)}")
        summaries.append(summary)

    combined_summary = " ".join(summaries)
    print(f"[DEBUG] Combined summary length: {len(combined_summary)}")

    final_prompt = f"""
    Combine the following summaries into well-structured study notes.

    Requirements:
    - Start with a short overview paragraph
    - Then provide 5–8 concise bullet-point notes
    - Use clear, student-friendly language

    Summaries:
    {combined_summary}
    """
    
    print(f"[DEBUG] Sending final prompt to Ollama (length: {len(final_prompt)})")
    result = ollama_chat(final_prompt)
    print(f"[DEBUG] Final notes generated, length: {len(result)}")
    return result
