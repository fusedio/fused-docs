@fused.udf
def single_job_udf(val):
    import pandas as pd
    return pd.DataFrame({'val':[val]})
    
# Run over 10 UDFs
job_pool = fused.submit(udf, [0,1,2,3,4,5,6,7,8,9])

# Retrieve your results
processed_df = job_pool.collect_df()