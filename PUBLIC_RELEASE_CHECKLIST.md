# HYDRA Public Release Checklist

Use this before publishing a recruiter-facing build.

## Identity and links
- [ ] Set the real public repository URL in `site.config.js`.
- [ ] Set LinkedIn only when the profile is ready for recruiter traffic.
- [ ] Set a public contact email only if desired.
- [ ] Confirm no private file paths, usernames, internal hostnames, or secrets are present.

## Truth / scope
- [ ] Every capability labeled current is actually demonstrable.
- [ ] AWS services remain roadmap/target language until a real AWS slice is deployed.
- [ ] Representative walkthroughs remain visibly labeled until replaced by real sanitized artifacts.
- [ ] No production-scale metrics are published unless measured and reproducible.
- [ ] No proprietary purchased data is redistributed.

## Engineering proof
- [ ] Public repo README matches the website story.
- [ ] At least one reproducible test path is documented.
- [ ] At least one sanitized receipt / output is available.
- [ ] Architecture diagram matches the public code surface.

## Web release
- [ ] Run `TEST_HYDRA_SITE.ps1`.
- [ ] Check desktop and mobile layouts.
- [ ] Verify keyboard navigation and visible focus states.
- [ ] Confirm 404 page, internal links, favicon, and social preview.
- [ ] Add the final production URL to social metadata after deployment.
