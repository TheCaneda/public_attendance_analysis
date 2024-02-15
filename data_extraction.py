from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd  # Import pandas for DataFrame creation
import time
import os

teams = {
    "inter": "https://www.transfermarkt.com.br/sc-internacional/spielplan/verein/6600/saison_id/",
    "gremio": "https://www.transfermarkt.com.br/gremio-porto-alegre/spielplan/verein/210/saison_id/",
}

years = [n for n in range(2010, 2021)]

elements = {
    "table-container": {"class": "box"},
    "tables": {"class": "responsive-table"},
}

main_header = ['Rodada', 'Data', 'Horário', 'Cidade', 'Ranking', 'Adversário', 'Sistema de jogo', 'Público', 'Resultado']
corrected_main_header = ['Rodada', 'Data', 'Horário', 'Cidade', 'Ranking', 'Adversário Logo', 'Adversário', 'Sistema de jogo', 'Público', 'Resultado']

webdriver = webdriver.Chrome()

for year in years:
    for team_key, team_url in teams.items():
        url = team_url + str(year)
        webdriver.get(url)
        time.sleep(4)  # Consider using WebDriverWait for better reliability
        html_content = webdriver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all 'box' containers as tables may be within them
        boxes = soup.find_all('div', class_=elements["table-container"]["class"])
        
        for box in boxes:
            tables = box.find_all('div', class_=elements["tables"]["class"])
            for table_container in tables:
                table = table_container.find('table')
                if table:
                    # Extract table name if available or use a placeholder
                    table_name = table_container.find_previous('h2').text.strip() if table_container.find_previous('h2') else "Unknown Table"
                    
                    # Check for header correction
                    headers = [header.text.strip() for header in table.find('thead').find_all('th')]
                    if headers == main_header:
                        headers = corrected_main_header
                    
                    # Extract body
                    rows = []
                    for row in table.find('tbody').find_all('tr'):
                        cols = [ele.text.strip() for ele in row.find_all('td')]
                        rows.append(cols)
                    
                    # Create a DataFrame for the current table
                    df = pd.DataFrame(rows, columns=headers)
                    
                    # Prepare directory and file paths
                    directory_path = f'./data/{team_key}/{table_name.lower()}'
                    os.makedirs(directory_path, exist_ok=True)  
                    csv_file_path = f'{directory_path}/{year}.csv'
                    
                    # Save the DataFrame
                    df.to_csv(csv_file_path, encoding='utf-8', sep=';')
                    print(f"Saved DataFrame to {csv_file_path}")

webdriver.quit()