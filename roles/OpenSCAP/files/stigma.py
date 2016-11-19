#!/usr/bin/env python

import sys
import math
import argparse

try:
  import untangle
except ImportError:
  print 'Untangle required. Install using `pip install untangle`'
try:
  from tabulate import tabulate
except ImportError:
  print 'Tabulate required. Install using `pip install tabulate`'

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Checks Pass percentage of OSCAP report.'
                         ' Includes customizable success criteria for '
                         ' low, medium, and high severity levels. Intended'
                         ' to be ran as part of a CI pipeline, but can be'
                         ' used as a standalone validation tool as well')
  parser.add_argument('-P', '--results-path', required=True, dest='results_xml', help='Path to results xml file'
                                                                                      ' generated by OSCAP')

  parser.add_argument('-T', '--total-pass', required=False, dest='total_pass', type=int,
                      help='No Default. The overall pass percentage to determines success')

  parser.add_argument('-H', '--high-pass', required=False, dest='high_pass', type=int, default=100,
                       help='Default 100%%. The pass percentage to determines success for'
                            ' high severity benchmarks')

  parser.add_argument('-M', '--medium-pass', required=False, dest='medium_pass', type=int, default=90,
                      help='Default 90%%. The pass percentage to determines success for'
                           ' medium severity benchmarks')

  parser.add_argument('-L', '--low-pass', required=False, dest='low_pass', type=int, default=90,
                         help='Default 90%%. The pass percentage to determines success for'
                              ' low severity benchmarks')
  parser.add_argument('--show-failures', required=False, dest='show', type=str,
                      choices=['all', 'high', 'medium', 'low'],
                      help='Returns failures by rule ID.')
  args = parser.parse_args()
  result_meta = untangle.parse(args.results_xml)
  
class bcolors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

class StigReport:

  if __name__ != "__main__":
    try:
      args
    except NameError:
      class args:
        high_pass   =   90,
        medium_pass =   90,
        low_pass    =   90,
        total_pass  =   10

    try:
      result_meta
    except NameError:
      result_meta = untangle.parse('tests/results.xml')
    else:
      sys.exit("There is an issue with result_meta and/args")

  
  def percentage(self, part, whole):
      return 100 * int(part)/int(whole)

  failure = False

  severity_success = {
    'High'    : bcolors.OKGREEN + 'PASSED' + bcolors.ENDC,
    'Medium'  : bcolors.OKGREEN + 'PASSED' + bcolors.ENDC,
    'Low'   : bcolors.OKGREEN + 'PASSED' + bcolors.ENDC,
    'Overall' : bcolors.OKGREEN + 'PASSED' + bcolors.ENDC
  }

  metrics = {
      'high_pass'  : 0,
      'high_fail'  : 0,
      'high_total' : 0,
      'med_pass'   : 0,
      'med_fail'   : 0,
      'med_total'  : 0,
      'low_pass'   : 0,
      'low_fail'   : 0,
      'low_total'  : 0,
      'total_pass' : 0,
      'total_fail' : 0,
  }

  success_meta = {}
  high_fails = []
  med_fails = []
  low_fails = []

  rule_list = [rule.Rule['id'] for rule in result_meta.Benchmark.Group]
  pass_fail_list = [res.result.cdata for res in result_meta.Benchmark.TestResult.rule_result]
  title_list = [ttl.Rule.title.cdata for ttl in result_meta.Benchmark.Group]
  description_list = [desc.Rule.description.cdata for desc in result_meta.Benchmark.Group]
  severity_list =  [sev.Rule['severity'] for sev in result_meta.Benchmark.Group]
  fix_list = [fix.Rule.fixtext.cdata for fix in result_meta.Benchmark.Group]

  for rule_id, success, severity in zip(rule_list, pass_fail_list, severity_list):
    success_meta.update({ rule_id : {'result': success, 'severity': severity} })
    if success == 'fail':
      if severity == 'high':
        high_fails.append(rule_id)
      elif severity == 'medium':
        med_fails.append(rule_id)
      else:
        low_fails.append(rule_id)

  for rule, meta in success_meta.items():
    if meta['severity'] == 'low':
      metrics['low_total'] += 1
      if meta['result'] == 'fail':
        metrics['low_fail'] += 1
      else:
        metrics['low_pass'] += 1

    elif meta['severity'] == 'medium':
      metrics['med_total'] += 1
      if meta['result'] == 'fail':
        metrics['med_fail'] += 1
      else:
        metrics['med_pass'] += 1

    elif meta['severity'] == 'high':
      metrics['high_total'] += 1
      if meta['result'] == 'fail':
        metrics['high_fail'] += 1
      else:
        metrics['high_pass'] += 1

    if meta['result'] == 'fail':
      metrics['total_fail'] += 1
    else:
      metrics['total_pass'] += 1

  high_success    = percentage(None, metrics['high_pass'], metrics['high_total'])
  high_fail     = bcolors.FAIL + str(metrics['high_fail']) + bcolors.ENDC
  high_total    = str(metrics['high_total'])
  high_pass     = bcolors.OKGREEN + str(metrics['high_pass']) + bcolors.ENDC

  med_success     = percentage(None, metrics['med_pass'], metrics['med_total'])
  med_fail    = bcolors.FAIL + str(metrics['med_fail']) + bcolors.ENDC
  med_total     = str(metrics['med_total']) + bcolors.ENDC
  med_pass    = bcolors.OKGREEN + str(metrics['med_pass']) + bcolors.ENDC

  low_success     = percentage(None, metrics['low_pass'], metrics['low_total'])
  low_fail    = bcolors.FAIL + str(metrics['low_fail']) + bcolors.ENDC
  low_total     = str(metrics['low_total'])
  low_pass    = bcolors.OKGREEN + str(metrics['low_pass']) + bcolors.ENDC

  total       = str(len(rule_list)) 
  total_success   = percentage(None, metrics['total_pass'], total)
  total_fail    = bcolors.FAIL + str(metrics['total_fail']) + bcolors.ENDC
  total_pass    = bcolors.OKGREEN + str(metrics['total_pass']) + bcolors.ENDC


  if args.high_pass:
    if args.high_pass > high_success:
      severity_success['High'] = bcolors.FAIL + 'FAILED' + bcolors.ENDC
      failure = True

  if args.medium_pass:
    if args.medium_pass > med_success:
      severity_success['Medium'] = bcolors.FAIL + 'FAILED' + bcolors.ENDC
      failure = True

  if args.low_pass:
    if args.low_pass > low_success:
      severity_success['Low'] = bcolors.FAIL + 'FAILED' + bcolors.ENDC
      failure = True

  if args.total_pass:
    if args.total_pass > total_success:
      severity_success['Overall'] = bcolors.FAIL + 'FAILED' + bcolors.ENDC
      failure = True
  else: 
    severity_success['Overall'] = 'N/A'


  headers = ['Severity Type', 'Passed', 'Failed', '# Benchmarks', '% Success', 'Pass/Fail']
  table = [
    ['High', high_pass, high_fail, high_total, high_success, severity_success['High']],
    ['Medium', med_pass, med_fail, med_total, med_success, severity_success['Medium']],
    ['Low', low_pass, low_fail, low_total, low_success, severity_success['Low']],
    ['Overall', total_pass, total_fail, total, total_success, severity_success['Overall']]
  ]

if __name__ == "__main__":

  print tabulate(StigReport.table, headers=StigReport.headers, numalign='center', stralign='center', tablefmt="grid")
  
  if args.show:
    if args.show == 'all':
      print 'Low Failures are: %s \n' % ', '.join(StigReport.low_fails)
      print 'Medium Failures are: %s \n' % ', '.join(StigReport.med_fails)
      print 'High Failures are: %s \n' % ', '.join(StigReport.high_fails)
    elif args.show == 'high':
      print 'High Failures are: %s \n' % ', '.join(StigReport.high_fails)
    elif args.show == 'medium':
      print 'Medium Failures are: %s \n' % ', '.join(StigReport.med_fails)
    elif args.show == 'low':
      print 'Low Failures are: %s \n' % ', '.join(StigReport.low_fails)

  if StigReport.failure:
    sys.exit(1)

