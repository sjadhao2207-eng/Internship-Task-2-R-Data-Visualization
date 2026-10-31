# Week 2 – Data Visualization and Insight Communication Using R

**Intern:** Sahil Jadhao  
**Internship:** Virtual R Data Analyst Internship  
**Project:** Titanic Passenger Data Visualization  
**Tools:** R, ggplot2, dplyr, tidyr, Visual Studio Code

## Project Overview

This project focuses on visualizing and communicating insights from the Titanic passenger dataset using R.

Six different visualizations were created to understand passenger survival patterns, age distribution, ticket fares, and differences across passenger classes.

## Dataset

- Dataset: Titanic Training Dataset
- Rows: 891
- Original columns: 12
- Source: Titanic public training dataset

## Visualizations

1. Bar Chart – Survival Distribution
2. Histogram – Passenger Age Distribution
3. Scatter Plot – Age vs Fare
4. Line Chart – Survival Rate by Age Group
5. Box Plot – Fare Distribution by Passenger Class
6. Heatmap – Survival by Age Group and Passenger Class

## Key Findings

- 342 passengers survived.
- 549 passengers did not survive.
- Overall survival rate was approximately 38.4%.
- Children recorded a 58.0% survival rate.
- Seniors recorded a 22.7% survival rate.
- Survival rates varied across passenger classes and age groups.

## Project Structure

```text
Internship TASK 2/
├── Dataset/
│   └── titanic_train.csv
├── R_Scripts/
│   └── week2_visualizations.R
├── Outputs/
│   ├── Graphs/
│   └── Results/
├── Report/
│   ├── Week_2_Data_Visualization_Report.docx
│   └── create_week2_report.py
└── README.md
```

## How to Run

Install the required R packages:

```r
install.packages(c("ggplot2", "dplyr", "tidyr"))
```

Run the visualization script from the project directory:

```powershell
Rscript .\R_Scripts\week2_visualizations.R
```

Generate the Word report:

```powershell
python .\Report\create_week2_report.py
```

## Deliverables

- Six visualization images
- Three CSV result files
- Complete R source code
- Word internship report with explanations and interpretations

## Conclusion

This project demonstrates the use of R visualization libraries to convert raw data into meaningful graphical insights. It improves practical understanding of exploratory data analysis, data visualization, and insight communication.

**Submitted by: Sahil Jadhao**
