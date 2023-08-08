def main():
    ...


def sort_semesters(semester):
    year = ""
    semester_name = ""

    for i in semester:
        if i.isnumeric():
            year = year + i
        else:
            semester_name = semester_name + i

    semester_rank = {"Spring": 1, "Summer" : 2, "Autumn": 3}

    return int(year), semester_rank[semester_name.strip()]

if __name__ == "__main__":
    main()

