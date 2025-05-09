import streamlit as st
import matplotlib.pyplot as plt

def show_tax_graph_with_labels(belastbare_winst_per_persoon):
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
        if belastbare_winst_per_persoon <= last_limit:
            break

        upper = bracket["max"]
        rate = bracket["rate"]
        taxable = min(belastbare_winst_per_persoon, upper) - last_limit

        if taxable > 0:
            tax_segment = taxable * rate
            total_tax += tax_segment
            labels.append(f"{int(rate*100)}%\n€{tax_segment:,.0f}")
            taxes.append(tax_segment)

        last_limit = upper

    # Grafiek maken
    fig, ax = plt.subplots(figsize=(10, 7))
    bars = ax.bar(labels, taxes, color='skyblue')
    ax.set_title("Belasting per persoon per schijf (IRPF Spanje 2025)")
    ax.set_xlabel("Belastingtarief + Bedrag")
    ax.set_ylabel("Te betalen belasting (€)")
    ax.grid(axis='y')

    for bar, tax in zip(bars, taxes):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(taxes)*0.01,
                f"€{tax:,.0f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

    st.pyplot(fig)
    return total_tax

# Streamlit UI
st.title("🏠 Winstbelastingtool woningverkoop (IRPF Spanje)")
st.write("Bereken hoeveel belasting je betaalt over de verkoopwinst van een woning als Spaans resident.")

aankoopprijs = st.number_input("Aankoopprijs woning (€)", min_value=0.0, step=1000.0)
verkoopprijs = st.number_input("Verkoopprijs woning (€)", min_value=0.0, step=1000.0)
aftrekbare_kosten = st.number_input("Aftrekbare kosten (€)", min_value=0.0, step=500.0)
deelgenoten = st.number_input("Aantal eigenaren", min_value=1, step=1)

if st.button("Bereken belasting"):
    totale_winst = verkoopprijs - aankoopprijs
    belastbare_winst = max(totale_winst - aftrekbare_kosten, 0)
    winst_per_persoon = belastbare_winst / deelgenoten

    st.subheader("📊 Resultaten")
    st.write(f"**Totale winst:** €{totale_winst:,.2f}")
    st.write(f"**Aftrekbare kosten:** €{aftrekbare_kosten:,.2f}")
    st.write(f"**Belastbare winst:** €{belastbare_winst:,.2f}")
    st.write(f"**Belastbare winst per persoon ({deelgenoten}):** €{winst_per_persoon:,.2f}")

    belasting_per_persoon = show_tax_graph_with_labels(winst_per_persoon)
    totale_belasting = belasting_per_persoon * deelgenoten

    st.success(f"💰 Totale belasting te betalen: €{totale_belasting:,.2f}")
