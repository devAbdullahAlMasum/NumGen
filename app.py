import streamlit as st
import time
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from src.RandomPicker import RandomPicker
import numpy as np
import statistics

def initialize_session_state():
    if 'history' not in st.session_state:
        st.session_state.history = []
    if 'picker' not in st.session_state:
        st.session_state.picker = None

def create_distribution_plot(numbers, start, end):
    df = pd.DataFrame({'Generated Numbers': numbers})
    fig = px.histogram(
        df,
        x='Generated Numbers',
        nbins=min(30, end-start+1),
        title='Distribution of Generated Numbers',
        labels={'Generated Numbers': 'Number', 'count': 'Frequency'}
    )
    fig.update_layout(
        showlegend=False,
        xaxis_range=[start-1, end+1]
    )
    return fig

def create_heatmap(numbers, start, end, num_bins=10):
    bins = np.linspace(start, end, num_bins + 1)
    hist, _ = np.histogram(numbers, bins=bins)

    # Create heatmap data
    ranges = [f'{int(bins[i])}-{int(bins[i+1])}' for i in range(len(bins)-1)]

    fig = go.Figure(data=[
        go.Bar(
            x=ranges,
            y=hist,
            text=[f'{(count/len(numbers)*100):.1f}%' for count in hist],
            textposition='outside'
        )
    ])

    fig.update_layout(
        title='Distribution Heatmap',
        xaxis_title='Number Range',
        yaxis_title='Frequency',
        showlegend=False
    )

    return fig

def create_sequence_plot(numbers):
    df = pd.DataFrame({
        'Index': range(1, len(numbers) + 1),
        'Value': numbers
    })
    fig = px.line(
        df,
        x='Index',
        y='Value',
        title='Sequence of Generated Numbers'
    )
    return fig

def create_difference_plot(numbers):
    differences = [0] + [numbers[i] - numbers[i-1] for i in range(1, len(numbers))]
    df = pd.DataFrame({
        'Index': range(1, len(differences) + 1),
        'Difference': differences
    })
    fig = px.bar(
        df,
        x='Index',
        y='Difference',
        title='Differences Between Consecutive Numbers'
    )
    return fig

def safe_statistics(numbers):
    """Calculate statistics safely with error handling"""
    stats = {
        'count': len(numbers),
        'mean': 'N/A',
        'median': 'N/A',
        'std_dev': 'N/A',
        'min': 'N/A',
        'max': 'N/A',
        'mode': 'N/A',
        'unique': 0
    }

    if numbers:
        stats['mean'] = f"{sum(numbers)/len(numbers):.2f}"
        stats['min'] = min(numbers)
        stats['max'] = max(numbers)
        stats['unique'] = len(set(numbers))

        if len(numbers) >= 2:
            stats['std_dev'] = f"{statistics.stdev(numbers):.2f}"
            stats['median'] = f"{statistics.median(numbers):.2f}"

            try:
                stats['mode'] = f"{statistics.mode(numbers)}"
            except statistics.StatisticsError:
                stats['mode'] = "Multiple modes"

    return stats

def main():
    st.title("NumGen - Advanced Random Number Generator")
    st.write("This application demonstrates a complex random number generation system with multiple layers of randomness.")

    # Initialize session state
    initialize_session_state()

    # Sidebar controls
    st.sidebar.header("Configuration")

    start = st.sidebar.number_input("Start Range", value=1)
    end = st.sidebar.number_input("End Range", value=100)

    if start >= end:
        st.error("Start range must be less than end range!")
        return

    # Initialize or reinitialize picker if range changes
    if (st.session_state.picker is None or
        st.session_state.picker.start != start or
        st.session_state.picker.end != end):
        st.session_state.picker = RandomPicker(start, end)
        st.session_state.history = []

    # Main content
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Generate Single Number"):
            with st.spinner("Generating..."):
                number = st.session_state.picker.pick()
                st.session_state.history.append(number)
                st.success(f"Generated Number: {number}")

    with col2:
        num_multiple = st.number_input("Generate Multiple Numbers",
                                     min_value=1, max_value=1000, value=10)
        if st.button(f"Generate {num_multiple} Numbers"):
            progress_bar = st.progress(0)
            for i in range(num_multiple):
                number = st.session_state.picker.pick()
                st.session_state.history.append(number)
                progress_bar.progress((i + 1) / num_multiple)
            st.success(f"Generated {num_multiple} numbers!")

    # Display analysis if we have numbers
    if st.session_state.history:
        st.header("Results Analysis")

        # Calculate statistics safely
        stats = safe_statistics(st.session_state.history)

        # Statistics display
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Count", stats['count'])
        with col2:
            st.metric("Mean", stats['mean'])
        with col3:
            st.metric("Median", stats['median'])
        with col4:
            st.metric("Std Dev", stats['std_dev'])

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Min", stats['min'])
        with col2:
            st.metric("Max", stats['max'])
        with col3:
            st.metric("Mode", stats['mode'])
        with col4:
            st.metric("Unique Numbers", stats['unique'])

        # Visualizations
        if len(st.session_state.history) >= 2:
            st.subheader("Distribution Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_distribution_plot(st.session_state.history, start, end), use_container_width=True)
            with col2:
                st.plotly_chart(create_heatmap(st.session_state.history, start, end), use_container_width=True)

            st.subheader("Sequence Analysis")
            col1, col2 = st.columns(2)
            with col1:
                st.plotly_chart(create_sequence_plot(st.session_state.history), use_container_width=True)
            with col2:
                st.plotly_chart(create_difference_plot(st.session_state.history), use_container_width=True)

        # History table
        st.subheader("Generation History")
        history_df = pd.DataFrame({
            'Index': range(1, len(st.session_state.history) + 1),
            'Generated Number': st.session_state.history,
            'Running Mean': [sum(st.session_state.history[:i+1])/(i+1)
                           for i in range(len(st.session_state.history))]
        })

        if len(st.session_state.history) >= 2:
            history_df['Distance from Mean'] = [
                abs(x - float(stats['mean']))
                for x in st.session_state.history
            ]

        st.dataframe(history_df)

        # Clear history button
        if st.button("Clear History"):
            st.session_state.history = []
            st.rerun()

    # Technical details
    with st.expander("Technical Details"):
        st.write("""
        This random number generator uses multiple layers of complexity:
        1. **Segmented Pool**: Numbers are organized in segments with strategic gaps
        2. **Multiple Data Structures**: Uses Min-Heap, Max-Heap, and Custom Deque
        3. **Bitwise Transformations**: XOR, shifts, rotations, and bit swapping
        4. **Mathematical Transformations**: Prime numbers, trigonometry, and exponentials
        5. **Cryptographic Hashing**: Multiple rounds of SHA-256, SHA-512, and BLAKE2b
        """)

if __name__ == "__main__":
    main()
