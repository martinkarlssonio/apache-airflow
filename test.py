import polars as pl
from datetime import datetime, timedelta
import random

dfSize = 1000
timestampList = [datetime.now() - timedelta(minutes=i) for i in range(dfSize)]
idList = [random.randint(1, 5) for _ in range(dfSize)]
valueList = [random.randint(10, 50) for _ in range(dfSize)]
groupList = [random.choice(['A', 'B']) for _ in range(dfSize)]

df = pl.DataFrame({
    'id': idList,
    'timestamp': timestampList,
    'value': valueList,
    'group': groupList
})

# Make sure to use "1h" for truncating to the nearest hour
df = df.with_columns(
    pl.col('timestamp').dt.truncate("1h").alias('timestamp_hour')
)

# Example of a grouping and aggregation after truncation
aggregated_df = df.groupby(['group', 'id', 'timestamp_hour']).agg(
    [pl.col('value').mean().alias('average_value')]
)

print(aggregated_df)
