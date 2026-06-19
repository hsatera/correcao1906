import streamlit as st
import pandas as pd

# Configurações básicas da página
st.set_page_config(page_title="Gabarito Instantâneo PMMC", page_icon="📝", layout="centered")

# Matriz de Correção Oficial com os respectivos Domínios de Competência
MATRIZ_COMPLETA = {
    1: {"resp": "A", "dominios": ["Gestão e Organização do Processo de Trabalho", "Saúde Coletiva"]},
    2: {"resp": "D", "dominios": ["Gestão e Organização do Processo de Trabalho", "Avaliação da Qualidade e Auditoria", "Saúde Coletiva"]},
    3: {"resp": "D", "dominios": ["Princípios da APS", "Avaliação da Qualidade e Auditoria", "Saúde Coletiva"]},
    4: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    5: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    6: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    7: {"resp": "A", "dominios": ["Atenção à Saúde"]},
    8: {"resp": "C", "dominios": ["Pesquisa Médica", "Gestão em Saúde", "Comunicação e Docência"]},
    9: {"resp": "B", "dominios": ["Atenção à Saúde"]},
    10: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    11: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    12: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    13: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    14: {"resp": "C", "dominios": ["Atenção à Saúde", "Princípios da APS"]},
    15: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    16: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    17: {"resp": "D", "dominios": ["Atenção à Saúde"]},
    18: {"resp": "A", "dominios": ["Atenção à Saúde"]},
    19: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    20: {"resp": "B", "dominios": ["Atenção à Saúde"]},
    21: {"resp": "D", "dominios": ["Atenção à Saúde"]},
    22: {"resp": "D", "dominios": ["Atenção à Saúde"]},
    23: {"resp": "D", "dominios": ["Atenção à Saúde"]},
    24: {"resp": "B", "dominios": ["Atenção à Saúde"]},
    25: {"resp": "D", "dominios": ["Atenção à Saúde"]},
    26: {"resp": "A", "dominios": ["Atenção à Saúde"]},
    27: {"resp": "A", "dominios": ["Atenção à Saúde"]},
    28: {"resp": "B", "dominios": ["Atenção à Saúde"]},
    29: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    30: {"resp": "D", "dominios": ["Atenção à Saúde"]},
    31: {"resp": "B", "dominios": ["Atenção à Saúde"]},
    32: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    33: {"resp": "D", "dominios": ["Atenção à Saúde"]},
    34: {"resp": "A", "dominios": ["Atenção à Saúde", "Saúde Coletiva"]},
    35: {"resp": "B", "dominios": ["Atenção à Saúde"]},
    36: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    37: {"resp": "C", "dominios": ["Atenção à Saúde"]},
    38: {"resp": "A", "dominios": ["Atenção à Saúde"]},
    39: {"resp": "B", "dominios": ["Saúde Coletiva"]},
    40: {"resp": "B", "dominios": ["Atenção à Saúde"]}
}

st.title("📝 Correção Instantânea de Simulado")
st.markdown("Marque suas respostas abaixo e clique em **Emitir Boletim**. Nada será salvo.")

st.subheader("📋 Folha de Respostas")
respostas_usuario = {}

# Exibe as 40 questões em 2 colunas
col_esq, col_dir = st.columns(2)
for q in range(1, 41):
    with col_esq if q <= 20 else col_dir:
        respostas_usuario[q] = st.radio(
            f"Questão {q}:",
            ["A", "B", "C", "D"],
            index=0,
            key=f"q_{q}",
            horizontal=True
        )

st.divider()

# Botão para calcular e exibir o resultado
if st.button("📊 Emitir Meu Boletim", type="primary", use_container_width=True):
    total_acertos = 0
    detalhes_prova = []
    calculo_dominios = {}

    # Processa as respostas
    for q, resp_aluno in respostas_usuario.items():
        dados_q = MATRIZ_COMPLETA[q]
        gabarito_oficial = dados_q["resp"]
        correto = (resp_aluno == gabarito_oficial)
        
        if correto:
            total_acertos += 1
            
        # Contabiliza os domínios de competência
        for dom in dados_q["dominios"]:
            if dom not in calculo_dominios:
                calculo_dominios[dom] = {"acertos": 0, "total": 0}
            calculo_dominios[dom]["total"] += 1
            if correto:
                calculo_dominios[dom]["acertos"] += 1

        detalhes_prova.append({
            "Questão": q,
            "Sua Resposta": resp_aluno,
            "Gabarito": gabarito_oficial,
            "Resultado": "🟢 Correto" if correto else "🔴 Incorreto",
            "Domínios": ", ".join(dados_q["dominios"])
        })

    # 1. MENSURAÇÃO GERAL (Métricas)
    st.header("📋 Seu Resultado Geral")
    c1, c2, c3 = st.columns(3)
    nota_final = (total_acertos / 40) * 10
    porcentagem = (total_acertos / 40) * 100
    
    c1.metric("Nota Final", f"{nota_final:.1f} / 10.0")
    c2.metric("Total de Acertos", f"{total_acertos} de 40")
    c3.metric("Aproveitamento", f"{porcentagem:.1f}%")

    st.divider()
    
    # 2. DESEMPENHO POR DOMÍNIO DE COMPETÊNCIA
    st.subheader("🎯 Desempenho por Domínio de Competência")
    
    # Renderiza barras de progresso limpas para cada domínio encontrado nas questões
    for dom, valores in calculo_dominios.items():
        pct_dom = (valores["acertos"] / valores["total"]) * 100
        st.write(f"**{dom}** ({valores['acertos']}/{valores['total']} acertos)")
        st.progress(pct_dom / 100)
        st.caption(f"Aproveitamento: {pct_dom:.1f}%")
        st.write("")

    st.divider()
    
    # 3. TABELA DETALHADA
    st.subheader("🔍 Espelho da Prova")
    df_resultado = pd.DataFrame(detalhes_prova)
    st.dataframe(df_resultado.set_index("Questão"), use_container_width=True, height=500)
    
    st.success("Boletim por competências gerado com sucesso! (Nenhum dado foi salvo)")
