import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuração da página
st.set_page_config(page_title="Pedido de Folga - Aeroportos GOL", layout="centered")

st.title("📆 Formulário de Pedido de Folga - Dezembro 2025")
st.markdown("Preencha os dados abaixo para solicitar folga no **Natal (24/25)** ou **Ano Novo (31/12 e 01/01)**.")

# Caminhos das pastas e arquivos
base_folder = "FP AERPOPORTOS/streamlit/folgas/2025"
log_folder = "FP AERPOPORTOS/streamlit/folgas/logs"
os.makedirs(base_folder, exist_ok=True)
os.makedirs(log_folder, exist_ok=True)

natal_file = os.path.join(base_folder, "natal.csv")
ano_novo_file = os.path.join(base_folder, "ano_novo.csv")
log_file = os.path.join(log_folder, "registros_completos.csv")

# Bases disponíveis
bases_disponiveis = ["GRU", "CGH", "GIG", "BSB", "CNF", "POA", "SSA", "REC", "FOR", "CWB"]

# Formulário
with st.form("form_folga"):
    cif = st.text_input("CIF do colaborador", max_chars=10)
    email = st.text_input("E-mail corporativo")
    base = st.selectbox("Base de trabalho", bases_disponiveis)
    tipo_folga = st.radio("Preferência de folga", ["Natal (24/25)", "Ano Novo (31/12 e 01/01)"])
    observacoes = st.text_area("Observações adicionais (opcional)")
    enviar = st.form_submit_button("Enviar pedido")

    if enviar:
        if not cif or not email:
            st.error("⚠️ CIF e e-mail são obrigatórios.")
        else:
            registro = {
                "Data do Registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "CIF": cif,
                "Email": email,
                "Base": base,
                "Tipo de Folga": tipo_folga,
                "Observações": observacoes
            }

            # Salva no arquivo correspondente
            destino = natal_file if "Natal" in tipo_folga else ano_novo_file
            df_individual = pd.DataFrame([registro])
            if os.path.exists(destino):
                df_existente = pd.read_csv(destino)
                df_atualizado = pd.concat([df_existente, df_individual], ignore_index=True)
            else:
                df_atualizado = df_individual
            df_atualizado.to_csv(destino, index=False)

            # Salva no log geral
            if os.path.exists(log_file):
                df_log = pd.read_csv(log_file)
                df_log = pd.concat([df_log, df_individual], ignore_index=True)
            else:
                df_log = df_individual
            df_log.to_csv(log_file, index=False)

            st.success("✅ Pedido registrado com sucesso!")

# Exibe relatório resumido
st.subheader("📋 Resumo dos pedidos registrados")
if os.path.exists(log_file):
    df_log = pd.read_csv(log_file)
    st.dataframe(df_log)
else:
    st.info("Nenhum pedido registrado ainda.")