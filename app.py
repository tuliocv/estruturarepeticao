import json
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from filelock import FileLock

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="Java — Loops na Prática",
    page_icon="🔁",
    layout="wide",
    initial_sidebar_state="expanded"
)

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

CSV_PATH = DATA_DIR / "feedback_java_loops.csv"
JSONL_PATH = DATA_DIR / "feedback_java_loops.jsonl"
LOCK_PATH = DATA_DIR / "feedback_java_loops.lock"

STATUS_OPTS = ["✅ Consegui", "🟡 Parcial", "❌ Não consegui"]
DIF_OPTS = ["Muito fácil", "Fácil", "Médio", "Difícil"]
HELP_OPTS = ["Não", "Sim"]

TEACHER_PASS = st.secrets.get("app", {}).get("teacher_password", "")

LEVEL_ORDER = ["Primeiro contato", "Básico", "Intermediário", "Aplicação real", "Desafiador"]
LEVEL_COLORS = {
    "Primeiro contato": ("#E8F5E9", "#1B5E20"),
    "Básico": ("#E3F2FD", "#0D47A1"),
    "Intermediário": ("#FFF8E1", "#E65100"),
    "Aplicação real": ("#FCE4EC", "#880E4F"),
    "Desafiador": ("#F3E5F5", "#4A148C"),
}

LOOP_BADGE = {
    "for": "🔹 for",
    "while": "🔸 while",
    "do-while": "🔷 do-while",
    "for/while": "🔁 for ou while",
    "while/do-while": "🔁 while ou do-while",
    "livre": "🧠 escolha livre",
}

# =========================
# EXERCÍCIOS
# =========================
EXS = [
    {
        "id": "Ex 01",
        "title": "Imprima 'Olá' 5 vezes",
        "level": "Primeiro contato",
        "loop_hint": "for",
        "skills": ["repetição", "contagem"],
        "goal": "Perceber que o loop evita repetir código manualmente.",
        "prompt": "Escreva um programa que imprima a palavra 'Olá' 5 vezes na tela.",
    },
    {
        "id": "Ex 02",
        "title": "Conte de 1 até 5",
        "level": "Primeiro contato",
        "loop_hint": "for",
        "skills": ["sequência", "variável de controle"],
        "goal": "Entender início, fim e passo do loop.",
        "prompt": "Escreva um programa que mostre os números de 1 até 5, um por linha.",
    },
    {
        "id": "Ex 03",
        "title": "Conte de 1 até 10 na mesma linha",
        "level": "Primeiro contato",
        "loop_hint": "for",
        "skills": ["saída formatada", "repetição"],
        "goal": "Treinar repetição com saída simples.",
        "prompt": "Escreva um programa que mostre os números de 1 até 10 na mesma linha, separados por espaço.",
    },
    {
        "id": "Ex 04",
        "title": "Par ou ímpar de 1 a 10",
        "level": "Básico",
        "loop_hint": "for",
        "skills": ["if", "módulo", "repetição"],
        "goal": "Combinar loop com decisão simples.",
        "prompt": "Mostre os números de 1 até 10 e, ao lado de cada um, informe se ele é par ou ímpar.",
    },
    {
        "id": "Ex 05",
        "title": "Conte de 1 até um número informado",
        "level": "Básico",
        "loop_hint": "for",
        "skills": ["entrada", "limite do loop"],
        "goal": "Usar valor do usuário como limite da repetição.",
        "prompt": "Peça um número ao usuário e mostre todos os números de 1 até esse valor.",
    },
    {
        "id": "Ex 06",
        "title": "Mostre apenas os pares até N",
        "level": "Básico",
        "loop_hint": "for",
        "skills": ["filtro", "condição"],
        "goal": "Filtrar valores dentro do loop.",
        "prompt": "Peça um número ao usuário e mostre apenas os números pares entre 1 e esse valor.",
    },
    {
        "id": "Ex 07",
        "title": "Conte quantos pares existem até N",
        "level": "Intermediário",
        "loop_hint": "for",
        "skills": ["acumulador", "contador"],
        "goal": "Usar variável para contar ocorrências.",
        "prompt": "Peça um número ao usuário e informe quantos números pares existem entre 1 e esse valor.",
    },
    {
        "id": "Ex 08",
        "title": "Soma de 1 até N",
        "level": "Intermediário",
        "loop_hint": "for",
        "skills": ["soma acumulada", "variável auxiliar"],
        "goal": "Treinar acumulador com loop.",
        "prompt": "Peça um número ao usuário e calcule a soma de 1 até esse número.",
    },
    {
        "id": "Ex 09",
        "title": "Validar número positivo",
        "level": "Intermediário",
        "loop_hint": "while/do-while",
        "skills": ["validação", "repetição por condição"],
        "goal": "Repetir até a entrada ficar correta.",
        "prompt": "Peça um número ao usuário até que ele digite um valor positivo.",
    },
    {
        "id": "Ex 10",
        "title": "Somar números até digitar 0",
        "level": "Intermediário",
        "loop_hint": "while/do-while",
        "skills": ["sentinela", "acumulador"],
        "goal": "Trabalhar parada por valor especial.",
        "prompt": "Peça números ao usuário e some todos eles até que seja digitado 0.",
    },
    {
        "id": "Ex 11",
        "title": "Contar quantos números foram digitados",
        "level": "Intermediário",
        "loop_hint": "while/do-while",
        "skills": ["contador", "sentinela"],
        "goal": "Contar repetições úteis.",
        "prompt": "Peça números ao usuário até digitar 0 e informe quantos números válidos foram digitados.",
    },
    {
        "id": "Ex 12",
        "title": "Soma, quantidade e média até 0",
        "level": "Intermediário",
        "loop_hint": "while/do-while",
        "skills": ["média", "contador", "acumulador"],
        "goal": "Integrar soma, contagem e cálculo final.",
        "prompt": "Peça números ao usuário até digitar 0. Ao final, mostre a soma, a quantidade de números digitados e a média.",
    },
    {
        "id": "Ex 13",
        "title": "Caixa de compras",
        "level": "Aplicação real",
        "loop_hint": "while/do-while",
        "skills": ["contexto real", "totalização"],
        "goal": "Mostrar uso do loop em compras sucessivas.",
        "prompt": "Peça o valor de produtos até o usuário digitar 0. Ao final, mostre o total da compra.",
    },
    {
        "id": "Ex 14",
        "title": "Sistema de senha",
        "level": "Aplicação real",
        "loop_hint": "while/do-while",
        "skills": ["validação", "segurança"],
        "goal": "Aplicar repetição em autenticação simples.",
        "prompt": "Peça uma senha ao usuário e continue solicitando até que ele digite a senha correta.",
    },
    {
        "id": "Ex 15",
        "title": "Média de notas",
        "level": "Aplicação real",
        "loop_hint": "while/do-while",
        "skills": ["sentinela", "média"],
        "goal": "Aplicar repetição em contexto acadêmico.",
        "prompt": "Peça notas de alunos até que o usuário digite -1. Ao final, mostre a média das notas válidas.",
    },
    {
        "id": "Ex 16",
        "title": "Minutos de treino",
        "level": "Aplicação real",
        "loop_hint": "for",
        "skills": ["entrada repetida", "total semanal"],
        "goal": "Somar valores em um cenário real.",
        "prompt": "Pergunte quantos dias a pessoa treinou e, em seguida, peça os minutos de cada dia. Ao final, mostre o total de minutos treinados.",
    },
    {
        "id": "Ex 17",
        "title": "Tabuada de um número",
        "level": "Aplicação real",
        "loop_hint": "for",
        "skills": ["padrão numérico", "multiplicação"],
        "goal": "Usar loop para gerar resultados previsíveis.",
        "prompt": "Peça um número ao usuário e mostre sua tabuada de 1 até 10.",
    },
    {
        "id": "Ex 18",
        "title": "Verificar se um número é primo",
        "level": "Desafiador",
        "loop_hint": "for",
        "skills": ["divisibilidade", "otimização básica"],
        "goal": "Explorar teste repetitivo com condição de parada.",
        "prompt": "Peça um número ao usuário e informe se ele é primo ou não.",
    },
    {
        "id": "Ex 19",
        "title": "Jogo de adivinhação simples",
        "level": "Desafiador",
        "loop_hint": "while/do-while",
        "skills": ["tentativas", "condição de parada"],
        "goal": "Repetir até acertar um objetivo.",
        "prompt": "Crie um jogo com um número secreto. O usuário deve tentar adivinhar até acertar. Ao final, mostre quantas tentativas foram necessárias.",
    },
    {
        "id": "Ex 20",
        "title": "Menu de caixa eletrônico simples",
        "level": "Desafiador",
        "loop_hint": "while/do-while",
        "skills": ["menu", "controle de fluxo", "saldo"],
        "goal": "Usar loop com menu e múltiplas ações.",
        "prompt": "Monte um menu com opções para ver saldo, depositar e sair. O sistema deve continuar executando até o usuário escolher sair.",
    },
    {
        "id": "Ex 21",
        "title": "[Desafiador] Notas com estatística",
        "level": "Desafiador",
        "loop_hint": "while/do-while",
        "skills": ["maior", "menor", "média", "validação"],
        "goal": "Integrar múltiplos cálculos em um único fluxo.",
        "prompt": "Peça notas de 0 a 10 até o usuário digitar -1. Ignore valores inválidos. Ao final, mostre quantidade de notas válidas, média, maior nota e menor nota.",
    },
    {
        "id": "Ex 22",
        "title": "[Desafiador] Simulação de votação",
        "level": "Desafiador",
        "loop_hint": "while/do-while",
        "skills": ["contadores", "menu", "votos inválidos"],
        "goal": "Contabilizar escolhas em repetição.",
        "prompt": "Crie um sistema de votação com 3 candidatos e opção 0 para encerrar. Ao final, mostre o total de votos por candidato, total geral e o vencedor.",
    },
    {
        "id": "Ex 23",
        "title": "[Desafiador] Caixa eletrônico avançado",
        "level": "Desafiador",
        "loop_hint": "while/do-while",
        "skills": ["menu", "extrato", "regras de negócio"],
        "goal": "Controlar saldo e operações com regras.",
        "prompt": "Crie um caixa eletrônico com opções: depositar, sacar, ver saldo, ver quantidade de operações e sair. Não permita saque maior que o saldo.",
    },
    {
        "id": "Ex 24",
        "title": "[Desafiador] Padrão crescente e decrescente",
        "level": "Desafiador",
        "loop_hint": "for",
        "skills": ["loop aninhado", "padrões"],
        "goal": "Trabalhar loops dentro de loops.",
        "prompt": "Peça um número N e imprima um padrão crescente de 1 até N. Depois, imprima o padrão decrescente correspondente.",
    },
    {
        "id": "Ex 25",
        "title": "[Desafiador] Jogo com dicas",
        "level": "Desafiador",
        "loop_hint": "while/do-while",
        "skills": ["feedback", "diferença", "tentativas"],
        "goal": "Dar respostas inteligentes a cada repetição.",
        "prompt": "Crie um jogo com número secreto de 1 a 100. A cada tentativa, informe se o número secreto é maior ou menor. Ao final, mostre a quantidade de tentativas. Como extra, avise se o palpite está 'perto' ou 'muito longe'.",
    },
]

# =========================
# ESTILO
# =========================
st.markdown(
    """
    <style>
    .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1350px;
    }
    .hero {
        border-radius: 24px;
        padding: 24px 28px;
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 45%, #0ea5e9 100%);
        color: white;
        margin-bottom: 1rem;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.18);
    }
    .hero h1 {
        margin: 0 0 6px 0;
        font-size: 2rem;
    }
    .hero p {
        margin: 0;
        opacity: 0.95;
        font-size: 1rem;
    }
    .metric-card {
        border: 1px solid rgba(15, 23, 42, 0.08);
        border-radius: 18px;
        padding: 16px 18px;
        background: white;
        box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
        margin-bottom: 10px;
    }
    .exercise-card {
        border-radius: 20px;
        padding: 20px 20px 18px 20px;
        border: 1px solid rgba(15, 23, 42, 0.10);
        box-shadow: 0 10px 22px rgba(15, 23, 42, 0.05);
        margin-bottom: 12px;
    }
    .exercise-title {
        font-weight: 800;
        font-size: 1.15rem;
        margin-bottom: 6px;
    }
    .exercise-chip {
        display: inline-block;
        padding: 4px 10px;
        margin-right: 6px;
        margin-bottom: 6px;
        border-radius: 999px;
        font-size: 0.82rem;
        background: rgba(255,255,255,0.65);
        border: 1px solid rgba(15,23,42,0.06);
    }
    .section-label {
        font-size: 0.86rem;
        text-transform: uppercase;
        letter-spacing: .06em;
        color: #475569;
        margin-bottom: 6px;
        font-weight: 700;
    }
    .small-note {
        font-size: 0.92rem;
        color: #475569;
    }
    .tip-box {
        background: #F8FAFC;
        border: 1px dashed #CBD5E1;
        border-radius: 16px;
        padding: 14px 16px;
    }
    .pill-desafiante {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        background: #4A148C;
        color: white;
        font-size: 0.78rem;
        font-weight: 700;
        margin-left: 8px;
        vertical-align: middle;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# =========================
# PERSISTÊNCIA
# =========================
def append_submission(row: dict):
    with FileLock(str(LOCK_PATH)):
        with open(JSONL_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

        df_new = pd.DataFrame([row])
        if CSV_PATH.exists():
            df_old = pd.read_csv(CSV_PATH)
            df = pd.concat([df_old, df_new], ignore_index=True)
        else:
            df = df_new
        df.to_csv(CSV_PATH, index=False)


def load_df() -> pd.DataFrame:
    if not CSV_PATH.exists():
        return pd.DataFrame(columns=[
            "timestamp", "student_names", "exercise_id", "exercise_title", "exercise_level",
            "loop_hint", "status", "difficulty", "needed_help", "comment", "java_code"
        ])
    return pd.read_csv(CSV_PATH)


# =========================
# AUTH PROFESSOR
# =========================
def teacher_is_enabled() -> bool:
    return bool(TEACHER_PASS)


def teacher_is_logged() -> bool:
    return st.session_state.get("teacher_ok", False) is True


def teacher_login_ui():
    st.sidebar.subheader("🔐 Professor")
    if not teacher_is_enabled():
        st.sidebar.info("Modo professor desativado.")
        return

    if "teacher_ok" not in st.session_state:
        st.session_state["teacher_ok"] = False

    if teacher_is_logged():
        st.sidebar.success("Logado ✅")
        if st.sidebar.button("Sair", use_container_width=True):
            st.session_state["teacher_ok"] = False
            st.rerun()
    else:
        pwd = st.sidebar.text_input("Senha", type="password", key="teacher_pwd_sidebar")
        if st.sidebar.button("Entrar", use_container_width=True):
            st.session_state["teacher_ok"] = (pwd == TEACHER_PASS)
            st.rerun()


# =========================
# HELPERS
# =========================
def get_exercise_by_option(option_text: str):
    for ex in EXS:
        label = format_ex_option(ex)
        if label == option_text:
            return ex
    return None


def format_ex_option(ex: dict) -> str:
    tag = " • DESAFIADOR" if ex["level"] == "Desafiador" else ""
    return f"{ex['id']} — {ex['title']} [{ex['level']}]" + tag


def render_exercise_card(ex: dict):
    bg, accent = LEVEL_COLORS.get(ex["level"], ("#F8FAFC", "#0F172A"))
    challenge = "<span class='pill-desafiante'>DESAFIADOR</span>" if ex["level"] == "Desafiador" else ""
    skills = " ".join([f"<span class='exercise-chip'>{s}</span>" for s in ex.get("skills", [])])
    loop_badge = LOOP_BADGE.get(ex.get("loop_hint", "livre"), LOOP_BADGE["livre"])

    st.markdown(
        f"""
        <div class="exercise-card" style="background:{bg}; border-left: 8px solid {accent};">
            <div class="exercise-title" style="color:{accent};">{ex['id']} — {ex['title']}{challenge}</div>
            <div style="margin-bottom:8px;">
                <span class="exercise-chip"><b>Nível:</b> {ex['level']}</span>
                <span class="exercise-chip"><b>Loop sugerido:</b> {loop_badge}</span>
            </div>
            <div class="section-label">Objetivo didático</div>
            <div style="margin-bottom:10px;">{ex.get('goal','')}</div>
            <div class="section-label">Enunciado</div>
            <div style="margin-bottom:12px;">{ex['prompt']}</div>
            <div class="section-label">Habilidades mobilizadas</div>
            <div>{skills}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def difficulty_score(value: str) -> int:
    mapping = {"Muito fácil": 1, "Fácil": 2, "Médio": 3, "Difícil": 4}
    return mapping.get(str(value), 0)


def status_score(value: str) -> int:
    mapping = {"✅ Consegui": 2, "🟡 Parcial": 1, "❌ Não consegui": 0}
    return mapping.get(str(value), 0)


def progress_counts(df: pd.DataFrame):
    total = len(df)
    ok = int((df["status"] == "✅ Consegui").sum()) if total else 0
    partial = int((df["status"] == "🟡 Parcial").sum()) if total else 0
    no = int((df["status"] == "❌ Não consegui").sum()) if total else 0
    return total, ok, partial, no


def build_summary_by_level(exercises: list[dict]) -> pd.DataFrame:
    rows = []
    for lvl in LEVEL_ORDER:
        qtd = len([e for e in exercises if e["level"] == lvl])
        rows.append({"Nível": lvl, "Quantidade": qtd})
    return pd.DataFrame(rows)


# =========================
# SIDEBAR
# =========================
teacher_login_ui()

st.sidebar.divider()
if teacher_is_logged():
    view = st.sidebar.radio("📌 Menu", ["Aluno", "Professor"], index=0)
else:
    view = "Aluno"
    st.sidebar.radio("📌 Menu", ["Aluno"], index=0, disabled=True)

st.sidebar.divider()
st.sidebar.markdown("### 🔁 Aula de Loops")
st.sidebar.caption("for, while e do-while em Java")

level_df = build_summary_by_level(EXS)
for _, row in level_df.iterrows():
    st.sidebar.caption(f"{row['Nível']}: {row['Quantidade']} exercícios")

# =========================
# MAIN
# =========================
st.markdown(
    """
    <div class="hero">
        <h1>🔁 Java — Laboratório de Loops</h1>
        <p>Prática progressiva para alunos iniciantes: do primeiro contato até desafios com aplicações reais.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.caption(
    ""
    ""
)

if view == "Aluno":
    top1, top2, top3, top4 = st.columns(4)
    top1.markdown("<div class='metric-card'><b>25 exercícios</b><br><span class='small-note'>com progressão gradual</span></div>", unsafe_allow_html=True)
    top2.markdown("<div class='metric-card'><b>5 níveis</b><br><span class='small-note'>do inicial ao desafiador</span></div>", unsafe_allow_html=True)
    top3.markdown("<div class='metric-card'><b>5 desafios</b><br><span class='small-note'>marcados explicitamente</span></div>", unsafe_allow_html=True)
    top4.markdown("<div class='metric-card'><b>Registro pedagógico</b><br><span class='small-note'>com comentários e código</span></div>", unsafe_allow_html=True)

    left, right = st.columns([1.05, 1.7], gap="large")

    with left:
        st.subheader("👤 Identificação e filtro")
        student_names = st.text_input(
            "Nome do aluno ou nomes da dupla",
            placeholder="Ex: Ana Silva ou Ana Silva e Bruno Souza",
            key="student_names",
        )

        level_filter = st.selectbox(
            "Filtrar por nível",
            ["(Todos)"] + LEVEL_ORDER,
            key="student_level_filter",
        )

        loop_filter = st.selectbox(
            "Filtrar por tipo de loop sugerido",
            ["(Todos)", "for", "while", "do-while", "for/while", "while/do-while", "livre"],
            key="student_loop_filter",
        )

        search = st.text_input("Buscar por palavra-chave", placeholder="Ex: senha, soma, menu, primo")

        ex_list = EXS.copy()
        if level_filter != "(Todos)":
            ex_list = [e for e in ex_list if e["level"] == level_filter]
        if loop_filter != "(Todos)":
            ex_list = [e for e in ex_list if e["loop_hint"] == loop_filter]
        if search.strip():
            term = search.strip().lower()
            ex_list = [
                e for e in ex_list
                if term in e["title"].lower() or term in e["prompt"].lower() or any(term in s.lower() for s in e.get("skills", []))
            ]

        if not ex_list:
            st.warning("Nenhum exercício encontrado com esse filtro.")
            st.stop()

        options = [format_ex_option(e) for e in ex_list]
        selected = st.selectbox("📌 Escolha o exercício", options, key="exercise_select")
        ex = get_exercise_by_option(selected)

        idx = EXS.index(ex) + 1
        st.progress(idx / len(EXS), text=f"Exercício {idx} de {len(EXS)} na trilha")

        st.markdown(
            """
            <div class="tip-box">
                <b>Dica para pensar antes de programar:</b><br>
                1. Onde o loop começa?<br>
                2. Quando ele para?<br>
                3. O que muda a cada repetição?
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.subheader("🧩 Detalhes do exercício")
        render_exercise_card(ex)

    tab1, tab2 = st.tabs(["✅ Registrar tentativa", "🗂️ Ver trilha completa"])

    with tab1:
        with st.form(key=f"form_{ex['id']}", clear_on_submit=True):
            c1, c2, c3 = st.columns(3)
            with c1:
                status = st.radio("Como foi sua tentativa?", STATUS_OPTS, key=f"status_{ex['id']}")
            with c2:
                difficulty = st.radio("Dificuldade percebida", DIF_OPTS, key=f"difficulty_{ex['id']}")
            with c3:
                needed_help = st.radio("Precisou de ajuda?", HELP_OPTS, key=f"help_{ex['id']}")

            comment = st.text_area(
                "Comentário sobre sua experiência",
                height=100,
                placeholder="Ex: consegui fazer a repetição, mas errei a condição / travei na média / entendi melhor o while...",
                key=f"comment_{ex['id']}",
            )

            java_code = st.text_area(
                "Cole aqui seu código Java (opcional)",
                height=240,
                placeholder="public class Main {\n    public static void main(String[] args) {\n        // seu código aqui\n    }\n}",
                key=f"code_{ex['id']}",
            )

            submitted = st.form_submit_button("💾 Salvar registro", use_container_width=True)

        if submitted:
            if not student_names.strip():
                st.warning("Preencha o campo de identificação antes de salvar.")
            else:
                row = {
                    "timestamp": datetime.now().isoformat(timespec="seconds"),
                    "student_names": student_names.strip(),
                    "exercise_id": ex["id"],
                    "exercise_title": ex["title"],
                    "exercise_level": ex["level"],
                    "loop_hint": ex["loop_hint"],
                    "status": status,
                    "difficulty": difficulty,
                    "needed_help": needed_help,
                    "comment": (comment or "").strip(),
                    "java_code": (java_code or "").strip(),
                }
                append_submission(row)
                st.success("Registro salvo com sucesso ✅")

    with tab2:
        st.subheader("📚 Trilha completa de exercícios")
        for lvl in LEVEL_ORDER:
            with st.expander(f"{lvl} — {len([e for e in EXS if e['level'] == lvl])} exercícios", expanded=(lvl == "Primeiro contato")):
                for e in [x for x in EXS if x["level"] == lvl]:
                    challenge = " <span class='pill-desafiante'>DESAFIADOR</span>" if e["level"] == "Desafiador" else ""
                    st.markdown(
                        f"<b>{e['id']} — {e['title']}</b>{challenge}<br><span class='small-note'>{e['prompt']}</span>",
                        unsafe_allow_html=True,
                    )
                    st.markdown("---")

elif view == "Professor":
    st.subheader("📊 Painel do Professor")
    df = load_df()

    st.markdown("### 🧨 Administração")
    with st.expander("Limpar respostas (apagar tudo)"):
        st.warning("Isso apaga TODOS os registros salvos. Não é possível desfazer.")
        confirm = st.checkbox("Confirmo que quero apagar todos os registros", key="confirm_delete_all")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🗑️ Limpar respostas agora", use_container_width=True, disabled=not confirm):
                try:
                    if CSV_PATH.exists():
                        CSV_PATH.unlink()
                    if JSONL_PATH.exists():
                        JSONL_PATH.unlink()
                    if LOCK_PATH.exists():
                        LOCK_PATH.unlink()
                    st.success("Respostas apagadas com sucesso ✅")
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao apagar arquivos: {e}")
        with col2:
            st.caption("Use no encerramento da aula ou antes de uma nova turma.")

    if df.empty:
        st.warning("Ainda não há registros salvos.")
    else:
        f1, f2, f3, f4, f5 = st.columns(5)
        with f1:
            ex_sel = st.selectbox("Filtrar por exercício", ["(Todos)"] + [e["id"] for e in EXS], key="prof_ex_filter")
        with f2:
            level_sel = st.selectbox("Filtrar por nível", ["(Todos)"] + LEVEL_ORDER, key="prof_level_filter")
        with f3:
            status_sel = st.selectbox("Filtrar por status", ["(Todos)"] + STATUS_OPTS, key="prof_status_filter")
        with f4:
            loop_sel = st.selectbox("Filtrar por loop", ["(Todos)", "for", "while", "do-while", "for/while", "while/do-while", "livre"], key="prof_loop_filter")
        with f5:
            last_n = st.slider("Mostrar últimos N", 20, 5000, 300, key="prof_last_n")

        dff = df.copy()
        if ex_sel != "(Todos)":
            dff = dff[dff["exercise_id"].astype(str) == ex_sel]
        if level_sel != "(Todos)":
            dff = dff[dff["exercise_level"].astype(str) == level_sel]
        if status_sel != "(Todos)":
            dff = dff[dff["status"].astype(str) == status_sel]
        if loop_sel != "(Todos)":
            dff = dff[dff["loop_hint"].astype(str) == loop_sel]
        if "timestamp" in dff.columns:
            dff = dff.sort_values("timestamp", ascending=False)

        total, ok, partial, no = progress_counts(dff)
        help_yes = int((dff["needed_help"] == "Sim").sum()) if total else 0
        avg_dif = dff["difficulty"].apply(difficulty_score).mean() if total else 0

        k1, k2, k3, k4, k5 = st.columns(5)
        k1.metric("Registros", total)
        k2.metric("✅ Consegui", ok)
        k3.metric("🟡 Parcial", partial)
        k4.metric("❌ Não consegui", no)
        k5.metric("Média de dificuldade", f"{avg_dif:.2f}")

        st.markdown("#### 📈 Distribuições")
        g1, g2, g3 = st.columns(3)
        with g1:
            st.caption("Status")
            st.bar_chart(dff["status"].value_counts().reindex(STATUS_OPTS).fillna(0))
        with g2:
            st.caption("Dificuldade percebida")
            st.bar_chart(dff["difficulty"].value_counts().reindex(DIF_OPTS).fillna(0))
        with g3:
            st.caption("Precisou de ajuda?")
            st.bar_chart(dff["needed_help"].value_counts().reindex(HELP_OPTS).fillna(0))

        st.markdown("#### 🧩 Resumo por exercício")
        resumo = (
            dff.groupby(["exercise_id", "exercise_title", "exercise_level", "loop_hint"], dropna=False)
            .agg(
                registros=("exercise_id", "count"),
                consegui=("status", lambda s: (s == "✅ Consegui").sum()),
                parcial=("status", lambda s: (s == "🟡 Parcial").sum()),
                nao_consegui=("status", lambda s: (s == "❌ Não consegui").sum()),
                com_ajuda=("needed_help", lambda s: (s == "Sim").sum()),
            )
            .reset_index()
        )
        resumo["% consegui"] = ((resumo["consegui"] / resumo["registros"]) * 100).round(1)
        resumo["% com ajuda"] = ((resumo["com_ajuda"] / resumo["registros"]) * 100).round(1)

        st.dataframe(
            resumo.sort_values(["exercise_id"]),
            use_container_width=True,
            hide_index=True,
        )

        st.markdown("#### 🔥 Ranking dos exercícios mais difíceis")
        ranking = dff.copy()
        ranking["difficulty_points"] = ranking["difficulty"].apply(difficulty_score)
        ranking["status_points"] = ranking["status"].apply(status_score)
        ranking_df = (
            ranking.groupby(["exercise_id", "exercise_title", "exercise_level"], dropna=False)
            .agg(
                registros=("exercise_id", "count"),
                media_dificuldade=("difficulty_points", "mean"),
                desempenho_medio=("status_points", "mean"),
            )
            .reset_index()
        )
        ranking_df["media_dificuldade"] = ranking_df["media_dificuldade"].round(2)
        ranking_df["desempenho_medio"] = ranking_df["desempenho_medio"].round(2)
        ranking_df = ranking_df.sort_values(["media_dificuldade", "registros"], ascending=[False, False])

        st.dataframe(ranking_df, use_container_width=True, hide_index=True)

        st.markdown("#### 🧱 Gargalos por nível")
        by_level = (
            dff.groupby("exercise_level", dropna=False)
            .agg(
                registros=("exercise_id", "count"),
                dificuldade_media=("difficulty", lambda s: pd.Series(s).apply(difficulty_score).mean()),
                ajuda=("needed_help", lambda s: (s == "Sim").mean() * 100),
            )
            .reset_index()
        )
        by_level["dificuldade_media"] = by_level["dificuldade_media"].round(2)
        by_level["ajuda"] = by_level["ajuda"].round(1)
        st.dataframe(by_level, use_container_width=True, hide_index=True)

        st.markdown("#### 💬 Comentários dos alunos")
        comments_df = dff.copy()
        comments_df["comment"] = comments_df["comment"].fillna("").astype(str).str.strip()
        comments_df = comments_df[comments_df["comment"] != ""]
        if comments_df.empty:
            st.info("Ainda não há comentários registrados.")
        else:
            st.dataframe(
                comments_df[[
                    "timestamp", "student_names", "exercise_id",
                    "exercise_title", "exercise_level", "difficulty", "needed_help", "comment"
                ]].head(last_n),
                use_container_width=True,
                hide_index=True,
            )

        st.markdown("#### 💻 Códigos enviados")
        code_df = dff.copy()
        code_df["java_code"] = code_df["java_code"].fillna("").astype(str).str.strip()
        code_df = code_df[code_df["java_code"] != ""]
        if code_df.empty:
            st.info("Ainda não há códigos Java enviados.")
        else:
            code_labels = code_df.apply(
                lambda row: f"{row['timestamp']} | {row['student_names']} | {row['exercise_id']} — {row['exercise_title']}",
                axis=1,
            ).tolist()
            code_view = st.selectbox("Selecione um envio para visualizar o código", code_labels, key="selected_code_view")
            selected_row = code_df.iloc[code_labels.index(code_view)]
            st.code(selected_row["java_code"], language="java")

        st.markdown("#### 🧾 Registros")
        st.dataframe(dff.head(last_n), use_container_width=True, hide_index=True)

        st.markdown("#### ⬇️ Download")
        st.download_button(
            "Baixar CSV filtrado",
            data=dff.to_csv(index=False).encode("utf-8"),
            file_name="feedback_java_loops_filtrado.csv",
            mime="text/csv",
            use_container_width=True,
        )
        if CSV_PATH.exists():
            st.download_button(
                "Baixar CSV completo",
                data=CSV_PATH.read_bytes(),
                file_name="feedback_java_loops_completo.csv",
                mime="text/csv",
                use_container_width=True,
            )
