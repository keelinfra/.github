<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)"
          srcset="https://raw.githubusercontent.com/keelinfra/.github/main/assets/wordmark-dark.svg">
  <img alt="keelinfra" width="420"
       src="https://raw.githubusercontent.com/keelinfra/.github/main/assets/wordmark-light.svg">
</picture>

**Production-ready, self-hosted open-source infrastructure.**

HA · Backups & PITR · Observability · Tested upgrades — on your own machines, in one command.

[keelinfra.io](https://keelinfra.io) · [Pricing](https://keelinfra.io/pricing)

</div>

---

Great open-source infrastructure is easy to start and hard to run. keelinfra ships distributions that package what every team ends up building by hand — clustering, HA databases, backup and point-in-time recovery, monitoring, and upgrade paths that are actually tested against every upstream release.

Built for teams that can't or won't hand their data to a managed cloud: regulated industries, data residency, air-gapped environments.

| Project | What it is | Status |
|---|---|---|
| [**keycloak**](https://github.com/keelinfra/keycloak) | HA Keycloak distribution: Patroni-managed PostgreSQL, pgBackRest PITR, Prometheus/Grafana, tested upgrade paths | 🟢 working |
| **openbao** | The same treatment for OpenBao (secrets) | ⚪ coming next |

```bash
git clone https://github.com/keelinfra/keycloak && cd keycloak
./configure -c examples/ha-3node.yml
./install    # ~10 minutes on 3 clean VMs
```

The distributions are free and Apache-2.0. A per-node subscription adds offline bundles, CVE tracking, upgrade runbooks, and direct access to the people who build it.
