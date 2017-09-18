import pyinotify
import sys
from chromote import Chromote
import subprocess

wm = pyinotify.WatchManager()  # Watch Manager
mask = pyinotify.IN_CLOSE_WRITE  # watched events

md = sys.argv[1]
html = sys.argv[2]
way_to_pdf_save = sys.argv[3]
file_name = sys.argv[4]


def bash(cmd):
    subprocess.Popen(cmd, shell=True, executable='/bin/bash')


class MyEventHandler(pyinotify.ProcessEvent):
    def my_init(self, file_object=sys.stdout):
        self._file_object = file_object

    def process_default(self, event):
        subprocess.call([
            "pandoc",
            md,
            "-f",
            "markdown",
            "-t",
            "html",
            "-s",
            "-o",
            html,
            "-c",
            "/css/latex-style.css",
            "--mathjax",
        ])
        chrome = Chromote()
        Chromote(host="localhost", port=9222)
        tab = chrome.tabs[0]
        tab.set_url('http://localhost:8080')
        tab.reload()
        bash('pandoc {} --latex-engine=xelatex -o {}/pdf/{}.pdf --variable mainfont="CMU Serif" --variable sansfont="CMU Sans Serif" --variable monofont="CMU Typewriter Text"'.format(md, way_to_pdf_save, file_name))
        bash("cp text.md {}/md/{}.md".format(way_to_pdf_save, file_name))
        bash("cp index.html {}/html/{}.html".format(way_to_pdf_save, file_name))

handler = MyEventHandler()
notifier = pyinotify.Notifier(wm, handler)
wdd = wm.add_watch(md, mask, rec=False)

notifier.loop()
