<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="https://raw.githubusercontent.com/keelinfra/.github/main/assets/wordmark-dark.svg">
  <img alt="keelinfra" width="420"
       src="https://raw.githubusercontent.com/keelinfra/.github/main/assets/wordmark-light.svg">
</picture>

**Open-source tools that keep Jenkins, GitLab and their build hosts current.**

Jenkins agents for legacy build hosts · security fixes for Jenkins 2.541.x on Java 17 · a tested upgrade path for old controllers · GitLab Runner for AIX.

[keelinfra.io](https://keelinfra.io) · [Agent8](https://github.com/keelinfra/agent8) · [Extended Security](https://github.com/keelinfra/jenkins-extended-security) · [Upgrade matrix](https://keelinfra.io/jenkins/upgrade-matrix/) · [AIX Runner](https://github.com/keelinfra/aix-runner)

</div>

---

Jenkins moves fast; the machines around it don't. Controllers sit on old LTS lines because nobody knows which plugins will break or because they can't leave Java 17 yet, and build hosts on AIX, Solaris and HP-UX can't run the Java a current agent needs. keelinfra builds the tools and publishes the test data that get them current again.

### [keelinfra/agent8 →](https://github.com/keelinfra/agent8)

**Agent8 for Jenkins: run Jenkins agents on hosts stuck on Java 8, 11 or 17.** Current Jenkins needs Java 21 on every agent, which many AIX, Solaris and HP-UX build hosts can't run. Agent8 is the Jenkins agent, built to run on their Java, so they stay ordinary nodes of an up-to-date controller. Available and free: an install script with checksum verification, an Ansible playbook for fleets, and a release tested for each Jenkins version. Linux (HotSpot and OpenJ9) is tested in CI; AIX, Solaris and HP-UX have been tested. [Why it's needed →](https://keelinfra.io/blog/jenkins-java-21-aix-rhel6-build-hosts/) · [Help with a rollout →](https://keelinfra.io/jenkins-assessment/)

### [keelinfra/jenkins-extended-security →](https://github.com/keelinfra/jenkins-extended-security)

**Extended Security for Jenkins 2.541.x: core security fixes for controllers that can't leave Java 17 yet.** Jenkins 2.541.3 is the last LTS that runs on Java 17. This line backports the Jenkins core, Remoting and Stapler fixes released after it, each listed with its upstream commit and any change from upstream. The WAR is reproducible, ships with a checksum, an SBOM and a build attestation, and is built and tested in public CI on Java 17 and 21. Plugins are not patched. Not an official Jenkins release. [Latest release →](https://github.com/keelinfra/jenkins-extended-security/releases/latest)

### [Jenkins upgrade matrix →](https://keelinfra.io/jenkins/upgrade-matrix/)

**Which Jenkins LTS lines can go straight to 2.580.1, and which need to stop on the way.** 328 rehearsed Jenkins starts: 38 LTS lines from 2.60.3 to 2.568.3, with the 100 and the 300 most installed plugins, core-only and in steps. Built with [keelinfra/jenkins-upgrade-check](https://github.com/keelinfra/jenkins-upgrade-check), which can rehearse your own plugin list.

### [AIX Runner for GitLab →](https://github.com/keelinfra/aix-runner)

**GitLab Runner for AIX 7.2 and 7.3, which GitLab doesn't ship.** The unmodified upstream runner with four small dependency patches. CI builds the latest upstream release every day; releases are published by hand. Experimental: the shell executor has been tested on AIX 7.3 (jobs, artifacts, cache, git clone, cancel). For AIX 7.1, Solaris and HP-UX build hosts, see Agent8.

---

<sub>Everything here is free and open source: Agent8 under MIT (its jars include LGPL-2.1 classes from JvmDowngrader), jenkins-extended-security under MIT (its patches keep the Jenkins, Remoting and Stapler licenses), jenkins-upgrade-check under Apache-2.0, aix-runner under MIT (based on GitLab software; not affiliated with GitLab Inc.). The earlier Keycloak distribution was [discontinued](https://keelinfra.io/keycloak/) on 24 October 2026.</sub>
