#!/usr/bin/env python
# coding: utf-8

"""
    The approach taken is explained below. I decided to do it simply.
    Initially I was considering parsing the data into some sort of
    structure and then generating an appropriate README. I am still
    considering doing it - but for now this should work. The only issue
    I see is that it only sorts the entries at the lowest level, and that
    the order of the top-level contents do not match the order of the actual
    entries.

    This could be extended by having nested blocks, sorting them recursively
    and flattening the end structure into a list of lines. Revision 2 maybe ^.^.
"""

def sort_blocks():
    # First, we load the current README into memory
    with open('README.md', 'r', encoding="latin-1") as read_me_file:
        read_me = read_me_file.read()

    # Separating the 'table of contents' from the contents (blocks)
    table_of_contents = ''.join(read_me.split('---')[0])
    blocks = ''.join(read_me.split('---')[1]).split('\n# ')
    # print(table_of_contents)
    for i in range(len(blocks)):
        if i == 0:
            blocks[i] = blocks[i] + '\n'
        else:
            blocks[i] = '# ' + blocks[i] + '\n'

    # Sorting the libraries
    # inner_blocks = sorted(blocks[0].split('##')) ## this sorts categories as well which we do not want
    inner_blocks = blocks[0].split('###')
    for i in range(1, len(inner_blocks)):
        if inner_blocks[i][0] != '#':
            inner_blocks[i] = '###' + inner_blocks[i]
    inner_blocks = ''.join(inner_blocks)
    # Replacing the non-sorted libraries by the sorted ones and gathering all at the final_README file
    blocks[0] = inner_blocks
    final_README = table_of_contents + '---\n\n' + ''.join(blocks).strip() + '\n'

    with open('README.md', 'w+', encoding="latin-1") as sorted_file:
        sorted_file.write(final_README)


def main():
    # First, we load the current README into memory as an array of lines
    with open('README.md', 'r', encoding="latin-1") as read_me_file:
        read_me = read_me_file.readlines()

    # Then we cluster the lines together as blocks
    # Each block represents a collection of lines that should be sorted
    # This was done by assuming only links ([...](...)) are meant to be sorted
    # Clustering is done by indentation
    blocks = []
    last_indent = None
    for line in read_me:
        s_line = line.lstrip()
        indent = len(line) - len(s_line)

        if any([s_line.startswith(s) for s in ['* [', '- [']]):
            if indent == last_indent:
                blocks[-1].append(line)
            else:
                blocks.append([line])
            last_indent = indent
        else:
            blocks.append([line])
            last_indent = None

    ignore_sort_list = ["- [Awesome Utrecht University](#awesome-utrecht-university)",
  "- [Projects](#projects)",
    "- [Research code](#research-code)",
    "- [Research software](#research-software)",
    "- [Research data](#research-data)",
    "- [Research project management](#research-project-management)",
    "- [Education and workshops](#education-and-workshops)",
    "- [Collaboration groups](#collaboration-groups)",
  "- [Add project to this list](#add-project-to-this-list)",
  "- [Background](#background)",
    "- [What is an Awesome list?](#what-is-an-awesome-list)",
    "- [Initial project collection](#initial-project-collection)",
  "- [Contact](#contact)"]
    # print(not any(substring in ''.join(blocks[20]) for substring in ignore_sort_list))
    with open('README.md', 'w+', encoding="latin-1") as sorted_file:
        # Then all of the blocks are sorted individually
        blocks = [
            ''.join(sorted(block, key=str.lower)) if not any(toc_block in ''.join(block) for toc_block in ignore_sort_list) else ''.join(block) for block in blocks # do not sort ToC
        ]
        # And the result is written back to README.md
        sorted_file.write(''.join(blocks))

    # Then we call the sorting method
    sort_blocks()


if __name__ == "__main__":
    main()
