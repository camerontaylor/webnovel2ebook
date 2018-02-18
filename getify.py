# pylint: disable-all
from bs4 import BeautifulSoup
import urllib.request
import shutil
import os.path
import sys
import zipfile
import time
import os


def remove_empty_lines(file_name):
    if not os.path.isfile(file_name):
        print("{} does not exist ".format(file_name))
        return
    with open(file_name) as filehandle:
        lines = filehandle.readlines()

    with open(file_name, 'w') as filehandle:
        lines = filter(lambda x: x.strip(), lines)
        filehandle.writelines(lines)

#Downloads Chapters
def download(link, file_name):
	url = urllib.request.Request(
		link,
		data=None, 
		headers={
			'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
		}
	)

	with urllib.request.urlopen(url) as response, open(file_name + ".xhtml", 'wb') as out_file:
		shutil.copyfileobj(response, out_file)

#Page Clean-up
def clean(filename):
	with open(filename + ".xhtml", "r", encoding="utf8") as f:
		soup = BeautifulSoup(f, "html.parser")
		pretext = soup.find("div", {"class":"cha-content"})
		chapter_title = soup.find("h3")
		[s.extract() for s in pretext('form')]
		[s.extract() for s in pretext('a')]
		[s.extract() for s in pretext('script')]
		for div in pretext("div", {"class":"g_ad_ph"}):
			div.decompose()
		for div in pretext("div", {"class":"cha-bts"}):
			div.decompose()
		pretext = str(pretext)
		chapter_title = str(chapter_title)
				
	file = open(filename + "m" + ".xhtml", "w", encoding = "utf8")

	file.write('''
	<html xmlns="http://www.w3.org/1999/xhtml">
	<head><title>%(chapter_title)s</title>
	<link href="../Styles/style.css" rel="stylesheet" type="text/css"/>
	</head>
	<body>
	''')
	file.write(chapter_title)
	for line in pretext:
		if "href" not in line:
			file.write(line)	
	file.write("</body>")
	file.write("</html>")
	os.remove(filename + ".xhtml")
	
#Displays and updates the download progress bar
def update_progress(progress):
    barLength = 25 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rDownload Progress: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()
	
def generate(html_files, novelname, author, chaptername, chapter_s, chapter_e):
	if ":" in novelname:
		novelname = "enterManuallyPlz"
	epub = zipfile.ZipFile(novelname + "_" + chapter_s + "-" + chapter_e + ".epub", "w")

	# The first file must be named "mimetype"
	epub.writestr("mimetype", "application/epub+zip")

	# The filenames of the HTML are listed in html_files
	# We need an index file, that lists all other HTML files
	# This index file itself is referenced in the META_INF/container.xml file
	epub.writestr("META-INF/container.xml", '''<?xml version="1.0" encoding="UTF-8"?>
	<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
    	<rootfiles>
        	<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
   		</rootfiles>
	</container>''')
	# The index file is another XML file, living per convention
	# in OEBPS/Content.opf
	index_tpl = '''<?xml version="1.0" encoding="utf-8" ?>
	<package unique-identifier="BookId" version="2.0" xmlns="http://www.idpf.org/2007/opf">
		<metadata xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:opf="http://www.idpf.org/2007/opf">
			%(metadata)s
		</metadata>
		<manifest>
			<item href="Styles/style.css" id= "style.css" media-type= "text/css" />
    		<item href="Fonts/Ovo-Regular.ttf" id="Ovo-Regular.ttf" media-type="application/x-font-ttf"/>
    		<item href="Fonts/Andalus.ttf" id="Andalus.ttf" media-type="application/x-font-ttf"/>
			<item href="toc.ncx" id="ncx" media-type="application/x-dtbncx+xml"/>
			%(manifest)s
		</manifest>
		<spine toc="ncx">
			%(spine)s
		</spine>
		<guide>

    	</guide>
	</package>'''

	manifest = ""
	spine = ""
	metadata = '''<dc:title xmlns:dc="http://purl.org/dc/elements/1.1/">%(novelname)s</dc:title>
    <dc:creator xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:ns0="http://www.idpf.org/2007/opf" ns0:role="aut" ns0:file-as="Unbekannt">%(author)s</dc:creator>
	<dc:identifier id="BookId" opf:scheme="UUID">urn:uuid:1a82cc17-601c-4aa5-9d0e-cf3c3fa2d50c</dc:identifier>
	<meta content="0.9.5" name="Sigil version"/>
	<dc:language>en</dc:language>''' % {
	"novelname": novelname + ": " + chapter_s + "-" + chapter_e, "author": author, "series": novelname}
	
	# Write each HTML file to the ebook, collect information for the index
	for i, html in enumerate(html_files):
		basename = os.path.basename(html)
		manifest += '<item id="file_%s" href="Text/%s" media-type="application/xhtml+xml"/>' % (
					  i+1, basename)
		spine += '<itemref idref="file_%s" />' % (i+1)
		epub.write(html, "OEBPS/Text/"+basename)

	# Write stylesheet and fonts
	epub.write("Assets/Style.css", "OEBPS/Styles/style.css")
	epub.write("Assets/Andalus.ttf", "OEBPS/Fonts/Andalus.ttf")
	epub.write("Assets/Ovo-Regular.ttf", "OEBPS/Fonts/Ovo-Regular.ttf")

	# Finally, write the index
	epub.writestr("OEBPS/content.opf", index_tpl % {
	"metadata": metadata,
	"manifest": manifest,
	"spine": spine,
	})
	
	 #Generates a Table of Contents + lost strings
	toc_start = '''<?xml version="1.0" encoding="utf-8" ?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN"
 "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd"><ncx version="2005-1" xmlns="http://www.daisy.org/z3986/2005/ncx/">
  <head>
  <meta content="urn:uuid:1a82cc17-601c-4aa5-9d0e-cf3c3fa2d50c" name="dtb:uid"/>
    <meta content="2" name="dtb:depth"/>
    <meta content="0" name="dtb:totalPageCount"/>
    <meta content="0" name="dtb:maxPageNumber"/>
  </head>
		<docTitle>
    <text>%(novelname)s</text>
  </docTitle>
	<navMap>
    <navPoint id="navPoint-1" playOrder="1">
	<navLabel>
    <text>%(novelname)s</text>
    </navLabel>
	<content src=""/>
				%(toc_mid)s
		%(toc_end)s'''
	toc_mid = ""
	toc_end = '''</navPoint></navMap></ncx>'''
	j=2	
	for i, y in enumerate(html_files):
		ident = 0
		chapter = chaptername[i]["text"]
		toc_mid += '''<navPoint id="navPoint-%s" playOrder="%s">
      <navLabel>
        <text>%s</text>
      </navLabel>
	  <content src="OEBPS/Text/%s"/>
	  </navPoint>''' % (j, j, chapter, html_files[i])
		j+=1

epub.writestr("OEBPS/toc.ncx", toc_start % {"novelname": novelname, "toc_mid": toc_mid, "toc_end": toc_end})
epub.write("cover.jpg", "OEBPS/Images/cover.jpg")
epub.close()
os.remove("cover.jpg")
#removes all the temporary files
for x in html_files:
	os.remove(x)
