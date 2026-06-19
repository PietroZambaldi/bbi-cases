from engine import analisar

def main():
    print("Earnings Call Intelligence Tracker")
    print("\nDigite o caminho para o arquivo de transcrição.")
    print("\nCaminho do arquivo:")

    caminho = input(">> ").strip()

    if not caminho:
        print("Caminho não pode ser vazio.")
        return

    print("\nAnalisando transcrição...\n")
    dados, markdown, json_path, mkdn_path = analisar(caminho)

    print("\nAnalise concluida!")
    print(f"JSON salvo em: {json_path}")
    print(f"Relatorio salvo em: {mkdn_path}")
    print("\nPrevia do relatorio\n")
    print(markdown)

if __name__ == "__main__":
    main()