# UBC Transcript Generator
Easily generate an unofficial UBC transcript formatted nicely with LaTeX
![](https://i.imgur.com/cmYLlyv.png)
## Instructions
`git clone https://github.com/tomginsberg/transcript-generator.git`

 Get your data from the [ssc](ssc.adm.ubc.ca/sscportal/servlets/SSCMain.jsp?function=SessGradeRpt) and copy paste it into mydata.txt. The format must be exactly as pasted from the **"Your Grades Summary"** data table.
```
# Example data format
ELEC 501	501	50	F	5050W	1	BASC	3	4.0	50
MATH 500	502	50	F	5050W	1	BASC	3	3.0	50
MECH 505	502	50	F	5050W	1	BASC	3	4.0	50
MECH 500	501	50	F	5050W	1	BASC	3	3.0	50
...
```
###### Run
```
usage: auto_transcript.py [-h] [--name NAME] [--data DATA] [--compile] [--descriptive]

optional arguments:
  -h, --help     show this help message and exit
  --name NAME    Your full name
  --data DATA    Path to the text file containing your grades copied directly from the ssc.
                 Defaults to `mydata.txt` See https://github.com/tomginsberg/transcript-generator
                 for more instructions
  --compile      [flag] If passed compiles pdf with pdflatex
  --descriptive  [flag] If passed add a column of course names fetched from UBC course catalogue
  ```
