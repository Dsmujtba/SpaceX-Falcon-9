# SpaceX Falcon 9 Launch Prediction Project

## Table of Contents
1. [Project Overview](#project-overview)
2. [Dataset Information](#dataset-information)
3. [Installation](#installation)
4. [Usage](#usage)
5. [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
6. [Machine Learning Models](#machine-learning-models)
7. [Results and Discussion](#results-and-discussion)
8. [Conclusion](#conclusion)
9. [Future Work](#future-work)
10. [Contributing](#contributing)
11. [License](#license)

## Project Overview
This project aims to analyze the SpaceX Falcon 9 launch data to understand various factors influencing the success of the launches. The project includes data cleaning, exploratory data analysis (EDA), and the implementation of multiple machine learning models to predict the success of future SpaceX launches. The models used are Logistic Regression, Support Vector Machine (SVM), Decision Tree, and K-Nearest Neighbors (KNN).

## Dataset Information
The dataset used for this project contains records of SpaceX Falcon 9 launches, including details such as launch date, launch site, payload mass, booster version, and launch outcome (success or failure).

- **Source**: [IBM Data Science Course Dataset](https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBM-DS0321EN-SkillsNetwork/datasets/spacex_launch_dash.csv)
- **Columns**:
  - `Flight Number`
  - `Launch Site`
  - `Payload Mass (kg)`
  - `Booster Version`
  - `Class` (1 for success, 0 for failure)

## Installation
To run this project, you need to have Python installed along with the required libraries. You can install the necessary dependencies using the following command:

```bash
pip install -r requirements.txt
```

**requirements.txt**:
```
pandas
numpy
scikit-learn
dash
plotly
```

## Usage
To use this project, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/spacex-falcon9-launch-analysis.git
   cd spacex-falcon9-launch-analysis
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the dashboard application:
   ```bash
   python app.py
   ```

4. Open your web browser and go to `http://127.0.0.1:8050/` to view the dashboard.

## Exploratory Data Analysis (EDA)
The EDA includes visualizations and statistical analysis to understand the distribution and relationships within the data. Key findings from the EDA include:

- Analysis of flight numbers across different launch sites.
- Distribution of payload masses.
- Success rates across different booster versions.

## Machine Learning Models
We implemented several machine learning models to predict the success of SpaceX Falcon 9 launches:

1. **Logistic Regression**:
   - Best performing model with AUC = 0.92.
   - High precision and recall.

2. **Support Vector Machine (SVM)**:
   - Good performance with AUC = 0.83.
   - Balanced true positive and false positive rates.

3. **Decision Tree**:
   - Moderate performance with AUC = 0.70.
   - Higher false positive rate compared to Logistic Regression and SVM.

4. **K-Nearest Neighbors (KNN)**:
   - Lowest performance with AUC = 0.67.
   - Lower true positive rate and higher false positive rate.

### Model Evaluation
- **Classification Report and Confusion Matrix**: Evaluated for Decision Tree, indicating precision, recall, and F1-score.
- **ROC Curve and AUC**: Evaluated for all models, with Logistic Regression performing the best.

## Results and Discussion
- **Logistic Regression** outperformed other models with an AUC of 0.92.
- The models help identify key factors contributing to the success of SpaceX Falcon 9 launches, such as payload mass and booster version.
- The analysis and models can aid SpaceX in improving their launch success rates.

## Conclusion
The project successfully demonstrates how data analysis and machine learning can be applied to real-world problems like predicting the success of SpaceX Falcon 9 launches. Logistic Regression proved to be the most effective model, providing valuable insights into the factors influencing launch success.

## Future Work
- Incorporate more features into the models, such as weather conditions and launch time.
- Use more advanced models like Random Forest and Gradient Boosting.
- Deploy the model as a web service for real-time predictions.

## Contributing
Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

