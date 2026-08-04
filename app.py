import streamlit as st
from fpdf import FPDF  # <--- CÓDIGO CORRIGIDO AQUI
from datetime import datetime

# Configuração da página do aplicativo
st.set_page_config(
    page_title="Registro de Ocorrência",
    page_icon="🚓",
    layout="centered"
)

class PDFOcorrencia(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, self.encode_str("RELATÓRIO DE OCORRÊNCIA POLICIAL"), border=False, new_x="LMARGIN", new_y="NEXT", align="C")
        self.ln(2)
        self.set_draw_color(100, 100, 100)
        self.line(10, 22, 200, 22)
        self.ln(5)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, self.encode_str(f"Página {self.page_no()}"), align="C")

    def encode_str(self, text):
        """Converte o texto para a codificação aceita pelo FPDF padrão (latin-1)"""
        if not text:
            return ""
        return str(text).encode("latin-1", "replace").decode("latin-1")

def gerar_pdf(dados):
    pdf = PDFOcorrencia()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    def add_campo(rotulo, valor):
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(50, 7, pdf.encode_str(f"{rotulo}:"), border=0)
        pdf.set_font("Helvetica", "", 10)
        pdf.multi_cell(0, 7, pdf.encode_str(valor if valor else "Não informado"))
        pdf.ln(1)

    # Preenchimento dos dados do formulário no PDF
    add_campo("Data do Fato", dados['data_fato'].strftime("%d/%m/%Y") if dados['data_fato'] else "")
    add_campo("Tipo de Procedimento", dados['tipo_proc'])
    add_campo("Tipo de Crime", dados['tipo_crime'])
    add_campo("Equipe Responsável", dados['equipe'])
    add_campo("Local do Fato", dados['local'])
    add_campo("Acusado(s)", dados['acusados'])
    
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, pdf.encode_str("Material Apreendido:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, pdf.encode_str(dados['material'] if dados['material'] else "Nenhum material apreendido informado."))
    
    pdf.ln(3)
    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 7, pdf.encode_str("Narrativa Sucinta dos Fatos:"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 10)
    pdf.multi_cell(0, 6, pdf.encode_str(dados['narrativa'] if dados['narrativa'] else "Sem narrativa registrada."))
    
    # Adiciona data e hora da emissão
    pdf.ln(8)
    pdf.set_font("Helvetica", "I", 8)
    pdf.cell(0, 5, pdf.encode_str(f"Relatório gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M')}"), new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())

# --- INTERFACE DO USUÁRIO ---
st.title("🚓 Registro de Ocorrência Policial")
st.markdown("Preencha os campos abaixo para gerar o relatório consolidado em PDF.")

with st.form("form_ocorrencia"):
    col1, col2 = st.columns(2)
    
    with col1:
        data_fato = st.date_input("Data do Fato", value=datetime.today())
        tipo_proc = st.selectbox("Tipo de Procedimento", ["Prisão em Flagrante", "Cumprimento de Mandado", "Outros"])
        equipe = st.text_input("Equipe Responsável", placeholder="Ex: VTR 1020 / 1º Batalhão")
        tipo_crime = st.text_input("Tipo de Crime", placeholder="Ex: Tráfico de Drogas (Art. 33)")

    with col2:
        local = st.text_input("Local do Fato", placeholder="Ex: Av. Principal, nº 100 - Bairro Centro")
        acusados = st.text_input("Acusado(s) / Envolvido(s)", placeholder="Nome(s) ou 'A apurar'")
    
    material = st.text_area("Material Apreendido", placeholder="Descreva os materiais, armas, substâncias ou objetos apreendidos...")
    narrativa = st.text_area("Narrativa Sucinta dos Fatos", placeholder="Descreva brevemente o histórico da ocorrência...", height=150)
    
    submitted = st.form_submit_button("Gerar Prévia do PDF")

if submitted:
    dados_formulario = {
        "data_fato": data_fato,
        "tipo_proc": tipo_proc,
        "equipe": equipe,
        "tipo_crime": tipo_crime,
        "local": local,
        "acusados": acusados,
        "material": material,
        "narrativa": narrativa
    }
    
    # Geração do arquivo PDF em memória
    pdf_bytes = gerar_pdf(dados_formulario)
    
    st.success("Relatório gerado com sucesso!")
    
    # Botão para baixar diretamente o PDF
    st.download_button(
        label="📄 Baixar Relatório em PDF",
        data=pdf_bytes,
        file_name=f"Ocorrencia_{data_fato.strftime('%Y%m%d')}_{tipo_proc.replace(' ', '_')}.pdf",
        mime="application/pdf"
        )
    
