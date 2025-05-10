import streamlit as st
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="Winstbelastingtool Spanje IRPF 2025 – Gratis belasting calculator",
    page_icon="💰",
    layout="centered",
    initial_sidebar_state="auto",
)

st.markdown("""
<meta name="description" content="Bereken gratis hoeveel belasting (IRPF) je betaalt bij verkoop van een woning in Spanje. Meertalig: Nederlands, Engels, Spaans en Valencià.">
""", unsafe_allow_html=True)


# 🔤 Taalkeuze
language = st.selectbox("🌐 Kies een taal / Choose language / Elige idioma / Tria idioma", ["Nederlands", "English", "Español", "Valencià"])

# 🗨️ Teksten per taal
texts = {
    "Nederlands": {
        "title": "🏠 Winstbelastingtool woningverkoop (IRPF Spanje)",
        "intro": "Bereken hoeveel belasting je betaalt over de verkoopwinst van een woning als Spaans resident.",
        "aankoop": "Aankoopprijs woning (€)",
        "verkoop": "Verkoopprijs woning (€)",
        "kosten": "Aftrekbare kosten (€)",
        "eigenaren": "Aantal eigenaren",
        "bereken": "Bereken belasting",
        "resultaten": "📊 Resultaten",
        "totale_winst": "Totale winst",
        "aftrekbare_kosten": "Aftrekbare kosten",
        "belastbare_winst": "Belastbare winst",
        "per_persoon": "Belastbare winst per persoon",
        "totaal_te_betalen": "💰 Totale belasting te betalen",
        "per_persoon_belasting": "📄 Dat is ongeveer €{:.2f} per persoon bij {} eigenaren.",
        "grafiek_titel": "Belasting per persoon per schijf (IRPF Spanje 2025)",
        "grafiek_x": "Belastingtarief + Bedrag",
        "grafiek_y": "Te betalen belasting (€)"
    },
    "English": {
        "title": "🏠 Capital Gains Tax Tool (Spain IRPF)",
        "intro": "Calculate how much tax you pay on your property sale profit as a Spanish resident.",
        "aankoop": "Purchase price (€)",
        "verkoop": "Selling price (€)",
        "kosten": "Deductible costs (€)",
        "eigenaren": "Number of owners",
        "bereken": "Calculate tax",
        "resultaten": "📊 Results",
        "totale_winst": "Total profit",
        "aftrekbare_kosten": "Deductible costs",
        "belastbare_winst": "Taxable profit",
        "per_persoon": "Taxable profit per person",
        "totaal_te_betalen": "💰 Total tax payable",
        "per_persoon_belasting": "📄 That’s approximately €{:.2f} per person with {} owners.",
        "grafiek_titel": "Tax per person per bracket (Spain IRPF 2025)",
        "grafiek_x": "Tax rate + Amount",
        "grafiek_y": "Tax to be paid (€)"
    },
    "Español": {
        "title": "🏠 Calculadora de Ganancia Patrimonial (IRPF España)",
        "intro": "Calcula cuánto impuesto pagas por la venta de una vivienda como residente fiscal en España.",
        "aankoop": "Precio de compra (€)",
        "verkoop": "Precio de venta (€)",
        "kosten": "Costes deducibles (€)",
        "eigenaren": "Número de propietarios",
        "bereken": "Calcular impuesto",
        "resultaten": "📊 Resultados",
        "totale_winst": "Ganancia total",
        "aftrekbare_kosten": "Costes deducibles",
        "belastbare_winst": "Ganancia sujeta a impuestos",
        "per_persoon": "Ganancia imponible por persona",
        "totaal_te_betalen": "💰 Impuesto total a pagar",
        "per_persoon_belasting": "📄 Eso equivale a unos €{:.2f} por persona ({} propietarios).",
        "grafiek_titel": "Impuesto por persona por tramo (IRPF España 2025)",
        "grafiek_x": "Tramo + Importe",
        "grafiek_y": "Impuesto a pagar (€)"
    },
    "Valencià": {
        "title": "🏠 Eina d'impost sobre guanys immobiliaris (IRPF Espanya)",
        "intro": "Calcula quant impost pagaràs per la venda d'un habitatge com a resident fiscal a Espanya.",
        "aankoop": "Preu de compra (€)",
        "verkoop": "Preu de venda (€)",
        "kosten": "Despeses deduïbles (€)",
        "eigenaren": "Nombre de propietaris",
        "bereken": "Calcula l'impost",
        "resultaten": "📊 Resultats",
        "totale_winst": "Guany total",
        "aftrekbare_kosten": "Despeses deduïbles",
        "belastbare_winst": "Guany subjecte a impostos",
        "per_persoon": "Guany imposable per persona",
        "totaal_te_betalen": "💰 Impost total a pagar",
        "per_persoon_belasting": "📄 Això és aproximadament €{:.2f} per persona ({} propietaris).",
        "grafiek_titel": "Impost per persona segons tram (IRPF Espanya 2025)",
        "grafiek_x": "Tram + Import",
        "grafiek_y": "Impost a pagar (€)"
    }

}

T = texts[language]

def show_tax_graph_with_labels(winst_pp):
    brackets = [
        {"max": 6000, "rate": 0.19},
        {"max": 50000, "rate": 0.21},
        {"max": 200000, "rate": 0.23},
        {"max": 300000, "rate": 0.27},
        {"max": float("inf"), "rate": 0.30},
    ]

    total_tax = 0
    last_limit = 0
    labels = []
    taxes = []

    for bracket in brackets:
        if winst_pp <= last_limit:
            break
        upper = bracket["max"]
        rate = bracket["rate"]
        taxable = min(winst_pp, upper) - last_limit
        if taxable > 0:
            tax_segment = taxable * rate
            total_tax += tax_segment
            labels.append(f"{int(rate*100)}%\n€{tax_segment:,.0f}")
            taxes.append(tax_segment)
        last_limit = upper

    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.bar(labels, taxes, color='skyblue')
    ax.set_title(T["grafiek_titel"])
    ax.set_xlabel(T["grafiek_x"])
    ax.set_ylabel(T["grafiek_y"])
    ax.grid(axis='y')

    for bar, tax in zip(bars, taxes):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(taxes)*0.01,
                f"€{tax:,.0f}", ha='center', va='bottom', fontsize=10, fontweight='bold')
    st.pyplot(fig)
    return total_tax

# Streamlit interface
# 💅 Stijl en layout verbeteren
st.markdown("""
    <style>
    .main {
        background-color: #f9f9f9;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
        max-width: 800px;
        margin: auto;
    }
    .block-container {
        padding-top: 2rem;
    }
    h1, h2, h3, h4 {
        color: #003366;
    }
    .stButton>button {
        background-color: #0072c6;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title(T["title"])
st.write(T["intro"])

aankoopprijs = st.number_input(T["aankoop"], min_value=0.0, step=1000.0)
verkoopprijs = st.number_input(T["verkoop"], min_value=0.0, step=1000.0)
aftrekbare_kosten = st.number_input(T["kosten"], min_value=0.0, step=500.0)
deelgenoten = st.number_input(T["eigenaren"], min_value=1, step=1)

if st.button(T["bereken"]):
    totale_winst = verkoopprijs - aankoopprijs
    belastbare_winst = max(totale_winst - aftrekbare_kosten, 0)
    winst_pp = belastbare_winst / deelgenoten

    st.subheader(T["resultaten"])
    st.write(f"**{T['totale_winst']}:** €{totale_winst:,.2f}")
    st.write(f"**{T['aftrekbare_kosten']}:** €{aftrekbare_kosten:,.2f}")
    st.write(f"**{T['belastbare_winst']}:** €{belastbare_winst:,.2f}")
    st.write(f"**{T['per_persoon']} ({deelgenoten}):** €{winst_pp:,.2f}")

    belasting_pp = show_tax_graph_with_labels(winst_pp)
    totaal_belasting = belasting_pp * deelgenoten

    st.success(f"{T['totaal_te_betalen']}: €{totaal_belasting:,.2f}")
    st.info(T["per_persoon_belasting"].format(belasting_pp, deelgenoten))

# ℹ️ Juridische disclaimer onderaan
disclaimers = {
    "Nederlands": "© 2025 Winstbelasting Tool. Alle rechten voorbehouden. Deze tool is informatief en geen fiscaal advies. Raadpleeg altijd een lokale belastingadviseur.",
    "English": "© 2025 Capital Gains Tax Tool. All rights reserved. This tool is for informational purposes only and does not constitute tax advice. Always consult a local tax advisor.",
    "Español": "© 2025 Herramienta de Ganancia Patrimonial. Todos los derechos reservados. Esta herramienta es solo informativa y no constituye asesoramiento fiscal. Consulta siempre a un asesor fiscal local.",
    "Valencià": "© 2025 Eina d'impost sobre guanys. Tots els drets reservats. Aquesta eina és informativa i no substitueix l'assessorament fiscal. Consulta sempre un assessor fiscal local."
}

st.markdown("---")
st.markdown(f"📝 {disclaimers[language]}")
