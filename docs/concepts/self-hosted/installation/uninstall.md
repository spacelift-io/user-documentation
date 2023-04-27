# Uninstalling

If you want to completely uninstall Spacelift, you can use the `uninstall.sh` script. Please be aware that this will completely remove your Spacelift database as well as any data stored in S3 buckets, so please make sure you either have backups or don't need any of your data.

To run the uninstall script, use the following command, specifying your AWS region:

```bash
./uninstall.sh -r <region>
```

For example:

```bash
./uninstall.sh -r us-east-1
```
