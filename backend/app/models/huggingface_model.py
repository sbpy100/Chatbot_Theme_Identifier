
import os
import requests

def summarize_themes(chunks, question):
    hf_token = os.getenv("HUGGINGFACE_API_KEY")
    if not hf_token:
        return "Error: Missing Hugging Face token."

    #Use top 3 chunks, fallback to top 5 if top ones are empty
    top_chunks = [c.strip() for c in chunks[:3] if c.strip()]
    context = "\n".join(top_chunks)

    if not context:
        all_chunks = [c.strip() for c in chunks if c.strip()]
        context = "\n".join(all_chunks[:5])

    if not context:
        return "Error: Could not extract meaningful content from documents."

    #Prompt for a more detailed structured summary
    prompt = (
        f"{context}\n\n"
        f"Based on the document content above, identify and summarize the two most important legal or regulatory themes. "
        f"For each theme, include:\n"
        f"– A concise theme title\n"
        f"– Associated document IDs\n"
        f"– 2 to 3 sentences explaining each theme clearly\n\n"
        f"Your response should be approximately 8 to 10 lines total, grouped as:\n\n"
        f"Theme 1 – <Theme Title>: <DOC IDs> – <Explanation>\n"
        f"Theme 2 – <Theme Title>: <DOC IDs> – <Explanation>"
    )

    url = "https://api-inference.huggingface.co/models/HuggingFaceH4/zephyr-7b-beta"
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json={"inputs": prompt})

    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    try:
        output = response.json()
        summary = output[0].get("generated_text", "").strip()
        return "\n".join(summary.splitlines()[:20])
    except Exception as e:
        return "Error: Failed to parse model output."
