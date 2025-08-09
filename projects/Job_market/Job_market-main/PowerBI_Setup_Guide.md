# Power BI Dashboard Quick Setup Guide

## 🚀 Quick Start (5 Minutes)

### Step 1: Run Analysis
```bash
python simplified_analysis.py
```

### Step 2: Open Power BI Desktop
1. Launch Power BI Desktop
2. Click "Get Data" → "Text/CSV"
3. Navigate to `powerbi_exports/` folder
4. Import these key files:
   - `job_market_sample_data.csv` (main dataset)
   - `summary_metrics.csv` (KPIs)
   - `top_job_categories.csv` (charts)
   - `salary_analysis.csv` (insights)

### Step 3: Create Dashboard Pages

#### Page 1: Executive Summary
**KPI Cards:**
- Total Jobs: `summary_metrics[Value]` where `Metric = "Total Jobs"`
- Avg Salary: `summary_metrics[Value]` where `Metric = "Avg Salary"`
- Unique Companies: `summary_metrics[Value]` where `Metric = "Unique Companies"`

**Charts:**
- Job Categories: Bar chart using `top_job_categories.csv`
- Salary Distribution: Histogram using `job_market_sample_data[salary_year_avg]`

#### Page 2: Detailed Analysis
**Charts:**
- Jobs by Location: Bar chart using `top_locations.csv`
- Top Companies: Bar chart using `top_companies.csv`
- Salary by Job Category: Bar chart using `salary_analysis.csv`

### Step 4: Add Interactivity
1. Add slicers for:
   - Job Category (`job_title_short`)
   - Location (`job_location`)
   - Company (`company_name`)

2. Configure cross-filtering between visuals

## 📊 Key DAX Measures

### Basic Metrics
```dax
Total Jobs = COUNTROWS('job_market_sample_data')
Average Salary = AVERAGE('job_market_sample_data'[salary_year_avg])
Median Salary = MEDIAN('job_market_sample_data'[salary_year_avg])
```

### Advanced Metrics
```dax
High Paying Jobs = 
CALCULATE(
    COUNTROWS('job_market_sample_data'),
    'job_market_sample_data'[salary_year_avg] > 150000
)

Salary Percentile 75 = 
PERCENTILE.INC('job_market_sample_data'[salary_year_avg], 0.75)
```

## 🎨 Visual Recommendations

### Color Scheme
- Primary: #2E86AB (Blue)
- Secondary: #A23B72 (Purple) 
- Accent: #F18F01 (Orange)
- Success: #C73E1D (Green)

### Chart Types
- **KPIs**: Card visuals
- **Categories**: Horizontal bar charts
- **Trends**: Line charts
- **Distribution**: Histograms
- **Comparison**: Clustered bar charts

## 🔧 Tips for Best Results

1. **Data Refresh**: Set up automatic refresh if using live data
2. **Performance**: Use DirectQuery for large datasets
3. **Mobile**: Create mobile-optimized layouts
4. **Sharing**: Publish to Power BI Service for collaboration

## 📈 Sample Insights to Display

- "Data Analyst roles represent 25% of all job postings"
- "Average salary is $123K with 75th percentile at $150K"
- "Top 5 companies account for X% of total postings"
- "Remote work options available in Y% of positions"

---
*This guide gets you from data to dashboard in under 10 minutes!*
