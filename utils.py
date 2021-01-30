import pandas as pd

def load():
    df = pd.read_csv('preprocessed.csv', index_col=0)
    drop_cols = ["('Applied')", "('Admitted')", "('SIRed')"]
    applied = df[~pd.isna(df["('Applied')"])].drop(columns=drop_cols)
    admitted = df[~pd.isna(df["('Admitted')"])].drop(columns=drop_cols)
    committed = df[~pd.isna(df["('SIRed')"])].drop(columns=drop_cols)
    return applied, admitted, committed

applied, admitted, committed = load()

def group(data, categories):
    filtered = data.copy()
    filtered['admit_rate'] = filtered['admit_rate'] * filtered['count']
    filtered['yield_rate'] = filtered['admit_rate'] * filtered['count']
    filtered = filtered[filtered['count'] != 0]
    weighted_average = lambda x: round(sum(x) / sum(filtered.loc[x.index, "count"]), 2)
    filtered = filtered.groupby(categories).agg({
        'admit_rate': weighted_average,
        'yield_rate': weighted_average,
        'count': 'sum'
    }).reset_index()
    return filtered


def merge(a, b, c, cols):
    ab = pd.merge(a, b, on=cols, how='outer').rename(columns={
        'count_x': 'applied',
        'count_y': 'admitted'
    })[cols + ['applied', 'admitted']]
    abc = pd.merge(ab, c, on=cols, how='outer').rename(columns={
        'count': 'committed'
    })[cols + ['applied', 'admitted', 'committed']]
    abc['admit_rate'] = round(abc['admitted'] / abc['applied'], 4)
    abc['yield_rate'] = round(abc['committed'] / abc['admitted'], 4)
    abc = abc.fillna(0)
    return abc

def query(cols, filters={}):
    """
    cols: ['ethnicity_l1', 'ethnicity_l2', ...]
    filters: [
        ['year': ['2015', '2016'],
        'major': ['Computer Science']]
    ]
    """
    
    dss = [applied, admitted, committed]
    results = []
    for ds in dss:
        for index, values in filters.items():
            ds = ds[ds[index].isin(values)]
        results.append(group(ds, cols))
    
    a, b, c = results[0], results[1], results[2]
    return merge(a, b, c, cols)