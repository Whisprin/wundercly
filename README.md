# wundercly
A command line interface (CLI) for wunderlist.com, support for batch add and import from Google Keep (text only)

this is work in progress, currently supported:

- find existing lists by name
- create new lists
- add tasks to list
  - tasks starting with a space will be added as completed
- understand Google Keep exports
  - first line is \<list_title\>
  - following lines start with "[x] " or "[ ] ", depending on completed state
  
Important: The only way (that I know of) to get your data from Google Keep is to use the Android App and choose to send list.
The resulting data is already in the required format (described above).
