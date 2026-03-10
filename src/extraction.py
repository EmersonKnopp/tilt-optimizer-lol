import requests
import pandas as pd
import time
import os

# =================================================================
# CONFIGURAÇÕES DE ACESSO (Use Variáveis de Ambiente para Segurança)
# =================================================================
# No GitHub, você configurará isso em Settings > Secrets
API_KEY = os.getenv("RIOT_API_KEY", "SUA_CHAVE_AQUI_PARA_TESTE_LOCAL")
REGION = "americas"   # Para histórico de partidas (Match-V5)
SUB_REGION = "br1"    # Servidor Brasileiro
SUMMONER_NAME = "NomeDoInvocador"
TAG_LINE = "BR1"

headers = {"X-Riot-Token": API_KEY}

def get_puuid(name, tag):
    """Obtém o identificador único do jogador (PUUID)"""
    url = f"https://{REGION}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Erro ao buscar PUUID: {response.status_code}")
        return None
    return response.json()['puuid']

def get_match_ids(puuid, count=20):
    """Busca os IDs das últimas partidas jogadas"""
    url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}"
    response = requests.get(url, headers=headers)
    return response.json()

def analyze_matches(match_ids, my_puuid):
    """Extrai métricas de Micro-Eficiência e possíveis sinais de 'Tilt'"""
    data_list = []
    
    for match_id in match_ids:
        url = f"https://{REGION}.api.riotgames.com/lol/match/v5/matches/{match_id}"
        res = requests.get(url, headers=headers)
        
        if res.status_code != 200:
            continue
            
        match_data = res.json()
        info = match_data['info']
        
        # Encontrar os dados do jogador específico na partida
        try:
            participant = next(p for p in info['participants'] if p['puuid'] == my_puuid)
        except StopIteration:
            continue
        
        # Criando métricas customizadas para análise de performance profunda
        duration_min = info['gameDuration'] / 60
        metrics = {
            "match_id": match_id,
            "win": participant['win'],
            "champion": participant['championName'],
            "role": participant['teamPosition'],
            "gold_per_min": participant['goldEarned'] / duration_min,
            "cs_per_min": (participant['totalMinionsKilled'] + participant['neutralMinionsKilled']) / duration_min,
            "vision_score_min": participant['visionScore'] / duration_min,
            "damage_per_gold": participant['totalDamageDealtToChampions'] / max(1, participant['goldEarned']),
            "kda": (participant['kills'] + participant['assists']) / max(1, participant['deaths']),
            # 'objectiveTakeowns' ajuda a ver se o jogador foca no jogo ou só em kills
            "obj_participation": participant.get('challenges', {}).get('objectiveTakeowns', 0)
        }
        
        data_list.append(metrics)
        time.sleep(1.2) # Respeita o limite da Riot (Rate Limit)

    return pd.DataFrame(data_list)

# =================================================================
# EXECUÇÃO DO SCRIPT
# =================================================================
if __name__ == "__main__":
    puuid = get_puuid(SUMMONER_NAME, TAG_LINE)
    if puuid:
        ids = get_match_ids(puuid, count=10)
        df_lol = analyze_matches(ids, puuid)
        
        # Exibe os dados processados (Insights de Micro-Jogo)
        print("--- Primeiras linhas da análise de eficiência ---")
        print(df_lol.head())
        
        # Salva em CSV para usar no Power BI depois
        df_lol.to_csv("dados_lol_eficiencia.csv", index=False)
