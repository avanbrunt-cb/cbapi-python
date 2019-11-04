#!/usr/bin/env python

import sys
from cbapi.example_helpers import build_cli_parser, get_cb_psc_object
from cbapi.psc.models import BaseAlert

def main():
    parser = build_cli_parser("List alerts")
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
    parser.add_argument("-S", "--sort_by", help="Field to sort the output by")
    parser.add_argument("-R", "--reverse", action="store_true", help="Reverse order of sort")
    
    args = parser.parse_args()
    cb = get_cb_psc_object(args)
    
    query = cb.select(BaseAlert)
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
    if args.sort_by:
        direction = "DESC" if args.reverse else "ASC"
        query = query.sort_by(args.sort_by, direction)

    alerts = list(query)
    print("{0:40} {1:40s} {2:40s} {3}".format("ID", "Hostname", "Threat ID", "Last Updated"))
    for alert in alerts:
        print("{0:40} {1:40s} {2:40s} {3}".format(alert.id, alert.device_name or "None", \
                                                  alert.threat_id or "Unknown", \
                                                  alert.last_update_time))

if __name__ == "__main__":
    sys.exit(main())
