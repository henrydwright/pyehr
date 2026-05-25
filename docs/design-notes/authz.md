# Authentication and Authorisation

OpenEHR leaves the question of how to do authentication and authorisation completely up to the platform's implementation of specification. These are required to ensure confidentiality and privacy for EHR subject information.

The main two routes for this are:

1. design of `ACCESS_CONTROL_SETTINGS` and the enforcement of the same in the EHR
2. implementation of API authentication/authorisation on the REST API endpoints

This set of notes provides the thinking behind the requirements for, and design of, the pyehr implementation of authz for its OpenEHR platform.

Though pyehr only provides a secure OpenEHR compliant repository rather than a fully featured healthcare application, the design notes below consider a fully featured healthcare application as the decision pyehr takes will influence to a greater/lesser extent choices made by the using applications.

**Geographical context**

pyehr has been built in England by someone with familiarity only with the UK healthcare sector. Other juristictions, such as the US, are taken into account such that decisions made are applicable globally, but where the platform is opinionated, it relies on English healthcare principles.

### OpenEHR spec considerations
The OpenEHR spec does not define detailed auth requirements (see the [security section of the architecture overview](https://specifications.openehr.org/releases/BASE/development/architecture_overview.html#_security_and_confidentiality)) but does define some considerations to be taken into account.

> Many of the concrete mechanisms relating to security and privacy are found in system deployments rather than in models such as openEHR, particularly the implementation of authentication, access control, and encryption.
>
> **OpenEHR Architecture Overview**

Security policy of OpenEHR:

General:
* Indelibility - record information cannot be deleted
* Audit trailing - all changes are audit trailed with user identity, time-stamp, reason and (optionally) digital signature
* Anonymity - content of the record is separate from identifying information

Access control (relevant for our purposes):
* Access list - user identity (who) and time (at what point in care cycle) should bet aken into account
* Access control of access settings - gate-keeper controls access to EHR access control established at time of creation. Usually patient, otherwise parent, guardian, etc.
* Privacy - Compositions can be marked as having privacy levels
* Usability - "sensible defaults" should be set which work for most of the info in the EHR most of the time

Other principles are listed but not relevant for these decisions other than: access logging, time-limitation of access, non-repudiation and certification.

### Entities involved
There are several entities involved in the interaction with an OpenEHR repository such as pyehr:
* EHR subject - the real life person who is the subject of the data held within the EHR
* EHR - the totality of data that makes up the EHR
* EHR repository - the digital system (pyehr) which holds the EHR
* EHR repository owner - the legal entity who is responsible for running the EHR repository
* Jurisdiction - the national, regional or local health system governing the EHR repository owner
* Accessing user - the person who wishes to perform some action on the EHR
* Accessing user's organisation - the organisation the accessing user is associated with
* Accessing application - the application used by the accessing user to access the EHR

### (UK) GDPR
The General Data Protection Regulations (GDPR) are European legislation retained in the UK which govern the use of data.

It sets out roles relating to data and principles for its protection.

The principles are:
* Lawfulness, fairness and transparency
* Purpose limitation
* Data minimisation
* Accuracy
* Storage limitation
* Integrity and confidentiality (security)
* Accountability

There are two roles that organisations involved in data can have under UK GDPR:
> **Controller** - the natural or legal person, public authority, agency or body which, alone or jointly with others, determines the purposes and means of processing of personal data
> **Processor** - the natural or legal person, public authority, agency or other body which processes personal data on behalf of the controller.

Sub-contractors to the processors are sometimes referred to as sub-processors although this term does not exist in GDPR itself.

EHR data is likely to contain some of the most sensitive data, including "special categories" under GDPR such as:
* racial or ethnic origin
* religious or philosophical beliefts
* genetic data
* biometric data
* health
* sex life or sexual orientation

This data cannot be processed at all unless it is done under one of 10 exceptions:
1. explicit consent
2. employment, social securit and social protection
3. vital interests
4. not-for-profit bodies
5. made public by data subject
6. legal claims or judicial acts
7. reasons of substantial public interest (with a basis in law)
8. health or social care (with a basis in law)
9. public health (with a basis in law)
10. archiving, research and statistics (with a basis in law)

The EHR repository owner is almost certainly a controller under UK GDPR and the accessing users' organisations may be joint controllers depending on access. The EHR subject is likely the data subject.

What this means for pyehr is that it MUST:
1. Ensure its authz mechanisms adhere to GDPR principles
2. Allow organisations to record and evidence adherence to GDPR provisions for special category data
3. Provide a way for data subjects to exercise their rights (informed, access, rectification, erasure, processing, data portability, objection)

### HIPAA
HIPAA stands for the Health insurance portability and acountability act 1996 and is US legislation designed to improve portability of health insurance and establish standards for privacy and security of health information.

HIPAA regulations apply to:
* Health plans
* Most health care providers (that conduct business electronically)
* Health care clearinghouses

> The Privacy Rule protects all "individually identifiable health information" held or transmitted by a covered entity or its business associate, in any form or media, whether electronic, paper, or oral.
> "Individually identifiable health information" is information, including demographic data, that relates to:
> * the individual's past, present or future physical or mental health or condition,
> * the provision of health care to the individual, or
> * the past, present, or future payment for the provision of health care to the individual,
> 
> **[Summary of HIPAA privacy rule](https://www.hhs.gov/hipaa/for-professionals/privacy/laws-regulations/index.html)**

Under HIPAA a covered entity is permitted to use information without an individual's authorisation to:
1. disclose to the individual who is the subject of information
2. use for treatment, payment or health care operations
3. be added to facility directory or notification (with opportunity to object)
4. be used incidentally to the above
5. for public interest and benefit activities (within the 12 priority purposes)
6. disclose a limited data set to others

In order to prove that pyehr can deal with other juristictions in the general case it MUST also ensure it can:
* Provide access control that would allow an EHR repository owner using pyehr to be HIPAA compliant
* Record in the relevant way that an organisation is meeting its HIPAA obligations

## Authentication (X is who they say they are)

Authentication on an EHR must deliver the following:

1. Basic demographic information on who the user (or system) is
2. Information on the level of confidence of authentication (as some actions may only be authorised with higher confidence authentication)
3. For staff, a link between the user and the organisation they are accessing the record for
4. For patients, a link between the user and their healthcare record
5. For trusted others (proxies), a link between the user and other people's healthcare records
6. For systems, a link between the system and the organisation the system belongs to
7. The information above to persist in the stored record even if the downstream technical implementation changes

### General considerations
The OpenEHR model allows for federated as well as centralised repositories of information. The authentication model for pyehr MUST support both.

**Centralised repositories**:

pyehr's authentication model MUST support:
* Ability for the central authority to configure multiple different authentication providers to handle multiple organisations accessing the pyehr repository
* Ability to authenticate multiple systems for unsupervised access to perform some bulk operations

**Federalised repositories**:

pyehr's authentication model MUST support:
* Ability for organisations to permit certain actions for staff in outside organisations
* Configuration of a pyehr instance such that it may be linked to other pyehr systems sharing an authentication model

**Platform independence**:

In addition, such that pyehr can be as platform independent and secure as possible, the design MUST:
1. Permit for as many choices of authentication provider as possible
2. Separate authentication from authorisation
3. Ensure pyehr does not 'roll its own auth'
4. Utilise existing, accepted definitions of authentication levels where they exist
5. Utilise existing, accepted authentication models and protocols of a sufficient level of security

### Authenticator assurance levels
NIST defines a set of [Authentication Assurance Levels (AAL)](https://pages.nist.gov/800-63-4/sp800-63b.html#AAL_SEC4) which are widely understood across industry and sectors. These give standardised levels of confidence in the authentication of claimants. 

The levels are:
1. AAL1 - basic confidence - single or multi factor authentication using password, look-up secret, out-of-band device, OTP, etc.
2. AAL2 - high confidence - proof of posession and two authentication factors from etiher multi-factor out-of-band authenticator, OTP, cryptographic auth OR two single-factors (something you have + something you are)
3. AAL3 - very high confidence - proof of possesion of a key + actication factor / password using multi-factor cryptographic auth or single-factor cryptographic auth + password/biometrics

pyehr MUST make use of AALs for configuration of the authentication method(s)

### NHS Care Identity Service
In order to allow seamless integration with NHS organisations, pyehr MUST implement authentication in such a way that [NHS Care Identity Service](https://digital.nhs.uk/services/care-identity-service) may be used as one of its providers.

Authentication uses [OpenID Connect and returns an ID token containing standard OIDC (depending on claims)](https://digital.nhs.uk/services/care-identity-service/applications-and-services/cis2-authentication/integrate/design-and-build/scopes-and-claims) but also below:
* nhsperson (user profile info)
* associatedorgs (orgs the user has a role with)
* nationalrbacaccess
* professionalmemberships
* organisationalmemberships
* selectedrole
* changedrole

### NHS Login
To allow for easy login for patient facing apps, pyehr MUST implement authentication in such a way that the [NHS Login](https://digital.nhs.uk/services/nhs-login) service for patients may be used as one of its providers.

Authentication uses OpenID Connect and scopes can return the standard scopes plus:
* gp_integration_credentials
* gp_registration_details (registered GP)
* profile_extended (PDS info)
* client_metadata
* basic_demographics (DOB, family_name, identity_proofing_level)

### OpenID Connect
[OpenID Connect](https://www.microsoft.com/en-us/security/business/security-101/what-is-openid-connect-oidc?msockid=3ec928f56c9e6fcc10cd3c2a6d5c6e9e) is a way of allowing users to authenticate to multiple applications with the same identity.

The process includes:
1. User goes to the application (relying part)
2. User enters their details
3. Relying party sends request to OpenID provider
4. OpenID provider validates credentials and obtains authorisation from user (if needed)
5. OpenID sends identity token and often access token to relying party
6. User is given access based on cntent of token

Given the above NHS services use it and it is a well used international standard, pyehr MUST support OpenID connect.

## Authorisation (X can perform this action)

Role-based access control as the main form of authentication works well in healthcare settings, as staff members fulfil (potentially multiple) well-scoped roles, each of which may have actions/activities attached to them.

The model of RBAC must deliver the following:
1. For organisations, an ability to associate authenticated users with roles
1. For registered professionals, a link between the role and their professional registration
2. For staff, a list of actions they may perform on an EHR, and the level of authentication required to do so
3. For staff, the ability to pick a role should they fulfil multiple roles
4. For patients, the ability to choose (within limits) who can access their healthcare information
5. Ability to electronically sign items within the EHR when required to allow for proof that the information was not subsequently tampered with (e.g. ionising radiation orders, prescriptions, etc.)

### NHS national RBAC and APIs

Whatever design is proposed, MUST allow for adherence to the NHS England national RBAC model if needed, so national integration between a pyehr based system and NHS England services is made as easy as possible.

The national model has:
* Job codes (R) - sets of roles that can be assigned to users
* Activities (B) - sets of activities a user can perform
* Baseline policy - default mapping of roles to activities (e.g. Clinical Practitioner to Amend Patient Demographics)

Information on this can be found on the [NHS England webpages](https://digital.nhs.uk/services/care-identity-service/applications-and-services/cis2-authentication/integrate/design-and-build/national-rbac-for-developers)

Most APIs make use of OAuth2 for authorisation linked to the national RBAC roles and two authentication methods above.

### OAuth 2.0
[OAuth stands for Open _Authorization_](https://auth0.com/docs/authenticate/protocols/oauth) and is designed to allow a website or application to access resources hosted by other apps on behalf of a user.

It has the following roles:
* Resource owner: Entity that can grant access to the resource (typically, the end-user)
* Resource server: Server hosting the protected resources
* Client: Application requesting access to protected resource on behalf of resource owner
* Authorisation server: Server that authenticates resources owner and issues access tokens.

With mapping to the pyehr roles set out earlier, for an OAuth style architecture this would look like:
* Resource owner - accessing user (could include EHR subject)
* Resource server - EHR repository
* Client - accessing application
* Authorisation server - TBC as part of design

Permissions are referred to as scopes

### OpenEHR REST API
The method of a client using the pyehr repository is through the REST API.

The client essentially provides pyehr with an authenticated user who requests authorisation to perform an action.

For flexibility the EHR controller's role mostly looks like this:
1. Link people to users (and credentials) within an identity provider
2. Link those users to a set of roles determined by the EHR controller
2. Determine a policy which links the set of roles to actions that may or may not be performed by each role
3. Link this policy to an EHR or set of EHRs

The role of pyehr is then to:
1. Determine the role that the authenticated user has
2. Check whether the action requested by the role of the user is permitted
3. Permit or deny the action as appropriate
4. Audit the action that has been taken (and provide signature of that action as needed)

Given the broadness of the OpenEHR API it is possible that the EHR controller may wish to restrict possible actions beyond a simple API endpoint level.

## pyehr Authz design

### Design choices

Technology choices:
* pyehr will support any auth mechanism that provides it with a unique identity for a user and a list of roles the user has
* Accessing applications are responsible for running the authorisation flow before calling a pyehr endpoint
* The first mechanism to be supported will be OAuth2 authorisation with OIDC authentication

Architectural choices:
* Users must belong to an organisation, unless they are a patient in which case they belong to a special "patients" organisation
* Each accessing users' organisation may have one or more auth providers associated with it
* Role allocation is configured solely in the identity provider of the accessing users' organisation
* Policies linking roles to actions are configured solely in pyehr using EHR_ACCESS and ACCESS_CONTROL_SETTINGS specific to pyehr
* Configuration of ROLE and ORGANISATION objects is done in the relevant OpenEHR demographic service. PERSON objects will be generated automatically during authentication. Accessing applications are free to modify this as required (assuming they have the rights).
* The OpenEHR demographic information will be referenced in OpenEHR audit classes to maintain persistence even if iDP is lost or unconfigured.
* Configuration of auth providers is done outside of OpenEHR RM space through custom pyehr-specific configuration

Access control settings choices:
* pyehr will implement its own subclass of ACCESS_CONTROL_SETTINGS called PYEHR_ACCESS_CONTROL_SETTINGS
* Each instance of PYEHR_ACCESS_CONTROL_SETTINGS will be independently identified by OBJECT_VERSION_ID so it can be retrieved and referred to by others
* pyehr will define a REST API similar to existing endpoints which allows for versioned changes to individual instances of PYEHR_ACCESS_CONTROL_SETTINGS
* Policies either permit or deny an activity to take place for a role or an individual user
* Policies may be based on other policies, and indeed this is recommended (e.g. default EHR repository policy, sensitive patients built on this, individual patient choice added to that, etc.)
* Later policy layers take precedence over earlier ones (e.g. default policy allows access to all users in a group, but the more detailed policy denies access, the later one takes precedence)
* The default assumption is to DENY access unless explictly granted somewhere by a policy
* Activities can be allowed/denied at the following level of granularity
    * REST resource
        * REST API endpoint
            * archetype_node_id
* To help users and be able to comply with CIS2 national authentication, a default policy will be provided that makes use of NHS national roles

> Example: The EHR repository owner wishes for there to be a role X which can only access Compositions of a certain archetype.
> 
> This can be created in the policy by allowing access at response content level within /GET/Composition to responses with certain `archetype_node_id`

### Access control design

**Note:** This documentation represents the originally proposed design. For the latest design, please consult the codebase and documentation as this page is not kept up to date. It is left here as a reference for design thinking at time of inception.

#### VERSIONED_PYEHR_ACCESS_CONTROL_SETTINGS

Inherits: VERSIONED_OBJECT[PYEHR_ACCESS_CONTROL_SETTINGS]

#### PYEHR_ENDPOINT_ACTION

Members:
* GET
* GET_VERSION
* CREATE
* CREATE_WITH_ID
* UPDATE
* DELETE

#### PYEHR_POLICY_ITEM

Members:
* resource_endpoint - str - 0..1 - resource endpoint to which this policy applies (if None, assumed to apply to all resource endpoints)
* resource_action - list[PYEHR_ENDPOINT_ACTION] - 0..1 - resource actions to which this policy applies (if None, assume to apply to all resource endpoints)
* archetype_id - list[str] - 0..1 - list of archetype_ids that this rule should match in the request body or in the response object (dependant on action). This will match the archetype_node_id in the top level object being retrieved. (if None, assume to apply to all archetype_ids)

* match_roles - 0..1 - set[PartyRef] - set of roles that the user or system has that would caues the policy to trigger (if None, assume to match all roles)
* action_allowed - bool - 1..1 - if True the action is ALLOWED, if False the action is DENIED

#### PYEHR_ACCESS_CONTROL_SETTINGS

Inherits: ACCESS_CONTROL_SETTINGS

Members:
* base_settings - OBJECT_REF - 0..1 - reference to another set of settings which this one specialises
* policies - dict[str, PYEHR_POLICY_ITEM] - 0..1 - dict of resource endpoints to policy items

### Auth setup configuration

Those setting up pyehr therefore would need to:
1. Create ORGANISATIONs in the demographic service and note the UID identifiers
2. Create ROLEs in the authorisation provider and assign them to uesrs and applications
3. Provide some configuration as follows for each organisation accessing the repository
    1. Identifier of ORGANISATION in the demographic service
    2. Supported auth providers
    3. (OAuth) Scopes to request from auth providers
    4. (OAuth) The claim corresponding to the list of roles
    5. (OAuth) The claim corresponding to the user ID
    6. (OAuth) The claim(s) corresponding to user details
4. Set the policy for access to administrative endpoints (i.e. the ones allowing policy to be set)
5. Upload a PYEHR_ACCESS_CONTROL_SETTINGS for the default policy and then mark it as such in the settings.
