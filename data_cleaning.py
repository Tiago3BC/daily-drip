import pandas as pd

def clean_rain_data(input_path: str, output_path: str = None) -> pd.DataFrame:
    # Load with skiprows to ignore metadata rows
    df = pd.read_csv(input_path, header=9)

    # Rename columns
    df = df.rename(columns={
        'timestamp': 'Date/Hour',
        'Jardim de Belém Precipitation Total': 'Precipitation (mm)'
    })

    # Convert datetime and extract date/hour
    df['Date/Hour'] = pd.to_datetime(df['Date/Hour'])
    df['Date'] = df['Date/Hour'].dt.date
    df['Hour'] = df['Date/Hour'].dt.hour
    df.drop(columns=['Date/Hour'], inplace=True)
    df = df[['Date', 'Hour', 'Precipitation (mm)']]

    # Filter hours between 7am and 5pm
    df = df[(df['Hour'] >= 7) & (df['Hour'] <= 17)]

    # Group by date and sum precipitation
    df = df.groupby('Date').agg({'Precipitation (mm)': 'sum'}).reset_index()

    # Classify rain intensity
    def rain_intensity(mm):
        if mm == 0:
            return 'No Rain'
        elif mm <= 2.5:
            return 'Mild Rain'
        elif mm <= 10:
            return 'Moderate Rain'
        else:
            return 'Heavy Rain'

    df['Rain Intensity'] = df['Precipitation (mm)'].apply(rain_intensity)

    # Save if requested
    if output_path:
        df.to_csv(output_path, index=False)

    return df