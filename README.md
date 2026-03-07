# 🚀 HTML Quick-Styler

> AI-Powered HTML Page Generator using IBM Granite 3.3 2B Instruct

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/yogi910910-hash
/HTML-Quick-Styler/blob/main/HTML_Quick_Styler.ipynb)

---

## 📌 Project Description

**HTML Quick-Styler** is an intelligent web page generation platform that leverages IBM's Granite 3.3 2B Instruct model to deliver:

- 🎨 AI-powered HTML/CSS generation from plain text descriptions
- 🔍 Automatic section detection (hero, features, about, pricing, etc.)
- 🌈 8 pre-built professional color palettes
- 📱 Responsive, mobile-first design out of the box
- 🖥️ Interactive Gradio UI with Live Preview

---

## 🗂️ Project Structure

```
HTML-Quick-Styler/
├── html_quick_styler.py     # Main application (all classes + Gradio UI)
├── requirements.txt         # Python dependencies
├── HTML_Quick_Styler.ipynb  # Google Colab notebook version
└── README.md
```

---

## ⚙️ Setup & Installation

### Option A: Google Colab (Recommended)

1. Open [Google Colab](https://colab.research.google.com)
2. Upload `HTML_Quick_Styler.ipynb` or copy cells from `html_quick_styler.py`
3. Set Runtime → **GPU** (T4 recommended)
4. Run all cells top to bottom

### Option B: Local

```bash
git clone https://github.com/YOUR_USERNAME/HTML-Quick-Styler.git
cd HTML-Quick-Styler
pip install -r requirements.txt
python html_quick_styler.py
```

---

## 🚀 Quick Start (Colab Cells)

### Cell 1 – Install
```python
!pip install gradio transformers torch accelerate huggingface_hub
```

### Cell 2 – Load Model
```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

MODEL_ID = "ibm-granite/granite-3.3-2b-instruct"
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_ID,
    torch_dtype=torch.float16,
    device_map="auto"
)
print("✅ Model loaded!")
```

### Cell 3 – Run the App
```python
# Copy all classes from html_quick_styler.py, then:
demo = create_interface()
demo.launch(share=True)
```

The terminal will print a public URL like:
```
Running on public URL: https://xxxxxxxx.gradio.live
```

---

## 🎨 Color Styles

| Style    | Vibe               |
|----------|--------------------|
| modern   | Indigo/Purple, dark |
| vibrant  | Coral/Teal, energetic |
| ocean    | Blues, professional |
| forest   | Greens, natural    |
| sunset   | Warm oranges       |
| luxury   | Gold, premium      |
| creative | Purple/Cyan, bold  |
| minimal  | Grayscale, clean   |

---

## 🔑 Architecture

```
User Input (Gradio)
     ↓
HTMLPageBuilder.detect_sections()
     ↓
ColorPaletteGenerator.get_palette()
     ↓
IBM Granite 3.3 2B  →  ai_enhance_content()
     ↓
generate_css() + section builders
     ↓
Complete HTML Page Output
```

---

## 📋 Detected Sections

Describe your page using natural language. The system auto-detects:

| Keyword in description | Section generated |
|------------------------|-------------------|
| hero, welcome, banner  | Hero              |
| feature, service, benefit | Features       |
| about, mission, team   | About             |
| portfolio, gallery     | Portfolio         |
| testimonial, review    | Testimonials      |
| pricing, plan, cost    | Pricing           |
| contact, form, email   | Contact           |
| footer (always added)  | Footer            |

---

## 📦 Dependencies

- `gradio >= 4.0`
- `transformers >= 4.40`
- `torch >= 2.0`
- `accelerate >= 0.26`
- `huggingface_hub >= 0.21`

---

## 🤝 Contributing

Pull requests are welcome! For major changes, open an issue first.

---

## 📄 License

MIT License © 2025
