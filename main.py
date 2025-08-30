from src.extract_transform.scraping_data_to_json import coletar_dados_acoes
from src.extract_transform.Coletando_lista_acoes_atualizada import atualizar_acoes

def main():
    atualizar_acoes()
    print("✅ Lista de ações atualizada (acoes.txt).")
    df = coletar_dados_acoes()
    print("✅ Dados das ações coletados e salvos em dados_json2.json.")
    print(df.head())

if __name__ == "__main__":
    main()
