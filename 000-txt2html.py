import os, glob, sys
import string
from pathlib import Path
import subprocess as sub

'''
delete RCLF
'''

INDEX= 1 # build index of html -trad files

def is_ascii(char):
    return ord(char) < 128

def is_japanese(char):
    code = ord(char)
    return (
        0x3040 <= code <= 0x309F or  # Hiragana
        0x30A0 <= code <= 0x30FF or  # Katakana
        0x4E00 <= code <= 0x9FAF or  # Kanji (CJK Unified Ideographs)
        0xFF66 <= code <= 0xFF9F     # Half-width Katakana
    )

if INDEX:  # build index of html -trad files
  word1='<title>'
  word2='</title>'
  fo= open('00-wrk.html','w')

  filelist= glob.glob('*.html')
  filelist.sort()
  for ff in filelist:
    stem = Path(ff).stem
    epub = stem+'.epub'
    if stem.endswith("-trad"):
      print(ff)
      with open(ff, 'r') as file:
        # Read each line in the file
        title= ff
        for line in file:
          indx1 = line.find(word1)
          indx2 = line.find(word2)
          if indx1 != -1 and indx2 != -1:
            # Move start index to the end of 'word1'
            title = line[indx1 + len(word1):indx2].strip()
            print(title)  # Output: some text to extract  sys.exit()
            break
      fo.write('<p>\n')
      fo.write('<a href="'+ff+'"target="_blank">\n')
      fo.write(title+'\n')
      fo.write('</a>\n')
      fo.write('</p>\n')
      
      if not ("'" in title):
        command = [
          'ebook-meta',
          epub,
          '--title', 
          title
        ]
        sub.run(command, check=True)
      
  fo.close()
  sys.exit()

fiName= '001.txt'

with open(fiName, 'r', encoding='utf-8') as file:
  lines = [line.strip() for line in file if line.strip() and line[0]!='.' ]

print(lines[0])

fstyle= open('000-style.html','r')
style= fstyle.readlines()
fstyle.close()

ENTETE= 1

if ENTETE:
  fname= lines[0].strip()
  title_1= lines[1].strip()
  title_2= lines[2].strip()
  key1= title_1.split()[0]
  key2= title_2.split()[0]
else:
  fname= '002.txt'

fo= open(fname+'.html','w')

if ENTETE:
  fo.write('<!DOCTYPE html>\n')
  fo.write('<html>\n')
  fo.write('<head>\n')
  fo.write('<meta name="keywords" content="')
  fo.write('aozora, japonais, traduction,'+key1+','+key2)
  fo.write('">\n')
  fo.write('<meta name="viewport" content="width=device-width, initial-scale=1.0">\n')
  fo.write('<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n')
  # fo.write("<style>\n")
  for line in style: fo.write(line)
  # fo.write("</style>\n")
  fo.write('<title>'+title_1+'</title>\n')
  fo.write('</head>\n')
  fo.write('<body>\n')

  fo.write('<h1>'+title_1+'</h1>'+'\n')
  fo.write('<h2>'+title_2+'</h2>'+'\n')

for i,line in enumerate(lines):
  line= line.strip()
  if len(line)==0: continue
  if ENTETE and i<3: continue
  if line[0]=='<': 
    fo.write(line+'\n')
    continue
  if line[0]=='.' and len(set(line))<=1: continue
  if line[0]=='*':
    line= line[1:]
    line= '<p class=blue>'+line+'</p>'
    fo.write(line+'\n')
    continue
  if line[0]=='§':
    line= line[1:]
    line= '<h2>'+line+'</h2>'
    fo.write(line+'\n')
    continue
  if line.find('http')==0:
    line= '<a href="'+line+'" target="_blank">\n' +'source: '+line +'</a>'
    line= '<p class=thick>'+line+'</p>'
    fo.write(line+'\n')
    continue
  if '¤' or '£' in line:
    words = line.split(' ')
    line= ''
    for w in words:
      if len(w)<2: 
        line= line+w+' '
        continue
      if w[0]=='¤': 
        print(w)
        w='<i>'+w[1:]+'</i>'
      if w[0]=='£': 
        print(w)
        w='<b>'+w[1:]+'</b>'
      line= line+w+' ' 
  line= '<p>'+line+'</p>'
  fo.write(line+'\n')

if 0:
  frefs= open('index-refs.html','r')
  refs= frefs.readlines()
  frefs.close()
  for line in refs: fo.write(line)

fo.write('</body>\n')
fo.write('</html>\n')
fo.close()

sys.exit()
