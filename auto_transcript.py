from sys import argv
import subprocess
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

# Paste raw data here
raw_data = """ELEC 221	101	92	A+	2018W	1	BASC	3	4.0	71	
MATH 220	102	76	B+	2018W	1	BASC	3	3.0	58	
MECH 325	102	76	B+	2018W	1	BASC	3	4.0	77	
MECH 360	101	90	A+	2018W	1	BASC	3	3.0	73	
PHYS 301	101	97	A+	2018W	1	BASC	3	3.0	71	
PHYS 304	101	87	A	2018W	1	BASC	3	3.0	73	
APSC 278	201	84	A-	2018W	2	BASC	3	3.0	74	
APSC 279	211	92	A+	2018W	2	BASC	3	1.0	87	
CPEN 312	201	99	A+	2018W	2	BASC	3	3.0	75	
CPSC 221	201	90	A+	2018W	2	BASC	3	4.0	81	
MATH 305	201	90	A+	2018W	2	BASC	3	3.0	76	
MATH 318	201	90	A+	2018W	2	BASC	3	3.0	72	
MECH 280	201	82	A-	2018W	2	BASC	3	3.0	74	
PHYS 350	201	95	A+	2018W	2	BASC	3	3.0	80	
PHYS 250	941	86	A	2018S	1	BASC	2	3.0	83	
MATH 257	921	87	A	2018S	1	BASC	2	3.0	80	
ENPH 270	941	83	A-	2018S	1	BASC	2	2.0	80	
ENPH 257	941	76	B+	2018S	1	BASC	2	2.0	78	
ENPH 253	941	96	A+	2018S		BASC	2	5.0	89	
CPEN 221	101	93	A+	2017W	1	BASC	2	4.0	76	
ELEC 204	101	96	A+	2017W	1	BASC	2	4.0	79	
ENPH 259	101	94	A+	2017W	1	BASC	2	3.0	88	
MATH 217	101	88	A	2017W	1	BASC	2	4.0	73	
MATH 255	101	91	A+	2017W	1	BASC	2	3.0	60	
MECH 260	102	68	B-	2017W	1	BASC	2	3.0	60	
PSYC 101	006	77	B+	2017W	1	BASC	2	3.0	68	
APSC 110	606	 		2017W	2	BASC	2	6.0	n/a	P
PHYS 170	203	92	A+	2016W	2	BASC	1	3.0	84	
PHYS 159	L2B	91	A+	2016W	2	BASC	1	1.0	85	
PHYS 158	203	95	A+	2016W	2	BASC	1	3.0	67	
MATH 152	201	94	A+	2016W	2	BASC	1	3.0	68	
MATH 101	206	94	A+	2016W	2	BASC	1	3.0	73	
APSC 160	204	94	A+	2016W	2	BASC	1	3.0	79	
APSC 101	202	82	A-	2016W	2	BASC	1	3.0	75	
PHYS 157	103	83	A-	2016W	1	BASC	1	3.0	73	
MATH 100	105	84	A-	2016W	1	BASC	1	3.0	66	
ENGL 112	06C	79	B+	2016W	1	BASC	1	3.0	77	
ECON 101	006	93	A+	2016W	1	BASC	1	3.0	71	
CHEM 154	133	95	A+	2016W	1	BASC	1	3.0	73	
APSC 100	103	83	A-	2016W	1	BASC	1	3.0	79"""


def get_name(course: str, code: str) -> str:
    url = f"https://courses.students.ubc.ca/cs/courseschedule?pname=subjarea&tname=subj-course&dept={course}" \
          f"&course={code}"
    res = requests.get(url)
    html_page = res.content

    soup = BeautifulSoup(html_page, 'html.parser')
    text = soup.find_all(text=True)
    name = text[19][11:-23]
    formatted = []
    line = ""
    for word in name.split():
        if len(line) + len(word) < 40:
            line += f" {word}"
        else:
            formatted.append(line[1:])
            line = f" {word}"
    formatted.append(line[1:])

    name = "\\\\".join(formatted)
    return name


raw_doc = lambda data, name, add_col: f"""\\documentclass{{article}}
\\usepackage[paper=letterpaper,left=20mm,right=20mm,top=3cm,bottom=2cm]{{geometry}}
\\usepackage[utf8]{{inputenc}}
\\usepackage{{fancyhdr}}
\\pagestyle{{fancy}}
\\usepackage{{longtable}}
\\usepackage{{makecell}}
\\usepackage[makeroom]{{cancel}}

\\lhead{{{name}}}
\\rhead{{University of British Columbia}}
\\renewcommand{{\\headrulewidth}}{{0.4pt}}

\\begin{{document}}
\\subsection*{{Unofficial Transcript of Records}}
    \\begin{{longtable}}{{{"|c" if add_col else ""}|l|c| c|  c|c |}}
    \\hline
    {"Course Name &" if add_col else ""}Course Code & Grade & Letter & Year of Study & Class Average\\\\\\hline\\hline
    {data}
 \\end{{longtable}}
\\end{{document}}"""

if __name__ == '__main__':
    next_arg = 1
    arg_len = len(argv)
    add_names = "names" in argv
    rows = []

    for line in tqdm(raw_data.split("\n")):
        values = line.split("\t")
        try:
            if values[2].strip() == "":
                print(f"{values[0]} has no grade. Ignoring.")
            else:
                if add_names:
                    rows.append(f"\\thead{{{get_name(*values[0].split())}}}&{values[0]} & {values[2]} & {values[3]} & {values[7]} & {values[9]} \\\\ \\hline")
                else:
                    rows.append(f"{values[0]} & {values[2]} & {values[3]} & {values[7]} & {values[9]} \\\\ \\hline")
        except IndexError:
            print(f"Parse error in {line}. Ignoring.")

    rd = raw_doc("\n".join(rows), argv[next_arg], add_names)

    next_arg += (1 + add_names)

    with open("transcript.tex", "w") as f:
        f.write(rd)

    if next_arg < arg_len and argv[next_arg] == "-compile":
        subprocess.call(["pdflatex", "transcript.tex"])
        subprocess.call(["rm", "transcript.log", "transcript.bbl", "transcript.blg", "transcript.aux"])
        next_arg += 1
        if next_arg < arg_len:
            subprocess.call([argv[next_arg], "transcript.pdf"])
