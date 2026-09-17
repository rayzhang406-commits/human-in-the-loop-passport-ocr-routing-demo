# Application Language

Use the internship and the public demo as related but separate evidence. Do not
say that the public repository is the company system or that synthetic results
are production outcomes.

## Resume wording

**FDE internship contribution**

"Within an existing Django and React application, scoped and implemented a P0
single-document OCR workflow for travel-document operations, including raw and
normalized field handling, historical customer matching, conflict protection,
and unverified-result routing."

**Independent portfolio demo**

"Built a privacy-preserving Streamlit demo with synthetic data to independently
illustrate OCR field normalization, deterministic historical matching, conflict
detection, and human-review routing; added reproducible data generation and
automated rule tests."

## Personal statement wording

"My FDE experience showed me that OCR is only the beginning of a document
workflow. The consequential decisions occur after extraction: whether a noisy
field can be standardized safely, whether a historical record can be reused,
and when ambiguity should be handed back to a person. To communicate this work
without exposing sensitive information, I built a separate synthetic demo that
models those decision points with explicit rules and visible review reasons."

## Interview answer

**Question: Why does the public demo use Streamlit instead of the original web
stack?**

"The public demo is intentionally independent and much smaller. I used
Streamlit to make the decision layer easy to inspect in one screen. The actual
internship work was integrated into an existing Django and React application;
the public project does not copy that code or claim to reproduce the full
system."

## Claims to avoid

- Do not say that you trained an OCR model.
- Do not claim that the synthetic percentages are business performance results.
- Do not name or imply access to client data, source code, credentials, or
  proprietary rules.
- Do not describe the demo as a full EDMS or production deployment.
