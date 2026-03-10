# 🎮 The Tilt Factor & Win-Condition Optimizer

Este projeto utiliza a **API da Riot Games** para realizar uma análise avançada de performance em League of Legends. O objetivo é superar a análise comum de "taxa de vitória" e focar em **Micro-Eficiência** e indicadores comportamentais de "Tilt".

---

### 🚀 Diferencial do Projeto
Diferente de dashboards comuns, esta análise busca identificar o **Ponto de Ruptura**:
* **Gold Efficiency:** Por que ter mais ouro nem sempre garante a vitória?
* **The "Tilt" Proxy:** Como mortes consecutivas afetam o farm (CS/min) e a tomada de decisão.
* **Damage per Gold:** Uma métrica de eficiência para identificar quem realmente carrega o jogo.

---

### 🛠️ Tecnologias e Ferramentas
* **Python (Requests/Pandas):** Extração de dados complexos de APIs REST e tratamento de JSON.
* **Engenharia de Features:** Criação de métricas customizadas de eficiência de recursos.
* **Data Storytelling:** Documentação técnica voltada para insights de performance.

---

### 📁 Estrutura do Repositório
* `/src`: Scripts de extração e consumo da API da Riot.
* `/reports`: (Em breve) Relatório técnico de metodologia.

---

### 🔧 Como os dados são extraídos?
O script em `src/extraction.py` consome os endpoints da Riot (Match-V5), normaliza os dados e calcula métricas de eficiência por minuto para análise posterior em ferramentas de BI ou modelos de Machine Learning.
