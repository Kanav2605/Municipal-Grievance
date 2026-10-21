# Municipal Grievance - Contribution Guidelines

## Branches
- main: stable releases
- develop: shared integration branch
- feat/nlp-baseline: NLP team
- feat/cv-baseline: Computer Vision team
- feat/dedup-engine: Deduplication team
- feat/risk-model: Predictive Maintenance team
- feat/backend-api: Backend team
- feat/citizen-portal: Citizen Portal team
- feat/officer-dashboard: Officer Dashboard team

## Workflow
1. Work only on your assigned feature branch.
2. Pull the latest changes before starting work.
3. Make changes within your assigned directory.
4. Test your code before committing.
5. Push your branch to GitHub.
6. Open a pull request targeting develop.
7. Request a review before merging.

## Commit Messages
Use descriptive messages such as:
- feat(nlp): add complaint classification
- feat(backend): add complaint submission endpoint
- fix(dedup): handle missing coordinates
- docs: update API contracts

## Security
- Never commit passwords, API keys, or private citizen data.
- Keep local .env files out of Git.
- Do not commit large datasets or model weights.
- Use synthetic data for development and demonstrations.
