## System reserved ranges
To make it easier for those configuring the system, pyehr reserves two areas within the UUID v4 space for system and user-configured resources. 

This makes hand configuring certain base items of your EPR easier as you may use more memorable identifiers.

These are:
|Range|Purpose|
|-|-|
|`d0000000-0000-0000-FFYY-FFFFFFFFXXXX` (X may have any value, Y may be 0-9) | Reserved for system demographic objects |
|`d0000000-0000-0000-FFYY-FFFFFFFFXXXX` (X may have any value, Y may be a-f) | Reserved for user hand-configured demographic objects |
|`e0000000-0000-0000-FFYY-FFFFFFFFXXXX` (X may have any value, Y may be 0-9) | Reserved for system EHR objects |
|`e0000000-0000-0000-FFYY-FFFFFFFFXXXX` (X may have any value, Y may be a-f) | Reserved for user hand-configured demographic objects |

In operation, pyehr systems will never use these ranges for automatically placed objects, though will allow accessing systems to upload objects with these UIDs.

Accessing systems which overwrite data in these ranges may lead to undesired effects so efforts should be taken to prevent this.

#### System demographic objects
This is a record for those developing pyehr as to which ranges have been reserved within the system space for what purposes.

|Range|Purpose|
|-|-|
|`d0000000-0000-0000-FF00-FFFFFFFFXXXX`|System demographics objects (placeholder subject, staff member, organisation, repository AGENT, etc.)|
|`d0000000-0000-0000-FF00-FFFFFFFF1000`|Default EHR access policy|
|`d0000000-0000-0000-FF02-FFFFFFFFXXXX`|NHS National RBAC roles, where XXXX is the numeric part of the job role code|

#### System EHR objects

|Range|Purpose|
|-|-|
|`e0000000-0000-0000-FF00-FFFFFFFF1000`|Default EHR access policy|