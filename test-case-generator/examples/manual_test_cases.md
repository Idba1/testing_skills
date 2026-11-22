# Hand-authored example of a test design table (NOT executed)

**Source assumption for this example only:** `REG-01: registration age must be between 18 and 65 inclusive.` The system's API and error strings are not provided.

| Case ID | Requirement | Category | Preconditions | Input/actions | Expected result backed by source | Evidence / uncertainty |
|---|---|---|---|---|---|---|
| TC-REG-01 | REG-01 | Positive | Registration form available | Enter age 18 | Age satisfies the declared range constraint | Source: REG-01; application response unspecified |
| TC-REG-02 | REG-01 | Positive / boundary | Form available | Enter age 65 | Age satisfies declared range constraint | Source: REG-01; response unspecified |
| TC-REG-03 | REG-01 | Negative / boundary | Form available | Enter age 17 | Age violates declared range constraint | Source: REG-01; rejection message unspecified |
| TC-REG-04 | REG-01 | Negative / boundary | Form available | Enter age 66 | Age violates declared range constraint | Source: REG-01; rejection message unspecified |

## Coverage review
This table covers the numeric range only; it does not establish form validation behavior, authentication, accessibility, or integration coverage. The JSON helper outputs *additional candidate probes* and does not execute the form.
