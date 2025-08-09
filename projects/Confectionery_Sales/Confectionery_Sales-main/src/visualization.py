"""
Visualization Module for Confectionery Sales Analysis
Functions for creating charts and graphs for sales performance analysis
"""

import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Set style for matplotlib plots
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class SalesVisualization:
    """Class for creating various sales analysis visualizations"""
    
    def __init__(self, figsize=(12, 8), dpi=100):
        self.figsize = figsize
        self.dpi = dpi
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']
        
    def plot_revenue_trend(self, df, save_path=None):
        """Plot revenue trend by brand over years"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        brands = df['brand_name'].unique()
        for i, brand in enumerate(brands):
            brand_data = df[df['brand_name'] == brand]
            ax.plot(brand_data['year'], brand_data['total_revenue'], 
                   marker='o', linewidth=2, label=brand, color=self.colors[i])
        
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Total Revenue (VND)', fontsize=12)
        ax.set_title('Revenue Trend by Brand (2010-2020)', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Format y-axis to show values in billions
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e9:.1f}B'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        return fig
    
    def plot_market_share(self, df, save_path=None):
        """Plot market share evolution over time"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        brands = df['brand_name'].unique()
        for i, brand in enumerate(brands):
            brand_data = df[df['brand_name'] == brand]
            ax.plot(brand_data['year'], brand_data['avg_market_share'], 
                   marker='s', linewidth=2, label=brand, color=self.colors[i])
        
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('Market Share (%)', fontsize=12)
        ax.set_title('Market Share Evolution (2010-2020)', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_ylim(0, max(df['avg_market_share']) * 1.1)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        return fig
    
    def plot_seasonal_patterns(self, df, save_path=None):
        """Plot seasonal sales patterns by quarter"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        pivot_data = df.pivot(index='quarter', columns='brand_name', values='avg_quarterly_revenue')
        pivot_data.plot(kind='bar', ax=ax, color=self.colors[:len(pivot_data.columns)])
        
        ax.set_xlabel('Quarter', fontsize=12)
        ax.set_ylabel('Average Quarterly Revenue (VND)', fontsize=12)
        ax.set_title('Seasonal Sales Patterns by Brand', fontsize=14, fontweight='bold')
        ax.legend(title='Brand')
        ax.set_xticklabels(['Q1', 'Q2', 'Q3', 'Q4'], rotation=0)
        
        # Format y-axis
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e6:.0f}M'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        return fig
    
    def plot_product_performance(self, df, top_n=10, save_path=None):
        """Plot top performing products by revenue"""
        top_products = df.nlargest(top_n, 'total_revenue')
        
        fig, ax = plt.subplots(figsize=(14, 8), dpi=self.dpi)
        
        bars = ax.barh(range(len(top_products)), top_products['total_revenue'], 
                      color=plt.cm.viridis(np.linspace(0, 1, len(top_products))))
        
        ax.set_yticks(range(len(top_products)))
        ax.set_yticklabels([f"{row['brand_name']}\n{row['product_name']}" 
                           for _, row in top_products.iterrows()])
        ax.set_xlabel('Total Revenue (VND)', fontsize=12)
        ax.set_title(f'Top {top_n} Products by Revenue (2010-2020)', fontsize=14, fontweight='bold')
        
        # Add value labels on bars
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width, bar.get_y() + bar.get_height()/2, 
                   f'{width/1e9:.1f}B', ha='left', va='center', fontsize=10)
        
        ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e9:.1f}B'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        return fig
    
    def plot_category_analysis(self, df, save_path=None):
        """Plot category performance analysis"""
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8), dpi=self.dpi)
        
        # Revenue by category (stacked bar)
        pivot_revenue = df.pivot(index='brand_name', columns='category_name', values='total_revenue')
        pivot_revenue.plot(kind='bar', stacked=True, ax=ax1, color=plt.cm.Set3.colors)
        ax1.set_title('Revenue by Product Category', fontsize=14, fontweight='bold')
        ax1.set_xlabel('Brand', fontsize=12)
        ax1.set_ylabel('Total Revenue (VND)', fontsize=12)
        ax1.legend(title='Category', bbox_to_anchor=(1.05, 1), loc='upper left')
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e9:.1f}B'))
        
        # Market share by category (pie chart)
        category_totals = df.groupby('category_name')['total_revenue'].sum()
        ax2.pie(category_totals.values, labels=category_totals.index, autopct='%1.1f%%')
        ax2.set_title('Market Share by Category', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        return fig
    
    def plot_growth_analysis(self, df, save_path=None):
        """Plot year-over-year growth analysis"""
        # Filter out NaN growth rates
        df_clean = df.dropna(subset=['yoy_growth_rate'])
        
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        brands = df_clean['brand_name'].unique()
        for i, brand in enumerate(brands):
            brand_data = df_clean[df_clean['brand_name'] == brand]
            ax.plot(brand_data['year'], brand_data['yoy_growth_rate'], 
                   marker='o', linewidth=2, label=brand, color=self.colors[i])
        
        ax.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax.set_xlabel('Year', fontsize=12)
        ax.set_ylabel('YoY Growth Rate (%)', fontsize=12)
        ax.set_title('Year-over-Year Growth Rate by Brand', fontsize=14, fontweight='bold')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        return fig
    
    def plot_regional_performance(self, df, save_path=None):
        """Plot regional sales performance"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        pivot_data = df.pivot(index='region', columns='brand_name', values='total_revenue')
        pivot_data.plot(kind='bar', ax=ax, color=self.colors[:len(pivot_data.columns)])
        
        ax.set_xlabel('Region', fontsize=12)
        ax.set_ylabel('Total Revenue (VND)', fontsize=12)
        ax.set_title('Regional Sales Performance by Brand', fontsize=14, fontweight='bold')
        ax.legend(title='Brand')
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        
        ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{x/1e9:.1f}B'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        return fig
    
    def create_interactive_dashboard(self, revenue_df, market_share_df, save_path=None):
        """Create interactive Plotly dashboard"""
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Revenue Trend', 'Market Share Evolution', 
                          'Revenue Comparison', 'Growth Rates'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Revenue trend
        brands = revenue_df['brand_name'].unique()
        for brand in brands:
            brand_data = revenue_df[revenue_df['brand_name'] == brand]
            fig.add_trace(
                go.Scatter(x=brand_data['year'], y=brand_data['total_revenue'],
                          mode='lines+markers', name=f'{brand} Revenue'),
                row=1, col=1
            )
        
        # Market share evolution
        for brand in brands:
            if brand in market_share_df['brand_name'].values:
                brand_data = market_share_df[market_share_df['brand_name'] == brand]
                fig.add_trace(
                    go.Scatter(x=brand_data['year'], y=brand_data['avg_market_share'],
                              mode='lines+markers', name=f'{brand} Market Share'),
                    row=1, col=2
                )
        
        # Total revenue comparison (bar chart)
        total_revenue_by_brand = revenue_df.groupby('brand_name')['total_revenue'].sum()
        fig.add_trace(
            go.Bar(x=total_revenue_by_brand.index, y=total_revenue_by_brand.values,
                   name='Total Revenue'),
            row=2, col=1
        )
        
        fig.update_layout(height=800, showlegend=True, 
                         title_text="Confectionery Sales Dashboard")
        
        if save_path:
            fig.write_html(save_path)
        
        return fig
    
    def plot_correlation_heatmap(self, df, metrics_cols, save_path=None):
        """Plot correlation heatmap of different metrics"""
        correlation_matrix = df[metrics_cols].corr()
        
        fig, ax = plt.subplots(figsize=(10, 8), dpi=self.dpi)
        
        sns.heatmap(correlation_matrix, annot=True, cmap='RdBu_r', center=0,
                   square=True, ax=ax, cbar_kws={'shrink': .8})
        
        ax.set_title('Correlation Matrix of Sales Metrics', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, bbox_inches='tight')
        
        return fig
    
    def save_all_plots(self, data_dict, output_dir='reports/charts'):
        """Save all plots to specified directory"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        plots_created = []
        
        # Revenue trend
        if 'revenue_trend' in data_dict:
            fig = self.plot_revenue_trend(data_dict['revenue_trend'])
            save_path = output_path / 'revenue_trend.png'
            fig.savefig(save_path, bbox_inches='tight')
            plots_created.append(str(save_path))
            plt.close(fig)
        
        # Market share
        if 'market_share' in data_dict:
            fig = self.plot_market_share(data_dict['market_share'])
            save_path = output_path / 'market_share.png'
            fig.savefig(save_path, bbox_inches='tight')
            plots_created.append(str(save_path))
            plt.close(fig)
        
        # Seasonal patterns
        if 'seasonal' in data_dict:
            fig = self.plot_seasonal_patterns(data_dict['seasonal'])
            save_path = output_path / 'seasonal_patterns.png'
            fig.savefig(save_path, bbox_inches='tight')
            plots_created.append(str(save_path))
            plt.close(fig)
        
        # Product performance
        if 'product_performance' in data_dict:
            fig = self.plot_product_performance(data_dict['product_performance'])
            save_path = output_path / 'product_performance.png'
            fig.savefig(save_path, bbox_inches='tight')
            plots_created.append(str(save_path))
            plt.close(fig)
        
        return plots_created

# Example usage
def demo_visualization():
    """Demonstrate visualization capabilities with sample data"""
    # Create sample data
    years = list(range(2010, 2021))
    brands = ['Orion Food Vina', 'Kido', 'Kinh Do']
    
    sample_revenue = pd.DataFrame([
        {'brand_name': brand, 'year': year, 'total_revenue': np.random.uniform(1e9, 5e9)}
        for brand in brands for year in years
    ])
    
    sample_market_share = pd.DataFrame([
        {'brand_name': brand, 'year': year, 'avg_market_share': np.random.uniform(20, 40)}
        for brand in brands for year in years
    ])
    
    # Create visualizations
    viz = SalesVisualization()
    
    # Revenue trend
    fig1 = viz.plot_revenue_trend(sample_revenue)
    plt.show()
    
    # Market share
    fig2 = viz.plot_market_share(sample_market_share)
    plt.show()
    
    return sample_revenue, sample_market_share

if __name__ == "__main__":
    demo_visualization()
