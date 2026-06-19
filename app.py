import streamlit as st
import pandas as pd

# Configurações básicas da página
st.set_page_config(page_title="Gabarito Instantâneo PMMC", page_icon="📝", layout="centered")

# Matriz de Correção Oficial (Gabarito Oculto)
MATRIZ_RESPOSTAS = {
    1: "A", 2: "D", 3: "D", 4: "C", 5: "C", 6: "C", 7: "A", 8: "C", 9: "B", 10: "C",
    11: "C", 12: "C", 13: "C", 14: "C", 15: "C", 16: "C", 17: "D", 18: "A", 19: "C", 20: "B",
    21: "D", 22: "D", 23: "D", 24: "B", 25: "D", 26: "A", 27: "A", 28: "B", 29: "C", 30: "D",
    31: "B", 32: "C", 33: "D", 34: "A", 35: "B", 36: "C", 37: "C", 38: "A", 39: "B", 40: "B"
}

st.title("📝 Correção Instantânea de Simulado")
st.markdown("Marque suas respostas abaixo e clique em **Emitir Boletim**. Nada será salvo.")

st.subheader("📋 Folha de Respostas")
respostas_usuario = {}

# Exibe as 40 questões de forma limpa e compacta (em 2 colunas para poupar rolagem)
col_esq, col_dir = st.columns(2)

for q in range(1, 41):
    # Divide as questões igualmente entre a coluna da esquerda e da direita
    with col_esq if q <= 20 else col_dir:
        respostas_usuario[q] = st.radio(
            f"Questão {q}:",
            ["A", "B", "C", "D"],
            index=0,
            key=f"q_{q}",
            horizontal=True
        )

st.divider()

# Botão para calcular e exibir o resultado na hora
if st.button("📊 Emitir Meu Boletim", type="primary", use_container_width=True):
    total_acertos = 0
    detalhes_prova = []

    # Processa as respostas comparando com o gabarito
    for q, resp_aluno in respostas_usuario.items():
        gabarito_oficial = MATRIZ_RESPOSTAS[q]
        correto = (resp_aluno == gabarito_oficial)
        
        if correto:
            total_acertos += 1
            
        detalhes_prova.append({
            "Questão": q,
            "Sua Resposta": resp_aluno,
            "Gabarito": gabarito_oficial,
            "Resultado": "🟢 Correto" if correto else "🔴 Incorreto"
        })

    # Exibição dos Resultados (Métricas)
    st.header("📋 Seu Resultado")
    
    c1, c2, c3 = st.columns(3)
    nota_final = (total_acertos / 40) * 10
    porcentagem = (total_acertos / 40) * 100
    
    c1.metric("Nota Final", f"{nota_final:.1f} / 10.0")
    c2.metric("Total de Acertos", f"{total_acertos} de 40")
    c3.metric("Aproveitamento", f"{porcentagem:.1f}%")

    st.divider()
    
    # Tabela detalhada (Espelho da Prova)
    st.subheader("🔍 Espelho da Prova")
    df_resultado = pd.DataFrame(detalhes_prova)
    st.dataframe(df_resultado.set_index("Questão"), use_container_width=True, height=500)
    
    st.success("Boletim gerado com sucesso! (Nenhum dado foi coletado ou armazenado)")
