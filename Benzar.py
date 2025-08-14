import base64
import gradio as gr
import requests
from google.colab import userdata

# Load Groq API key exactly as in your original code
GROQ_API_KEY = userdata.get('Groq_AJ')
if not GROQ_API_KEY:
    raise RuntimeError("❌ Please add your 'Groq_AJ' key to Colab Secrets!")

def review_pr(code_text):
    if not code_text.strip():
        return "❌ Please enter some code to review!"

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are Benzar, a helpful assistant that reviews code, make suggestions and gives correct code.Also provides the code when asked for code."},
            {"role": "user", "content": f"Please review this code:\n{code_text}"}
        ],
        "max_tokens": 500
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        return f"API Error: {response.status_code} - {response.text}"

    return response.json()["choices"][0]["message"]["content"]

# Load and encode your mascot image to base64
with open("/content/Benzar.png", "rb") as img_file:
    img_b64 = base64.b64encode(img_file.read()).decode()

img_md = f'<img src="data:image/png;base64,{img_b64}" width="200" style="display: block; margin-left: auto; margin-right: auto;" />'

with gr.Blocks() as demo:
    # Inject CSS for glowing blue buttons
    gr.Markdown("""
    <style>
    .glow-button {
        background: #0d6efd;
        color: white;
        border: none;
        padding: 10px 25px;
        font-size: 16px;
        border-radius: 8px;
        cursor: pointer;
        box-shadow: 0 0 8px #0d6efd;
        transition: box-shadow 0.3s ease-in-out;
    }
    .glow-button:hover {
        box-shadow: 0 0 15px 5px #0d6efd;
    }
    </style>
    """)

    # Centered mascot image
    gr.Markdown(img_md)

    # Centered title only
    gr.Markdown("""
    <h2 style="text-align: center; margin-bottom: 5px;">🤖 📝 Benzar - Your AI Code Review Assistant 😸</h2>
    <p>Paste your code and get insightful, detailed reviews from Benzar.</p>
    """)

    with gr.Row():
        code_input = gr.Textbox(lines=20, placeholder="Paste your code here...", label="code_text")
        output = gr.Textbox(label="Review response")

    with gr.Row():
        review_btn = gr.Button("Review Code", elem_classes="glow-button")
        clear_btn = gr.Button("Clear", elem_classes="glow-button")

    review_btn.click(fn=review_pr, inputs=code_input, outputs=output)

    # Clear button resets both inputs
    def clear_all():
        return "", ""

    clear_btn.click(fn=clear_all, inputs=[], outputs=[code_input, output])

demo.launch()
