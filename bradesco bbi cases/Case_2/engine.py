import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from prompts import MACRO_SCENARIO_PROMPT

load_dotenv() #executa a leitura do .env

#essa função configura a conexão com a API do Groq
def config_groq(): 
    api_key = os.getenv("GROQ_API_KEY")  #lê pega a chave da API do arquivo .env
    if not api_key: #se a chave não for encontrada, mostra mensagem de erro amigavel
        raise ValueError("GROQ_API_KEY não encontrado no arquivo .env")
    
    return Groq(api_key=api_key) #retorna o cliente com a chave configurada

def chamar_groq(model, cenario: str) -> dict: #essa função chama a API do Groq para processar o cenário e retornar os dados
    prompt = MACRO_SCENARIO_PROMPT.format(cenario=cenario)  #formata o prompt com o cenário recebido
    response = model.chat.completions.create( #chama a API 
        model="llama-3.3-70b-versatile", #modelo recente e gratuito do Groq
        #passa o prompt para a API, com instrução para retornar apenas JSON
        messages=[{"role": "system", "content": "retorne apenas json válido, sem texto extra"}, {"role": "user", "content": prompt}], 
        temperature=0.3 #temperature baixo para respostas mais consistentes
    )
    texto = response.choices[0].message.content.strip() #extrai o texto da resposta da API e remove espaços desnecessarios
    texto = re.sub(r'```json\s*', '', texto) #remove eventuais blocos de código, mantendo JSON limpo
    texto = re.sub(r'\s*```', '', texto) #remove o fechamento do bloco de código 
    dados = json.loads(texto) #converte o texto JSON em um dicionário Python
    return dados #retorna o dicioário com os dados processados pela API

def gerar_markdown(dados: dict) -> str: #essa função gera o markdown formatado
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #formata a data e hora atual para incluir no markdown

    mkdn = f"Macro scenario engine ..." #título do markdown
    mkdn += f"gerado em {agora}\n\n" #data e hora da geração do markdown
    mkdn += f"Cenario analisado\n {dados['cenario_recebido']}\n\n" #exibe o cenário que foi analisado, para contextualizar
 
    mkdn += "Setores Beneficiados\n" #título da seção de setores beneficiados
    for s in dados['setores_beneficiados']: #percorre a lista de setores beneficiados e adiciona cada um ao markdown
        mkdn += f"- **{s['setor']}**: {s['rationale']}\n" 

    mkdn += "\nSetores Prejudicados\n"
    for s in dados['setores_prejudicados']: #percorre a lista de setores prejudicados e adiciona cada um ao markdown
        mkdn += f"- **{s['setor']}**: {s['rationale']}\n"
    
    mkdn += "\nTickers Positivos\n"
    for t in dados['tickers_positivos']: #percorre cada ticker positivo com ticker, nome da empresa e justificativa
        mkdn += f"- **{t['ticker']} ({t['empresa']})**: {t['justificativa']}\n"

    mkdn += "\nTickers Negativos\n"
    for t in dados['tickers_negativos']: #percorre cada ticker negativo com ticker, nome da empresa e justificativa
        mkdn += f"- **{t['ticker']} ({t['empresa']})**: {t['justificativa']}\n"

    mkdn += "\n3 Maiores riscos\n"
    for i, r in enumerate(dados['riscos_da_tese'], 1): #percorre os riscos da tese, numerando cada um
        mkdn += f"{i}. {r['risco']}\n"

    return mkdn #retorna o markdown formatado como string

def salvar_output(dados, markdown, cenario): #essa função salva o resultado em arquivos JSON e Markdown
    os.makedirs("outputs", exist_ok=True) #cria a pasta outputs se ela não existir, para organizar os arquivos gerados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") #gera um timestamp para incluir no nome dos arquivos

    json_path = f"outputs/resultado_{timestamp}.json" #define o caminhoi do JSON com o timestamp no nome
    with open(json_path, "w", encoding="utf-8") as f: #abre o arquivo para escrita
        json.dump({"cenario_input": cenario, "dados": dados}, f, ensure_ascii=False, indent=2) #garante que vai ser salvo fomatado e com acentos

    mkdn_path = f"outputs/resultado_{timestamp}.md" #define o caminho do Markdown com o timestamp no nome
    with open(mkdn_path, "w", encoding="utf-8") as f: #abre o arquivo para escrita
        f.write(markdown)

    return json_path, mkdn_path #retorna os caminhos dos arquivos salvos

def analisar(cenario:str): #essa função é a principal do processo da análise, chamando as outras funções
    print("Config a IA...")
    client = config_groq()
    print("Chamando a IA...")
    dados = chamar_groq(client, cenario)
    print("Gerando markdown...")
    markdown = gerar_markdown(dados)
    print("Salvando output...")
    json_path, mkdn_path = salvar_output(dados, markdown, cenario) #salva o JSOn e o markdown e recebe os arquivos

    return dados, markdown, json_path, mkdn_path #returna tudo para o main.py para exibir ao usuário