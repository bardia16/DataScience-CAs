from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

driver = webdriver.Edge()

start_block = 19333837
end_block = 19263903

transactions = []

base_url = 'https://etherscan.io/txs'

page_size = 100

for page_number in range(1, 200):
    url = f'{base_url}?ps={page_size}&p={page_number}'

    driver.get(url)
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    table = soup.find('table', {'class': 'table table-hover table-align-middle mb-0'})

    for row in table.find_all('tr')[1:]:  # Skip the header row
        cols = row.find_all('td')
        if cols:
            block_number = int(cols[3].text.strip())
            transaction_hash = cols[1].text.strip()
            method = cols[2].text.strip()
            # todo: fix the indices
            from_address = cols[5].text.strip()
            to_address = cols[6].text.strip()
            value = cols[7].text.strip()
            txn_fee = cols[8].text.strip()
            #print([transaction_hash, method, block_number, from_address, to_address, value, txn_fee])
            transactions.append([transaction_hash, method, block_number, from_address, to_address, value, txn_fee])
    time.sleep(1)

driver.quit()

df = pd.DataFrame(transactions, columns=['Txn Hash', 'Method', 'Block Number', 'From', 'To', 'Value', 'Txn Fee'])

print(df.head())

df.to_csv('etherscan_dataset.csv', index=False)