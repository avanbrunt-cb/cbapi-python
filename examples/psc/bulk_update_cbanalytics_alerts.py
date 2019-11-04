#!/usr/bin/env python

import sys
from time import sleep
from cbapi.example_helpers import build_cli_parser, get_cb_psc_object
from cbapi.psc.models import CBAnalyticsAlert

def main():
    parser = build_cli_parser("Bulk update the status of CB Analytics alerts")
    parser.add_argument("-q", "--query", help="Query string for looking for alerts")
    parser.add_argument("--category", action="append", choices=["THREAT", "MONITORED", "INFO",
                                                                "MINOR", "SERIOUS", "CRITICAL"],
                        help="Restrict search to the specified categories")
    parser.add_argument("--deviceid", action="append", type=int, help="Restrict search to the specified device IDs")
    parser.add_argument("--devicename", action="append", type=str, help="Restrict search to the specified device names")
    parser.add_argument("--os", action="append", choices=["WINDOWS", "ANDROID", "MAC", "IOS", "LINUX", "OTHER"],
                        help="Restrict search to the specified device operating systems")
    parser.add_argument("--osversion", action="append", type=str,
                        help="Restrict search to the specified device operating system versions")
    parser.add_argument("--username", action="append", type=str, help="Restrict search to the specified user names")
    parser.add_argument("--group", action="store_true", help="Group results")
    parser.add_argument("--alertid", action="append", type=str, help="Restrict search to the specified alert IDs")
    parser.add_argument("--legacyalertid", action="append", type=str, help="Restrict search to the specified legacy alert IDs")
    parser.add_argument("--severity", type=int, help="Restrict search to the specified minimum severity level")
    parser.add_argument("--policyid", action="append", type=int, help="Restrict search to the specified policy IDs")
    parser.add_argument("--policyname", action="append", type=str, help="Restrict search to the specified policy names")
    parser.add_argument("--processname", action="append", type=str, help="Restrict search to the specified process names")
    parser.add_argument("--processhash", action="append", type=str,
                        help="Restrict search to the specified process SHA-256 hash values")
    parser.add_argument("--reputation", action="append", choices=["KNOWN_MALWARE", "SUSPECT_MALWARE", "PUP",
                                                                  "NOT_LISTED", "ADAPTIVE_WHITE_LIST",
                                                                  "COMMON_WHITE_LIST", "TRUSTED_WHITE_LIST",
                                                                  "COMPANY_BLACK_LIST"],
                        help="Restrict search to the specified reputation values")
    parser.add_argument("--tag", action="append", type=str, help="Restrict search to the specified tag values")
    parser.add_argument("--priority", action="append", choices=["LOW", "MEDIUM", "HIGH", "MISSION_CRITICAL"],
                        help="Restrict search to the specified priority values")
    parser.add_argument("--threatid", action="append", type=str, help="Restrict search to the specified threat IDs")
    parser.add_argument("--type", action="append", choices=["CB_ANALYTICS", "VMWARE", "WATCHLIST"],
                        help="Restrict search to the specified alert types")
    parser.add_argument("--workflow", action="append", choices=["OPEN", "DISMISSED"],
                        help="Restrict search to the specified workflow statuses")
    parser.add_argument("--blockedthreat", action="append", choices=["UNKNOWN", "NON_MALWARE", "NEW_MALWARE",
                                                                     "KNOWN_MALWARE", "RISKY_PROGRAM"],
                        help="Restrict search to the specified threat categories that were blocked")
    parser.add_argument("--location", action="append", choices=["ONSITE", "OFFSITE", "UNKNOWN"],
                        help="Restrict search to the specified device locations")
    parser.add_argument("--killchain", action="append", choices=["RECONNAISSANCE", "WEAPONIZE", "DELIVER_EXPLOIT",
                                                                 "INSTALL_RUN", "COMMAND_AND_CONTROL", "EXECUTE_GOAL",
                                                                 "BREACH"],
                        help="Restrict search to the specified kill chain status values")
    parser.add_argument("--notblockedthreat", action="append", choices=["UNKNOWN", "NON_MALWARE", "NEW_MALWARE",
                                                                        "KNOWN_MALWARE", "RISKY_PROGRAM"],
                        help="Restrict search to the specified threat categories that were NOT blocked")
    parser.add_argument("--policyapplied", action="append", choices=["APPLIED", "NOT_APPLIED"],
                        help="Restrict search to the specified policy-application status values")
    parser.add_argument("--reason", action="append", type=str, help="Restrict search to the specified reason codes")
    parser.add_argument("--runstate", action="append", choices=["DID_NOT_RUN", "RAN", "UNKNOWN"],
                        help="Restrict search to the specified run states")
    parser.add_argument("--sensoraction", action="append", choices=["POLICY_NOT_APPLIED", "ALLOW", "ALLOW_AND_LOG",
                                                                    "TERMINATE", "DENY"],
                        help="Restrict search to the specified sensor actions")
    parser.add_argument("--vector", action="append", choices=["EMAIL", "WEB", "GENERIC_SERVER", "GENERIC_CLIENT",
                                                              "REMOTE_DRIVE", "REMOVABLE_MEDIA", "UNKNOWN",
                                                              "APP_STORE", "THIRD_PARTY"],
                        help="Restrict search to the specified threat cause vectors")
    parser.add_argument("-R", "--remediation", help="Remediation message to store for the selected alerts")
    parser.add_argument("-C", "--comment", help="Comment message to store for the selected alerts")
    operation = parser.add_mutually_exclusive_group(required=True)
    operation.add_argument("--dismiss", action="store_true", help="Dismiss all selected alerts")
    operation.add_argument("--undismiss", action="store_true", help="Undismiss all selected alerts")
    
    args = parser.parse_args()
    cb = get_cb_psc_object(args)

    if args.dismiss:
        query = cb.bulk_alert_dismiss("CBANALYTICS")
    elif args.undismiss:
        query = cb.bulk_alert_undismiss("CBANALYTICS")
    else:
        raise NotImplemented("one of --dismiss or --undismiss must be specified")
    
    if args.query:
        query = query.where(args.query)
    if args.category:
        query = query.categories(args.category)
    if args.deviceid:
        query = query.device_ids(args.deviceid)
    if args.devicename:
        query = query.device_names(args.devicename)
    if args.os:
        query = query.device_os(args.os)
    if args.osversion:
        query = query.device_os_version(args.osversion)
    if args.username:
        query = query.device_username(args.username)
    if args.group:
        query = query.group_results(True)
    if args.alertid:
        query = query.alert_ids(args.alertid)
    if args.legacyalertid:
        query = query.legacy_alert_ids(args.legacyalertid)
    if args.severity:
        query = query.minimum_severity(args.severity)
    if args.policyid:
        query = query.policy_ids(args.policyid)
    if args.policyname:
        query = query.policy_names(args.policyname)
    if args.processname:
        query = query.process_names(args.processname)
    if args.processhash:
        query = query.process_sha256(args.processhash)
    if args.reputation:
        query = query.reputations(args.reputation)
    if args.tag:
        query = query.tags(args.tag)
    if args.priority:
        query = query.target_priorities(args.priority)
    if args.threatid:
        query = query.threat_ids(args.threatid)
    if args.type:
        query = query.types(args.type)
    if args.workflow:
        query = query.workflows(args.workflow)
    if args.blockedthreat:
        query = query.blocked_threat_categories(args.blockedthreat)
    if args.location:
        query = query.device_locations(args.location)
    if args.killchain:
        query = query.kill_chain_statuses(args.killchain)
    if args.notblockedthreat:
        query = query.not_blocked_threat_categories(args.notblockedthreat)
    if args.policyapplied:
        query = query.policy_applied(args.policyapplied)
    if args.reason:
        query = query.reason_code(args.reason)
    if args.runstate:
        query = query.run_states(args.runstate)
    if args.sensoraction:
        query = query.sensor_actions(args.sensoraction)
    if args.vector:
        query = query.threat_cause_vectors(args.vector)
    if args.sort_by:
        direction = "DESC" if args.reverse else "ASC"
        query = query.sort_by(args.sort_by, direction)

    if args.remediation:
        query = query.remediation(args.remediation)
    if args.comment:
        query = query.comment(args.comment)
    statobj = query.run()
    print("Submitted query with ID {0}".format(statobj.id_))
    while not statobj.finished:
        print("Waiting...")
        sleep(1)
    if statobj.errors:
        print("Errors encountered:")
        for err in statobj.errors:
            print("\t{0}".format(err))
    if statobj.failed_ids:
        print("Failed alert IDs:")
        for i in statobj.failed_ids:
            print("\t{0}".format(err))
    print("{0} total alert(s) found, of which {1} were successfully changed" \
          .format(statobj.num_hits, statobj.num_success))


if __name__ == "__main__":
    sys.exit(main())
