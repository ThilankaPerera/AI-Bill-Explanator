import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, List
import pandas as pd


class Visualizer:
    """Create visualizations for bill data"""
    
    @staticmethod
    def create_pie_chart(charges_summary: Dict) -> go.Figure:
        """Create a pie chart of charge categories"""
        if not charges_summary:
            return None
        
        labels = list(charges_summary.keys())
        values = list(charges_summary.values())
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=values,
            hole=0.3,
            marker=dict(colors=px.colors.qualitative.Set3)
        )])
        
        fig.update_layout(
            title="Bill Breakdown by Category",
            font=dict(size=14),
            showlegend=True,
            height=400
        )
        
        return fig
    
    @staticmethod
    def create_bar_chart(charges_summary: Dict) -> go.Figure:
        """Create a bar chart of charges"""
        if not charges_summary:
            return None
        
        df = pd.DataFrame(list(charges_summary.items()), 
                         columns=['Category', 'Amount'])
        df = df.sort_values('Amount', ascending=False)
        
        fig = go.Figure(data=[go.Bar(
            x=df['Category'],
            y=df['Amount'],
            marker=dict(
                color=df['Amount'],
                colorscale='Viridis',
                showscale=True
            ),
            text=df['Amount'].apply(lambda x: f'Rs. {x:,.2f}'),
            textposition='auto'
        )])
        
        fig.update_layout(
            title="Charges Comparison",
            xaxis_title="Category",
            yaxis_title="Amount (LKR)",
            font=dict(size=12),
            height=400,
            showlegend=False
        )
        
        return fig
    
    