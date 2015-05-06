# Usage
```python
  import CBD as cbd

  f = cbd.CBDDocExplorer("20150427 - Accounting_RSP.txt")

  # Add to p & c direct bills
  f.add_folder('BCBST', 'pc')

  # Add to group benefits - It creates subfolders as well. Though may have
  # issues with nesting. Currently creates any needed object, but you'll need to
  # sort the subfolders
  f.add_folder('BCBST', 'gb')

  # Add multiples
  f.add_folder(['BCBST', 'Cincinnati', 'Pinnacle'], 'pc')

```
