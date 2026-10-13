<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="https://raw.githubusercontent.com/keelinfra/.github/main/assets/wordmark-dark.svg">
  <img alt="keelinfra" width="420"
       src="https://raw.githubusercontent.com/keelinfra/.github/main/assets/wordmark-light.svg">
</picture>

**Production-ready, self-hosted open-source infrastructure.**

Self-hosted Keycloak · Jenkins agents for legacy build hosts — on your own machines, tested in public CI.

[keelinfra.io](https://keelinfra.io) · [Keycloak docs](https://keelinfra.io/docs/keycloak/) · [Agent8](https://github.com/keelinfra/agent8)

</div>

---

Great open-source infrastructure is easy to start and hard to run. keelinfra ships distributions that package what every team ends up building by hand — clustering, HA databases, backup and point-in-time recovery, monitoring, and upgrade paths that are actually tested against every upstream release.

Built for teams that can't or won't hand their data to a managed cloud, and for the long tail of machines that can't simply be upgraded: regulated industries, data residency, air-gapped environments, legacy build hosts.

### [keelinfra/keycloak →](https://github.com/keelinfra/keycloak)

**Production-ready, self-hosted Keycloak.** HA cluster, Patroni-managed PostgreSQL with automatic failover, pgBackRest backups & point-in-time recovery, Prometheus/Grafana monitoring, and upgrade paths tested against upstream releases.

### [keelinfra/agent8 →](https://github.com/keelinfra/agent8)

**Agent8 for Jenkins: run Jenkins agents on hosts stuck on Java 8, 11 or 17.** Current Jenkins needs Java 21 on every agent, which RHEL/CentOS 6, AIX, Solaris and HP-UX build hosts can't run. Agent8 is the Jenkins agent, built to run on their Java, so they stay ordinary nodes of an up-to-date controller. Available and free: an install script with checksum verification, an Ansible playbook for fleets, and a release tested for each Jenkins version. Linux (HotSpot and OpenJ9) is tested in CI; AIX, Solaris and HP-UX are experimental. [Why it's needed →](https://keelinfra.io/blog/jenkins-java-21-aix-rhel6-build-hosts/) · [Help with a rollout →](https://keelinfra.io/jenkins-assessment/)

---

<sub>Everything here is free and open source: the Keycloak distribution under Apache-2.0, Agent8 under MIT (its jars include LGPL-2.1 classes from JvmDowngrader). For Keycloak, a [per-node subscription](https://keelinfra.io/keycloak/pricing/) adds offline bundles, CVE tracking, upgrade runbooks, and direct access to the people who build it.</sub>
