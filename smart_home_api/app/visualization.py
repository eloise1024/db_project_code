import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import List, Dict

def create_usage_duration_bar_chart(device_id: str, durations: Dict[str, float]):
    df = pd.DataFrame({
        "Period": ["Day", "Week", "Month", "Year"],
        "Duration (seconds)": [durations.get("day", 0), durations.get("week", 0), durations.get("month", 0), durations.get("year", 0)]
    })
    fig = px.bar(df, x="Period", y="Duration (seconds)", title=f"Usage Duration for Device {device_id}")
    return fig.to_json()

def create_time_distribution_bar_chart(device_id: str, data: Dict):
    df = pd.DataFrame({
        "Time Slot": data["hours"],
        "Duration (seconds)": data["counts"]
    })
    fig = px.bar(df, x="Time Slot", y="Duration (seconds)", title=f"Time Distribution for Device {device_id}")
    return fig.to_json()

def create_correlation_chord_chart(primary_device_id: str, correlations: Dict[str, float]):
    labels = [primary_device_id] + list(correlations.keys())
    source = [0] * len(correlations)
    target = list(range(1, len(correlations) + 1))
    values = list(correlations.values())
    
    fig = go.Figure(data=[go.Sankey(
        node=dict(label=labels),
        link=dict(source=source, target=target, value=values)
    )])
    fig.update_layout(title_text=f"Device Usage Correlation with {primary_device_id}")
    return fig.to_json()

def create_area_usage_scatter_chart(device_type: str, data: List[Dict]):
    df = pd.DataFrame(data)
    fig = px.scatter(df, x="area", y="avg_usage", title=f"Area vs. {device_type} Usage")
    return fig.to_json()

def create_event_distribution_pie_chart(data: List[Dict], home_id: str = None):
    df = pd.DataFrame(data)
    title = f"Security Event Distribution {'for Home ' + home_id if home_id else 'System-Wide'}"
    fig = px.pie(df, names="device_type", values="count", title=title)
    return fig.to_json()

def create_feedback_distribution_pie_chart(data: List[Dict]):
    df = pd.DataFrame(data)
    fig = px.pie(df, names="device_type", values="count", title="Feedback Distribution by Device Type")
    return fig.to_json()