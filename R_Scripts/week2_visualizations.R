
# ============================================================
# WEEK 2: DATA VISUALIZATION AND INSIGHT COMMUNICATION
# Dataset: Titanic Passenger Dataset
# Author: Sahil Jadhao
# ============================================================

# 1. Load required libraries
library(ggplot2)
library(dplyr)
library(tidyr)

# 2. Set project paths
project_dir <- normalizePath(".", winslash = "/", mustWork = TRUE)

dataset_path <- file.path(
  project_dir, "Dataset", "titanic_train.csv"
)

graph_dir <- file.path(project_dir, "Outputs", "Graphs")
result_dir <- file.path(project_dir, "Outputs", "Results")

dir.create(graph_dir, recursive = TRUE, showWarnings = FALSE)
dir.create(result_dir, recursive = TRUE, showWarnings = FALSE)

# 3. Load dataset
titanic <- read.csv(
  dataset_path,
  stringsAsFactors = FALSE
)

cat("Dataset loaded successfully!\n")
cat("Rows:", nrow(titanic), "\n")
cat("Columns:", ncol(titanic), "\n")

# 4. Prepare visualization data
# Age is filled with the median for visualization.
titanic$Age[is.na(titanic$Age)] <-
  median(titanic$Age, na.rm = TRUE)

titanic$Embarked[is.na(titanic$Embarked)] <- "S"

titanic$Survival <- factor(
  titanic$Survived,
  levels = c(0, 1),
  labels = c("Did Not Survive", "Survived")
)

titanic$Sex <- factor(titanic$Sex)

titanic$Pclass <- factor(
  titanic$Pclass,
  levels = c(1, 2, 3),
  labels = c("First Class", "Second Class", "Third Class")
)

titanic$AgeGroup <- cut(
  titanic$Age,
  breaks = c(0, 12, 18, 35, 60, Inf),
  labels = c("Child", "Teenager", "Young Adult",
             "Adult", "Senior"),
  include.lowest = TRUE
)

# Consistent theme
professional_theme <- theme_minimal(base_size = 13) +
  theme(
    plot.title = element_text(
      face = "bold", size = 17
    ),
    plot.subtitle = element_text(
      size = 11, color = "gray40"
    ),
    axis.title = element_text(face = "bold"),
    legend.position = "bottom"
  )

# ============================================================
# CHART 1: SURVIVAL DISTRIBUTION - BAR CHART
# ============================================================

survival_data <- titanic %>%
  count(Survival)

p1 <- ggplot(
  survival_data,
  aes(x = Survival, y = n, fill = Survival)
) +
  geom_col(width = 0.6) +
  geom_text(
    aes(label = n),
    vjust = -0.5,
    fontface = "bold",
    size = 5
  ) +
  labs(
    title = "Titanic Passenger Survival Distribution",
    subtitle = "Number of passengers by survival outcome",
    x = "Survival Status",
    y = "Number of Passengers",
    fill = "Outcome"
  ) +
  scale_fill_manual(
    values = c("#D95F59", "#2A9D8F")
  ) +
  professional_theme

ggsave(
  file.path(graph_dir, "01_survival_distribution.png"),
  p1, width = 9, height = 6, dpi = 300
)

# ============================================================
# CHART 2: AGE DISTRIBUTION - HISTOGRAM
# ============================================================

p2 <- ggplot(
  titanic,
  aes(x = Age)
) +
  geom_histogram(
    binwidth = 5,
    fill = "#457B9D",
    color = "white"
  ) +
  labs(
    title = "Age Distribution of Titanic Passengers",
    subtitle = "Passenger ages grouped into five-year intervals",
    x = "Age (Years)",
    y = "Number of Passengers"
  ) +
  professional_theme

ggsave(
  file.path(graph_dir, "02_age_distribution.png"),
  p2, width = 9, height = 6, dpi = 300
)

# ============================================================
# CHART 3: AGE VS FARE - SCATTER PLOT
# ============================================================

p3 <- ggplot(
  titanic,
  aes(x = Age, y = Fare, color = Survival)
) +
  geom_point(alpha = 0.65, size = 2) +
  scale_color_manual(
    values = c("#D95F59", "#2A9D8F")
  ) +
  labs(
    title = "Relationship Between Passenger Age and Fare",
    subtitle = "Points are colored according to survival status",
    x = "Age (Years)",
    y = "Fare",
    color = "Survival Status"
  ) +
  professional_theme

ggsave(
  file.path(graph_dir, "03_age_vs_fare_scatter.png"),
  p3, width = 9, height = 6, dpi = 300
)

# ============================================================
# CHART 4: SURVIVAL RATE BY AGE GROUP - LINE CHART
# ============================================================

age_survival <- titanic %>%
  group_by(AgeGroup) %>%
  summarise(
    Total = n(),
    Survivors = sum(Survived),
    Survival_Rate = mean(Survived) * 100,
    .groups = "drop"
  )

p4 <- ggplot(
  age_survival,
  aes(
    x = AgeGroup,
    y = Survival_Rate,
    group = 1
  )
) +
  geom_line(
    color = "#6A4C93",
    linewidth = 1.2
  ) +
  geom_point(
    color = "#F4A261",
    size = 4
  ) +
  geom_text(
    aes(label = paste0(round(Survival_Rate, 1), "%")),
    vjust = -1
  ) +
  labs(
    title = "Survival Rate Across Passenger Age Groups",
    subtitle = "Percentage of passengers who survived in each age group",
    x = "Age Group",
    y = "Survival Rate (%)"
  ) +
  scale_y_continuous(limits = c(0, 100)) +
  professional_theme

ggsave(
  file.path(graph_dir, "04_survival_by_age_group.png"),
  p4, width = 9, height = 6, dpi = 300
)

# ============================================================
# CHART 5: FARE BY PASSENGER CLASS - BOXPLOT
# ============================================================

p5 <- ggplot(
  titanic,
  aes(x = Pclass, y = Fare, fill = Pclass)
) +
  geom_boxplot(outlier.alpha = 0.5) +
  labs(
    title = "Fare Distribution Across Passenger Classes",
    subtitle = "Comparison of ticket fare spread and outliers",
    x = "Passenger Class",
    y = "Fare",
    fill = "Class"
  ) +
  scale_fill_brewer(palette = "Set2") +
  professional_theme

ggsave(
  file.path(graph_dir, "05_fare_by_class_boxplot.png"),
  p5, width = 9, height = 6, dpi = 300
)

# ============================================================
# CHART 6: SURVIVAL RATE HEATMAP
# ============================================================

heatmap_data <- titanic %>%
  group_by(Pclass, AgeGroup) %>%
  summarise(
    Survival_Rate = mean(Survived) * 100,
    Passengers = n(),
    .groups = "drop"
  )

p6 <- ggplot(
  heatmap_data,
  aes(x = AgeGroup, y = Pclass, fill = Survival_Rate)
) +
  geom_tile(color = "white", linewidth = 1) +
  geom_text(
    aes(label = paste0(round(Survival_Rate, 1), "%")),
    size = 4
  ) +
  scale_fill_gradient(
    low = "#F4A261",
    high = "#264653",
    name = "Survival Rate (%)"
  ) +
  labs(
    title = "Titanic Survival Rate Heatmap",
    subtitle = "Survival percentage by age group and passenger class",
    x = "Age Group",
    y = "Passenger Class"
  ) +
  professional_theme

ggsave(
  file.path(graph_dir, "06_survival_heatmap.png"),
  p6, width = 10, height = 6, dpi = 300
)

# ============================================================
# 7. EXPORT ANALYSIS RESULTS
# ============================================================

write.csv(
  survival_data,
  file.path(result_dir, "survival_distribution.csv"),
  row.names = FALSE
)

write.csv(
  age_survival,
  file.path(result_dir, "survival_by_age_group.csv"),
  row.names = FALSE
)

write.csv(
  heatmap_data,
  file.path(result_dir, "survival_heatmap_data.csv"),
  row.names = FALSE
)

# ============================================================
# 8. DISPLAY COMPLETION MESSAGE
# ============================================================

cat("\n====================================\n")
cat("WEEK 2 VISUALIZATION COMPLETED!\n")
cat("====================================\n")

cat("Graphs generated: 6\n")
cat("Results exported: 3 CSV files\n")
cat("Graph folder:", graph_dir, "\n")
cat("Results folder:", result_dir, "\n")

cat("\nSurvival by age group:\n")
print(age_survival)

cat("\nSurvival heatmap data:\n")
print(heatmap_data)
