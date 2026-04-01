import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from math import pi

# ==============================================================================
# 1. CONFIGURAÇÕES DA PÁGINA E ESTILO
# ==============================================================================
st.set_page_config(
    page_title="Sistema Especialista Médico - Diagnóstico Tropical",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS customizado para melhorar a aparência
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stMetric {
        background-color: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    .logic-box {
        background-color: #f1f8ff;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #2196f3;
        margin-bottom: 20px;
    }
    .sidebar-footer {
        position: fixed;
        bottom: 20px;
        font-size: 12px;
        color: #6c757d;
    }
    </style>
    """, unsafe_allow_html=True)

# Configuração visual dos gráficos
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = [12, 6]
plt.rcParams['font.size'] = 10

# ==============================================================================
# 2. BASE DE CONHECIMENTO E PRÉ-PROCESSAMENTO
# ==============================================================================

@st.cache_data
def carregar_e_processar_dados():
    """Carrega o CSV e converte as descrições textuais em valores numéricos (1-5)."""
    try:
        df = pd.read_csv('sintomas_doencas.csv')
        
        # Mapeamento expandido para evitar erros de termos não encontrados
        mapping = {
            'ausente': 1,
            'baixa': 2,
            'leve': 2,
            'raro': 2,
            'moderada': 3,
            'moderado': 3,
            'alta': 4,
            'forte': 4,
            'frequente': 4,
            'seca': 4,
            'muito_alta': 5,
            'muito_forte': 5,
            'muito_frequente': 5
        }
        
        # Converter colunas de sintomas (todas exceto 'doenca')
        df_num = df.copy()
        for col in df.columns[1:]:
            df_num[col] = df[col].map(lambda x: mapping.get(str(x).lower().strip(), 1))
            
        return df, df_num
    except FileNotFoundError:
        return None, None
    except Exception as e:
        st.error(f"Erro ao processar dados: {e}")
        return None, None

df_original, df_base = carregar_e_processar_dados()

# ==============================================================================
# 3. MOTOR DE INFERÊNCIA E EXPLICAÇÃO DA LÓGICA
# ==============================================================================

class SistemaEspecialistaMedico:
    """
    Sistema Especialista para diagnóstico médico baseado em sintomas.
    Utiliza uma lógica de Pontuação por Proximidade (Similaridade de Manhattan).
    """
    def __init__(self, base_dados):
        self.base_dados = base_dados
        self.sintomas_disponiveis = base_dados.columns[1:]
    
    def diagnosticar(self, sintomas_paciente):
        resultados = []
        for index, row in self.base_dados.iterrows():
            pontuacao_total = 0
            # Diferença máxima por sintoma é 4 (5 - 1)
            max_pontos_possiveis = len(self.sintomas_disponiveis) * 4
            
            for sintoma in self.sintomas_disponiveis:
                valor_paciente = sintomas_paciente.get(sintoma, 1)
                valor_esperado = row[sintoma]
                
                # Lógica de Proximidade:
                # Calculamos a distância absoluta entre o que o paciente sente e o esperado.
                # Se a diferença é 0, ganha 4 pontos (match perfeito).
                # Se a diferença é 4, ganha 0 pontos (extremos opostos).
                diferenca = abs(valor_paciente - valor_esperado)
                pontos = 4 - diferenca
                pontuacao_total += pontos
            
            # Cálculo de Confiança (Normalização para %)
            confianca = (pontuacao_total / max_pontos_possiveis) * 100
            resultados.append({
                'doenca': row['doenca'],
                'confianca': round(confianca, 2),
                'pontuacao': pontuacao_total
            })
        
        return sorted(resultados, key=lambda x: x['confianca'], reverse=True)

# ==============================================================================
# 4. INTERFACE DO USUÁRIO (STREAMLIT)
# ==============================================================================

st.title("🩺 Sistema Especialista para Diagnóstico de Doenças Tropicais")

# Introdução e Explicação da Lógica
with st.expander("ℹ️ Sobre o Sistema e a Lógica de Inferência", expanded=False):
    st.markdown("""
    ### 🧠 Como este sistema "pensa"? (Lógica Fuzzy-like)
    Diferente de sistemas tradicionais que usam apenas **Sim/Não**, este sistema utiliza uma abordagem de 
    **Raciocínio Aproximado** baseada em graus de intensidade (1 a 5).
    
    1.  **Representação do Conhecimento**: As doenças são armazenadas como "perfis típicos" de sintomas.
    2.  **Cálculo de Proximidade (Distância de Manhattan)**:
        - Para cada sintoma, comparamos o valor informado ($V_p$) com o valor esperado na base ($V_e$).
        - Calculamos a distância: $dist = |V_p - V_e|$.
        - Atribuímos uma pontuação inversamente proporcional à distância.
    3.  **Agregação**: Somamos as pontuações de todos os sintomas para gerar um índice de confiança final.
    
    ### 🛡️ Tratamento de Incertezas
    Esta lógica permite que o sistema identifique doenças mesmo quando o paciente não apresenta a 
    intensidade "exata" descrita nos livros médicos, lidando com a subjetividade da dor e dos sintomas.
    """)

if df_base is not None:
    se = SistemaEspecialistaMedico(df_base)
    
    # Sidebar para entrada de dados
    st.sidebar.header("📋 Avaliação de Sintomas")
    st.sidebar.info("Deslize para indicar a intensidade de cada sintoma no seu corpo atual.")
    
    DESCRICOES_SINTOMAS = {
        'febre': '🌡️ Febre',
        'dor_cabeca': '🤕 Dor de Cabeça',
        'dor_articular': '🦴 Dor nas Articulações',
        'dor_muscular': '💪 Dor Muscular',
        'manchas_pele': '🔴 Manchas na Pele / Erupções',
        'dor_olhos': '👁️ Dor nos Olhos',
        'tosse': '😷 Tosse',
        'nausea_vomito': '🤢 Náusea / Vômito',
        'dor_garganta': '😮 Dor de Garganta',
        'congestao_nasal': '👃 Congestão Nasal'
    }
    
    # Escala explicativa na sidebar
    st.sidebar.markdown("""
    **Escala:**
    1. Ausente
    2. Leve
    3. Moderado
    4. Forte
    5. Muito Forte
    """)
    
    sintomas_input = {}
    for sintoma in se.sintomas_disponiveis:
        label = DESCRICOES_SINTOMAS.get(sintoma, sintoma.replace('_', ' ').title())
        sintomas_input[sintoma] = st.sidebar.slider(label, 1, 5, 1, key=sintoma)
    
    # Rodapé com Autores
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    **✍️ Autores:**
    - Davi Eduardo
    - Vitória Cordeiro
    - Nathália Gualberto
    - Caio Queiroz
    """)
    
    # Executar Diagnóstico
    resultados = se.diagnosticar(sintomas_input)
    df_resultados = pd.DataFrame(resultados)
    
    # Layout em abas
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Diagnóstico", 
        "🔍 Análise Detalhada", 
        "📈 Distribuição",
        "📚 Base de Conhecimento"
    ])
    
    with tab1:
        st.header("🔬 Resultados do Diagnóstico")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            melhor_match = resultados[0]
            st.metric("Diagnóstico Provável", melhor_match['doenca'])
            st.metric("Confiança do Sistema", f"{melhor_match['confianca']}%")
            
            st.write("### Ranking de Hipóteses")
            st.dataframe(df_resultados[['doenca', 'confianca']].rename(
                columns={'doenca': 'Doença', 'confianca': 'Confiança (%)'}
            ), use_container_width=True)
            
        with col2:
            # Gráfico de Ranking (Barra)
            fig_bar, ax_bar = plt.subplots(figsize=(10, 6))
            cores = ['#d62728' if i == 0 else '#1f77b4' for i in range(len(df_resultados))]
            sns.barplot(data=df_resultados, x='confianca', y='doenca', palette=cores, ax=ax_bar)
            ax_bar.set_title("Probabilidade de Diagnóstico por Doença")
            ax_bar.set_xlabel("Confiança (%)")
            ax_bar.set_xlim(0, 100)
            
            # Adicionar labels nas barras
            for i, v in enumerate(df_resultados['confianca']):
                ax_bar.text(v + 1, i, f"{v}%", va='center')
                
            st.pyplot(fig_bar)

    with tab2:
        st.header("🎯 Análise de Compatibilidade")
        
        doenca_principal = resultados[0]['doenca']
        st.write(f"Comparando seus sintomas com o perfil típico de: **{doenca_principal}**")
        
        col_radar, col_contrib = st.columns(2)
        
        with col_radar:
            # Gráfico de Radar
            perfil_doenca = df_base[df_base['doenca'] == doenca_principal].iloc[0].drop('doenca')
            
            categorias = list(sintomas_input.keys())
            valores_paciente = list(sintomas_input.values())
            valores_doenca = [perfil_doenca[cat] for cat in categorias]
            
            N = len(categorias)
            angulos = [n / float(N) * 2 * pi for n in range(N)]
            valores_paciente += valores_paciente[:1]
            valores_doenca += valores_doenca[:1]
            angulos += angulos[:1]
            
            fig_radar, ax_radar = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
            ax_radar.plot(angulos, valores_paciente, 'o-', linewidth=2, label='Seus Sintomas', color='#d62728')
            ax_radar.fill(angulos, valores_paciente, alpha=0.25, color='#d62728')
            ax_radar.plot(angulos, valores_doenca, 'o-', linewidth=2, label=f'Perfil: {doenca_principal}', color='#1f77b4')
            ax_radar.fill(angulos, valores_doenca, alpha=0.25, color='#1f77b4')
            
            # Nomes curtos para o radar
            clean_labels = [label.split()[-1] for label in DESCRICOES_SINTOMAS.values()]
            ax_radar.set_xticks(angulos[:-1])
            ax_radar.set_xticklabels(clean_labels, size=10)
            ax_radar.set_ylim(0, 5)
            plt.legend(loc='upper right', bbox_to_anchor=(1.1, 1.1))
            st.pyplot(fig_radar)
            
        with col_contrib:
            # Análise de Contribuição
            st.write(f"### O que mais contribuiu para este diagnóstico?")
            contribuicoes = []
            for s in sintomas_input.keys():
                prox = 4 - abs(sintomas_input[s] - perfil_doenca[s])
                contribuicoes.append({
                    'sintoma': DESCRICOES_SINTOMAS.get(s, s),
                    'compatibilidade': (prox / 4) * 100
                })
            df_contrib = pd.DataFrame(contribuicoes).sort_values('compatibilidade', ascending=False)
            
            fig_contrib, ax_contrib = plt.subplots(figsize=(10, 8))
            cores_contrib = ['#2ecc71' if c >= 75 else '#f39c12' if c >= 50 else '#e74c3c' for c in df_contrib['compatibilidade']]
            sns.barplot(data=df_contrib, x='compatibilidade', y='sintoma', palette=cores_contrib, ax=ax_contrib)
            ax_contrib.set_xlim(0, 100)
            ax_contrib.set_title("Match por Sintoma")
            st.pyplot(fig_contrib)

    with tab3:
        st.header("📈 Análise de Distribuição e Gaps")
        
        # Gráfico de Linha (Evolução das Probabilidades)
        fig_line, ax_line = plt.subplots(figsize=(12, 5))
        ax_line.plot(df_resultados['doenca'], df_resultados['confianca'], marker='o', linewidth=2, color='#2E86AB')
        ax_line.fill_between(range(len(df_resultados)), df_resultados['confianca'], alpha=0.2, color='#2E86AB')
        ax_line.set_title("Diferenciação entre Hipóteses")
        ax_line.set_ylabel("Confiança (%)")
        ax_line.set_ylim(0, 105)
        plt.xticks(rotation=45)
        st.pyplot(fig_line)
        
        gap = resultados[0]['confianca'] - resultados[1]['confianca']
        st.info(f"💡 **Gap de Diferenciação**: A primeira hipótese ({resultados[0]['doenca']}) está **{gap:.2f}%** acima da segunda. Quanto maior este gap, mais específico é o seu quadro sintomático.")

        # Heatmap Comparativo Geral
        st.write("### 🌡️ Comparação Visual: Seus Sintomas vs. Todas as Doenças")
        df_comp = df_base.set_index('doenca').copy()
        df_comp.loc['VOCÊ'] = pd.Series(sintomas_input)
        
        fig_hm, ax_hm = plt.subplots(figsize=(14, 8))
        sns.heatmap(df_comp.T, annot=True, cmap='RdYlGn_r', linewidths=0.5, ax=ax_hm, vmin=1, vmax=5)
        st.pyplot(fig_hm)

    with tab4:
        st.header("📊 Inteligência do Sistema")
        st.write("Abaixo você vê como o sistema 'enxerga' cada doença (valores convertidos de 1 a 5).")
        st.dataframe(df_base.style.background_gradient(cmap='YlOrRd', axis=None), use_container_width=True)
        
        with st.expander("Ver Base de Dados Original (Texto)"):
            st.dataframe(df_original, use_container_width=True)

    # Disclaimer de Segurança
    st.error("""
    ⚠️ **DISCLAIMER MÉDICO CRÍTICO**:
    Este software é um protótipo acadêmico para fins de demonstração de **Inteligência Artificial (Sistemas Especialistas)**.
    1. **NÃO** fornece diagnóstico médico real.
    2. **NÃO** substitui a consulta com um profissional de saúde.
    3. Em caso de febre alta, dores intensas ou dificuldades respiratórias, **procure uma unidade de saúde imediatamente**.
    """)
