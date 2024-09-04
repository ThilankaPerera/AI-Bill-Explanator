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
    
    