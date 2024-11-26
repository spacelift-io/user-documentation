---
description: Encryption reference documentation.
---

# Encryption

Spacelift requires an encryption key to store sensitive information in the Postgres database, as well as to sign tokens used for authenticating requests. Currently there are two options that can be used:

- KMS keys when deploying to AWS.
- An RSA key when deploying to other environments.

!!! warning
    Please be very careful with your encryption keys regardless of the option you use. If you choose to use KMS you cannot currently switch to an RSA key later, and vice-versa. If you lose access to your encryption key, you will lose access to any credentials and secrets encrypted using that key within Spacelift. Recovering from this will either require deleting and re-creating the affected items (stacks, contexts, VCS integrations, etc), or completely dropping your Spacelift database and re-creating it.

## Configuration

The following environment variables can be used to configure encryption:

| Environment variable               | Required  | Description                                              |
| ---------------------------------- | --------- | -------------------------------------------------------- |
| `ENCRYPTION_TYPE`                  | No        | Can be set to either `kms` or `rsa`. Defaults to `kms`.  |
| `ENCRYPTION_KMS_ENCRYPTION_KEY_ID` | For `kms` | The ID of the KMS key used for encryption.               |
| `ENCRYPTION_KMS_SIGNING_KEY_ID`    | For `kms` | The ID of the KMS key used for signing JWTs.             |
| `ENCRYPTION_RSA_PRIVATE_KEY`       | For `rsa` | An RSA private key in PEM format, encoded using base-64. |

## KMS

When using KMS, two keys are required:

- A key used for signing JWTs with a key usage of `SIGN_VERIFY` and a key spec of `RSA_4096`.
- A key used for encryption with a key usage of `ENCRYPT_DECRYPT` and a key spec of `SYMMETRIC_DEFAULT`.

!!! tip
    It is important to carefully choose between using a single-region or [multi-region KMS key](https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html) for the encryption key. KMS does not support changing a key from single to multi-region after key creation. Choosing a single-region key can prevent you from being able to switch Spacelift to another AWS region, or to configure a failover region.

## RSA

When using RSA, you need to generate an RSA private key that is not password protected. For example you could use the following openssl command:

```shell
openssl req -new -newkey rsa:4096 -nodes -keyout spacelift.key -subj "/CN=Spacelift RSA key"
```

The common name specified in the command above is purely informative and can be changed.

This RSA key is used to encrypt a symmetric AES-256 key that is generated during the initial setup. The encrypted AES key is then stored in the Postgres database.

This key is then used to perform cryptographic operations, such as encrypting and decrypting sensitive data entries in the database.

!!! info
    You need to encode the private key using base-64 before passing it to the `ENCRYPTION_RSA_PRIVATE_KEY` environment variable. The simplest approach is to just run `cat spacelift.key | base64 -w 0` in your command line. For Mac users, the command is `cat spacelift.key | base64 -b 0`.
