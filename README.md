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
python3 auto_transcript.py "Your Name" (names) (-compile) (open|start)
```
#### Optional arguments include 
* `names` fetches course names from the web to create a more descriptive transcript. Warning this can be a bit slow ~*2min*.
* `-compile` compiles the output file using `pdflatex`
* `open` or `start` depending on unix/windows system respectively can be added after `-compile` to automatically open the generated pdf 
