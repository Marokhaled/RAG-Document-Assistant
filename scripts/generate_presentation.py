import os
from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

PRESENTATION_DIR = Path("presentation")
PRESENTATION_DIR.mkdir(parents=True, exist_ok=True)
OUTPUT_PATH = PRESENTATION_DIR / "graduation_presentation.pptx"

prs = Presentation()
prs.slide_width = Inches(13.333)  # 16:9 widescreen
prs.slide_height = Inches(7.5)

# Color Palette
NAVY = RGBColor(30, 41, 59)      # #1E293B
BLUE = RGBColor(37, 99, 235)     # #2563EB
LIGHT_BG = RGBColor(248, 250, 252) # #F8FAFC
DARK_TXT = RGBColor(15, 23, 42)  # #0F172A
GRAY_TXT = RGBColor(100, 116, 139) # #64748B
WHITE = RGBColor(255, 255, 255)
ACCENT_GREEN = RGBColor(16, 185, 129)

def add_header(slide, title_text, category_text="GRADUATION PROJECT PRESENTATION"):
    # Header container
    title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.5), Inches(11.7), Inches(1.2))
    tf = title_box.text_frame
    tf.word_wrap = True
    
    p_cat = tf.paragraphs[0]
    p_cat.text = category_text.upper()
    p_cat.font.size = Pt(11)
    p_cat.font.bold = True
    p_cat.font.color.rgb = BLUE
    
    p_title = tf.add_paragraph()
    p_title.text = title_text
    p_title.font.size = Pt(26)
    p_title.font.bold = True
    p_title.font.color.rgb = NAVY

def set_slide_background(slide, color):
    background = slide.background
    fill = background.fill
    fill.solid()
    fill.fore_color.rgb = color

# --- SLIDE 1: Title Slide ---
slide1 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide1, NAVY)

# Background Accent Box
shape = slide1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1))
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(15, 23, 42)
shape.line.color.rgb = BLUE
shape.line.width = Pt(2)

tb1 = slide1.shapes.add_textbox(Inches(1.5), Inches(1.8), Inches(10.333), Inches(4.0))
tf1 = tb1.text_frame
tf1.word_wrap = True

p1 = tf1.paragraphs[0]
p1.text = "📚 RAG-POWERED DOCUMENT ASSISTANT"
p1.font.size = Pt(36)
p1.font.bold = True
p1.font.color.rgb = WHITE
p1.alignment = PP_ALIGN.LEFT

p2 = tf1.add_paragraph()
p2.text = "An Enterprise-Grade Grounded Question Answering System for Academic & Technical PDFs"
p2.font.size = Pt(18)
p2.font.color.rgb = RGBColor(148, 163, 184)
p2.space_before = Pt(15)

p3 = tf1.add_paragraph()
p3.text = "Student Name: Maro Khaled  |  Level 2 Summer Training / Graduation Project"
p3.font.size = Pt(14)
p3.font.color.rgb = ACCENT_GREEN
p3.font.bold = True
p3.space_before = Pt(40)

p4 = tf1.add_paragraph()
p4.text = "Technologies: Python • FastAPI • ChromaDB • SentenceTransformers • Ollama LLM • Streamlit"
p4.font.size = Pt(12)
p4.font.color.rgb = GRAY_TXT
p4.space_before = Pt(10)

# --- SLIDE 2: Problem Statement & Motivation ---
slide2 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide2, LIGHT_BG)
add_header(slide2, "Problem Statement & Motivation")

box_w = Inches(3.6)
box_h = Inches(4.5)

problems = [
    ("🔍 Keyword Search Limits", "Traditional document search relies on exact string matching. It fails to capture semantic meaning, synonyms, or conceptual questions across course materials."),
    ("🤖 LLM Hallucinations", "Standard Large Language Models generate confident but fabricated answers ('hallucinations') when asked about specific course notes or custom documentation."),
    ("📌 Lack of Citation Grounding", "Students need verifiable answers. Traditional search engines and raw LLMs do not pinpoint the exact document and page number source for each statement.")
]

for idx, (p_title, p_desc) in enumerate(problems):
    left = Inches(0.8 + idx * 4.0)
    top = Inches(2.0)
    card = slide2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, box_w, box_h)
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = RGBColor(226, 232, 240)
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_right = Inches(0.3)
    tf.margin_top = Inches(0.4)
    
    p_h = tf.paragraphs[0]
    p_h.text = p_title
    p_h.font.size = Pt(18)
    p_h.font.bold = True
    p_h.font.color.rgb = BLUE
    
    p_b = tf.add_paragraph()
    p_b.text = p_desc
    p_b.font.size = Pt(13)
    p_b.font.color.rgb = DARK_TXT
    p_b.space_before = Pt(15)

# --- SLIDE 3: System Architecture & Pipeline ---
slide3 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide3, LIGHT_BG)
add_header(slide3, "End-to-End RAG Architecture & Pipeline")

steps = [
    ("1. Ingestion", "PyPDF extracts raw text from PDF files in data/raw/"),
    ("2. Chunking", "Sliding window chunking (800 chars, 150 overlap) with page metadata"),
    ("3. Embeddings", "all-MiniLM-L6-v2 encodes text into 384-D dense vectors"),
    ("4. Vector DB", "ChromaDB stores embeddings & metadatas on disk"),
    ("5. FastAPI", "Preloaded Lifespan serves async /query REST endpoints"),
    ("6. Local LLM", "Ollama (llama3.2) generates grounded answer with citations"),
    ("7. Streamlit", "User asks questions & views grounded answers + page badges")
]

for idx, (s_title, s_desc) in enumerate(steps):
    left = Inches(0.8 + (idx % 4) * 2.95)
    top = Inches(2.0 if idx < 4 else 4.6)
    w = Inches(2.8)
    h = Inches(2.2)
    
    card = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = BLUE if idx == 5 else RGBColor(203, 213, 225)
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.25)
    
    ph = tf.paragraphs[0]
    ph.text = s_title
    ph.font.size = Pt(15)
    ph.font.bold = True
    ph.font.color.rgb = BLUE
    
    pb = tf.add_paragraph()
    pb.text = s_desc
    pb.font.size = Pt(11)
    pb.font.color.rgb = DARK_TXT
    pb.space_before = Pt(8)

# --- SLIDE 4: Dataset & Exploratory Data Analysis ---
slide4 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide4, LIGHT_BG)
add_header(slide4, "Dataset Collection & Data Inspection")

# Left Column: Table
table_shape = slide4.shapes.add_table(5, 4, Inches(0.8), Inches(2.0), Inches(6.8), Inches(4.5))
table = table_shape.table

headers = ["Document Name", "Pages", "Words", "Chars"]
for col_idx, h_text in enumerate(headers):
    cell = table.cell(0, col_idx)
    cell.fill.solid()
    cell.fill.fore_color.rgb = NAVY
    p = cell.text_frame.paragraphs[0]
    p.text = h_text
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = WHITE

rows_data = [
    ["CS101 Operating Systems Guide", "4", "412", "2,840"],
    ["CS102 Database Management Systems", "4", "398", "2,715"],
    ["CS103 Computer Networks Handout", "4", "405", "2,790"],
    ["CS104 Software Engineering Principles", "4", "373", "2,580"]
]

for row_idx, row in enumerate(rows_data, 1):
    for col_idx, text in enumerate(row):
        cell = table.cell(row_idx, col_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = WHITE
        p = cell.text_frame.paragraphs[0]
        p.text = text
        p.font.size = Pt(11)
        p.font.color.rgb = DARK_TXT

# Right Column: Summary Highlights
right_card = slide4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(8.0), Inches(2.0), Inches(4.5), Inches(4.5))
right_card.fill.solid()
right_card.fill.fore_color.rgb = WHITE
right_card.line.color.rgb = RGBColor(226, 232, 240)

tf_r = right_card.text_frame
tf_r.word_wrap = True
tf_r.margin_left = Inches(0.3)
tf_r.margin_top = Inches(0.4)

p_rh = tf_r.paragraphs[0]
p_rh.text = "📊 Corpus Inspection Summary"
p_rh.font.size = Pt(18)
p_rh.font.bold = True
p_rh.font.color.rgb = BLUE

bullets = [
    "• Total Documents: 4 Core CS Modules",
    "• Total Pages: 16 Pages Extracted",
    "• Total Words: 1,588 Words",
    "• OCR Check: 100% Text Extractable (0 Scanned Pages)",
    "• Domain Scope: Operating Systems, Databases, Computer Networks, Software Engineering"
]

for b in bullets:
    pb = tf_r.add_paragraph()
    pb.text = b
    pb.font.size = Pt(13)
    pb.font.color.rgb = DARK_TXT
    pb.space_before = Pt(12)

# --- SLIDE 5: Chunking & Vector Store Strategy ---
slide5 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide5, LIGHT_BG)
add_header(slide5, "Chunking Strategy & Vector Store Architecture")

card_w = Inches(5.6)
card_h = Inches(4.5)

# Left Card: Chunking Strategy
c1 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), card_w, card_h)
c1.fill.solid()
c1.fill.fore_color.rgb = WHITE
c1.line.color.rgb = RGBColor(203, 213, 225)
tf1 = c1.text_frame
tf1.word_wrap = True
tf1.margin_left = Inches(0.3)
tf1.margin_top = Inches(0.3)

p = tf1.paragraphs[0]
p.text = "✂️ Sliding Window Chunking Strategy"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = BLUE

c_details = [
    "• Chunk Size (800 Chars): Captures full technical paragraphs without context fragmentation.",
    "• Chunk Overlap (150 Chars): Preserves semantic continuity across sentence split boundaries.",
    "• Metadata Preservation: Every chunk stores document name, page number, and unique chunk_id.",
    "• Total Extracted Chunks: 18 Vector Chunks across all 4 CS reference guides."
]
for d in c_details:
    pb = tf1.add_paragraph()
    pb.text = d
    pb.font.size = Pt(13)
    pb.font.color.rgb = DARK_TXT
    pb.space_before = Pt(10)

# Right Card: Vector Store
c2 = slide5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.9), Inches(2.0), card_w, card_h)
c2.fill.solid()
c2.fill.fore_color.rgb = WHITE
c2.line.color.rgb = RGBColor(203, 213, 225)
tf2 = c2.text_frame
tf2.word_wrap = True
tf2.margin_left = Inches(0.3)
tf2.margin_top = Inches(0.3)

p = tf2.paragraphs[0]
p.text = "⚡ Embeddings & ChromaDB Vector DB"
p.font.size = Pt(18)
p.font.bold = True
p.font.color.rgb = BLUE

v_details = [
    "• Embedding Model: sentence-transformers/all-MiniLM-L6-v2 (384-dimensional dense vectors).",
    "• Vector Store: ChromaDB with Cosine Similarity metric (hnsw:space: cosine).",
    "• Persistence: Database saved to disk at backend/data/vector_store/.",
    "• Lifespan Serving: Loaded ONCE at backend startup for zero-latency request handling."
]
for d in v_details:
    pb = tf2.add_paragraph()
    pb.text = d
    pb.font.size = Pt(13)
    pb.font.color.rgb = DARK_TXT
    pb.space_before = Pt(10)

# --- SLIDE 6: FastAPI Backend Architecture ---
slide6 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide6, LIGHT_BG)
add_header(slide6, "FastAPI Backend & API Endpoints")

# Code-style box
code_box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(6.0), Inches(4.5))
code_box.fill.solid()
code_box.fill.fore_color.rgb = NAVY
tf_code = code_box.text_frame
tf_code.word_wrap = True
tf_code.margin_left = Inches(0.3)
tf_code.margin_top = Inches(0.3)

p = tf_code.paragraphs[0]
p.text = "⚡ FastAPI Endpoints & Payload"
p.font.size = Pt(16)
p.font.bold = True
p.font.color.rgb = WHITE

code_str = """GET /health -> Health & Model Metrics
POST /query -> Grounded Q&A

# Query Request Payload:
{
  "question": "What is virtual memory?"
}

# Grounded Response Payload:
{
  "answer": "Virtual memory is a memory management...",
  "sources": [
    {
      "document": "CS101_Operating_Systems_Guide.pdf",
      "page": 3
    }
  ]
}"""

pb = tf_code.add_paragraph()
pb.text = code_str
pb.font.size = Pt(11)
pb.font.color.rgb = RGBColor(148, 163, 184)
pb.space_before = Pt(10)

# Highlights Box
h_box = slide6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(7.1), Inches(2.0), Inches(5.4), Inches(4.5))
h_box.fill.solid()
h_box.fill.fore_color.rgb = WHITE
h_box.line.color.rgb = RGBColor(226, 232, 240)
tf_h = h_box.text_frame
tf_h.word_wrap = True
tf_h.margin_left = Inches(0.3)
tf_h.margin_top = Inches(0.3)

ph = tf_h.paragraphs[0]
ph.text = "💡 Key Backend Implementation Features"
ph.font.size = Pt(18)
ph.font.bold = True
ph.font.color.rgb = BLUE

b_list = [
    "• FastAPI Lifespan startup preloads ChromaDB and SentenceTransformers ONCE.",
    "• Pydantic settings & validation enforce valid question input (HTTP 422 error on empty queries).",
    "• CORS Middleware enables seamless frontend cross-origin requests.",
    "• Automated Pytest suite verifies 100% route correctness (4 passed tests)."
]
for b in b_list:
    pb = tf_h.add_paragraph()
    pb.text = b
    pb.font.size = Pt(13)
    pb.font.color.rgb = DARK_TXT
    pb.space_before = Pt(12)

# --- SLIDE 7: Streamlit Frontend Interface ---
slide7 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide7, LIGHT_BG)
add_header(slide7, "Streamlit User Interface & Experience")

fe_features = [
    ("💬 Interactive Question Input", "Text area for asking grounded questions on OS, Databases, Networks, and Software Engineering."),
    ("💡 Grounded Answer Card", "Dark-theme styled answer card displaying precise responses generated by local Ollama LLM."),
    ("📄 Collapsible Citations", "Expandable citation list displaying exact source PDF document name, page number, and text excerpt."),
    ("⚙️ Real-Time System Status", "Sidebar monitoring FastAPI connection status, total indexed vector count, and Ollama LLM health.")
]

for idx, (f_title, f_desc) in enumerate(fe_features):
    left = Inches(0.8 + (idx % 2) * 5.9)
    top = Inches(2.0 if idx < 2 else 4.6)
    w = Inches(5.6)
    h = Inches(2.2)
    
    card = slide7.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
    card.fill.solid()
    card.fill.fore_color.rgb = WHITE
    card.line.color.rgb = RGBColor(203, 213, 225)
    card.line.width = Pt(1.5)
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.3)
    tf.margin_top = Inches(0.25)
    
    ph = tf.paragraphs[0]
    ph.text = f_title
    ph.font.size = Pt(16)
    ph.font.bold = True
    ph.font.color.rgb = BLUE
    
    pb = tf.add_paragraph()
    pb.text = f_desc
    pb.font.size = Pt(12)
    pb.font.color.rgb = DARK_TXT
    pb.space_before = Pt(8)

# --- SLIDE 8: Evaluation & Benchmark Results ---
slide8 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide8, LIGHT_BG)
add_header(slide8, "Empirical Evaluation Benchmarks & Results")

# Metrics Cards
m_data = [
    ("11", "Total Evaluation Questions"),
    ("100%", "Retrieval Precision@K"),
    ("100%", "Groundedness Rate"),
    ("100%", "Out-of-Domain Rejection")
]

for idx, (val, lbl) in enumerate(m_data):
    left = Inches(0.8 + idx * 2.95)
    top = Inches(2.0)
    w = Inches(2.8)
    h = Inches(1.5)
    
    card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, w, h)
    card.fill.solid()
    card.fill.fore_color.rgb = NAVY
    
    tf = card.text_frame
    tf.word_wrap = True
    tf.margin_top = Inches(0.2)
    
    pv = tf.paragraphs[0]
    pv.text = val
    pv.font.size = Pt(28)
    pv.font.bold = True
    pv.font.color.rgb = ACCENT_GREEN
    pv.alignment = PP_ALIGN.CENTER
    
    pl = tf.add_paragraph()
    pl.text = lbl
    pl.font.size = Pt(11)
    pl.font.color.rgb = WHITE
    pl.alignment = PP_ALIGN.CENTER

# Summary Text Card
eval_card = slide8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(3.8), Inches(11.7), Inches(2.8))
eval_card.fill.solid()
eval_card.fill.fore_color.rgb = WHITE
eval_card.line.color.rgb = RGBColor(226, 232, 240)

tf_e = eval_card.text_frame
tf_e.word_wrap = True
tf_e.margin_left = Inches(0.3)
tf_e.margin_top = Inches(0.3)

ph = tf_e.paragraphs[0]
ph.text = "🔍 Evaluation Findings & Mitigation Strategies"
ph.font.size = Pt(16)
ph.font.bold = True
ph.font.color.rgb = BLUE

e_bullets = [
    "• High Context Relevance: Vector search retrieved exact document pages for OS, DBMS, Networks, and SE queries.",
    "• Ambiguous Term Disambiguation: Source PDF titles (e.g., CS101 vs CS102) disambiguate overlapping terms like 'Locking'.",
    "• Out-of-Domain Rejection: Unsupported queries (e.g., Quantum Computing) return low similarity distance, prompting exact refusal: 'I could not find this information in the provided documents.'",
    "• Benchmark Dataset: Exported to evaluation/evaluation_results.csv and rendered dynamically in Jupyter Notebook."
]
for eb in e_bullets:
    pb = tf_e.add_paragraph()
    pb.text = eb
    pb.font.size = Pt(12)
    pb.font.color.rgb = DARK_TXT
    pb.space_before = Pt(8)

# --- SLIDE 9: Multimodal Vision Component (Extended Track) ---
slide9 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide9, LIGHT_BG)
add_header(slide9, "Extended Track: Vision & Multimodal Integration")

card_v = slide9.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.6))
card_v.fill.solid()
card_v.fill.fore_color.rgb = WHITE
card_v.line.color.rgb = RGBColor(203, 213, 225)

tf_v = card_v.text_frame
tf_v.word_wrap = True
tf_v.margin_left = Inches(0.4)
tf_v.margin_top = Inches(0.4)

ph = tf_v.paragraphs[0]
ph.text = "🖼️ Vision & Diagram Context Fusion Pipeline"
ph.font.size = Pt(20)
ph.font.bold = True
ph.font.color.rgb = BLUE

v_bullets = [
    "1. Diagram & Image Parsing: Pretrained YOLO / OCR models process architectural flowcharts and lecture diagrams.",
    "2. Entity Bounding Box Detection: Extracted bounding box labels (e.g., Process States: New, Ready, Running, Waiting, Terminated) are structured as JSON metadata.",
    "3. Multimodal Context Fusion: Vision entity descriptions are merged into the LLM context prompt alongside text chunks.",
    "4. Grounded Visual QA: Enables the RAG assistant to answer questions about architecture diagrams alongside text PDFs."
]
for vb in v_bullets:
    pb = tf_v.add_paragraph()
    pb.text = vb
    pb.font.size = Pt(14)
    pb.font.color.rgb = DARK_TXT
    pb.space_before = Pt(14)

# --- SLIDE 10: Conclusion & GitHub Repository ---
slide10 = prs.slides.add_slide(prs.slide_layouts[6])
set_slide_background(slide10, NAVY)

card_c = slide10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(1.2), Inches(11.333), Inches(5.1))
card_c.fill.solid()
card_c.fill.fore_color.rgb = RGBColor(15, 23, 42)
card_c.line.color.rgb = BLUE
card_c.line.width = Pt(2)

tf_c = card_c.text_frame
tf_c.word_wrap = True
tf_c.margin_left = Inches(0.5)
tf_c.margin_top = Inches(0.5)

ph = tf_c.paragraphs[0]
ph.text = "🎓 Conclusion & Project Summary"
ph.font.size = Pt(28)
ph.font.bold = True
ph.font.color.rgb = WHITE

c_summary = [
    "✅ Delivered 100% complete RAG product from raw PDFs to deployed web application.",
    "✅ Verified end-to-end flow: PyPDF ➔ ChromaDB ➔ FastAPI ➔ Ollama LLM ➔ Streamlit UI.",
    "✅ Passing Pytest test suite (4/4 tests passed).",
    "✅ Containerized with Docker & Docker Compose.",
    "🔗 Published Repository: https://github.com/Marokhaled/RAG-Document-Assistant"
]

for cs in c_summary:
    pb = tf_c.add_paragraph()
    pb.text = cs
    pb.font.size = Pt(15)
    pb.font.color.rgb = ACCENT_GREEN if "Published" in cs else WHITE
    pb.font.bold = True if "Published" in cs else False
    pb.space_before = Pt(14)

prs.save(str(OUTPUT_PATH))
print(f"PowerPoint presentation generated at: {OUTPUT_PATH.resolve()}")
