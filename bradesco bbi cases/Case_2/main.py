from engine import analisar

def main():
    print("Macro scenario engine")
    print("-" * 30)
    print("\n")
    print("Descreva o cenário macroeconômico que deseja analisar.")
    print("Exemplo: 'O governo anunciou um pacote fiscal deo R$100 milhões para estimular o crédito.'")
    print("se valoriza contra o real, commodities caem, etc")
    print("\nDigite seu cenário:")

    cenario = input("Seu cenário: ").strip()

    if not cenario:
        print("Cenário não pode ser vazio")
        return
    
    print("\nAnalisando cenário...\n")
    dados, markdown, json_path, mkdn_path = analisar(cenario)

    print("Análise concluída!")
    print(f"JSON salvo em: {json_path}")
    print(f"Relatório salvo em: {mkdn_path}")
    print("\n Prévia do relatório:\n")
    print(markdown)


if __name__ == "__main__":
    main()