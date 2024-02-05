paper_list = []

with open('data/Referencias Machine Learning.docx.txt', 'r') as file:
    for line in file:
        # Remove leading and trailing whitespaces
        paper_info = line.strip()
        # Add paper information to the list
        paper_list.append(paper_info)

# Now, paper_list contains each line of the file as a separate item
print(paper_list)
