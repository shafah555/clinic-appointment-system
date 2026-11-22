# Project report guide — CarePoint Clinic Appointment Management System

Use this as a report-writing guide. Replace every instruction in square brackets with your own actual work and screenshots.

## Chapter 1: Introduction
Explain the appointment scheduling problem, project objectives, scope, and limitations.

## Chapter 2: Requirements
Include functional and non-functional requirements, user stories, and use cases. Use the requirements in your assignment brief and verify them against the implemented demo.

## Chapter 3: Process model
Selected model: Agile Incremental. Explain why modules can be developed and tested in increments. Include your actual development iteration table.

## Chapter 4: System design
Include your UML class diagram, database/ER diagram, architecture diagram, and prototype screenshots. The implementation currently uses User, Doctor, Appointment, Bill and Notification database models. The role factory classes are demonstration domain objects.

## Chapter 5: Design patterns
Explain Factory Method, Facade and Observer. For each: problem, implementation file, benefit and rejected alternative. Add screenshots of your own source code.

## Chapter 6: Implementation
Add screenshots of the home page, doctor list/search, booking form, appointments, billing and notifications. Explain the main routes and database persistence.

## Chapter 7: Testing
Explain RED-GREEN-REFACTOR. Add actual Pytest output, test cases, coverage report, mock usage and Selenium results. Do not invent test counts or coverage percentages.

## Chapter 8: Configuration management and CI
Add repository link, branch list, meaningful commits, one accepted PR, one revised/rejected PR, a real merge conflict and its resolution, plus a GitHub Actions run.

## Chapter 9: Self-directed learning
Explain OpenAPI/Swagger. Import `openapi.yaml` into Swagger Editor, inspect and improve the specification, and document what you learned. The project includes a starter OpenAPI document, not a full interactive Swagger server.

## Chapter 10: Reflection and conclusion
Write a 500–700 word reflection based on what you actually did, challenges, resources evaluated, lessons learned, and the next skill you plan to learn.

## Screenshot checklist
- [ ] Home page
- [ ] Doctor directory and search
- [ ] Appointment booking
- [ ] Duplicate slot rejection
- [ ] Appointment status update
- [ ] Billing invoice
- [ ] Notification centre
- [ ] Database in Neon
- [ ] UML and ER diagrams
- [ ] Pytest and coverage output
- [ ] Selenium run
- [ ] Git branches and commits
- [ ] Accepted and revised/rejected pull requests
- [ ] Merge conflict and resolution
- [ ] GitHub Actions result
- [ ] OpenAPI/Swagger Editor
- [ ] Render deployment dashboard and live URL

## Viva talking points
Explain why the project uses an incremental process, where each pattern appears, how duplicate appointments are prevented, why tests use an isolated database, what GitHub Actions checks, and what OpenAPI adds.
