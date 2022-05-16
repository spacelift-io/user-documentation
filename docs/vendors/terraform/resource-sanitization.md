# Resource Sanitization

Terraform state can contain very sensitive data. Sometimes this is unavoidable because of the design of certain Terraform providers, or because the definition of what is sensitive isn't always simple and may vary between individuals and organizations. To avoid leaking sensitive data, Spacelift takes the approach of automatically sanitizing any resources stored or passed to plan policies by default.

For example, if we take the following definition for an EC2 instance:

```javascript
resource "aws_instance" "this" {
  ami           = "ami-abc123"
  instance_type = "t3.small"

  root_block_device {
    volume_size = 50
  }

  tags = {
    Name = "My Instance"
  }
}
```

Spacelift will supply something similar to the following to any plan policies:

```javascript
{
  ...,
  "terraform": {
    "resource_changes": [
      {
        "address": "module.instance.aws_instance.this",
        "change": {
          "actions": ["create"],
          "after": {
            "ami": "c4cb6118",
            ...,
            "tags": {
              "Name": "d3dac282"
            },
            "tags_all": {
              "Name": "d3dac282"
            },
          }
        }
      }
    ]
  }
}

```

As you can see, the `ami` and `tags` fields have had their values sanitized, and replaced with hashes. The same sanitization is also applied to resources shown in the [resources](../../concepts/resources.md) views.

## Sanitization and Plan Policies

Sometimes you need to perform a comparison against a sanitized value in a plan policy. To help with this we provide a `sanitized()` [helper function](../../concepts/policy/terraform-plan-policy.md#string-sanitization) that you can use in your policies.

## Disabling Sanitization

If you have a situation where the `sanitized()` helper function doesn't provide you with enough flexibility to create a particular policy, you can disable sanitization completely for a stack. To do this, add the `feature:disable_resource_sanitization` label to your stack. This will disable sanitization for any future runs.
