import os
from pathlib import Path
import json

def setup_dataroot() -> None:
  '''Setup dataroot location to dump logging and scrapping results to.'''
  dataroot = os.environ['DATAROOT']
  Path(dataroot).mkdir(parents=True, exist_ok=True)
  Path(os.path.join(dataroot,'logging')).mkdir(parents=True, exist_ok=True)
  Path(os.path.join(dataroot,'scraping')).mkdir(parents=True, exist_ok=True)
  with open(os.path.join(dataroot,'scraping','scrape_input.json'),'w') as fp:
      d = {
          'college': '',
          'names': [],
          'table_name': '',
      }
      json.dump(d,fp,indent=4)

if __name__ == '__main__':
    setup_dataroot()