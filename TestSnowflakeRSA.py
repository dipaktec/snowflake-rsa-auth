#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 28 12:15:55 2021

@author: dipak
"""

from pyspark.sql import SparkSession

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

import os
import re

# access private key
with open(".../sf_rsa_key.p8", "rb") as key_file:
  sf_private_key = serialization.load_pem_private_key(
    key_file.read(),
    password = os.environ['PRIVATE_KEY_PASSWORD'].encode(),
    backend = default_backend()
    )

#serialize the key
  sf_pkb = private_key.private_bytes(
  encoding = serialization.Encoding.PEM,
  format = serialization.PrivateFormat.PKCS8,
  encryption_algorithm = serialization.NoEncryption()
  )
  
 #remove unwanted strings from the key
  sf_pkb = sf_pkb.decode("UTF-8")
  sf_pkb = re.sub("-*(BEGIN|END) PRIVATE KEY-*\n","",sf_pkb).replace("\n","")

 #Build Spark Session
spark = SparkSession\
            .builder\
            .appName("SnowflakeRSA")\
            .getOrCreate()    

#Build Snowflake Context
sfOptions = {
  "sfURL" : "<Snowflake account name, region, provider>.snowflakecomputing.com",
  "sfAccount" : "<Snowflake account name>",
  "sfUser" : "<Snowflake user name>",
  "pem_private_key" : sf_pkb,
  "sfDatabase" : "<Snowflake Database Name>",
  "sfSchema" : "<Snowflake Schema>",
  "sfWarehouse" : "<Snowflake WH>",
}

SNOWFLAKE_SOURCE_NAME = "net.snowflake.spark.snowflake"

#connect to Snowflake from Spark and read data
df = spark.read.format(SNOWFLAKE_SOURCE_NAME) \
   .options(**sfOptions) \
   .option("query",  "select * from <table name>") \
   .load()

df.printSchema()
df.show()



