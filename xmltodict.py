import os
import datetime
import random
import string
import hashlib
import argparse
import sys
import tkinter as tk
from tkinter import filedialog
import shutil
from tkinter.constants import FALSE
import xmltodict
import pprint
from pathlib import Path
from grobid_client.grobid_client import GrobidClient

parser = argparse.ArgumentParser()
parser.add_argument('-s', '--slug', action='store_true', default=False)
parser.add_argument('-c', '--no-newline', action='store_true', default=False)
parser.add_argument('-n', '--number', action='store', type=int, default=1)

def random_md5(string_length=25, slug=False, number=1):
  hashes = []
  for n in range(number):
    r = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(string_length)).encode('utf-8')
    m = hashlib.md5()
    m.update(r)
    if slug == True:
      hashes.append(m.hexdigest()[:6])
    else:
      hashes.append(m.hexdigest())
  return hashes

if __name__ == '__main__':
  
  arguments = parser.parse_args()
  hashes = random_md5(slug=arguments.slug, number=arguments.number)
  if (arguments.number == 1 and arguments.no_newline == True):
    sys.stdout.write(hashes[0])
  else:
    for hash in hashes:
      print (hash)  

id_paper_input = "./resources/input_pdf/" + str(hash) + '_' + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')
id_paper_output = "./resources/output_pdf/" + str(hash) + '_' + str(datetime.datetime.now().date()) + '_' + str(datetime.datetime.now().time()).replace(':', '.')

def main():
    
   if not os.path.exists(id_paper_input):
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.askopenfilename()
        print(file_path)
        os.makedirs(id_paper_input)
        os.makedirs(id_paper_output)
        print("Directory " , id_paper_input, id_paper_output, " Created ")
        shutil.copy(file_path, id_paper_input)
   else:    
        print("Directory " , id_paper_input ,  " already exists")  

if __name__ == "__main__":
    main()
    client = GrobidClient(config_path="./config.json")
    client.process("processHeaderDocument", id_paper_input, id_paper_output, consolidate_citations=True, force=True)
    for file in Path(id_paper_output).iterdir():
        if file.suffix == '.xml':
            with open(file, 'r', encoding='utf-8') as file:
                xml = file.read()
                DEBUG = True
                paper_dict = xmltodict.parse(xml)
                try:
                    title = paper_dict['TEI']['teiHeader']['fileDesc']['titleStmt']['title']['#text']
                except:
                    title = ""
                    if DEBUG:
                        print("Unable to find title")
                try:
                    abstract = paper_dict['TEI']['teiHeader']['profileDesc']['abstract']['p']
                except:
                    abstract = ""
                    if DEBUG:
                        print("Unable to find abstract")
        
                try:
                    if "term" in paper_dict['TEI']['teiHeader']['profileDesc']['textClass']['keywords']:
                        keywords = ", ".join(paper_dict['TEI']['teiHeader']['profileDesc']['textClass']['keywords']['term'])
                    else:
                        keywords = paper_dict['TEI']['teiHeader']['profileDesc']['textClass']['keywords']
                except:
                    keywords = ""
                    if DEBUG:
                        print("Unable to find keywords")

                print("Title: {}".format(title))
                print("Abstract: {}".format(abstract))
                print("Keywords: {}".format(keywords))
