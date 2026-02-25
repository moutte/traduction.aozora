import os, glob, sys
import string
from pathlib import Path
import subprocess as sub

from odf.opendocument import load
from odf.text import P, H
from odf import text,teletype

'''
delete RCLF
'''
SELECT= "EXTRACT"
SELECT= "EPUB"
SELECT= "INDEX" # build index of html -trad files

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

def txt2html(fiName):
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
    if line[0]=='#':
      line= line[1:]
      if line[0]=='#':
        line= line[1:]
        line= '<h2>'+line+'</h2>'
      else:
        line= '<h1>'+line+'</h1>'
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
  
  title = title_1.replace(' ','.')
  author = title_2.replace(' ','.')
  title = title_1.split(':')[0]
  author = title_2.split(':')[0]
  return title,author

def convert_odt_to_metadata_epub(input_file, output_file, title, author):
  import pypandoc
  """
  Converts ODT to EPUB and injects Title and Author metadata.
  """
  # Arguments to pass to Pandoc
  args = [
    '--standalone',
    f'--metadata=title:{title}',
    f'--metadata=author:{author}'
  ]
    
  try:
    pypandoc.convert_file(
      input_file, 
      'epub', 
      outputfile=output_file,
      extra_args=args
    )
    print(f"EPUB created successfully for '{title}' by {author}.")
  except RuntimeError as e:
    print(f"Error: {e}")

from odf import text, teletype
from odf.opendocument import load

def export_odt_properly(odt_path, output_txt):
  # Load the ODT file
  textdoc = load(odt_path)
  output_lines = []

  # Access the actual text body of the document
  # This is the container for all visible content
  body = textdoc.text

  # Iterate through every node in the body in order
  for node in body.childNodes:
    # Check if the node is a Paragraph (P) or Heading (H)
    # odfpy uses the .tagName attribute to identify these
    if node.tagName in ['text:p', 'text:h']:
      content = teletype.extractText(node)
      # If it's a heading, let's make it stand out 
      if node.tagName == 'text:h':
        level_str = node.getAttribute('outlinelevel')
        level = int(level_str) if level_str else 1
        prefix = "#" * level
        content = f"{prefix} {content.upper()}"
      output_lines.append(content)

  # Write to file
  with open(output_txt, 'w', encoding='utf-8') as f:
    f.write('\n\n'.join(output_lines))
  print(f"Done! Processed {len(output_lines)} elements.")

if SELECT=="EPUB" :
  directory = Path.cwd()
  for odt in sorted(directory.glob("*.odt")):
    if not odt.stem.endswith("-trad"): continue
    epub = odt.with_suffix(".epub")
    html = odt.with_suffix(".html")
    
    # fif not html.exists() or odt.stat().st_mtime > html.stat().st_mtime :
    if not html.exists() or os.path.getmtime(html) < os.path.getmtime(odt):
      # fo= open('001.txt','w')
      # print(odt)
      export_odt_properly(odt, "001.txt")
      if 0:
        textdoc = load(odt)
        extracted_text = []
        for element in textdoc.getElementsByType(text.P) + textdoc.getElementsByType(text.H):
          extracted_text.append(teletype.extractText(element))
        # Join all text into a single string
        full_text = "\n".join(extracted_text)
        # Write the text to a file
        with open("001.txt", "w", encoding="utf-8") as file:
          file.write(full_text)
      if 0:
        paragraphs = textdoc.getElementsByType((P))
        for para in paragraphs:
          extracted_text.append(teletype.extractText(para))
      if 0:
        elements = textdoc.getElementsByType((H, P))
        for elem in elements:
          text = teletype.extractText(elem)
          if elem.tagName == "text:h":
            level = elem.getAttribute("outline-level")
            extracted_text.append(f"\n{'#' * int(level)} {text}\n")
          else:
            extracted_text.append(text)
      if 0:
        node = textdoc.text
        for child in node.childNodes:
          if child.qname == ('text', 'p'):
            extracted_text.append(teletype.extractText(child))
          elif child.qname == ('text', 'h'):
            level = child.getAttribute("outline-level")
            text = teletype.extractText(child)
            extracted_text.append(f"\n{'#' * int(level)} {text}\n")   
        
      title, author = txt2html('001.txt')
      
      if 0: #epub.exists():
        command = [
            'ebook-meta', 
            epub, 
            '--title', title, 
            '--author', author
        ]
      if not epub.exists() or odt.stat().st_mtime > epub.stat().st_mtime :
        command = [
          'ebook-convert', 
          odt, 
          epub,
          '--title', title,
          '--authors', author
         ]
        sub.run(command, check=True)
      
    #if input("stop ?")=='y': sys.exit()
  sys.exit()

if SELECT=="EXTRACT":
  textdoc = load("Arishima-Takeo---Oyako--trad.odt")
  fo= open('001.txt','w')
  # Extract all paragraphs
  allparas = textdoc.getElementsByType(P)

  # Extract text from each paragraph
  extracted_text = []
  for para in allparas:
    extracted_text.append(teletype.extractText(para))

  # Join all text into a single string
  full_text = "\n".join(extracted_text)

  # Write the text to a file
  with open("001.txt", "w", encoding="utf-8") as file:
    file.write(full_text)

  # sys.exit()


if SELECT=="INDEX":  # build index of html -trad files
  word1='<title>'
  word2='</title>'
  fo= open('00-wrk.html','w')

  filelist= glob.glob('*.html')
  filelist.sort()
  for ff in filelist:
    stem = Path(ff).stem
    epub = stem+'.epub'
    odt  = stem+'.odt'
    if Path(ff).stem.endswith("-trad"):
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
      fo.write(title+'\n')
      fo.write('<a href="'+ff+'" target="_blank"> HTML </a> - \n')
      fo.write('<a href="'+odt+'"> ODT </a> - \n')
      fo.write('<a href="'+epub+'"> EBOOK </a>\n')
      fo.write('</p>\n')
      
      if 0:
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

sys.exit()
