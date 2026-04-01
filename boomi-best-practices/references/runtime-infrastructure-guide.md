# Runtime Infrastructure — Detailed Technical Reference

Deep-dive technical practices for §2 Runtime Infrastructure in `boomi-best-practices`.
Organized by sub-category matching the operational surface of Boomi runtimes.
Each item carries a runtime scope tag: `[Basic Atom]` `[Molecule]` `[Cloud Cluster]` `[All]`.

> **Source:** Boomi help.boomi.com, community.boomi.com, and field-validated practices.
> Always verify against live release notes — settings and defaults change with each runtime release.

---

## JVM Configuration

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Basic Atom | High | Set `-Xms` and `-Xmx` to the **same value** (e.g., `-Xms2g -Xmx2g`) to prevent heap resizing at runtime | Heap resizing triggers GC pauses and latency spikes | [help.boomi.com](https://help.boomi.com/bundle/integration/page/t-atm-Increasing_memory_available_to_Atom_or_Molecule.html) |
| Basic Atom | High | Set minimum JVM heap to **1 GB for dev; 2–4 GB for production** | Undersized heap causes frequent GC, OOM errors, and process aborts | [Atom system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Atom_system_requirements_e3656558-174d-438e-bc5a-6dd48d20c159) |
| Basic Atom | Medium | Enable `-XX:+HeapDumpOnOutOfMemoryError` in the Advanced Properties panel | Captures heap state automatically on OOM — essential for root cause analysis | [Properties panel](https://help.boomi.com/bundle/integration/page/r-atm-Properties_panel_Advanced_tab.html) |
| Basic Atom | High | Use **G1GC** (`-XX:+UseG1GC`) for production Atoms on Java 11+; set `-XX:MaxGCPauseMillis=200` as a starting point | G1GC provides predictable pause times vs Parallel GC — critical for listener-based workloads | [Boomi Community GC Blueprint](https://community.boomi.com/s/article/Boomi-Blueprint-Garbage-Collection) |
| Basic Atom | Medium | Configure GC logging (`-Xlog:gc*` on Java 11+) to a location **outside** the Atom install directory | GC logs are essential for diagnosing memory pressure; without them, slow degradation is invisible | [JMX monitoring](https://help.boomi.com/bundle/integration/page/r-atm-System_monitoring_with_JMX.html) |
| Molecule | High | Set JVM heap **per node** based on physical RAM; do not apply a single-size template across unequal hardware | Over-provisioning on smaller nodes causes OS-level swap, degrading the entire cluster | [Molecule system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Molecule_system_requirements_41f9a675-ab11-4f3b-bf51-1655394aba5b) |
| Molecule | High | Set Molecule node heap to **minimum 2 GB; 4+ GB** for high-concurrency deployments | Each node hosts a primary JVM + dozens of forked JVMs; size the primary JVM independently of forked runner heap | [Memory sizing](https://community.boomi.com/s/article/how-memory-sizing-works) |
| Molecule | High | **Do not** set the Molecule node heap too high when forked execution is enabled; reserve physical RAM for forked runner JVMs | Peak forked RAM = Runner Heap Size × Max Simultaneous Forked Executions per Node (default: 512 MB × 50 = **25 GB per node**) | [Forked execution sizing](https://www.xtivia.com/blog/boomi-molecule-forked-execution-pt2/) |
| Cloud Cluster | Medium | For private/dedicated Atom Clouds, apply the same G1GC and heap settings as Molecules; public clouds are Boomi-managed | Dedicated cloud nodes behave identically to Molecule nodes | [Cloud system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Atom_Cloud_system_requirements_45494670-1aa1-452f-8bb2-1928778a1041) |
| All | High | Use **Amazon Corretto OpenJDK** (not Oracle JDK) for Java 11+; Boomi no longer supports Oracle as JDK provider for Java 11 | Oracle JDK creates an unsupported configuration that Boomi support may decline to assist with | [Java upgrade FAQ](https://help.boomi.com/docs/Atomsphere/Integration/Integration%20management/c-atm-Java_upgrade_FAQ_7235338a-f640-4fa5-89be-c1e4e17f776c) |
| All | Medium | Manage JVM options via the **Properties Panel** (`container.properties`), not by directly editing `atom.vmoptions` | Properties set via UI are persisted and survive upgrades; manual edits to `atom.vmoptions` may be overwritten during runtime updates | [Startup Properties panel](https://help.boomi.com/bundle/integration/page/r-atm-Startup_Properties_panel.html) |

---

## Forked Execution

**Forked execution isolates each process in its own JVM — enabled by default on Clouds, recommended for production Molecules.**

**Memory math:** `Peak RAM = Runner Heap Size × Max Simultaneous Forked Executions × Nodes`
Default: `512 MB × 50 × node count`

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Molecule | High | Enable forked execution in production Molecules | JVM failures in one process do not crash the head node or other executions | [Forked execution docs](https://help.boomi.com/bundle/integration/page/c-atm-Forked_execution_in_Molecules_and_Atom_Clouds.html) |
| Molecule | High | Set **Runner Heap Size** based on your largest payload process; start at 512 MB, increase only if needed | Peak RAM = Runner Heap × Max Simultaneous Forked Executions × Nodes — oversizing causes OS-level OOM | [Memory sizing](https://community.boomi.com/s/article/how-memory-sizing-works) |
| Molecule | High | Tune **Max Simultaneous Forked Executions Per Node** (default: 50) downward if node RAM < 32 GB | At 50 × 512 MB = 25 GB peak per node just for forked JVMs; reduce to 10–20 on constrained nodes | [Forked execution tuning](https://www.xtivia.com/blog/boomi-molecule-forked-execution-pt2/) |
| Molecule | Medium | Set **Max Queued Forked Executions Per Node** (default: 200) to cap burst queue depth | Unbounded queuing during traffic spikes consumes heap holding queued execution metadata | [Forked execution properties](https://help.boomi.com/bundle/integration/page/t-atm-Setting_forked_execution_properties_for_a_Molecule.html) |
| Molecule | Medium | Set **Max Execution Threads Per Forked Execution** (default: 50) based on Flow Control concurrency needs | Thread pools are per-forked-JVM; oversetting wastes memory, undersetting throttles Flow Control parallelism | [Atom workers](https://help.boomi.com/bundle/integration/page/c-atm-Atom_workers.html) |
| Cloud Cluster | High | Forked execution is enabled by default on all Atom Clouds; **do not disable** unless directed by Boomi support | Cloud architecture relies on process isolation via forked JVMs; disabling collapses all executions into the cluster JVM | [Forked execution docs](https://help.boomi.com/bundle/integration/page/c-atm-Forked_execution_in_Molecules_and_Atom_Clouds.html) |
| Cloud Cluster | Medium | For private Atom Clouds, tune forked execution properties using the same methodology as Molecules | Private clouds are architecturally Molecules; same memory math applies | [Cloud system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Atom_Cloud_system_requirements_45494670-1aa1-452f-8bb2-1928778a1041) |
| All | High | Test all forked execution tuning changes in non-production first; some properties require restart | Misconfiguration can cause process starvation (too few slots) or node OOM (too many) | [Forked execution tuning](https://www.xtivia.com/blog/boomi-molecule-forked-execution-pt2/) |

---

## Clustering & NFS (Molecule / Cloud Cluster)

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Molecule | High | Synchronize all Molecule node clocks using NTP; set all nodes and the NFS server to the same timezone | Clock skew causes file locking errors, split-brain conditions, and unpredictable head node election | [Molecule install checklist](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/int-Molecule_installation_checklist_Linux_cff53cf9-83a2-400b-9cf0-f4f1a76013df) |
| Molecule | High | All nodes must run the **same OS and architecture** (e.g., all Linux x64); do not mix OS types | Mismatched architectures cause file locking incompatibilities and unpredictable class-loading | [Molecule system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Molecule_system_requirements_41f9a675-ab11-4f3b-bf51-1655394aba5b) |
| Molecule | High | Prefer **Linux** for production Molecule deployments; Boomi explicitly states Windows clusters can have unpredictable stability | Boomi's own guidance recommends Linux for production cluster environments | [Private cloud best practices](https://community.boomi.com/s/article/privateatomcloudconfigurationandmonitoringbestpractices) |
| Molecule | Medium | Use **multicast** (UDP 45588) for inter-node communication in trusted LAN environments; use **unicast** (TCP 7800) only when multicast is blocked | Multicast is more efficient for cluster health broadcast; unicast required when nodes span subnets | [Molecule system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Molecule_system_requirements_41f9a675-ab11-4f3b-bf51-1655394aba5b) |
| Molecule | High | Configure shared NFS mount with options: **`vers=3,noatime,nodiratime,hard,intr`**; enable NLM (file locking) on the NFS server | NFS without NLM causes data corruption on concurrent node writes; `hard` mount prevents silent I/O failures | [NFS options community Q&A](https://community.boomi.com/s/question/0D51W00006As0XnSAJ/what-are-the-recommended-nfs-options-for-a-shared-nfs-optboomi-mount-for-molecule) |
| Molecule | High | Ensure the NFS server is **not a single point of failure**; use HA NFS (Azure NetApp Files, AWS EFS, clustered NFS) | An NFS server failure takes down all Molecule nodes simultaneously, defeating the purpose of clustering | [NFS HA community Q&A](https://community.boomi.com/s/question/0D51W000089HhPGSA0/we-are-evaluating-shared-drivenfs-for-setting-up-boomi-molecule) |
| Molecule | High | Use **SMB/CIFS** (not NFS) as the shared file system on Windows-based Molecule clusters | Boomi recommends SMB/CIFS for Windows; NFS on Windows requires third-party clients that may not support required NLM semantics | [Molecule system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Molecule_system_requirements_41f9a675-ab11-4f3b-bf51-1655394aba5b) |
| Cloud Cluster | Medium | For private Atom Clouds on IaaS, use the cloud provider's **managed file service** (EFS, Azure Files, GCP Filestore) rather than self-managed NFS | Managed file services provide built-in HA, automatic failover, and SLA-backed durability | [HA on AWS](https://community.boomi.com/s/article/High-Availability-AWS-Integration-Runtime) |

---

## Disk I/O & Storage

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Basic Atom | High | Place the Atom installation directory on **local SSD** storage, never on NFS/SMB/network-mounted filesystem | Network storage introduces latency and failure paths into every process execution | [Working data storage](https://help.boomi.com/docs/atomsphere/integration/integration%20management/c-atm-molecule_and_atom_cloud_working_data_storage_b18ef1af-1e37-4a33-8712-d600f4e7b29d/) |
| Basic Atom | High | Ensure at least **50 GB free** disk space on the Atom partition; 100+ GB recommended for production with 30-day purge | Disk exhaustion causes process failures and can corrupt the working data directory | [Disk space best practices](https://community.boomi.com/s/article/Best-practices-for-avoiding-disk-space-issues) |
| Basic Atom | High | **Do not** use `/tmp` or `/var/tmp` as the Atom working data directory | The OS may purge `/tmp` on reboot or via cron, removing in-flight process data mid-execution | [Working data storage](https://help.boomi.com/docs/atomsphere/integration/integration%20management/c-atm-molecule_and_atom_cloud_working_data_storage_b18ef1af-1e37-4a33-8712-d600f4e7b29d/) |
| Molecule | High | Enable **local storage for working data** on each node; do not use the shared NFS as the working data location | Local I/O dramatically reduces NFS traffic; only coordination metadata needs to traverse the shared file system | [Enabling local storage](https://help.boomi.com/docs/atomsphere/integration/integration%20management/t-atm-enabling_local_storage_for_a_molecule_or_atom_cloud_8861cfb6-79fa-46bc-a957-a4a3cfa45d5f/) |
| Molecule | High | Configure **both** "Use Local Storage for Runtime Assets" AND "Working Data Local Storage Directory" | Enabling only one provides partial benefit; both are required to move all transient I/O off the shared file system | [Enabling local storage](https://help.boomi.com/docs/atomsphere/integration/integration%20management/t-atm-enabling_local_storage_for_a_molecule_or_atom_cloud_8861cfb6-79fa-46bc-a957-a4a3cfa45d5f/) |
| Molecule | High | Working Data Local Storage Directory must **NOT** be a subdirectory of the shared NFS mount point | Boomi explicitly prohibits this configuration — it defeats the purpose of local storage | [Working data storage](https://help.boomi.com/docs/atomsphere/integration/integration%20management/c-atm-molecule_and_atom_cloud_working_data_storage_b18ef1af-1e37-4a33-8712-d600f4e7b29d/) |
| Molecule | Medium | Size working data local storage per node at **3× peak daily data volume** to accommodate purge lag | Data accumulates between purge cycles; insufficient local storage causes node failures even if shared FS has capacity | [Disk space best practices](https://community.boomi.com/s/article/Best-practices-for-avoiding-disk-space-issues) |
| Cloud Cluster | High | Apply the same local storage configuration as Molecules for private Atom Cloud nodes | Cloud cluster nodes share the same storage architecture as Molecule nodes | [Cloud system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Atom_Cloud_system_requirements_45494670-1aa1-452f-8bb2-1928778a1041) |
| All | High | Monitor disk usage; **alert at 70%** utilization and take action before 85% | Disk exhaustion is one of the most common causes of Atom instability — causes execution failures, log loss, and may render the Atom unrecoverable | [Disk space best practices](https://community.boomi.com/s/article/Best-practices-for-avoiding-disk-space-issues) |

---

## High Availability

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Basic Atom | High | **Do not** use a Basic Atom (single-node) for mission-critical production integrations; upgrade to Molecule or Cloud Atom | A single Atom node is a SPOF — any crash, reboot, or OS patch causes full downtime with no automatic failover | [Atoms, Molecules, and Clouds](https://help.boomi.com/docs/Atomsphere/Integration/Getting%20started/int-Atoms_Molecules_and_Atom_Clouds_d8fe8ad8-3ba5-4eb1-967d-cd0fc9ffb062) |
| Basic Atom | High | If a Basic Atom must be used for production, implement an **external health-check and auto-restart** (systemd, AWS Auto Recovery, etc.) | Without automatic restart, an Atom crash requires manual intervention — minutes to hours of downtime | [HA and DR best practices](https://community.boomi.com/s/article/bestpracticesforruntimehighavailabilityanddisasterrecovery) |
| Molecule | High | Deploy a **minimum of 3 Molecule nodes** in production; 2 nodes provides redundancy but no quorum safety | With 3 nodes, 1 failure still maintains quorum and cluster operation; with 2 nodes, a single failure risks split-brain | [Molecule system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Molecule_system_requirements_41f9a675-ab11-4f3b-bf51-1655394aba5b) |
| Molecule | Medium | **Do not exceed 10 nodes** in a Molecule cluster; Boomi recommends against larger clusters | Beyond 10 nodes, coordination overhead increases and head node election slows; use multiple separate Molecules for very high scale | [Molecule system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Molecule_system_requirements_41f9a675-ab11-4f3b-bf51-1655394aba5b) |
| Molecule | High | Place Molecule nodes on **separate physical hosts or separate availability zones** to avoid correlated failures | Co-locating all nodes on the same physical host or same AZ means a single failure takes down the entire cluster | [HA and DR best practices](https://community.boomi.com/s/article/bestpracticesforruntimehighavailabilityanddisasterrecovery) |
| Molecule | High | Deploy an **HTTP load balancer** in front of Molecule nodes for inbound web service requests; do not expose individual node IPs | Without a load balancer, clients hardcoded to a specific node experience downtime when that node fails | [Load balancer blueprint](https://www.loadbalancer.org/applications/boomi-blueprint/) |
| Molecule | High | Molecule head node election is **automatic** — do not manually assign a permanent head node | Interfering with head node migration (e.g., always restarting the same node first) can cause `MULTIPLE_HEAD_NODES` errors | [Avoiding MULTIPLE_HEAD_NODES](https://community.boomi.com/s/article/How-to-avoid-MULTIPLE-HEAD-NODES-during-manual-molecule-restart) |
| Cloud Cluster | High | For workloads requiring VPN connectivity, data residency, or >512 MB per execution, use **Dedicated or Managed Cloud** over Public Cloud | Public cloud has shared execution limits (512 MB default) and no VPN support | [Atom Clouds](https://help.boomi.com/bundle/integration/page/c-atm-The_Dell_Boomi_Atom_Clouds.html) |
| Cloud Cluster | High | For private Atom Clouds, deploy a **minimum of 3 cluster nodes** | Private clouds are customer-managed and have all the same SPOF risks as under-provisioned Molecules | [Cloud system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Atom_Cloud_system_requirements_45494670-1aa1-452f-8bb2-1928778a1041) |

---

## Disaster Recovery

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Basic Atom | High | Document a **DR runbook** for Basic Atom recovery: installer location, service account credentials, connection properties backup, re-deployment procedure | Undocumented recovery extends MTTR; a tested runbook enables any ops team member to restore within a defined RTO | [HA and DR best practices](https://community.boomi.com/s/article/bestpracticesforruntimehighavailabilityanddisasterrecovery) |
| Molecule | High | Export and **back up Molecule configuration** (`atom.vmoptions`, `container.properties`) to a version-controlled repository after each change | Configuration drift is common; without a backup, rebuilding after catastrophic failure requires reconstructing from memory | [HA and DR best practices](https://community.boomi.com/s/article/bestpracticesforruntimehighavailabilityanddisasterrecovery) |
| Molecule | High | **Test DR recovery procedures at least annually** by simulating a head node failure | Untested DR is not DR; head node election should complete within seconds, but networking or NFS issues can prevent this | [HA and DR best practices](https://community.boomi.com/s/article/bestpracticesforruntimehighavailabilityanddisasterrecovery) |
| Cloud Cluster | High | For Boomi Public/Dedicated Cloud, document a **process re-deployment plan**; Boomi's infrastructure DR does not cover customer process configurations | Boomi's DR protects infrastructure, not customer-deployed processes | [Disaster recovery overview](https://community.boomi.com/s/article/disaster-recovery-overview) |
| All | High | **Export and commit all deployed process packages to a Git repository** as part of the CI/CD pipeline | Process components stored only in the platform are at risk during account-level disasters; external version control provides an independent recovery point | [HA and DR best practices](https://community.boomi.com/s/article/bestpracticesforruntimehighavailabilityanddisasterrecovery) |

---

## Purge Settings

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Basic Atom | High | Set "Purge History After x Days" to **30 days** for production; **never set to 0** (disabled) | Value of 0 disables purging entirely, causing unbounded disk growth from execution logs, documents, and temp files | [Purge logs and data](https://help.boomi.com/bundle/integration/page/c-atm-Purging_of_Atom_Molecule_or_Cloud_logs_and_data.html) |
| Basic Atom | Medium | Use **independent purge schedules** (`com.boomi.container.logs.purgeDays`, `com.boomi.container.data.purgeDays`, `com.boomi.container.temp.purgeDays`) for granular control | Different data types have different retention value; granular settings avoid over- or under-retention | [Independent purge schedules](https://help.boomi.com/docs/Atomsphere/Integration/Integration%20management/t-atm-Setting_independent_purge_schedules_896936a6-d360-4f19-becb-abe7f9aa425a) |
| Basic Atom | Medium | **Restart the Atom** after changing purge schedule properties; changes do not take effect until restart | Without restart, purge changes have no effect and disk continues to grow at the old retention rate | [Purge logs and data](https://help.boomi.com/bundle/integration/page/c-atm-Purging_of_Atom_Molecule_or_Cloud_logs_and_data.html) |
| Molecule | Medium | For high-volume Molecules, **increase the purge thread count** above the default (single-threaded) | Single-threaded purging on a high-volume node can take hours, keeping disk usage elevated for extended periods | [Purge logs and data](https://help.boomi.com/bundle/integration/page/c-atm-Purging_of_Atom_Molecule_or_Cloud_logs_and_data.html) |
| Cloud Cluster | High | For private Atom Clouds, configure **purge schedules per cloud account** to prevent one tenant's data from consuming disproportionate disk space | Multi-tenant clouds: a single account with no purge can affect the entire cluster's storage capacity | [Purge for cloud accounts](https://help.boomi.com/docs/atomsphere/integration/integration%20management/t-atm-setting_purge_schedules_for_an_atom_cloud_accounts_c232593a-21f4-4c1f-9fca-ef8648725d95/) |
| All | Medium | Do not rely solely on Boomi's local purge for document archiving; implement an **external archival strategy** for compliance/replay documents | Boomi's purge is a deletion mechanism, not an archive; export to S3/SFTP/etc. before the purge window expires | [Disk space best practices](https://community.boomi.com/s/article/Best-practices-for-avoiding-disk-space-issues) |

---

## Runtime Release Management

> **Naming note:** "Deployment" in this context refers to **runtime software updates** (Boomi quarterly releases), not SDLC process deployment — that is covered in §4 Deployment & Environments.

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Basic Atom | High | Set Runtime Release schedule to **SCHEDULED** (not MANUAL) with a maintenance window 1–2 weeks before the official Platform Release date | MANUAL schedules require human intervention for every update; missed updates accumulate unpatched security vulnerabilities | [Release Control Scheduling](https://help.boomi.com/docs/Atomsphere/Integration/Integration%20management/r-atm-Release_Control_Scheduling_panel_561dc2b7-3beb-49aa-91a4-8d0f6ed95685) |
| Basic Atom | High | Apply Runtime Release updates during a **low-traffic maintenance window** | Runtime updates restart the Atom process; updates during business hours risk interrupting in-flight executions | [Release best practices](https://community.boomi.com/s/article/Release-Best-Practices) |
| Molecule | High | Apply Runtime Release updates in a **rolling fashion** (one node at a time), not all nodes simultaneously | Rolling restarts maintain cluster availability during updates; simultaneous restart causes a full cluster outage | [Release best practices](https://community.boomi.com/s/article/Release-Best-Practices) |
| Molecule | High | **Validate a new Runtime Release in non-production** before applying to production | Boomi releases runtimes 2 weeks before Platform Release specifically to enable non-prod validation | [Runtime and AtomSphere releases](https://help.boomi.com/docs/Atomsphere/Platform/atm-Runtime_and_Atomsphere_releases_8aa6b48e-b0b6-4382-8ffa-a7cf23f0314f) |
| Cloud Cluster | High | For Boomi Public/Dedicated Cloud, validate integrations on the test cloud **during the 2-week validation window** before Platform Release | This window is the change validation opportunity; issues must be reported to Boomi support during this window | [Runtime and AtomSphere releases](https://help.boomi.com/docs/Atomsphere/Platform/atm-Runtime_and_Atomsphere_releases_8aa6b48e-b0b6-4382-8ffa-a7cf23f0314f) |
| All | High | Keep runtimes **within 1–2 releases** of the current Boomi platform release; 3+ releases behind is unsupported | Boomi support may decline to assist with very old runtimes; old runtimes also miss quarterly Amazon Corretto security patches | [Runtime and AtomSphere releases](https://help.boomi.com/docs/Atomsphere/Platform/atm-Runtime_and_Atomsphere_releases_8aa6b48e-b0b6-4382-8ffa-a7cf23f0314f) |
| All | High | Apply **quarterly Amazon Corretto (Java) updates** included with runtime releases | Outdated JVMs have known CVEs; Boomi bundles Corretto updates to maintain a patched JVM | [Java upgrade FAQ](https://help.boomi.com/docs/Atomsphere/Integration/Integration%20management/c-atm-Java_upgrade_FAQ_7235338a-f640-4fa5-89be-c1e4e17f776c) |

---

## Network

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Basic Atom | High | Ensure outbound HTTPS (port 443) access to `*.boomi.com`; this is the **only port** required for Atom-to-platform communication | Inbound firewall holes are not required; blocking port 443 outbound renders the Atom unable to receive deployments or report status | [Atom communication security](https://help.boomi.com/docs/atomsphere/platform/c-atm-atom_communication_security_63f5d42d-614e-4b0a-942d-d8693fd8000b/) |
| Basic Atom | High | For Atoms hosting inbound web service listeners, place a **reverse proxy or load balancer** in front; do not expose the Atom's listen port (default 9090) directly to the internet | Direct internet exposure bypasses WAF protection and exposes the JVM to direct attack | [Shared Web Server](https://help.boomi.com/docs/Atomsphere/Integration/Event-based%20integration/r-atm-Shared_Web_Server_panel_135fde50-19db-488d-bb5c-b9ef43456e75) |
| Basic Atom | High | Restrict the Atom Shared Web Server to **TLS 1.2 minimum**; disable TLS 1.0 and 1.1 via startup property | TLS 1.0 and 1.1 have known vulnerabilities (BEAST, POODLE) | [TLS restriction community Q&A](https://community.boomi.com/s/question/0D51W00006PTInnSAH/how-to-restrict-ssl-to-accept-only-tls12-on-local-atommolecule) |
| Molecule | High | Open internal cluster communication ports between all nodes: **UDP 45588** (multicast) or **TCP 7800** (unicast) | Cluster gossip and leadership election use these ports; blocking them causes nodes to appear isolated and triggers erroneous head node re-elections | [Molecule system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Molecule_system_requirements_41f9a675-ab11-4f3b-bf51-1655394aba5b) |
| Molecule | High | Ensure network latency between Molecule nodes is **<10 ms** (ideally <2 ms); do not cluster nodes across geographically separated data centers | High inter-node latency degrades head node election and shared file system locking | [HA and DR best practices](https://community.boomi.com/s/article/bestpracticesforruntimehighavailabilityanddisasterrecovery) |
| Molecule | High | For Molecules hosting inbound web services, put a **load balancer** in front of all nodes using the external base URL | Without a load balancer, a node failure leaves clients pointing at a dead endpoint | [Load balancer blueprint](https://www.loadbalancer.org/applications/boomi-blueprint/) |
| Cloud Cluster | Medium | For Dedicated Cloud with VPN requirements, configure the **VPN tunnel at the cloud cluster level**, not per process | Per-process VPN requires per-process configuration maintenance; cluster-level VPN provides uniform connectivity for all processes | [Atom Clouds](https://help.boomi.com/bundle/integration/page/c-atm-The_Dell_Boomi_Atom_Clouds.html) |

---

## OS & Infrastructure

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Basic Atom | High | Use a dedicated host; minimum **2 vCPU / 4 GB RAM** for production, **4 vCPU / 8 GB RAM** for high-volume workloads | Boomi's minimum spec (1.8 GHz / 2 GB) is a floor, not a production recommendation | [Atom system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Atom_system_requirements_e3656558-174d-438e-bc5a-6dd48d20c159) |
| Molecule | High | Size each node at minimum **4 vCPU / 16 GB RAM** for production; **8 vCPU / 32 GB RAM** for nodes with forked execution at default concurrency | Default forked settings (512 MB × 50) = 25 GB RAM peak just for forked JVMs; 32 GB provides safe headroom | [Community sizing Q&A](https://community.boomi.com/s/question/0D56S00009RlAp3SAF/recommended-cpu-ram-per-atom-and-molecule) |
| Molecule | Medium | Deploy Molecule nodes behind a **VM auto-scaling group** (AWS ASG, Azure VMSS) configured to replace failed nodes automatically | Auto-replacement of failed nodes maintains cluster size without manual intervention | [HA on AWS](https://community.boomi.com/s/article/High-Availability-AWS-Integration-Runtime) |
| Cloud Cluster | High | For private Atom Clouds, follow the same OS and infrastructure sizing guidance as Molecules; Boomi recommends Linux | Private cloud nodes are architecturally identical to Molecule nodes | [Private cloud best practices](https://community.boomi.com/s/article/privateatomcloudconfigurationandmonitoringbestpractices) |
| All | High | Use a **dedicated OS service account** for the Atom process; configure systemd (Linux) or Windows Service for **automatic restart on process exit** | Atom crashes without restart = undetected downtime; systemd/Windows Service restart provides first-line self-healing | [Atom/Molecule install guide](https://community.boomi.com/s/article/HowtoInstallaLocalAtomMoleculeorCloud) |

---

## Attachment Quotas

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Basic Atom | High | Configure **Attachment Quotas** (Max Attachment Size, Max Documents per Batch) on the Atom to prevent a single runaway process from consuming all heap | Without quotas, a process receiving an unexpectedly large payload can trigger an OOM that takes down the entire Atom | [Attachment Quotas](https://help.boomi.com/docs/Atomsphere/Integration/Integration%20management/r-atm-Attachment_Quotas_tab_4fbc3fff-7aaf-4bbd-a2dc-25d0edb5189c) |
| Molecule | High | Set per-node attachment quotas; these apply per forked JVM, so effective limits scale with `node count × forked executions` | Quotas protect individual forked JVMs from OOM; without them, a large payload in one forked execution can exhaust the node's RAM | [Attachment Quotas](https://help.boomi.com/docs/Atomsphere/Integration/Integration%20management/r-atm-Attachment_Quotas_tab_4fbc3fff-7aaf-4bbd-a2dc-25d0edb5189c) |
| Cloud Cluster | High | For private Atom Clouds, configure attachment quotas at the cloud level **and** per account; public clouds have Boomi-managed limits | Multi-tenant clouds require per-account quotas to prevent one account from consuming disproportionate execution resources | [Attachment Quotas](https://help.boomi.com/docs/Atomsphere/Integration/Integration%20management/r-atm-Attachment_Quotas_tab_4fbc3fff-7aaf-4bbd-a2dc-25d0edb5189c) |

---

## Queue Management

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Molecule | Medium | Size the **Shared Queue Server thread pool** (default: 250 threads) based on expected concurrent message consumers; increase for high-throughput event-driven architectures | At 250 threads × 3 nodes = 750 total consumer threads; undersizing causes queue backpressure and message delays | [Shared Queue Server config](https://help.boomi.com/docs/Atomsphere/Integration/Event-based%20integration/t-atm-Configuring_the_Shared_Queue_Server_a722cec1-fafe-4f21-9c33-e0bd0b2c2693) |
| Molecule | Medium | Set **Max Concurrent Executions per Atom queue** based on **downstream system throughput**, not Atom capacity | Setting too high overwhelms the downstream system; too low creates artificial throttling | [Queue concurrency Q&A](https://community.boomi.com/s/question/0D51W00006As25USAR/how-high-is-too-high-for-maximum-concurrent-executions-on-atom-queue-operation) |
| Cloud Cluster | Medium | For private Atom Clouds, configure queue server thread pool and queue depth to balance resources across tenant workloads | Multi-tenant clusters must prevent a single account from monopolizing the queue server | [Shared Queue Server config](https://help.boomi.com/docs/Atomsphere/Integration/Event-based%20integration/t-atm-Configuring_the_Shared_Queue_Server_a722cec1-fafe-4f21-9c33-e0bd0b2c2693) |
| All | Medium | Use Flow Control shape's parallel processing setting with an explicit **maximum thread count** appropriate for Atom heap | Unbounded parallel threads in Flow Control compound with forked execution concurrency | [Flow Control Q&A](https://community.boomi.com/s/question/0D51W00006As2V6SAJ/what-is-the-maximum-number-of-threads-we-can-use-in-a-flow-conrol) |

---

## Runtime Architecture Patterns

| Runtime | Priority | Practice | Rationale | Source |
|---|---|---|---|---|
| Basic Atom | High | **Isolate high-frequency listener processes from batch processes** on separate Atom instances | A batch process consuming 80% of Atom heap will starve concurrent listener processes, causing API latency spikes | [Architecture best practices](https://www.unitedtechno.com/boomi-integration-best-practices-architecture/) |
| Basic Atom | High | **Do not co-locate the Atom** with memory-intensive applications (databases, app servers) on the same host | Competing for RAM with a database leads to OS-level swapping, which is catastrophic for Atom performance | [Atom system requirements](https://help.boomi.com/docs/Atomsphere/Integration/Atom,%20Molecule,%20and%20Atom%20Cloud%20setup/r-atm-Atom_system_requirements_e3656558-174d-438e-bc5a-6dd48d20c159) |
| Molecule | High | Use **separate Molecules for different criticality tiers** (e.g., real-time API Molecule vs. batch ETL Molecule) | Batch processes saturating a Molecule's thread pool will queue out real-time API calls; workload isolation prevents cross-contamination of SLA classes | [Molecule reference architecture](https://community.boomi.com/s/article/Molecule-Boomi-Blueprint-Reference-Architecture) |
| Molecule | Medium | For containerized Molecule deployments on Kubernetes, use the **Boomi Blueprint Kubernetes reference architecture** with StatefulSets and persistent volume claims per node | Standard Deployments/ReplicaSets are unsuitable for Molecule; each node needs a stable identity and persistent local storage | [Kubernetes reference architecture](https://community.boomi.com/s/article/Scalable-Runtime-Fabric-based-on-Kubernetes-Cluster-and-Docker) |
| Cloud Cluster | High | Choose **Dedicated or Managed Cloud** over Public Cloud when processing PII/PHI data that must not co-mingle with other tenants' data | Public cloud is multi-tenant; dedicated/managed provides single-tenant isolation for HIPAA, GDPR, PCI-DSS compliance | [Atom Clouds](https://help.boomi.com/bundle/integration/page/c-atm-The_Dell_Boomi_Atom_Clouds.html) |
| All | High | Implement a formal environment topology: **Dev → Test/QA → Staging → Production**; map each environment to a distinct runtime | Direct-to-production deployments are the leading cause of production incidents; each tier must have its own dedicated runtime | [Release best practices](https://community.boomi.com/s/article/Release-Best-Practices) |
| All | High | Use **Environment Extensions** to externalize all environment-specific configuration; never hardcode production values in process components | Hardcoded values make it impossible to promote the same package across environments without modification | [Advanced properties](https://help.boomi.com/docs/Atomsphere/Integration/Integration%20management/r-atm-Properties_panel_Advanced_tab_c39737e8-1b16-4fdd-b414-152694364c14) |
| All | High | **Do not share a single runtime** across Development and Production environments; always use separate runtimes per environment tier | A shared runtime means a broken dev deployment can execute on the same JVM handling production traffic | [Release best practices](https://community.boomi.com/s/article/Release-Best-Practices) |
