<a href="https://keelinfra.io">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/keelinfra/.github/main/assets/readme/profile-hero-dark.svg">
    <img alt="keelinfra: CI that can't upgrade yet, kept running. Upstream Jenkins moves on to Java 21 only; keelinfra's 2.541.x line stays on Java 17 with the core security fixes released after it, and build hosts on AIX, Solaris and HP-UX keep Java 8 and connect to a Java 21 controller through Agent8." src="https://raw.githubusercontent.com/keelinfra/.github/main/assets/readme/profile-hero-light.svg" width="100%">
  </picture>
</a>

<p align="center">
  <a href="https://keelinfra.io"><b>keelinfra.io</b></a> &nbsp;·&nbsp;
  <a href="https://keelinfra.io/evidence/"><b>Evidence</b></a> &nbsp;·&nbsp;
  <a href="https://keelinfra.io/blog/"><b>Blog</b></a> &nbsp;·&nbsp;
  <a href="https://keelinfra.io/#get-involved"><b>Get involved</b></a>
</p>

<br>

<p align="center">
  <a href="https://github.com/keelinfra/jenkins-extended-security"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/keelinfra/.github/main/assets/readme/card-jenkins-extended-security-dark.svg"><img alt="Extended Security for Jenkins 2.541.x: Jenkins 2.541.3, the last LTS that runs on Java 17, with the core security fixes released after it." src="https://raw.githubusercontent.com/keelinfra/.github/main/assets/readme/card-jenkins-extended-security-light.svg" width="48%"></picture></a>
  <a href="https://github.com/keelinfra/agent8"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/keelinfra/.github/main/assets/readme/card-agent8-dark.svg"><img alt="Agent8 for Jenkins: run Jenkins agents on hosts stuck on Java 8, 11 or 17, while the controller moves to Java 21." src="https://raw.githubusercontent.com/keelinfra/.github/main/assets/readme/card-agent8-light.svg" width="48%"></picture></a>
</p>
<p align="center">
  <a href="https://keelinfra.io/jenkins/upgrade-matrix/"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/keelinfra/.github/main/assets/readme/card-jenkins-upgrade-check-dark.svg"><img alt="Jenkins upgrade matrix: which Jenkins LTS lines can go straight to 2.580.2, and which need to stop on the way." src="https://raw.githubusercontent.com/keelinfra/.github/main/assets/readme/card-jenkins-upgrade-check-light.svg" width="48%"></picture></a>
  <a href="https://github.com/keelinfra/aix-runner"><picture><source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/keelinfra/.github/main/assets/readme/card-aix-runner-dark.svg"><img alt="AIX Runner for GitLab: GitLab Runner for AIX 7.2 and 7.3, which GitLab doesn't ship." src="https://raw.githubusercontent.com/keelinfra/.github/main/assets/readme/card-aix-runner-light.svg" width="48%"></picture></a>
</p>

<br>

### How every keelinfra project works

| **01 · Open source first** | **02 · Tested in public** | **03 · Built with its users** |
| :-- | :-- | :-- |
| The code, install scripts and tests are public. You can run everything without talking to us. | Linux, the upgrade rehearsals and the security backports are tested in public CI. AIX, Solaris and HP-UX are tested by hand, not in CI, and each README says so. [The evidence ledger →](https://keelinfra.io/evidence/) | Bugs, questions and fixes go to each project's issues and pull requests, where the answer helps the next person too. A test report from a platform we can't reach is the most useful thing you can send. |

<br>

<sub>Everything here is free and open source: Agent8 under MIT (its jars include LGPL-2.1 classes from JvmDowngrader), jenkins-extended-security under MIT (its patches keep the Jenkins, Remoting and Stapler licenses), jenkins-upgrade-check under Apache-2.0, aix-runner under MIT (based on GitLab software; not affiliated with GitLab Inc.). Not affiliated with the Jenkins project. The earlier Keycloak distribution was [discontinued](https://keelinfra.io/keycloak/) on 24 October 2026.</sub>
