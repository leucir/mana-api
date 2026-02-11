## Constitution (High-Level)

* **Security is non-negotiable**
* **Multi-tenancy is a first-class concern**
* **Test-Driven Development comes first**
  * No production code without a failing test.
  * Tests define behavior; code exists to satisfy tests.
  * Bugs require regression tests.
* **Domain-Driven Design defines the system**
  * The domain model is the source of truth.
  * Entities, aggregates, and invariants live in the domain layer.
  * Ubiquitous language is used consistently in specs, tests, and code.
* **Object-Oriented design is required**
  * Encapsulate behavior and invariants inside objects.
  * Prefer composition over inheritance.
  * Avoid anemic models and god objects.
* **User experience is a competitive advantage**
  * Performance, clarity, and accessibility are product features.
  * Every flow defines loading, empty, error, and offline states.
  * UX requirements are part of acceptance criteria.
* **AI is encouraged, use it whenever is possible in the capabilities**
* **Architecture enforces clear boundaries**
  * UI, application, domain, and infrastructure are cleanly separated.
* **Reliability and observability are mandatory**
  * Failures are user-friendly and diagnosable.
  * Logging, metrics, and tracing respect security and tenant isolation.
* **Maintainability beats short-term speed**
  * Code must be readable, testable, and evolvable.
  * Delivery speed is optimized only after correctness, security, and UX.
* **Documentation is mandatory**
  * Every feature and domain concept must be documented.
  * Documentation includes **explanations, sample code, and diagrams** where relevant.
  * Undocumented behavior is considered incomplete.
* **Technology stack is fixed**
  * Backend: **Firebase**
    * **Cloud Functions (Python)**
    * **Firestore**
    * **Cloud Storage**
    * **Firebase Hosting** for the backend test

* When principles conflict, they are applied in the following priority order:
1. Correctness and safety (TDD, invariants, tests)
2. Security and privacy
3. User experience
4. Domain integrity (DDD and domain boundaries)
5. Delivery speed and convenience
6. Multi-tenancy isolation
7. Maintainability and architectural clarity
