---
description: Information about deploying Spacelift with custom requirements.
---

# Advanced Installations

## Custom VPC

In certain situations you may want to have full control of the network that Spacelift runs in, and the default VPC and security groups created by Spacelift don't fit your circumstances. In these situations, you can create your own networking components and supply them during the installation process.

If you choose to do this, you will need to create the following resources:

- A VPC.
- A set of private subnets.
- A set of public subnets (the same subnets IDs can be used if you don't need separate private and public subnets).
- Security groups for the various Spacelift components.

The following sections explain the requirements for each component.

Also, see the section on [HTTP Proxies](#http-proxies) if you need to use a proxy to allow the Spacelift components to make HTTP requests.

### VPC

The VPC needs to have a CIDR block large enough to run the Spacelift server and drain instances along with the database and a few other networking components. We would recommend using a minimum network prefix of `/27`.

### Private Subnets

The number of private subnets depends on the number of availability zones you want to deploy Spacelift to.

### Public Subnets

The public subnets are used to place the load balancer for the Spacelift server. If you don't need separate public and private subnets you can use the same subnets for both. Just use the same subnet IDs to populate both the private and public subnet configuration options.

### Security Groups

Security groups need to be created for the following components:

- Drain.
- Server.
- Load Balancer.
- Installation Task.
- Database.

The next sections explain the requirements of each group.

#### Drain

Needs to be able to access the following components:

- Your VCS system (e.g. GitHub, GitLab, etc).
- Various AWS APIs.
- The Spacelift database.

Our default CloudFormation template for the drain security group looks like the following, and allows unrestricted egress (for accessing VCS systems):

```yaml
DrainSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupName: "drain_sg"
    GroupDescription: "The security group for the Spacelift async-processing service"
    SecurityGroupEgress:
      - Description: "Unrestricted egress"
        FromPort: 0
        ToPort: 0
        IpProtocol: "-1"
        CidrIp: "0.0.0.0/0"
    VpcId: {Ref: VPC}
```

#### Server

Needs to be able to access the following components:

- Your VCS system (e.g. GitHub, GitLab, etc).
- Your identity provider for SSO.
- Various AWS APIs.
- The Spacelift database.

The server also needs to allow ingress from its load balancer.

Our default CloudFormation template for the server security group looks like the following, and allows unrestricted egress along with ingress via the load balancer:

```yaml
ServerSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupName: "server_sg"
    GroupDescription: "The security group for the Spacelift HTTP server"
    SecurityGroupEgress:
      - Description: "Unrestricted egress"
        FromPort: 0
        ToPort: 0
        IpProtocol: "-1"
        CidrIp: "0.0.0.0/0"
    SecurityGroupIngress:
      - Description: "Only accept HTTP connections on port 1983 from the load balancer"
        FromPort: 1983
        ToPort: 1983
        IpProtocol: "tcp"
        SourceSecurityGroupId: {Ref: LoadBalancerSecurityGroup}
    VpcId: {Ref: VPC}
```

#### Load Balancer

The load balancer needs to be able to accept traffic from any clients (e.g. users logging into Spacelift via a browser or using `spacectl`), and also needs to accept incoming webhooks from your VCS system. In addition it needs to be able to access the server container.

Our default CloudFormation template for the load balancer security group looks like the following:

```yaml
LoadBalancerSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupName: "load_balancer_sg"
    GroupDescription: "The security group for the load balancer sitting in front of the Spacelift HTTP server"
    SecurityGroupIngress:
      - Description: "Accept HTTPS connections on port 443"
        FromPort: 443
        ToPort: 443
        IpProtocol: "tcp"
        CidrIp: "0.0.0.0/0"
    VpcId: {Ref: VPC}

LoadBalancerToServerEgress:
  Type: AWS::EC2::SecurityGroupEgress
  Properties:
    Description: "Allow the server load balancer to access server app containers"
    DestinationSecurityGroupId: {Ref: ServerSecurityGroup}
    FromPort: 1983
    ToPort: 1983
    IpProtocol: "tcp"
    GroupId: {Ref: LoadBalancerSecurityGroup}
```

#### Installation Task

The installation task security group allows one-off tasks that are run during the installation process to access the Spacelift database. Our default CloudFormation template looks like the following:

```yaml
InstallationTaskSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupName: "installation_task_sg"
    GroupDescription: "The security group for tasks that run as part of the installation process"
    SecurityGroupEgress:
      - Description: "Unrestricted egress"
        FromPort: 0
        ToPort: 0
        IpProtocol: "-1"
        CidrIp: "0.0.0.0/0"
    VpcId: {Ref: VPC}
```

#### Database

The database security group needs to allow inbound access from the server, the drain and installation tasks. Our default CloudFormation template looks like the following:

```yaml
DatabaseSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupName: "database_sg"
    GroupDescription: "The security group defining what services can access the Spacelift database"
    SecurityGroupIngress:
      - Description: "Only accept TCP connections on appropriate port from the drain"
        FromPort: 5432
        ToPort: 5432
        IpProtocol: "tcp"
        SourceSecurityGroupId: {Ref: DrainSecurityGroup}
      - Description: "Only accept TCP connections on appropriate port from the server"
        FromPort: 5432
        ToPort: 5432
        IpProtocol: "tcp"
        SourceSecurityGroupId: {Ref: ServerSecurityGroup}
      - Description: "Only accept TCP connections on appropriate port from the installation tasks"
        FromPort: 5432
        ToPort: 5432
        IpProtocol: "tcp"
        SourceSecurityGroupId: {Ref: InstallationTaskSecurityGroup}
    VpcId: {Ref: VPC}
```

### Performing a custom VPC installation

To install Spacelift into a custom VPC, create your VPC along with all the other required components like security groups, then edit the `vpc_config` section of your _config.json_ file, making sure to set `use_custom_vpc` to `true`. A correctly populated `vpc_config` will look like this:

```json
{
    "vpc_config": {
        "use_custom_vpc": true,
        "vpc_id": "vpc-091e6f4d35908e7c1",
        "private_subnet_ids": "subnet-01a25f47c5a7e94fc,subnet-035169be40fbfbbbf,subnet-09c72e8ab5499eed1",
        "public_subnet_ids": "subnet-08aa756ab626d690f,subnet-0d03bb49f32922d93,subnet-0d85c4a80db226099",
        "drain_security_group_id": "sg-045061f7120343acd",
        "load_balancer_security_group_id": "sg-086a38a75894c4fc5",
        "server_security_group_id": "sg-0cb943fd285fc5c85",
        "installation_task_security_group_id": "sg-03b9b0e17cce91d3a",
        "database_security_group_id": "sg-0b67dd8ad00e237fd",
        "availability_zones": "eu-west-1a,eu-west-1b,eu-west-1c"
    }
}
```

Once you have populated your configuration, just run the installer as described in the [installation guide](./install.md#running-the-installer).

## HTTP Proxies

If you need to use an HTTP proxy to allow the Spacelift components to access the internet, you can specify this via the _config.json_ file:

```json
{
    "proxy_config": {
        "http_proxy": "",
        "https_proxy": "",
        "no_proxy": ""
    }
}
```

These three settings correspond to the `HTTP_PROXY`, `HTTPS_PROXY` and `NO_PROXY` environment variables, respectively. These environment variables are automatically added to the Spacelift ECS containers during installation when values are specified in the configuration file.

Any variable that isn't populated will not be added. For example, if you use the following configuration all three environment variables will be added to the containers:

```json
{
    "proxy_config": {
        "http_proxy": "http://my.http.proxy",
        "https_proxy": "https://my.https.proxy",
        "no_proxy": "safe.domain"
    }
}
```

However if you only need to specify the `HTTPS_PROXY` environment variable you can use the following configuration:

```json
{
    "proxy_config": {
        "http_proxy": "",
        "https_proxy": "https://my.https.proxy",
        "no_proxy": ""
    }
}
```

NOTE: you must include the protocol with your proxy URL (e.g. `http://` or `https://`), otherwise the proxy configuration can fail to parse and prevent the Spacelift ECS services from starting correctly.

## Using a TLS connection between the Application Load Balancer and Spacelift Server

The Spacelift server is served over TLS by default. This is achieved by using an AWS Application Load Balancer (ALB) to terminate the TLS connection and forward the request to the Spacelift server running in an ECS container. That is through HTTP.

```none
client -> (https) -> Load Balancer -> (http) -> ECS
```

If you want the server to use HTTPS as well, you can do so by specifying the TLS certificate in `config.json`. `tls_config.server_certificate_secrets_manager_arn` is the ARN of the SecretsManager secret that holds both the private and public keys of your TLS certificate in the following format:

```json
{"privateKey": "<base64-encoded-private-key>", "publicKey": "<base64-encoded-public-key>"}
```

Example `config.json`:

```json
{
    "tls_config": {
        "server_certificate_secrets_manager_arn": "arn:aws:secretsmanager:eu-west-1:123456789012:secret:spacelift-server-tls-cert-123456",
        "ca_certificates": []
    }
}
```

## Using custom CA certificates

If you use a custom certificate authority to issue TLS certs for components that Spacelift will communicate with, for example your VCS system, you need to provide your custom CA certificates. You can provide these via the `config.json` file via the `tls_config.ca_certificates` property:

```json
{
    "tls_config": {
        "server_certificate_secrets_manager_arn": "",
        "ca_certificates": [
          "<base64-encoded certificate 1>",
          "<base64-encoded certificate 2>"
        ]
    }
}
```

Please note that each certificate should be base64-encoded and formatted onto a single line. For example, if we had the following certificate:

```text
-----BEGIN CERTIFICATE-----
MIIFsTCCA5mgAwIBAgIUDD/4VBfLx5K/tAY+SckH05TJ8i8wDQYJKoZIhvcNAQEL
BQAwaDELMAkGA1UEBhMCR0IxETAPBgNVBAgMCFNjb3RsYW5kMRAwDgYDVQQHDAdH
bGFzZ293MRkwFwYDVQQKDBBBZGFtIEMgUm9vdCBDQSAxMRkwFwYDVQQDDBBBZGFt
IEMgUm9vdCBDQSAxMB4XDTIzMDMxMzExMzYxMVoXDTI1MTIzMTExMzYxMVowaDEL
MAkGA1UEBhMCR0IxETAPBgNVBAgMCFNjb3RsYW5kMRAwDgYDVQQHDAdHbGFzZ293
MRkwFwYDVQQKDBBBZGFtIEMgUm9vdCBDQSAxMRkwFwYDVQQDDBBBZGFtIEMgUm9v
dCBDQSAxMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAxjv/+sInXiQ+
2Fb+itF8ndlpmmYUoZwYN4dx+2wrcbOVngTvy4sE+33nGBzH4vt4pOhKTWwaYXFI
0CzqoIoazi8Zl0medyrwtIUDZ1pNcVugb4KAFb9Jbq40Ik3xG6t16maxQJGTiAG2
/xVtsuYdhnBGx//61SEbEwSpR145/Qf1cba8RlRQMz4QUWNe8XXo3SYaX2kxiw2V
1Op+fQxg2jf1AyzQXX1ch1jyG5RLESPUMFkBiQwi7LOSCaavfJEUzwqeoORgd7Ti
uyMV+4Gsb1XAnK7KXYwisGeP5/QNFPAByfAdPjR20rMYYHfxqEDth4Najjmu/iyF
PGk4CobRhitTtJXT/QxWcvtrRu1BCVnedyESMyiya4Q9dn27rFjjg3ZARqWOZhyq
OTWHo2mO2FzEJuxhvYNe2iYVp2s8wMTB02nP3wpWoYwje2yDwcjkIl8uXKzEZ9Gf
FATJaCLoO8o5J2HXsgOIqXlpzU9tUtEew/xTzZqX5A34o8/+NgUtm0F7joWa5mDC
QB7L8cKfACydfpekJx/gFUGSy/5vdfBzOczc6Bmh66yHPBRDcgyDFnnx34m/XVQa
rBwwIDDbqu3sscdOgm9v8csCJd0YlXGb/x4oAA61IITnsNd9NCw0GJIquSEcYiCE
A0YrQTKVfRAXuhSZ1VPIuxXiF2K3XTMCAwEAAaNTMFEwHQYDVR0OBBYEFD55R4mt
0hNOJUgPL0JBKZB1jybSMB8GA1UdIwQYMBaAFD55R4mt0hNOJUgPL0JBKZB1jybS
MA8GA1UdEwEB/wQFMAMBAf8wDQYJKoZIhvcNAQELBQADggIBAHecVjMklTkS2Py5
XNpJ9cdzG66GuPDw8aQZIunrxqYud74CA1Y0K26kyDJkLnWzVa7nT+F0d8Qn3tov
vFwI3xy5l+4upmuZ3u1jFEMiSk8C2FPohLDnDo3rwEUCGvJ6a4Gas7YyHPGL3DrJ
0dcu9wsX9cYB2YJ27QosZ5s6zmmUvBGTI30JNvPnSoC7kzqD3ArxvTEW9WaUqoJt
88lsMnn6+ps9A6exb/fK909ZWaEJWRd9cdMET0fna7EhhkO+Cqz415RgMxlK7ggT
97CvkjvvLNeFT5naHbzUANqfMVRRcUaP3PjTC9z5cDo9CaPaFjV/+Uxax2mAlARk
fqYyWoqvZH90czpvFG1jUo6P4NpyxZS8layJwD24qX+EON43WYApLsl/jE2A/JmQ
MdgWNhOy4HP8U8+aANr0Ev7gWWNi6VcR8T6PT/rbAGjnPmVmoZ4rc7CdoS8ZQZJh
K8ELA17+pnMTgo7wxfARqL+p+mqgtUxRbiWitev8F2hUVB/SwP8hpcGrdhTEN7td
pSW1ykPeGJFKSBo5QHanqqPFCzqtFeoL9DhYx5/xE6FpKMLg3vVcFsHu6glS8iMV
4Hvb2fXuhXxLTBCbD1+5lLP/bHXogQKmp2H6Oj0e6WBmQ0xqGou4Il6bavsZCx2v
ADWvlue5jXdNu5xPZdsNVNAluAne
-----END CERTIFICATE-----
```

We would base64-encode it and then use a tls_config.json file that looks something like the following:

```json
{
    "ServerCertificateSecretsManagerArn": "",
    "CACertificates": [
      "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUZzVENDQTVtZ0F3SUJBZ0lVREQvNFZCZkx4NUsvdEFZK1Nja0gwNVRKOGk4d0RRWUpLb1pJaHZjTkFRRUwKQlFBd2FERUxNQWtHQTFVRUJoTUNSMEl4RVRBUEJnTlZCQWdNQ0ZOamIzUnNZVzVrTVJBd0RnWURWUVFIREFkSApiR0Z6WjI5M01Sa3dGd1lEVlFRS0RCQkJaR0Z0SUVNZ1VtOXZkQ0JEUVNBeE1Sa3dGd1lEVlFRRERCQkJaR0Z0CklFTWdVbTl2ZENCRFFTQXhNQjRYRFRJek1ETXhNekV4TXpZeE1Wb1hEVEkxTVRJek1URXhNell4TVZvd2FERUwKTUFrR0ExVUVCaE1DUjBJeEVUQVBCZ05WQkFnTUNGTmpiM1JzWVc1a01SQXdEZ1lEVlFRSERBZEhiR0Z6WjI5MwpNUmt3RndZRFZRUUtEQkJCWkdGdElFTWdVbTl2ZENCRFFTQXhNUmt3RndZRFZRUUREQkJCWkdGdElFTWdVbTl2CmRDQkRRU0F4TUlJQ0lqQU5CZ2txaGtpRzl3MEJBUUVGQUFPQ0FnOEFNSUlDQ2dLQ0FnRUF4anYvK3NJblhpUSsKMkZiK2l0RjhuZGxwbW1ZVW9ad1lONGR4KzJ3cmNiT1ZuZ1R2eTRzRSszM25HQnpINHZ0NHBPaEtUV3dhWVhGSQowQ3pxb0lvYXppOFpsMG1lZHlyd3RJVURaMXBOY1Z1Z2I0S0FGYjlKYnE0MElrM3hHNnQxNm1heFFKR1RpQUcyCi94VnRzdVlkaG5CR3gvLzYxU0ViRXdTcFIxNDUvUWYxY2JhOFJsUlFNejRRVVdOZThYWG8zU1lhWDJreGl3MlYKMU9wK2ZReGcyamYxQXl6UVhYMWNoMWp5RzVSTEVTUFVNRmtCaVF3aTdMT1NDYWF2ZkpFVXp3cWVvT1JnZDdUaQp1eU1WKzRHc2IxWEFuSzdLWFl3aXNHZVA1L1FORlBBQnlmQWRQalIyMHJNWVlIZnhxRUR0aDROYWpqbXUvaXlGClBHazRDb2JSaGl0VHRKWFQvUXhXY3Z0clJ1MUJDVm5lZHlFU015aXlhNFE5ZG4yN3JGampnM1pBUnFXT1poeXEKT1RXSG8ybU8yRnpFSnV4aHZZTmUyaVlWcDJzOHdNVEIwMm5QM3dwV29Zd2plMnlEd2Nqa0lsOHVYS3pFWjlHZgpGQVRKYUNMb084bzVKMkhYc2dPSXFYbHB6VTl0VXRFZXcveFR6WnFYNUEzNG84LytOZ1V0bTBGN2pvV2E1bURDClFCN0w4Y0tmQUN5ZGZwZWtKeC9nRlVHU3kvNXZkZkJ6T2N6YzZCbWg2NnlIUEJSRGNneURGbm54MzRtL1hWUWEKckJ3d0lERGJxdTNzc2NkT2dtOXY4Y3NDSmQwWWxYR2IveDRvQUE2MUlJVG5zTmQ5TkN3MEdKSXF1U0VjWWlDRQpBMFlyUVRLVmZSQVh1aFNaMVZQSXV4WGlGMkszWFRNQ0F3RUFBYU5UTUZFd0hRWURWUjBPQkJZRUZENTVSNG10CjBoTk9KVWdQTDBKQktaQjFqeWJTTUI4R0ExVWRJd1FZTUJhQUZENTVSNG10MGhOT0pVZ1BMMEpCS1pCMWp5YlMKTUE4R0ExVWRFd0VCL3dRRk1BTUJBZjh3RFFZSktvWklodmNOQVFFTEJRQURnZ0lCQUhlY1ZqTWtsVGtTMlB5NQpYTnBKOWNkekc2Nkd1UER3OGFRWkl1bnJ4cVl1ZDc0Q0ExWTBLMjZreURKa0xuV3pWYTduVCtGMGQ4UW4zdG92CnZGd0kzeHk1bCs0dXBtdVozdTFqRkVNaVNrOEMyRlBvaExEbkRvM3J3RVVDR3ZKNmE0R2FzN1l5SFBHTDNEckoKMGRjdTl3c1g5Y1lCMllKMjdRb3NaNXM2em1tVXZCR1RJMzBKTnZQblNvQzdrenFEM0FyeHZURVc5V2FVcW9KdAo4OGxzTW5uNitwczlBNmV4Yi9mSzkwOVpXYUVKV1JkOWNkTUVUMGZuYTdFaGhrTytDcXo0MTVSZ014bEs3Z2dUCjk3Q3ZranZ2TE5lRlQ1bmFIYnpVQU5xZk1WUlJjVWFQM1BqVEM5ejVjRG85Q2FQYUZqVi8rVXhheDJtQWxBUmsKZnFZeVdvcXZaSDkwY3pwdkZHMWpVbzZQNE5weXhaUzhsYXlKd0QyNHFYK0VPTjQzV1lBcExzbC9qRTJBL0ptUQpNZGdXTmhPeTRIUDhVOCthQU5yMEV2N2dXV05pNlZjUjhUNlBUL3JiQUdqblBtVm1vWjRyYzdDZG9TOFpRWkpoCks4RUxBMTcrcG5NVGdvN3d4ZkFScUwrcCttcWd0VXhSYmlXaXRldjhGMmhVVkIvU3dQOGhwY0dyZGhURU43dGQKcFNXMXlrUGVHSkZLU0JvNVFIYW5xcVBGQ3pxdEZlb0w5RGhZeDUveEU2RnBLTUxnM3ZWY0ZzSHU2Z2xTOGlNVgo0SHZiMmZYdWhYeExUQkNiRDErNWxMUC9iSFhvZ1FLbXAySDZPajBlNldCbVEweHFHb3U0SWw2YmF2c1pDeDJ2CkFEV3ZsdWU1alhkTnU1eFBaZHNOVk5BbHVBbmUKLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo="
    ]
}
```

## Installing into a Private VPC

If you want to install Spacelift into a private VPC that does not have any internet access, you need to setup VPC endpoints for the following AWS services:

- ECR and ECR Docker endpoint.
- IoT.
- KMS.
- License manager.
- Logs.
- Monitoring.
- S3.
- Secrets manager.
- SQS.
- Xray.

In addition, if you want to deploy a worker pool into a VPC with no internet access and are using our CloudFormation template to deploy the pool, you need to create a VPC endpoint for the following service:

- EC2 autoscaling.

The following sections contain example CloudFormation definitions describing each endpoint that needs to be created.

### Proxy Configuration

As well as setting up VPC endpoints, you will also need to configure an [HTTP Proxy](#http-proxies). This is required because AWS does not currently provide an endpoint for the IoT control plane, meaning that these requests cannot use a private VPC endpoint.

When using VPC endpoints, you should include the following in your `NO_PROXY` environment variable to ensure that requests to the required AWS services are routed via your VPC endpoints rather than via the proxy (making sure to substitute `<region>` with your install region):

```shell
s3.<region>.amazonaws.com,license-manager.<region>.amazonaws.com,a3mducvsqca9re-ats.iot.<region>.amazonaws.com,logs.<region>.amazonaws.com,monitoring.<region>.amazonaws.com,sqs.<region>.amazonaws.com,xray.<region>.amazonaws.com,secretsmanager.<region>.amazonaws.com,kms.<region>.amazonaws.com,ecr.<region>.amazonaws.com,api.ecr.<region>.amazonaws.com
```

### VPC Endpoint Security Group

You need to provide a security group for the VPC endpoints to use. This security group should allow inbound access on port 443. For example you could use something like the following:

```yaml
VPCEndpointSecurityGroup:
  Type: AWS::EC2::SecurityGroup
  Properties:
    GroupName: "vpc_endpoint_sg"
    GroupDescription: "The sg to use for VPC endpoints"
    SecurityGroupIngress:
      - Description: "Allow inbound HTTPS access to VPC endpoints from VPC"
        FromPort: 443
        ToPort: 443
        IpProtocol: "tcp"
        CidrIp: "<replace-with-your-own-address-range>"
    VpcId: {Ref: VPC}
```

### ECR and ECR Docker endpoint

The following VPC endpoints need to be created:

```yaml
ECRInterfaceEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcEndpointType: Interface
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.ecr.api"}
    VpcId: {Ref: VPC}
    SubnetIds:
      - {Ref: PrivateSubnet1} # Replace this with at least one of your subnets
    SecurityGroupIds:
      - {Ref: VPCEndpointSecurityGroup}
    PrivateDnsEnabled: true

ECRDockerInterfaceEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcEndpointType: Interface
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.ecr.dkr"}
    VpcId: {Ref: VPC}
    SubnetIds:
      - {Ref: PrivateSubnet1} # Replace this with at least one of your subnets
    SecurityGroupIds:
      - {Ref: VPCEndpointSecurityGroup}
    PrivateDnsEnabled: true
```

### IoT

The following VPC endpoint needs to be created:

```yaml
IoTInterfaceEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcEndpointType: Interface
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.iot.data"}
    VpcId: {Ref: VPC}
    SubnetIds:
      - {Ref: PrivateSubnet1}
    SecurityGroupIds:
      - {Ref: VPCEndpointSecurityGroup}
    PrivateDnsEnabled: false
```

Note that the `PrivateDnsEnabled` option is set to false. For the IoT data endpoint you need to manually create the correct DNS entry to allow Spacelift workers to connect to the IoT broker for your account.

First, run the following command to find the correct IoT endpoint for your region:

```shell
aws iot describe-endpoint --endpoint-type iot:Data-ATS --region <region> --no-cli-pager --output json
```

This should output something like the following:

```shell
{
    "endpointAddress": "b2mdsfpsxca6rx-ats.iot.us-east-1.amazonaws.com"
}
```

Next, go to the Route53 console, and create a private hosted zone for your endpoint address. In the example above, this would be `b2mdsfpsxca6rx-ats.iot.us-east-1.amazonaws.com`.

Finally, create an A record for your endpoint address (for example `b2mdsfpsxca6rx-ats.iot.us-east-1.amazonaws.com`), and use an alias to point it at your IoT VPC endpoint.

**NOTE:** make sure that you create your private hosted zone for your full endpoint address, and not for `iot.<region>.amazonaws.com`. If you create a hosted zone for `iot.<region>.amazonaws.com` it will prevent the Spacelift server and drain processes from being able to access the IoT control plane.

### KMS

The following VPC endpoint needs to be created:

```yaml
KMSInterfaceEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcEndpointType: Interface
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.kms"}
    VpcId: {Ref: VPC}
    SubnetIds:
      - {Ref: PrivateSubnet1} # Replace this with at least one of your subnets
    SecurityGroupIds:
      - {Ref: VPCEndpointSecurityGroup}
    PrivateDnsEnabled: true
```

### License manager

The following VPC endpoint needs to be created:

```yaml
LicenseManagerInterfaceEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcEndpointType: Interface
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.license-manager"}
    VpcId: {Ref: VPC}
    SubnetIds:
      - {Ref: PrivateSubnet1} # Replace this with at least one of your subnets
    SecurityGroupIds:
      - {Ref: VPCEndpointSecurityGroup}
    PrivateDnsEnabled: true
```

### Logs

The following VPC endpoint needs to be created:

```yaml
LogsInterfaceEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcEndpointType: Interface
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.logs"}
    VpcId: {Ref: VPC}
    SubnetIds:
      - {Ref: PrivateSubnet1} # Replace this with at least one of your subnets
    SecurityGroupIds:
      - {Ref: VPCEndpointSecurityGroup}
    PrivateDnsEnabled: true
```

### Monitoring

The following VPC endpoint needs to be created:

```yaml
MonitoringInterfaceEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcEndpointType: Interface
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.monitoring"}
    VpcId: {Ref: VPC}
    SubnetIds:
      - {Ref: PrivateSubnet1} # Replace this with at least one of your subnets
    SecurityGroupIds:
      - {Ref: VPCEndpointSecurityGroup}
    PrivateDnsEnabled: true
```

### S3

The following VPC endpoint needs to be created. Also note that each of your Spacelift subnets will also
need a route table attached that can be referenced in the endpoint definition:

```yaml
S3GatewayEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.s3"}
    VpcEndpointType: Gateway
    VpcId: {Ref: VPC}
    RouteTableIds:
      # Attach a route table corresponding to each of the subnets being used for Spacelift
      - {Ref: PrivateSubnet1RouteTable}
      - {Ref: PrivateSubnet2RouteTable}
      - {Ref: PrivateSubnet3RouteTable}
    PolicyDocument:
      Version: 2012-10-17
      Statement:
        - Effect: Allow
          Principal: '*'
          Action: '*'
          Resource: '*'
```

### Secrets manager

The following VPC endpoint needs to be created:

```yaml
SecretsManagerInterfaceEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcEndpointType: Interface
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.secretsmanager"}
    VpcId: {Ref: VPC}
    SubnetIds:
      - {Ref: PrivateSubnet1} # Replace this with at least one of your subnets
    SecurityGroupIds:
      - {Ref: VPCEndpointSecurityGroup}
    PrivateDnsEnabled: true
```

### SQS

The following VPC endpoint needs to be created:

```yaml
SQSInterfaceEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcEndpointType: Interface
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.sqs"}
    VpcId: {Ref: VPC}
    SubnetIds:
      - {Ref: PrivateSubnet1} # Replace this with at least one of your subnets
    SecurityGroupIds:
      - {Ref: VPCEndpointSecurityGroup}
    PrivateDnsEnabled: true
```

### Xray

The following VPC endpoint needs to be created:

```yaml
XrayInterfaceEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcEndpointType: Interface
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.xray"}
    VpcId: {Ref: VPC}
    SubnetIds:
      - {Ref: PrivateSubnet1} # Replace this with at least one of your subnets
    SecurityGroupIds:
      - {Ref: VPCEndpointSecurityGroup}
    PrivateDnsEnabled: true
```

### EC2 Autoscaling

The following optional VPC endpoint can be created if using our CloudFormation worker pool template:

```yaml
AutoscalingInterfaceEndpoint:
  Type: AWS::EC2::VPCEndpoint
  Properties:
    VpcEndpointType: Interface
    ServiceName: {Fn::Sub: "com.amazonaws.${AWS::Region}.autoscaling"}
    VpcId: {Ref: VPC}
    SubnetIds:
      - {Ref: PrivateSubnet1} # Replace this with at least one of your subnets
    SecurityGroupIds:
      - {Ref: VPCEndpointSecurityGroup}
    PrivateDnsEnabled: true
```
