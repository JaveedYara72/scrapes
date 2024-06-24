from typing import Final,Dict,Tuple
from pyspark.sql.session import SparkSession
from pyspark.sql import DataFrame as SDF
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, ArrayType


def rename_dataframe_cols(df:SDF, col_names:Dict[str,str]) -> SDF:
    """
    Rename all columns in dataframe
    """

    return df.select(*[col(col_name).alias(col_names.get(col_name,col_name)) for col_name in df.columns])