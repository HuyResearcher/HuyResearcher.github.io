"""
Analysis Utilities for Confectionery Sales Performance
Helper functions for data analysis and calculations
"""

import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

class AnalysisUtils:
    """Utility class for sales analysis calculations and data transformations"""
    
    @staticmethod
    def calculate_growth_rate(current_value, previous_value):
        """Calculate growth rate between two values"""
        if previous_value == 0 or pd.isna(previous_value):
            return np.nan
        return ((current_value - previous_value) / previous_value) * 100
    
    @staticmethod
    def calculate_cagr(start_value, end_value, years):
        """Calculate Compound Annual Growth Rate"""
        if start_value <= 0 or end_value <= 0 or years <= 0:
            return np.nan
        return ((end_value / start_value) ** (1/years) - 1) * 100
    
    @staticmethod
    def add_growth_metrics(df, value_col, time_col, group_cols=None):
        """Add growth rate columns to dataframe"""
        df = df.copy()
        df = df.sort_values(time_col)
        
        if group_cols:
            df['prev_value'] = df.groupby(group_cols)[value_col].shift(1)
        else:
            df['prev_value'] = df[value_col].shift(1)
        
        df['growth_rate'] = df.apply(
            lambda row: AnalysisUtils.calculate_growth_rate(row[value_col], row['prev_value']), 
            axis=1
        )
        
        return df.drop('prev_value', axis=1)
    
    @staticmethod
    def calculate_market_share(brand_revenue, total_market_revenue):
        """Calculate market share percentage"""
        if total_market_revenue == 0:
            return 0
        return (brand_revenue / total_market_revenue) * 100
    
    @staticmethod
    def get_seasonal_indices(df, date_col, value_col, freq='month'):
        """Calculate seasonal indices for the data"""
        df = df.copy()
        df[date_col] = pd.to_datetime(df[date_col])
        
        if freq == 'month':
            df['period'] = df[date_col].dt.month
        elif freq == 'quarter':
            df['period'] = df[date_col].dt.quarter
        else:
            raise ValueError("Frequency must be 'month' or 'quarter'")
        
        # Calculate average for each period
        period_avg = df.groupby('period')[value_col].mean()
        overall_avg = df[value_col].mean()
        
        # Calculate seasonal index
        seasonal_index = (period_avg / overall_avg) * 100
        
        return seasonal_index.to_dict()
    
    @staticmethod
    def perform_trend_analysis(df, time_col, value_col):
        """Perform trend analysis using linear regression"""
        df = df.copy()
        df = df.sort_values(time_col)
        
        # Convert time to numeric for regression
        df['time_numeric'] = pd.to_numeric(pd.to_datetime(df[time_col]))
        
        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            df['time_numeric'], df[value_col]
        )
        
        # Calculate trend line
        df['trend_line'] = slope * df['time_numeric'] + intercept
        
        trend_info = {
            'slope': slope,
            'intercept': intercept,
            'r_squared': r_value**2,
            'p_value': p_value,
            'trend_direction': 'Increasing' if slope > 0 else 'Decreasing' if slope < 0 else 'Stable',
            'significance': 'Significant' if p_value < 0.05 else 'Not Significant'
        }
        
        return df, trend_info
    
    @staticmethod
    def calculate_concentration_metrics(df, brand_col, value_col):
        """Calculate market concentration metrics"""
        brand_totals = df.groupby(brand_col)[value_col].sum().sort_values(ascending=False)
        total_market = brand_totals.sum()
        
        # Market shares
        market_shares = (brand_totals / total_market * 100).round(2)
        
        # Herfindahl-Hirschman Index
        hhi = (market_shares ** 2).sum()
        
        # Top 3 concentration ratio
        cr3 = market_shares.head(3).sum()
        
        return {
            'market_shares': market_shares.to_dict(),
            'hhi': hhi,
            'cr3': cr3,
            'market_concentration': 'High' if hhi > 2500 else 'Moderate' if hhi > 1500 else 'Low'
        }
    
    @staticmethod
    def identify_outliers(df, value_col, method='iqr', threshold=1.5):
        """Identify outliers in the data"""
        if method == 'iqr':
            Q1 = df[value_col].quantile(0.25)
            Q3 = df[value_col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            outliers = df[(df[value_col] < lower_bound) | (df[value_col] > upper_bound)]
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(df[value_col]))
            outliers = df[z_scores > threshold]
        else:
            raise ValueError("Method must be 'iqr' or 'zscore'")
        
        return outliers
    
    @staticmethod
    def calculate_performance_metrics(df, revenue_col, cost_col=None, units_col=None):
        """Calculate various performance metrics"""
        metrics = {}
        
        # Basic metrics
        metrics['total_revenue'] = df[revenue_col].sum()
        metrics['average_revenue'] = df[revenue_col].mean()
        metrics['median_revenue'] = df[revenue_col].median()
        metrics['revenue_std'] = df[revenue_col].std()
        metrics['revenue_cv'] = metrics['revenue_std'] / metrics['average_revenue']
        
        if cost_col:
            total_cost = df[cost_col].sum()
            metrics['total_cost'] = total_cost
            metrics['total_profit'] = metrics['total_revenue'] - total_cost
            metrics['profit_margin'] = (metrics['total_profit'] / metrics['total_revenue']) * 100
        
        if units_col:
            metrics['total_units'] = df[units_col].sum()
            metrics['average_price_per_unit'] = metrics['total_revenue'] / metrics['total_units']
        
        return metrics
    
    @staticmethod
    def create_summary_table(df, group_col, metrics_cols):
        """Create a summary table with key metrics by group"""
        summary = df.groupby(group_col).agg({
            col: ['sum', 'mean', 'count'] for col in metrics_cols
        }).round(2)
        
        # Flatten column names
        summary.columns = ['_'.join(col).strip() for col in summary.columns.values]
        
        return summary.reset_index()
    
    @staticmethod
    def calculate_rank_correlation(df, brand_col, metrics):
        """Calculate rank correlation between different metrics"""
        brand_metrics = df.groupby(brand_col)[metrics].sum()
        
        correlations = {}
        for i, metric1 in enumerate(metrics):
            for metric2 in metrics[i+1:]:
                # Calculate Spearman rank correlation
                corr, p_value = stats.spearmanr(brand_metrics[metric1], brand_metrics[metric2])
                correlations[f"{metric1}_vs_{metric2}"] = {
                    'correlation': corr,
                    'p_value': p_value,
                    'significance': 'Significant' if p_value < 0.05 else 'Not Significant'
                }
        
        return correlations
    
    @staticmethod
    def format_currency(amount, currency='VND'):
        """Format amount as currency"""
        if currency == 'VND':
            return f"{amount:,.0f} VND"
        elif currency == 'USD':
            return f"${amount:,.2f}"
        else:
            return f"{amount:,.2f} {currency}"
    
    @staticmethod
    def format_percentage(value, decimal_places=1):
        """Format value as percentage"""
        return f"{value:.{decimal_places}f}%"
    
    @staticmethod
    def format_large_numbers(value):
        """Format large numbers with appropriate suffixes"""
        if value >= 1e9:
            return f"{value/1e9:.1f}B"
        elif value >= 1e6:
            return f"{value/1e6:.1f}M"
        elif value >= 1e3:
            return f"{value/1e3:.1f}K"
        else:
            return f"{value:.0f}"

# Example usage and testing functions
def test_analysis_utils():
    """Test the analysis utility functions"""
    # Create sample data
    sample_data = pd.DataFrame({
        'brand': ['Brand A', 'Brand B', 'Brand C'] * 10,
        'year': list(range(2010, 2020)) * 3,
        'revenue': np.random.uniform(100000, 500000, 30),
        'cost': np.random.uniform(60000, 300000, 30),
        'units': np.random.uniform(1000, 5000, 30)
    })
    
    # Test growth rate calculation
    sample_data = AnalysisUtils.add_growth_metrics(
        sample_data, 'revenue', 'year', ['brand']
    )
    
    # Test performance metrics
    metrics = AnalysisUtils.calculate_performance_metrics(
        sample_data, 'revenue', 'cost', 'units'
    )
    
    print("Sample Analysis Results:")
    print(f"Total Revenue: {AnalysisUtils.format_currency(metrics['total_revenue'])}")
    print(f"Profit Margin: {AnalysisUtils.format_percentage(metrics['profit_margin'])}")
    
    # Test concentration metrics
    concentration = AnalysisUtils.calculate_concentration_metrics(
        sample_data, 'brand', 'revenue'
    )
    print(f"Market Concentration: {concentration['market_concentration']}")
    
    return sample_data, metrics, concentration

if __name__ == "__main__":
    test_analysis_utils()
