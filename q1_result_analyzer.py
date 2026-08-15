def Student_marks(name,roll, marks):
    total=sum(marks)
    average=total/len(marks)

    if average>=90:
        grade='A'
    elif average>=75:
        grade='B'
    elif average>=60:
        grade='C'
    elif average>=40:
        grade='D'
    else:
        grade='Fail'
    below_40=[]

    for i,mark in enumerate(marks,start=1):
        if mark<40:
            below_40.append(i)

    print(f"Name: {name}")
    print(f"Roll: {roll}")
    print(f"Total Marks: {total}")
    print(f"Average Marks: {average}")
    print(f"Grade: {grade}")

    if below_40:
        print(f"Subjects below 40: {below_40}")
    else:
        print("All subjects are above 40.")

name="Raj"
roll=505
marks=[95.5, 30.4, 78.8, 88.2, 92.0]
Student_marks(name,roll,marks)