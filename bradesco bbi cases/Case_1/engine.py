import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
from groq import Groq
from prompts import EARNINGS_CALL_PROMPT

load_dotenv() #executa a leitura do .env

def config_groq(): #essa função configura a conexão com a API do Groq
    api_key = os.getenv("GROQ_API_KEY") #lê e pega a chave da API do arquivo .env
    if not api_key: #se a chave não for encontrada, mostra mensagem de erro amigavel
        raise ValueError("GROQ_API_KEY não encontrada no arquivo .env")
    return Groq(api_key=api_key) #retorna o cliente com a chave configurada

def ler_transcricao(caminho: str) -> str: #essa função lê o arquivo de transcrição
    if not os.path.exists(caminho): #verifica se o arquivo existe antes de tentar abrir
        raise FileNotFoundError(f"Arquivo não encontrado: {caminho}")
    with open(caminho, "r", encoding="utf-8") as f: #abre o arquivo com suporte a acentos
        return f.read() #retorna o conteúdo completo do arquivo

def chamar_groq(client, transcricao: str) -> dict: #essa função chama a API do Groq para processar a transcrição e retornar os dados
    prompt = EARNINGS_CALL_PROMPT.format(transcricao=transcricao) #formata o prompt com a transcrição recebida
    response = client.chat.completions.create( #chama a API
        model="llama-3.3-70b-versatile", #modelo recente e gratuito do Groq
        messages=[{"role": "system", "content": "retorne apenas json válido, sem texto extra"}, {"role": "user", "content": prompt}], #passa o prompt para a API com instrução para retornar apenas JSON
        temperature=0.2 #temperature baixo para respostas mais consistentes e precisas
    )
    texto = response.choices[0].message.content.strip() #extrai o texto da resposta da API e remove espaços desnecessários
    texto = re.sub(r'```json\s*', '', texto) #remove eventuais blocos de código, mantendo JSON limpo
    texto = re.sub(r'\s*```', '', texto) #remove o fechamento do bloco de código
    texto = re.sub(r'\s*```', '', texto)
    print("Resposta da ia:", texto[:500]) # mostra os primeiros 500 caracteres
    dados = json.loads(texto) #converte o texto JSON em um dicionário Python
    print("Chaves retornadas:", list(dados.keys()))#linha temporária para debug
    return dados #retorna o dicionário com os dados processados pela API

def gerar_markdown(dados: dict) -> str: #essa função gera o markdown formatado
    agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S") #formata a data e hora atual

    mkdn = f"# Earnings Call Intelligence Tracker\n" #título do markdown
    mkdn += f"**Empresa:** {dados['empresa']} | **Trimestre:** {dados['trimestre']}\n" #nome da empresa e trimestre
    mkdn += f"Gerado em: {agora}\n\n" #data e hora da geração
    mkdn += "---\n\n"

    mkdn += "## Tom Geral do Management\n" #título da seção de tom geral
    mkdn += f"Classificação: {dados['tom_geral']['classificacao'].upper()}\n\n" #classificação em maiúsculas
    mkdn += f"{dados['tom_geral']['justificativa']}\n\n" #justificativa do tom
    mkdn += "Trechos que justificam:\n"
    for t in dados['tom_geral']['trechos']: #percorre os trechos literais da transcrição
        mkdn += f"> {t}\n\n"

    mkdn += "## Mudanças de Guidance\n" #título da seção de guidance
    for g in dados['guidance']['mudancas']: #percorre cada mudança de guidance
        direcao = f"({g['direcao']})" #direção entre parênteses, sem emoji
        mkdn += f"- **{g['tema']}** {direcao}: {g['detalhe']}\n"
    mkdn += f"\nTemas principais: {', '.join(dados['guidance']['temas_principais'])}\n\n"

    mkdn += "## Top 3 Perguntas dos Analistas\n" #título da seção de perguntas
    for i, p in enumerate(dados['perguntas_analisas'], 1): #percorre as 3 perguntas numerando cada uma
        mkdn += f"**{i}. {p['analista']}**\n"
        mkdn += f"- Pergunta: {p['pergunta']}\n"
        mkdn += f"- Resposta: {p['resposta_resumo']}\n"
        mkdn += f"- Qualidade da resposta: {p['qualidade_resposta']}\n\n"

    mkdn += "## Red Flags Linguisticos\n" #título da seção de red flags
    for r in dados['red_flags']: #percorre cada red flag identificado
        mkdn += f"- **{r['tipo'].upper()}**\n"
        mkdn += f"  \"{r['trecho_literal']}\"\n"
        mkdn += f"  {r['interpretacao']}\n\n"

    mkdn += "## Surprise Score\n" #título da seção de surprise score
    mkdn += f"Score: {dados['surprise_score']['score']}/10\n\n" #score de 0 a 10
    for s in dados['surprise_score']['surpresas']: #percorre cada surpresa identificada
        mkdn += f"- **{s['item']}**: {s['justificativa']}\n"

    return mkdn #retorna o markdown formatado como string

def salvar_output(dados, markdown, caminho_transcricao): #essa função salva o resultado em arquivos JSON e Markdown
    os.makedirs("outputs", exist_ok=True) #cria a pasta outputs se ela não existir
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") #gera um timestamp para incluir no nome dos arquivos

    json_path = f"outputs/resultado_{timestamp}.json" #define o caminho do JSON com o timestamp no nome
    with open(json_path, "w", encoding="utf-8") as f: #abre o arquivo para escrita
        json.dump({"transcricao_input": caminho_transcricao, "analise": dados}, f, ensure_ascii=False, indent=2) #salva formatado e com acentos

    mkdn_path = f"outputs/resultado_{timestamp}.md" #define o caminho do Markdown com o timestamp no nome
    with open(mkdn_path, "w", encoding="utf-8") as f: #abre o arquivo para escrita
        f.write(markdown)

    return json_path, mkdn_path #retorna os caminhos dos arquivos salvos

def analisar(caminho_transcricao: str): #essa função é a principal do processo, chamando as outras funções
    print("Config a IA...")
    client = config_groq()
    print("Lendo transcrição...")
    transcricao = ler_transcricao(caminho_transcricao) #lê o arquivo de transcrição do disco
    print("Chamando a IA...")
    dados = chamar_groq(client, transcricao)
    print("Gerando markdown...")
    markdown = gerar_markdown(dados)
    print("Salvando output...")
    json_path, mkdn_path = salvar_output(dados, markdown, caminho_transcricao) #salva o JSON e o markdown

    return dados, markdown, json_path, mkdn_path #retorna tudo para o main.py exibir ao usuário