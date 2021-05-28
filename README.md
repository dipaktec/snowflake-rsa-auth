# snowflake-rsa-auth
This captures details on how to use Key Pairs to connect to Snowflake using PySpark.

## Background and Scope
Snowflake data can be accessed from different Snowflake clients(e.g. SnowSQL CLI, JDBC Driver, Snowflake Connector for Spark etc.) For more details on Snowflake connector & driver use this [link](https://docs.snowflake.com/en/user-guide/conns-drivers.html).

While Snowflake allows basic authentication, for enhance security it supports Key Pair(RSA) authentication.

This guide is to show how quickly we can build a pyspark application to do so.

## Prerequisites

- An Account in Snowflake (you can use [free tier](https://signup.snowflake.com/) for 30 days)
- Spark installtion completed
- Spark Snowflake connector are installed
- Any IDE/text editor to build pyspark code


## Steps

__1. Generate Private Key__

Snowflake allows using both encrypted and unencrypted keys, but some clients(SnowSQL CLI) need encrypted keys only. Also encrypted keys are recommended. Here we will use Openssl to create these keys.

  - __Create Unencrypted key__
  
  ```sh
  $ openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out sf_rsa_key.p8 -nocrypt
  ```
  - __Create Encrypted key__
  
  ```sh
  $ openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out sf_rsa_key.p8
  ```
  
__2. Generate Public Key__

This steps creates public key using the private key.

```sh
openssl rsa -in sf_rsa_key.p8 -pubout -out sf_rsa_key.pub
```

__3. Assign public key to Snowflake user

Open the public key file in a text editor(I have used VSCode) and copy the key. Then execute below from Snowflake UI or CLI.

```sh
alter user <username> set RSA_PUBLIC_KEY = '<key-value>;
```
__4. Veirfy

Use below command to verify that public key is added.

```sh
desc user <username>
```

![image](https://user-images.githubusercontent.com/67356200/119945219-c51e6f00-bf5a-11eb-84bf-81e0d72ae094.png)


__5. Configure Snowflake Client(in this case PySpark script) to use RSA authentication
<<to be added>>

## Key points to note
- This authentication method requires, as a minimum, a 2048-bit RSA key pair
- Snowflake supports uninterrupted rotation of public keys, uses two RSA Public Key properties to do same
- Creating encrypted private key, requires using a passphrase. Snowflake recommens PCI DSS standard to generate the passphrase.







