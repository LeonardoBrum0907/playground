#!/usr/bin/env python3
"""Gera avaliação de Geografia (3º ano) em formato Word (.docx)."""

from pathlib import Path

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

OUTPUT_PATH = Path("/workspace/Avaliacao_Geografia_3ano.docx")
ASSETS_DIR = Path("/workspace/avaliacao_geografia_assets")
GABARITO_PATH = Path("/workspace/Gabarito_Avaliacao_Geografia_3ano.docx")

GREEN = RGBColor(27, 94, 32)
DARK = RGBColor(31, 41, 55)
MUTED = RGBColor(75, 85, 99)

OBJETIVAS = [
    {
        "number": 1,
        "theme": "Lugares de vivência",
        "question": (
            "Observe a imagem abaixo. Qual alternativa descreve melhor um "
            "lugar de vivência?"
        ),
        "image": "bairro",
        "caption": "Bairro residencial em Minas Gerais.",
        "options": [
            "Um local onde vivemos, convivemos e realizamos atividades do dia a dia.",
            "Apenas lugares turísticos visitados nas férias.",
            "Somente a escola, pois é onde aprendemos.",
            "Lugares que existem apenas em mapas e atlas.",
        ],
        "answer": "A",
    },
    {
        "number": 2,
        "theme": "O que é cultura",
        "question": (
            "Cultura é o conjunto de costumes, festas, comidas, músicas e "
            "formas de viver de um grupo de pessoas. Qual item NÃO representa "
            "um elemento cultural?"
        ),
        "image": "cultura_festa",
        "caption": "Festa junina com dança de crianças.",
        "options": [
            "Preparar comidas típicas da região em datas especiais.",
            "Celebrar festas tradicionais com danças e músicas.",
            "A altura de uma montanha medida em metros.",
            "Contar histórias passadas de pais para filhos.",
        ],
        "answer": "C",
    },
    {
        "number": 3,
        "theme": "Cultura entre gerações",
        "question": (
            "Observe a imagem com pessoas de idades diferentes. Por que a "
            "cultura pode ser diferente entre avós, pais e crianças?"
        ),
        "image": "geracoes",
        "caption": "Três gerações de uma mesma família.",
        "options": [
            "Porque cada geração vive em épocas e contextos distintos.",
            "Porque apenas os avós têm cultura de verdade.",
            "Porque crianças não participam de nenhuma tradição.",
            "Porque a cultura nunca muda de uma geração para outra.",
        ],
        "answer": "A",
    },
    {
        "number": 4,
        "theme": "Cultura brasileira urbana",
        "question": (
            "Observe a imagem de arte urbana. Esse tipo de manifestação "
            "cultural é comum em cidades brasileiras porque:"
        ),
        "image": "cultura_urbana",
        "caption": "Grafite na Avenida Paulista, São Paulo.",
        "options": [
            "Só existe em países frios, longe do Brasil.",
            "Expressa identidade, criatividade e vida nas cidades.",
            "Não tem relação com a cultura local.",
            "Substitui completamente todas as outras tradições.",
        ],
        "answer": "B",
    },
]

DISSERTATIVAS = [
    {
        "number": 5,
        "theme": "Lugares de vivência",
        "question": (
            "Pedro acorda em casa, toma café, vai à escola, brinca na praça "
            "depois das aulas e ajuda a mãe no mercado. Cite três lugares de "
            "vivência presentes nessa rotina e explique por que a escola também "
            "é um lugar de vivência."
        ),
        "image": "escola",
        "caption": "Escola municipal — lugar de convivência e aprendizagem.",
        "lines": 6,
        "answer_hint": (
            "Lugares: casa, escola, praça, mercado. A escola é lugar de "
            "vivência porque o aluno convive, aprende, brinca e participa da "
            "vida coletiva diariamente."
        ),
    },
    {
        "number": 6,
        "theme": "O que é cultura",
        "question": (
            "Escreva com suas palavras o que é cultura. Depois, dê um exemplo "
            "de manifestação cultural que você conhece na sua cidade ou bairro."
        ),
        "image": None,
        "caption": None,
        "lines": 6,
        "answer_hint": (
            "Cultura é o conjunto de costumes, tradições, festas, comidas, "
            "músicas e formas de viver compartilhadas por um grupo. Exemplos: "
            "festa junina, capoeira, culinária regional, festa de bairro."
        ),
    },
    {
        "number": 7,
        "theme": "Cultura entre gerações",
        "question": (
            "Observe a imagem e escreva duas diferenças entre as brincadeiras "
            "ou hábitos culturais dos avós e os das crianças de hoje. "
            "Mencione também uma tradição que pode ser compartilhada entre "
            "as gerações."
        ),
        "image": "geracoes",
        "caption": "Avós, pais e crianças convivem e transmitem tradições.",
        "lines": 6,
        "answer_hint": (
            "Diferenças: brincadeiras de rua/pião vs jogos digitais; "
            "músicas e festas de épocas distintas. Compartilhada: contação "
            "de histórias, receitas de família, samba de roda, festas."
        ),
    },
    {
        "number": 8,
        "theme": "O que é cultura",
        "question": (
            "Observe a imagem da festa junina. Cite três elementos culturais "
            "visíveis ou relacionados a essa festa e explique o que cada um "
            "representa para a cultura brasileira."
        ),
        "image": "cultura_festa",
        "caption": "Dança típica em festa junina.",
        "lines": 6,
        "answer_hint": (
            "Trajes caipiras, danças (quadrilha), comidas (pipoca, "
            "canjica, quentão), fogueira, bandeirinhas. Representam tradições "
            "do campo e celebrações populares do Brasil."
        ),
    },
    {
        "number": 9,
        "theme": "Cultura brasileira urbana",
        "question": (
            "Observe a imagem de um bloco de carnaval nas ruas de São Paulo. "
            "Descreva o que acontece nesse tipo de manifestação cultural e "
            "explique por que ela faz parte da cultura urbana brasileira."
        ),
        "image": "samba_urbano",
        "caption": "Bloco de carnaval nas ruas de São Paulo.",
        "lines": 6,
        "answer_hint": (
            "Há música, dança, fantasias e convivência nas ruas da cidade. "
            "Faz parte da cultura urbana porque expressa identidade, "
            "criatividade e vida coletiva no espaço urbano."
        ),
    },
    {
        "number": 10,
        "theme": "Cultura brasileira urbana",
        "question": (
            "Cite três manifestações culturais urbanas do Brasil (como funk, "
            "grafite, samba, capoeira ou blocos de rua) e explique brevemente "
            "como cada uma se manifesta na cidade."
        ),
        "image": "cultura_urbana",
        "caption": "Arte urbana em grande centro metropolitano.",
        "lines": 7,
        "answer_hint": (
            "Funk: batidas e danças nas periferias; grafite: arte nas paredes "
            "e viadutos; samba/capoeira: rodas em praças e bairros; blocos: "
            "carnaval nas ruas."
        ),
    },
]


def set_run_font(run, size=11, bold=False, color=DARK, name="Arial"):
    run.font.name = name
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)


def add_horizontal_line(paragraph):
    p_pr = paragraph._p.get_or_add_pPr()
    p_bdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "B0B8C0")
    p_bdr.append(bottom)
    p_pr.append(p_bdr)


def add_paragraph(doc, text="", size=11, bold=False, color=DARK, align=None, space_after=6):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    if text:
        run = p.add_run(text)
        set_run_font(run, size=size, bold=bold, color=color)
    return p


def add_answer_lines(doc, count):
    for _ in range(count):
        p = add_paragraph(doc, space_after=0)
        add_horizontal_line(p)
        p.paragraph_format.space_after = Pt(14)


def add_image_block(doc, image_key, caption):
    image_path = ASSETS_DIR / f"{image_key}.jpg"
    if not image_path.exists():
        add_paragraph(doc, f"[Imagem: {caption}]", size=10, color=MUTED)
        return

    from io import BytesIO

    from PIL import Image

    with Image.open(image_path) as img:
        img = img.convert("RGB")
        buffer = BytesIO()
        img.save(buffer, format="JPEG", quality=90)
        buffer.seek(0)

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    run.add_picture(buffer, width=Cm(11))
    cap = doc.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    cap.paragraph_format.space_after = Pt(8)
    run_cap = cap.add_run(caption)
    set_run_font(run_cap, size=9, color=MUTED, bold=False)


def add_objective_question(doc, item):
    add_paragraph(
        doc,
        f"Questão {item['number']} — {item['theme']}",
        size=11,
        bold=True,
        color=GREEN,
        space_after=4,
    )
    add_paragraph(doc, item["question"], size=11, space_after=8)
    add_image_block(doc, item["image"], item["caption"])

    mark_table = doc.add_table(rows=1, cols=5)
    mark_table.autofit = True
    headers = ["Questão", "A", "B", "C", "D"]
    for idx, label in enumerate(headers):
        cell = mark_table.rows[0].cells[idx]
        cell.text = ""
        run = cell.paragraphs[0].add_run(label)
        set_run_font(run, size=10, bold=True, color=MUTED if idx else GREEN)
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER

    mark_row = mark_table.add_row().cells
    mark_row[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = mark_row[0].paragraphs[0].add_run(f"({item['number']})")
    set_run_font(run, size=10, bold=True)
    for idx in range(1, 5):
        mark_row[idx].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = mark_row[idx].paragraphs[0].add_run("(   )")
        set_run_font(run, size=12)

    doc.add_paragraph()

    labels = ["A", "B", "C", "D"]
    for label, option in zip(labels, item["options"]):
        p = add_paragraph(doc, space_after=4)
        run_mark = p.add_run("(   )  ")
        set_run_font(run_mark, size=11, bold=True)
        run_text = p.add_run(f"{label}) {option}")
        set_run_font(run_text, size=11)

    doc.add_paragraph()


def add_essay_question(doc, item):
    add_paragraph(
        doc,
        f"Questão {item['number']} — {item['theme']}",
        size=11,
        bold=True,
        color=GREEN,
        space_after=4,
    )
    add_paragraph(doc, item["question"], size=11, space_after=8)
    if item.get("image"):
        add_image_block(doc, item["image"], item["caption"])
    add_paragraph(doc, "Resposta:", size=11, bold=True, color=MUTED, space_after=6)
    add_answer_lines(doc, item["lines"])
    doc.add_paragraph()


def build_student_document(output_path):
    doc = Document()
    section = doc.sections[0]
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run("Avaliação de Geografia")
    set_run_font(run, size=18, bold=True, color=GREEN)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = subtitle.add_run("3º Ano do Ensino Fundamental")
    set_run_font(run, size=13, bold=True, color=DARK)

    theme = doc.add_paragraph()
    theme.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = theme.add_run(
        "Lugares de vivência • O que é cultura • Cultura entre gerações • Cultura brasileira urbana"
    )
    set_run_font(run, size=10, color=MUTED)
    theme.paragraph_format.space_after = Pt(12)

    info = doc.add_paragraph()
    info.alignment = WD_ALIGN_PARAGRAPH.LEFT
    run = info.add_run(
        "Aluno(a): ________________________________________________     "
        "Data: ____/____/________     Turma: __________"
    )
    set_run_font(run, size=11)
    info.paragraph_format.space_after = Pt(14)

    add_paragraph(doc, "Instruções", size=12, bold=True, color=GREEN, space_after=6)
    instructions = [
        "• Leia cada questão com atenção antes de responder.",
        "• Observe as imagens — elas ajudam na resposta.",
        "• Parte I: marque com X a alternativa correta nos espaços (   ).",
        "• Parte II: escreva a resposta completa nas linhas indicadas.",
        "• Avaliação de dificuldade média — valor total: 10 pontos (1 ponto por questão).",
        "• Tempo sugerido: 50 minutos.",
    ]
    for line in instructions:
        add_paragraph(doc, line, size=10, space_after=3)
    doc.add_paragraph()

    add_paragraph(doc, "PARTE I — QUESTÕES OBJETIVAS", size=13, bold=True, color=GREEN, space_after=10)
    for item in OBJETIVAS:
        add_objective_question(doc, item)

    doc.add_page_break()
    add_paragraph(doc, "PARTE II — QUESTÕES DISSERTATIVAS", size=13, bold=True, color=GREEN, space_after=10)
    for item in DISSERTATIVAS:
        add_essay_question(doc, item)

    doc.save(output_path)


def build_answer_key(output_path):
    doc = Document()
    add_paragraph(doc, "Gabarito — Avaliação de Geografia (3º ano)", size=16, bold=True, color=GREEN, space_after=8)
    add_paragraph(doc, "Uso exclusivo do(a) professor(a).", size=10, color=MUTED, space_after=12)

    add_paragraph(doc, "Parte I — Objetivas", size=12, bold=True, color=GREEN, space_after=6)
    for item in OBJETIVAS:
        add_paragraph(
            doc,
            f"Questão {item['number']}: alternativa {item['answer']}",
            size=11,
            space_after=4,
        )

    doc.add_paragraph()
    add_paragraph(doc, "Parte II — Dissertativas (respostas esperadas)", size=12, bold=True, color=GREEN, space_after=6)
    for item in DISSERTATIVAS:
        add_paragraph(doc, f"Questão {item['number']}:", size=11, bold=True, space_after=2)
        add_paragraph(doc, item["answer_hint"], size=10, space_after=8)

    doc.save(output_path)


if __name__ == "__main__":
    build_student_document(OUTPUT_PATH)
    build_answer_key(GABARITO_PATH)
    print(f"Avaliação gerada: {OUTPUT_PATH}")
    print(f"Gabarito gerado: {GABARITO_PATH}")
