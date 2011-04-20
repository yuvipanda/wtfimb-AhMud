# Note: This script likes it's input HTML to have been passed through tidy
import sys
import os
import re
import glob
import json
from lxml import html

routename_regex = re.compile(r'Route\s*(.+)\s*:\s*(.+)(\s*Print$)?', re.MULTILINE)

def data_from_table(table):
    data_tables = table.xpath("table[@align='center']")
    stops_table = data_tables[0]
    time_table = data_tables[1]
    stops = [tr[1].text_content() for tr in stops_table.xpath("tr")]
    start_times = [int(td.text_content().replace(":","")) for td in time_table.xpath("tr/td") if td.text_content().replace(":","") != '']

    header = table.xpath("div[@class='enTripGroupInfo']")[0]
    header_text = html.fragment_fromstring(html.tostring(header).replace("\n"," ").replace("<br>","\n")).text_content().replace('To\n','To').replace('-\n','-').replace('-','')
    data_lines = [h.strip() for h in header_text.split('\n')]
    data = {'stops':stops,
            'start_times': sorted(start_times)}
    for dl in data_lines:
        s = dl.split(":")
        data[s[0].strip()] = s[1].strip()
    return data

def data_from_file(filename):
    doc = html.parse(filename)
    header_text = doc.xpath("//div[@class='headerText']")[0].text_content().strip().replace("\n", " ")
    match = routename_regex.search(header_text)
    number = match.groups()[0]
    name = match.groups()[1]
    data_boxes = doc.xpath("//table[@id='hbox']//td[@valign='top']")
    data =  {'name': name,
            'number': number,
            'path_up': data_from_table(data_boxes[0])}
    if len(data_boxes) > 1:
        data['path_down'] = data_from_table(data_boxes[1])
    return data

if __name__ == "__main__":
    basedir = sys.argv[1]
    opname = sys.argv[2]

    files = glob.glob(os.path.join(basedir, "r*.html"))
    data = []
    for f in files:       
        print "Doing %s" % f
        data.append(data_from_file(f))

    op = open(opname, 'w')
    json.dump(data, op, sort_keys=True, indent=4)
    op.close()
