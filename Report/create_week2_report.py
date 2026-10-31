
import os
import csv
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

# =========================================================
# WEEK 2 REPORT GENERATOR
# Author: Sahil Jadhao
# Project: Titanic Data Visualization and Insight Communication
# =========================================================

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GRAPH_DIR = os.path.join(BASE, "Outputs", "Graphs")
RESULT_DIR = os.path.join(BASE, "Outputs", "Results")
SCRIPT_PATH = os.path.join(BASE, "R_Scripts", "week2_visualizations.R")
OUTPUT_PATH = os.path.join(
    os.path.dirname(__file__),
    "Week_2_Data_Visualization_Report.docx"
)

doc = Document()

# Page settings
section = doc.sections[0]
section.top_margin = Inches(0.7)
section.bottom_margin = Inches(0.7)
section.left_margin = Inches(0.8)
section.right_margin = Inches(0.8)

# Default font
styles = doc.styles
styles["Normal"].font.name = "Calibri"
styles["Normal"].font.size = Pt(10.5)

for style_name in ["Title", "Heading 1", "Heading 2"]:
    styles[style_name].font.name = "Calibri"

styles["Heading 1"].font.color.rgb = RGBColor(31, 78, 121)
styles["Heading 2"].font.color.rgb = RGBColor(46, 116, 181)

def add_paragraph(text, bold_start=None):
    p = doc.add_paragraph()
    if bold_start and text.startswith(bold_start):
        r = p.add_run(bold_start)
        r.bold = True
        p.add_run(text[len(bold_start):])
    else:
        p.add_run(text)
    return p

def add_bullet(text):
    doc.add_paragraph(text, style="List Bullet")

def add_number(text):
    doc.add_paragraph(text, style="List Number")

def add_graph(filename, title, explanation, insight, why):
    path = os.path.join(GRAPH_DIR, filename)

    doc.add_heading(title, level=2)
    add_paragraph(explanation)
    if os.path.exists(path):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(path, width=Inches(6.0))
    else:
        add_paragraph("Graph image not found: " + filename)

    add_paragraph("Key Insight: " + insight, "Key Insight:")
    add_paragraph("Why this chart was selected: " + why,
                  "Why this chart was selected:")

def add_csv_table(filename, heading, max_rows=20):
    path = os.path.join(RESULT_DIR, filename)
    if not os.path.exists(path):
        return

    doc.add_heading(heading, level=2)

    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f))

    if not rows:
        return

    rows = rows[:max_rows + 1]
    table = doc.add_table(rows=1, cols=len(rows[0]))
    table.style = "Light Shading Accent 1"

    for i, value in enumerate(rows[0]):
        table.rows[0].cells[i].text = value

    for row in rows[1:]:
        cells = table.add_row().cells
        for i, value in enumerate(row):
            cells[i].text = value

# =========================================================
# COVER PAGE
# =========================================================

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("\n\nWEEK 2 INTERNSHIP REPORT")
r.bold = True
r.font.size = Pt(25)
r.font.color.rgb = RGBColor(31, 78, 121)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("\nDATA VISUALIZATION AND\nINSIGHT COMMUNICATION USING R")
r.bold = True
r.font.size = Pt(19)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("\n\nTitanic Passenger Dataset").font.size = Pt(16)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("\n\nSubmitted by\n").bold = True
p.add_run("Sahil Jadhao\n")
p.add_run("Virtual R Data Analyst Internship\n")
p.add_run("Week 2 Task\n")
p.add_run("Tools: R, ggplot2, dplyr, Visual Studio Code")

doc.add_page_break()

# =========================================================
# ABSTRACT
# =========================================================

doc.add_heading("Abstract", level=1)

add_paragraph(
    "This project focuses on visualizing and communicating insights "
    "from the Titanic passenger dataset using the R programming language. "
    "The analysis uses the ggplot2 visualization library to create six "
    "different chart types: bar chart, histogram, scatter plot, line chart, "
    "box plot, and heatmap."
)

add_paragraph(
    "The visualizations explore passenger survival distribution, age "
    "patterns, fare differences, and survival rates across passenger "
    "age groups and classes. The report includes visualization outputs, "
    "interpretations, and the R source code used to generate them."
)

# =========================================================
# TABLE OF CONTENTS
# =========================================================

doc.add_heading("Table of Contents", level=1)

contents = [
    "1. Introduction",
    "2. Objectives",
    "3. Dataset Overview",
    "4. Tools and Technologies",
    "5. Data Preparation",
    "6. Visualization Design and Interpretation",
    "7. Statistical Results",
    "8. Key Findings",
    "9. Limitations",
    "10. Conclusion",
    "11. Appendix: Complete R Source Code"
]

for item in contents:
    add_paragraph(item)

# =========================================================
# INTRODUCTION
# =========================================================

doc.add_heading("1. Introduction", level=1)

add_paragraph(
    "Data visualization is the graphical representation of information "
    "and data. It helps analysts identify patterns, trends, relationships, "
    "and unusual observations. Well-designed visualizations make complex "
    "data easier to understand for technical and non-technical audiences."
)

add_paragraph(
    "In this project, the Titanic passenger dataset is used to demonstrate "
    "different visualization techniques in R. The charts are designed to "
    "communicate findings clearly and support data-driven interpretation."
)

# =========================================================
# OBJECTIVES
# =========================================================

doc.add_heading("2. Objectives", level=1)

objectives = [
    "Create multiple visualizations using R and ggplot2.",
    "Represent categorical and numerical data graphically.",
    "Understand passenger survival patterns.",
    "Compare survival rates across passenger age groups.",
    "Study the relationship between passenger age and fare.",
    "Compare fare distributions across passenger classes.",
    "Communicate insights through clear explanations."
]

for item in objectives:
    add_bullet(item)

# =========================================================
# DATASET
# =========================================================

doc.add_heading("3. Dataset Overview", level=1)

add_paragraph(
    "The Titanic dataset contains passenger information from the Titanic "
    "disaster. The original training dataset contains 891 rows and 12 "
    "columns."
)

add_paragraph("Important variables used in this project:")

variables = [
    ("Survived", "Survival indicator: 0 = Did not survive, 1 = Survived."),
    ("Pclass", "Passenger ticket class: 1, 2, or 3."),
    ("Sex", "Passenger gender category."),
    ("Age", "Passenger age in years."),
    ("Fare", "Passenger ticket fare."),
    ("SibSp", "Number of siblings or spouses aboard."),
    ("Parch", "Number of parents or children aboard."),
    ("Embarked", "Port of embarkation.")
]

table = doc.add_table(rows=1, cols=2)
table.style = "Light Shading Accent 1"
table.rows[0].cells[0].text = "Variable"
table.rows[0].cells[1].text = "Description"

for name, description in variables:
    cells = table.add_row().cells
    cells[0].text = name
    cells[1].text = description

# =========================================================
# TOOLS
# =========================================================

doc.add_heading("4. Tools and Technologies", level=1)

tools_used = [
    "R: Statistical computing and data analysis.",
    "ggplot2: Creation of high-quality statistical graphics.",
    "dplyr: Data manipulation and summarization.",
    "tidyr: Data organization and transformation.",
    "Visual Studio Code: Code editing and project development.",
    "Microsoft Word: Report preparation and documentation."
]

for item in tools_used:
    add_bullet(item)

# =========================================================
# DATA PREPARATION
# =========================================================

doc.add_heading("5. Data Preparation", level=1)

add_paragraph(
    "The original Titanic dataset was loaded using read.csv(). "
    "The dataset contained missing values in Age and Embarked. "
    "For this visualization task, missing Age values were replaced "
    "with the median age and missing Embarked values were assigned "
    "the most frequent category, S."
)

add_paragraph(
    "A Survival factor was created to display readable survival labels. "
    "Passenger classes were converted into First Class, Second Class, "
    "and Third Class. Age values were grouped into Child, Teenager, "
    "Young Adult, Adult, and Senior categories."
)

add_paragraph(
    "These transformations were performed to improve the readability "
    "and interpretability of the visualizations. The original dataset "
    "was not overwritten."
)

# =========================================================
# VISUALIZATIONS
# =========================================================

doc.add_heading("6. Visualization Design and Interpretation", level=1)

add_graph(
    "01_survival_distribution.png",
    "6.1 Bar Chart: Survival Distribution",
    "The bar chart compares the number of passengers who survived "
    "with the number who did not survive.",
    "The dataset contains 342 survivors and 549 non-survivors. "
    "Approximately 38.4% of passengers survived.",
    "A bar chart is suitable for comparing counts across discrete "
    "categories."
)

add_graph(
    "02_age_distribution.png",
    "6.2 Histogram: Passenger Age Distribution",
    "The histogram displays the frequency distribution of passenger "
    "ages using five-year intervals.",
    "The passenger dataset includes children, young adults, adults, "
    "and senior passengers. The largest concentration is among "
    "younger and middle-aged passengers.",
    "A histogram is effective for understanding the distribution "
    "of a continuous numerical variable."
)

add_graph(
    "03_age_vs_fare_scatter.png",
    "6.3 Scatter Plot: Age Versus Fare",
    "Each point represents a passenger. The horizontal axis shows "
    "age, while the vertical axis represents ticket fare. Point "
    "colors indicate survival outcome.",
    "The scatter plot helps compare passenger age, ticket fare, "
    "and survival status. It also shows variation in fares among "
    "passengers of different ages.",
    "A scatter plot is appropriate for examining the relationship "
    "between two numerical variables."
)

add_graph(
    "04_survival_by_age_group.png",
    "6.4 Line Chart: Survival Rate by Age Group",
    "This chart displays survival percentages across five ordered "
    "age groups: Child, Teenager, Young Adult, Adult, and Senior.",
    "Children recorded a 58.0% survival rate, while seniors recorded "
    "22.7%. Teenagers recorded 42.9%, young adults 35.3%, and adults "
    "40.0%.",
    "A line chart highlights changes across ordered categories. "
    "Here it is used to compare age-group progression, not a time series."
)

add_graph(
    "05_fare_by_class_boxplot.png",
    "6.5 Box Plot: Fare Distribution by Passenger Class",
    "The box plot compares the median, spread, and potential outliers "
    "of ticket fares across the three passenger classes.",
    "The visualization helps show differences in fare distributions "
    "between first, second, and third class passengers. Higher fares "
    "and wider variation are visible in the first-class group.",
    "A box plot is useful for comparing numerical distributions "
    "and identifying potential outliers across categories."
)

add_graph(
    "06_survival_heatmap.png",
    "6.6 Heatmap: Survival by Age Group and Passenger Class",
    "The heatmap represents survival percentages using different "
    "color intensities for combinations of passenger class and age group.",
    "First-class teenagers had a 91.7% survival rate, while third-class "
    "adults had an 8.62% survival rate. These groups contain 12 and "
    "58 passengers respectively.",
    "A heatmap helps compare values across two categorical dimensions "
    "and makes high and low values easy to identify."
)

# =========================================================
# RESULTS TABLES
# =========================================================

doc.add_heading("7. Statistical Results", level=1)

add_paragraph(
    "The following tables contain the actual summary results exported "
    "by the R visualization script."
)

add_csv_table(
    "survival_distribution.csv",
    "7.1 Survival Distribution"
)

add_csv_table(
    "survival_by_age_group.csv",
    "7.2 Survival Rate by Age Group"
)

add_csv_table(
    "survival_heatmap_data.csv",
    "7.3 Survival Heatmap Summary"
)

# =========================================================
# KEY FINDINGS
# =========================================================

doc.add_heading("8. Key Findings", level=1)

findings = [
    "Out of 891 passengers, 342 survived and 549 did not survive.",
    "The overall survival rate was approximately 38.4%.",
    "Children had the highest survival rate among the five age groups.",
    "Seniors had the lowest survival rate, although the group was small.",
    "Survival percentages differed across passenger classes.",
    "The heatmap revealed substantial differences between age and class combinations.",
    "The scatter plot showed how age and fare varied across survival outcomes."
]

for item in findings:
    add_bullet(item)

# =========================================================
# LIMITATIONS
# =========================================================

doc.add_heading("9. Limitations", level=1)

limitations = [
    "The analysis uses the Titanic training dataset and may not represent all passengers.",
    "Missing age values were imputed with the median, which may affect the displayed distribution.",
    "Some age-group and class combinations contain very few passengers.",
    "The visualizations show associations and descriptive patterns, not causal relationships.",
    "A line chart across age groups is a categorical comparison rather than a time-based trend."
]

for item in limitations:
    add_bullet(item)

# =========================================================
# CONCLUSION
# =========================================================

doc.add_heading("10. Conclusion", level=1)

add_paragraph(
    "This project demonstrates how R and ggplot2 can be used to "
    "communicate data insights through different visualization "
    "techniques. Six chart types were created to explore survival "
    "distribution, age patterns, fare differences, and survival "
    "percentages across passenger groups."
)

add_paragraph(
    "The analysis shows that visualizations make it easier to identify "
    "important patterns and communicate findings to non-technical "
    "audiences. The project strengthened practical skills in R "
    "programming, graphical analysis, interpretation, and report writing."
)

# =========================================================
# APPENDIX: COMPLETE R CODE
# =========================================================

doc.add_page_break()
doc.add_heading("11. Appendix: Complete R Source Code", level=1)

if os.path.exists(SCRIPT_PATH):
    with open(SCRIPT_PATH, "r", encoding="utf-8") as f:
        code_text = f.read()

    for line in code_text.splitlines():
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(line if line else " ")
        run.font.name = "Consolas"
        run.font.size = Pt(7.5)
else:
    add_paragraph("R source code file was not found.")

# =========================================================
# FOOTER
# =========================================================

for sec in doc.sections:
    footer = sec.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    footer.add_run(
        "Week 2 Data Visualization Internship Report | Sahil Jadhao"
    )

# =========================================================
# SAVE REPORT
# =========================================================

doc.save(OUTPUT_PATH)

print("\n==========================================")
print("WEEK 2 REPORT GENERATED SUCCESSFULLY")
print("==========================================")
print("Report:", OUTPUT_PATH)
print("Graphs included: 6")
print("Result tables: 3")
print("R source code: Included")
print("==========================================")
