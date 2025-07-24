import gradio as gr
from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch

# Load model and tokenizer
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

# Caption generation function
def generate_caption(prompt):
    full_prompt = f"Write a short creative social media caption with hiking vibes, emojis, and relevant hashtags for: \"{prompt}\""
    inputs = tokenizer(full_prompt, return_tensors="pt")
    output = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=True,
        temperature=0.9,
        top_p=0.95
    )
    result = tokenizer.decode(output[0], skip_special_tokens=True)
    caption = result.replace(full_prompt, "").strip()
    return caption if caption else "Couldn't generate a creative caption. Try again!"

# Gradio Interface
with gr.Blocks(css="""
    .output-bubble {
        background-color: #f3f4f6;
        padding: 10px;
        border-radius: 12px;
        font-size: 16px;
        margin-top: 10px;
        line-height: 1.5;
        white-space: pre-wrap;
    }
    .copy-button {
        margin-top: 6px;
        font-size: 14px;
        color: #2563eb;
        cursor: pointer;
        background: none;
        border: none;
        padding: 0;
    }
""") as app:

    gr.Markdown("""
    # 🏞️ Caption Genie – Nature & Hiking Vibes Generator  
    Type a scene description and get a ready-to-post creative caption with emojis & hashtags!
    """)

    with gr.Row():
        user_input = gr.Textbox(placeholder="e.g. A peaceful sunset over the mountains...", label="Enter a short description")

    output_text = gr.Markdown(label="Generated Caption")

    def update_output(prompt):
        caption = generate_caption(prompt)
        return f"<div class='output-bubble'>{caption}</div><button class='copy-button' onclick='navigator.clipboard.writeText(`{caption}`)'>📋 Copy Caption</button>"

    generate_btn = gr.Button("✨ Generate Caption")
    generate_btn.click(fn=update_output, inputs=user_input, outputs=output_text)

# Run the app
if __name__ == "__main__":
    app.launch()
