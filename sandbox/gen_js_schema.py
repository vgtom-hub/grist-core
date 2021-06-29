#!/usr/bin/env python -B
"""
Generates a JS schema file from sandbox/grist/schema.py.
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'grist'))

import schema   # pylint: disable=import-error,wrong-import-position

# These are the types that appear in Grist metadata columns.
_ts_types = {
  "Bool":           "boolean",
  "DateTime":       "number",
  "Int":            "number",
  "PositionNumber": "number",
  "Ref":            "number",
  "RefList":        "['L', ...number[]]|null",    # Non-primitive values are encoded
  "Text":           "string",
}

def get_ts_type(col_type):
  col_type = col_type.split(':', 1)[0]      # Strip suffix for Ref:, DateTime:, etc.
  return _ts_types.get(col_type, "CellValue")

def main():
  print("""\
/*** THIS FILE IS AUTO-GENERATED BY %s ***/
// tslint:disable:object-literal-key-quotes

export const schema = {
""" % __file__)

  for table in schema.schema_create_actions():
    print('  "%s": {' % table.table_id)
    for column in table.columns:
      print('    %-20s: "%s",' % (column['id'], column['type']))
    print('  },\n')

  print("""};

export interface SchemaTypes {
""")
  for table in schema.schema_create_actions():
    print('  "%s": {' % table.table_id)
    for column in table.columns:
      print('    %s: %s;' % (column['id'], get_ts_type(column['type'])))
    print('  };\n')
  print("}")

if __name__ == '__main__':
  main()
