
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

    # Grafiek
    plt.figure(figsize=(10, 7))
    bars = plt.bar(labels, taxes, color='skyblue')
    plt.title("Belasting per persoon per schijf (IRPF Spanje 2025)")
    plt.xlabel("Belastingtarief + Bedrag")
    plt.ylabel("Te betalen belasting (€)")
    plt.grid(axis='y')

    for bar, tax in zip(bars, taxes):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(taxes)*0.01,
                 f"€{tax:,.0f}", ha='center', va='bottom', fontsize=10, fontweight='bold')

    # Totale belasting onder grafiek tonen
    plt.figtext(0.5, 0.01, f"Totale belasting per persoon: €{total_tax:,.2f}",
                ha="center", fontsize=12, fontweight='bold', color='darkgreen')

    plt.tight_layout(rect=[0, 0.03, 1, 1])  # ruimte onderaan maken voor figtext

    print(f"Totale belasting per persoon: €{total_tax:,.2f}")

    plt.show()

    return total_tax

def run_tax_prompt():
    try:
        aankoopprijs = float(input("Wat was de aankoopprijs van de woning (€)? "))
        verkoopprijs = float(input("Wat is de verkoopprijs van de woning (€)? "))
        aftrekbare_kosten = float(input("Wat is het totaalbedrag aan aftrekbare kosten (€)? "))
        deelgenoten = int(input("Met hoeveel personen deel je de woning? "))

        totale_winst = verkoopprijs - aankoopprijs
        belastbare_winst = totale_winst - aftrekbare_kosten

        if belastbare_winst <= 0:
            print("\nEr is geen belastbare winst. Geen belasting verschuldigd.")
            return

        winst_per_persoon = belastbare_winst / deelgenoten

        print(f"\nTotale winst: €{totale_winst:,.2f}")
        print(f"Aftrekbare kosten: €{aftrekbare_kosten:,.2f}")
        print(f"→ Totale belastbare winst: €{belastbare_winst:,.2f}")
        print(f"→ Belastbare winst per persoon ({deelgenoten}): €{winst_per_persoon:,.2f}\n")

        belasting_per_persoon = show_tax_graph_with_labels(winst_per_persoon)

        print(f"\nTotaal te betalen belasting voor {deelgenoten} personen: €{belasting_per_persoon * deelgenoten:,.2f}")

    except ValueError:
        print("❌ Ongeldige invoer. Gebruik alleen getallen.")

# Start het script
run_tax_prompt()
